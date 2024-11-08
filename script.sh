#!/bin/bash

# Set up logging
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Function to check if a port is open
check_port() {
    local ip=$1
    local port=$2
    timeout 1 bash -c "echo >/dev/tcp/$ip/$port" 2>/dev/null
    return $?
}

# Function to get printer information
get_printer_info() {
    local ip=$1
    local port=$2
    local printer_info
    
    # Try to get printer information using netcat
    printer_info=$(echo -e '\0' | nc -w 1 $ip $port 2>/dev/null | tr -d '\0')
    
    if [ ! -z "$printer_info" ]; then
        echo "$ip $printer_info" >> printers.txt
    fi
}

# Function to scan an IP address
scan_ip() {
    local ip=$1
    local port=${2:-9100}
    
    if check_port "$ip" "$port"; then
        log "INFO: Open port found on $ip:$port"
        get_printer_info "$ip" "$port"
    fi
}

# Function to generate IP range
generate_ip_range() {
    local subnet=$1
    local base_ip=${subnet%/*}
    local mask=${subnet#*/}
    
    # Use ipcalc to generate IP range
    if command -v ipcalc >/dev/null 2>&1; then
        ipcalc -n "$subnet" | grep "HostMin\|HostMax" | awk '{print $2}' | \
        while read start; read end; do
            seq -f "$(echo $start | cut -d. -f1-3).%g" \
                $(echo $start | cut -d. -f4) \
                $(echo $end | cut -d. -f4)
        done
    else
        log "ERROR: ipcalc is required but not installed"
        exit 1
    fi
}

main() {
    local target_subnet=$1
    local max_processes=10
    
    if [ -z "$target_subnet" ]; then
        log "ERROR: Please provide a target subnet (e.g., 192.168.1.0/24)"
        exit 1
    }
    
    # Check for required tools
    for tool in nc timeout ipcalc; do
        if ! command -v $tool >/dev/null 2>&1; then
            log "ERROR: Required tool '$tool' is not installed"
            exit 1
        fi
    done
    
    # Clear previous results
    > printers.txt
    
    log "INFO: Starting printer scan on subnet $target_subnet"
    
    # Create a temporary file for process management
    tmp_fifo="/tmp/printer_scan_$$"
    mkfifo "$tmp_fifo"
    
    # Start background process to manage concurrent execution
    exec 3<>"$tmp_fifo"
    rm "$tmp_fifo"
    
    # Initialize process slots
    for ((i=1; i<=max_processes; i++)); do
        echo >&3
    done
    
    # Scan each IP in the subnet
    generate_ip_range "$target_subnet" | while read ip; do
        # Wait for a free slot
        read -u 3
        
        (
            scan_ip "$ip"
            echo >&3
        ) &
    done
    
    # Wait for all background processes to complete
    wait
    
    # Clean up
    exec 3>&-
    
    log "INFO: Scan complete. Results saved to printers.txt"
}

# Handle script interruption
trap 'log "INFO: Scan interrupted by user."; exit 1' INT

# Run the main function with the provided subnet
main "$1"
