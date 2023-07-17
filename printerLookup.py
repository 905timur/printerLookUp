import socket
import concurrent.futures
from queue import Queue
import netaddr
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ip_range(target_subnet):
    network = netaddr.IPNetwork(target_subnet)
    return [str(ip) for ip in network]

def portscan(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            return True
    except:
        return False

def get_printer_info(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            printer = sock.recv(1024)
            printers.append({'ip': ip, 'brand': printer.split(' ')[0], 'model': printer.split(' ')[1]})
    except Exception as e:
        logging.error(f"Error getting printer info for {ip}: {str(e)}")

def scan(ip, port=9100):
    try:
        if portscan(ip, port):
            get_printer_info(ip, port)
    except Exception as e:
        logging.error(f"Error scanning {ip}: {str(e)}")

try:
    printers = []
    queue = Queue()
    for ip in ip_range(target_subnet):
        queue.put(ip)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for ip in queue.queue:
            executor.submit(scan, ip)

    with open('printers.txt', 'w') as f:
        for printer in printers:
            f.write(f"{printer['ip']} {printer['brand']} {printer['model']}\n")

finally:
    f.close()

except Exception as e:
    logging.error(str(e))
