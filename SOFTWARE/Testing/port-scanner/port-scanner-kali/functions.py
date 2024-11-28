import socket
import threading
import queue
import requests  # Assicurati di importare requests per l'autenticazione

API_BASE_URL = "http://10.0.2.15:5000"  # Cambia con l'URL del server

# Funzione per autenticazione
def authenticate_user(username, password):
    try:
        response = requests.post(f"{API_BASE_URL}/auth", json={"username": username, "password": password})
        return response.json()
    except Exception as e:
        return {"success": False, "message": f"Errore di connessione: {e}"}

# Funzione per scansionare una singola porta
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
        result_queue.put((port, "Errore di Connessione"))  # Aggiunto per altre situazioni
    sock.close()

# Funzione per eseguire la scansione delle porte in parallelo
def scan_ports_in_parallel(target_ip, ports, result_queue):
    threads = []
    for port in ports:
        thread = threading.Thread(target=port_scanner, args=(target_ip, port, result_queue))
        threads.append(thread)
        thread.start()

    # Attendere che tutti i thread finiscano
    for thread in threads:
        thread.join()

# Funzione di avvio della scansione
def start_scan(target_ip, ports_to_scan, result_queue):
    try:
        # Esegui la scansione delle porte in parallelo
        scan_ports_in_parallel(target_ip, ports_to_scan, result_queue)
        
        # Processa i risultati dalla coda
        open_ports = []
        filtered_ports = []
        closed_ports = []
        error_ports = []  # Per gestire gli errori

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
