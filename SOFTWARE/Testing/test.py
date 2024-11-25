import customtkinter as ctk
import socket as so

def port_scanner(target_ip, port_range):
    open_ports = []
    closed_ports = []
    filtered_ports = []
    for port in range(port_range[0], port_range[1] + 1):
        sock = so.socket(so.AF_INET, so.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        elif result == 111:
            closed_ports.append(port)
        elif result == 110:
            filtered_ports.append(port)
        sock.close()
    return open_ports, filtered_ports, closed_ports

def start_scan():
    target_ip = ip_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())
    port_range = (start_port, end_port)

    open_ports, filtered_ports, closed_ports = port_scanner(target_ip, port_range)
    
    open_ports_box.delete(0, ctk.END)
    for port in open_ports:
        open_ports_box.insert(ctk.END, f"Porta {port}: Aperta")
    
    filtered_ports_box.delete(0, ctk.END)
    for port in filtered_ports:
        filtered_ports_box.insert(ctk.END, f"Porta {port}: Filtrata")
    
    closed_ports_box.delete(0, ctk.END)
    for port in closed_ports:
        closed_ports_box.insert(ctk.END, f"Porta {port}: Chiusa")

# Configurazione della finestra
ctk.set_appearance_mode("dark")  # Modalità scura
ctk.set_default_color_theme("blue")  # Tema blu

app = ctk.CTk()
app.title("Port Scanner")
app.geometry("600x400")

# Input per IP
ip_label = ctk.CTkLabel(app, text="Inserisci l'IP da scansionare:")
ip_label.pack(pady=10)
ip_entry = ctk.CTkEntry(app)
ip_entry.pack(pady=10)

# Input per intervallo di porte
start_port_label = ctk.CTkLabel(app, text="Porta iniziale:")
start_port_label.pack(pady=10)
start_port_entry = ctk.CTkEntry(app)
start_port_entry.pack(pady=10)

end_port_label = ctk.CTkLabel(app, text="Porta finale:")
end_port_label.pack(pady=10)
end_port_entry = ctk.CTkEntry(app)
end_port_entry.pack(pady=10)

# Pulsante per avviare la scansione
scan_button = ctk.CTkButton(app, text="Scansiona", command=start_scan)
scan_button.pack(pady=20)

# Risultati
open_ports_box = ctk.CTkTextbox(app, height=100)
open_ports_box.pack(pady=10)
filtered_ports_box = ctk.CTkTextbox(app, height=100)
filtered_ports_box.pack(pady=10)
closed_ports_box = ctk.CTkTextbox(app, height=100)
closed_ports_box.pack(pady=10)

app.mainloop()
