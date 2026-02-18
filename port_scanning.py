import socket
import threading
from queue import Queue
import time

target = input("Enter target IP: ")
num_threads = 200

queue = Queue()
open_ports = []


def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"

            print(f"[+] Port {port} OPEN | Service: {service}")
            open_ports.append(port)

        s.close()
    except:
        pass


def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()


print("Scanning started...\n")
start_time = time.time()

# Add all ports
for port in range(1, 65536):
    queue.put(port)

# Create threads
for _ in range(num_threads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

queue.join()

end_time = time.time()

print("\nScanning Completed!")
print(f"Total Open Ports: {len(open_ports)}")
print(f"Time Taken: {round(end_time - start_time, 2)} seconds")
