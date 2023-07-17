import socket
import threading
from queue import Queue

def ip_range(target_subnet):
    return [ip for ip in range(target_subnet.split("/")[0], target_subnet.split("/")[0] + 256)]

def portscan(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        return True
    except:
        return False

def get_printer_info(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        printer = sock.recv(1024)
        printers.append({'ip': ip, 
                        'brand': printer.split(' ')[0],
                        'model': printer.split(' ')[1]})
    except:
        pass

def scan(ip):
    if portscan(ip, 9100):
        get_printer_info(ip, 9100)

try:
    printers = []
    queue = Queue()
    for ip in ip_range(target_subnet):
        queue.put(ip)

    for i in range(256):
        t = threading.Thread(target=scan, args=(queue.get(),))
        t.daemon = True
        t.start()

    for t in threading.enumerate():
        if not t.daemon:
            t.join()

    with open('printers.txt', 'w') as f:
        for printer in printers:
            f.write(f"{printer['ip']} {printer['brand']} {printer['model']}\n")
except Exception as e:
    print(e)
