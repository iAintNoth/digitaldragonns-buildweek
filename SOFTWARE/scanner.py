import socket as so 


def port_scanner(target_ip, port_range):
    open_ports = []
    closed_ports = []
    filtered_port=[]
    for port in range(port_range[0], port_range[1] + 1):
        # Creazione del socket
        sock = so.socket(so.AF_INET, so.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port)) # 0 indica successo
        if result == 0:
            open_ports.append(port)
        elif result == 111:
            closed_ports.append(port)
        elif result == 110:
            filtered_port.append(port)
        sock.close()

    return open_ports, filtered_port, closed_ports


if __name__ == "__main__":

    target_ip = input("Inserisci l'IP da scansionare: ")

    start_port = int(input("Inserisci la porta iniziale: "))
    end_port = int(input("Inserisci la porta finale: "))

    port_range = (start_port, end_port)

    open_ports, filtered_ports, closed_ports = port_scanner(target_ip, port_range)

    print(f"Porte aperte su {target_ip}: {open_ports}")
    print(f"Porte Filtrate su {target_ip}: {filtered_ports}")
    print(f"Porte Chiuse su {target_ip}: {closed_ports}")