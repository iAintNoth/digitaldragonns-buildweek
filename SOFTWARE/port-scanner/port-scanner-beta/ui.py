import customtkinter as ctk
from tkinter import messagebox
from functions import start_scan_thread
from PIL import Image
from customtkinter import CTkImage
import queue

# Variabili globali per i box dei risultati
open_ports_box = None
filtered_ports_box = None
closed_ports_box = None
error_ports_box = None

def login(username_entry, password_entry, authenticate_user, login_window):
    username = username_entry.get()
    password = password_entry.get()

    # Autenticazione tramite API
    result = authenticate_user(username, password)

    if result.get("success"):
        login_window.destroy()  # Chiude la finestra di login
        show_main_window()  # Mostra la finestra principale di scansione
    else:
        messagebox.showerror("Errore", result["message"])

def show_main_window():
    global open_ports_box, filtered_ports_box, closed_ports_box, error_ports_box

    main_window = ctk.CTk()

    # Impostiamo la dimensione della finestra
    window_width = 800
    window_height = 600
    main_window.geometry(f"{window_width}x{window_height}")

    # Creazione della UI...
    # (il codice del layout UI non cambia rispetto a quanto già scritto nel tuo esempio)

    main_window.mainloop()

def start_scan_thread(ip_entry, start_port_entry, end_port_entry, specific_ports_entry):
    try:
        target_ip = ip_entry.get()
        specific_ports_input = specific_ports_entry.get()
        specific_ports = []

        if specific_ports_input:
            # Validazione delle porte specifiche
            specific_ports = [int(port.strip()) for port in specific_ports_input.split(",") if port.strip().isdigit()]
            if len(specific_ports) == 0:
                messagebox.showerror("Errore", "Le porte specifiche devono essere numeriche.")
                return
        else:
            specific_ports = []

        # Verifica intervallo di porte
        if not specific_ports:
            start_port = start_port_entry.get()
            end_port = end_port_entry.get()
            if not start_port.isdigit() or not end_port.isdigit():
                messagebox.showerror("Errore", "Inserisci valori numerici validi per le porte dell'intervallo.")
                return

            start_port = int(start_port)
            end_port = int(end_port)

            if start_port > end_port:
                messagebox.showerror("Errore", "La porta iniziale deve essere minore o uguale alla porta finale.")
                return

            ports_to_scan = list(range(start_port, end_port + 1))
        else:
            ports_to_scan = specific_ports

        result_queue = queue.Queue()
        scan_thread = threading.Thread(target=run_scan, args=(target_ip, ports_to_scan, result_queue))
        scan_thread.start()

    except ValueError as e:
        messagebox.showerror("Errore", f"Errore nei dati di input: {str(e)}")
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore inaspettato: {str(e)}")
