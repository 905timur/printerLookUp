import socket
import concurrent.futures
import netaddr
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ip_range(target_subnet):
    network = netaddr.IPNetwork(target_subnet)
    return [str(ip) for ip in network]

def portscan(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set socket timeout to 1 second
            sock.connect((ip, port))
            return True
    except:
        return False

def get_printer_info(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Set socket timeout to 1 second
            sock.connect((ip, port))
            printer = sock.recv(1024)
            printers.add((ip, printer.split(' ')[0], printer.split(' ')[1]))  # Use a set to store printers
    except Exception as e:
        logging.error(f"Error getting printer info for {ip}: {str(e)}")

def scan(ip, port=9100):
    try:
        if portscan(ip, port):
            get_printer_info(ip, port)
    except Exception as e:
        logging.error(f"Error scanning {ip}: {str(e)}")

try:
    printers = set()  # Use a set to store printers

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:  # Limit the maximum number of concurrent threads to 10
        for ip in ip_range(target_subnet):
            executor.submit(scan, ip)

    collected_data = '\n'.join([f"{printer[0]} {printer[1]} {printer[2]}" for printer in printers])

    with open('printers.txt', 'w') as f:
        f.write(collected_data)

except KeyboardInterrupt:
    logging.info("Scan interrupted by user.")

except Exception as e:
    logging.error(str(e))
