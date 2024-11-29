import socket
import threading
import queue

def port_scanner(target_ip, port, result_queue):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target_ip, port))
    if result == 0:
        result_queue.put((port, "Aperta"))
    elif result == 111:
        result_queue.put((port, "Chiusa"))
    elif result == 110:
        result_queue.put((port, "Filtrata"))
    else:
        result_queue.put((port, "Errore di Connessione"))
    sock.close()

def scan_ports_in_parallel(target_ip, ports, result_queue):
    threads = []
    for port in ports:
        thread = threading.Thread(target=port_scanner, args=(target_ip, port, result_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def start_scan(target_ip, ports_to_scan, result_queue):
    try:
        scan_ports_in_parallel(target_ip, ports_to_scan, result_queue)
        
        open_ports = []
        filtered_ports = []
        closed_ports = []
        error_ports = []

        while not result_queue.empty():
            port, status = result_queue.get()
            if status == "Aperta":
                open_ports.append(port)
            elif status == "Filtrata":
                filtered_ports.append(port)
            elif status == "Chiusa":
                closed_ports.append(port)
            elif status == "Errore di Connessione":
                error_ports.append(port)

        return open_ports, filtered_ports, closed_ports, error_ports

    except Exception as e:
        raise Exception(f"Si è verificato un errore durante la scansione: {str(e)}")
