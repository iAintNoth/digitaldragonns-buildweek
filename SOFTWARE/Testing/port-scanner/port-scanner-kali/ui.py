import customtkinter as ctk
import threading
from customtkinter import CTkImage
from tkinter import messagebox
import queue
from tkinter import PhotoImage
from PIL import Image, ImageTk
from functions import start_scan
import pandas as pd

# Variabili globali per i box dei risultati
open_ports_box = None
filtered_ports_box = None
closed_ports_box = None
error_ports_box = None  # Nuova variabile globale per le porte con errore

# Funzione di login
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

# Funzione per mostrare la finestra principale di scansione
def show_main_window():
    global open_ports_box, filtered_ports_box, closed_ports_box, error_ports_box  # Rendi globali le variabili

    main_window = ctk.CTk()

    # Impostiamo la dimensione della finestra
    window_width = 800
    window_height = 600
    main_window.geometry(f"{window_width}x{window_height}")

    # Calcoliamo la posizione per centrare la finestra
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    main_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
    main_window.title("DD Port Scanner")

    # Creiamo il layout con due colonne: Dati a sinistra, Risultati a destra
    left_frame = ctk.CTkFrame(main_window)
    left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Aggiungi il contenuto della colonna sinistra (dati di input)
    ip_label = ctk.CTkLabel(left_frame, text="Inserisci l'IP da scansionare:")
    ip_label.pack(pady=10)
    ip_entry = ctk.CTkEntry(left_frame)
    ip_entry.pack(pady=10)

    specific_ports_label = ctk.CTkLabel(left_frame, text="Porte specifiche (es. 22,80,443):")
    specific_ports_label.pack(pady=10)
    specific_ports_entry = ctk.CTkEntry(left_frame)
    specific_ports_entry.pack(pady=10)

    start_port_label = ctk.CTkLabel(left_frame, text="Porta iniziale:")
    start_port_label.pack(pady=10)
    start_port_entry = ctk.CTkEntry(left_frame)
    start_port_entry.pack(pady=10)

    end_port_label = ctk.CTkLabel(left_frame, text="Porta finale:")
    end_port_label.pack(pady=10)
    end_port_entry = ctk.CTkEntry(left_frame)
    end_port_entry.pack(pady=10)

    scan_button = ctk.CTkButton(left_frame, text="Scansiona", command=lambda: start_scan_thread(ip_entry, start_port_entry, end_port_entry, specific_ports_entry))
    scan_button.pack(pady=20)

    # Sezione destra (risultati)
    right_frame = ctk.CTkFrame(main_window)
    right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    # Aggiungi un pulsante per salvare i risultati
    save_button = ctk.CTkButton(right_frame, text="Salva Risultati", command=save_scan_results)
    save_button.pack(pady=20)

    # Risultati: Box per porte aperte, filtrate, chiuse e con errore
    open_ports_box = ctk.CTkTextbox(right_frame, height=100)
    open_ports_box.pack(pady=10)
    filtered_ports_box = ctk.CTkTextbox(right_frame, height=100)
    filtered_ports_box.pack(pady=10)
    closed_ports_box = ctk.CTkTextbox(right_frame, height=100)
    closed_ports_box.pack(pady=10)
    error_ports_box = ctk.CTkTextbox(right_frame, height=100)  # Box per porte con errore
    error_ports_box.pack(pady=10)

    # Impostiamo il layout per permettere la ridimensionabilità
    main_window.grid_rowconfigure(0, weight=1)
    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_columnconfigure(1, weight=1)

    main_window.mainloop()

def start_scan_thread(ip_entry, start_port_entry, end_port_entry, specific_ports_entry):
    try:
        target_ip = ip_entry.get()

        # Ottieni le porte specifiche
        specific_ports_input = specific_ports_entry.get()
        specific_ports = []

        if specific_ports_input:
            # Verifica se le porte specifiche sono valide (numeri separati da virgola)
            specific_ports = [int(port.strip()) for port in specific_ports_input.split(",") if port.strip().isdigit()]
            if len(specific_ports) == 0:
                messagebox.showerror("Errore", "Le porte specifiche devono essere numeriche.")
                return
        else:
            specific_ports = []

        # Se non sono state inserite porte specifiche, controlla l'intervallo
        if not specific_ports:
            start_port = start_port_entry.get()
            end_port = end_port_entry.get()

            # Verifica che entrambi i campi dell'intervallo siano validi
            if not start_port.isdigit() or not end_port.isdigit():
                messagebox.showerror("Errore", "Inserisci valori numerici validi per le porte dell'intervallo.")
                return

            # Converti le porte in interi
            start_port = int(start_port)
            end_port = int(end_port)

            if start_port > end_port:
                messagebox.showerror("Errore", "La porta iniziale deve essere minore o uguale alla porta finale.")
                return

            # Se non ci sono porte specifiche, unisci l'intervallo di porte
            ports_to_scan = list(range(start_port, end_port + 1))
        else:
            # Se ci sono porte specifiche, usa solo quelle
            ports_to_scan = specific_ports

        # Unisci le porte specifiche con l'intervallo di porte, evitando duplicati
        ports_to_scan = list(set(ports_to_scan))  # Usa un set per rimuovere duplicati

        # Crea una coda per raccogliere i risultati
        result_queue = queue.Queue()

        # Esegui la scansione in un thread separato
        scan_thread = threading.Thread(target=run_scan, args=(target_ip, ports_to_scan, result_queue))
        scan_thread.start()

    except ValueError as e:
        messagebox.showerror("Errore", f"Errore nei dati di input: {str(e)}")
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore inaspettato: {str(e)}")


# Funzione per eseguire la scansione delle porte e aggiornare la UI
def run_scan(target_ip, ports_to_scan, result_queue):
    try:
        open_ports, filtered_ports, closed_ports, error_ports = start_scan(target_ip, ports_to_scan, result_queue)

        # Aggiorna la UI con i risultati
        open_ports_box.delete(1.0, ctk.END)
        for port in open_ports:
            open_ports_box.insert(ctk.END, f"Porta {port}: Aperta\n")
        
        filtered_ports_box.delete(1.0, ctk.END)
        for port in filtered_ports:
            filtered_ports_box.insert(ctk.END, f"Porta {port}: Filtrata\n")
        
        closed_ports_box.delete(1.0, ctk.END)
        for port in closed_ports:
            closed_ports_box.insert(ctk.END, f"Porta {port}: Chiusa\n")
        
        error_ports_box.delete(1.0, ctk.END)  # Pulisce il box delle porte con errore
        for port in error_ports:
            error_ports_box.insert(ctk.END, f"Porta {port}: Errore\n")
        
        # Mostra un messaggio quando la scansione è completa
        messagebox.showinfo("Scansione completata", "La scansione delle porte è terminata.")
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")

def save_scan_results():
    try:
        # Preleva i dati dai box dei risultati
        open_ports_text = open_ports_box.get(1.0, ctk.END).strip()
        filtered_ports_text = filtered_ports_box.get(1.0, ctk.END).strip()
        closed_ports_text = closed_ports_box.get(1.0, ctk.END).strip()
        error_ports_text = error_ports_box.get(1.0, ctk.END).strip()

        # Funzione per estrarre le porte da un testo
        def extract_ports(text):
            return [port.split(":")[0].split()[-1] for port in text.splitlines() if port.strip()]

        # Estrai le porte da ciascun box, se il testo non è vuoto
        open_ports_list = extract_ports(open_ports_text)
        filtered_ports_list = extract_ports(filtered_ports_text)
        closed_ports_list = extract_ports(closed_ports_text)
        error_ports_list = extract_ports(error_ports_text)

        # Trova la lunghezza massima tra le liste
        max_length = max(len(open_ports_list), len(filtered_ports_list), len(closed_ports_list), len(error_ports_list))

        # Riempi le liste con None (o un valore vuoto) fino alla lunghezza massima
        open_ports_list.extend([None] * (max_length - len(open_ports_list)))
        filtered_ports_list.extend([None] * (max_length - len(filtered_ports_list)))
        closed_ports_list.extend([None] * (max_length - len(closed_ports_list)))
        error_ports_list.extend([None] * (max_length - len(error_ports_list)))

        # Crea un DataFrame con i risultati
        df = pd.DataFrame({
            "Open Ports": open_ports_list,
            "Filtered Ports": filtered_ports_list,
            "Closed Ports": closed_ports_list,
            "Error Ports": error_ports_list,
        })

        # Salva i risultati in un file Excel
        file_path = "scan_results.xlsx"
        df.to_excel(file_path, index=False)

        messagebox.showinfo("Salvataggio completato", f"I risultati sono stati salvati in {file_path}")

    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore durante il salvataggio dei risultati: {str(e)}")
        
# Funzione di login
def create_ui(authenticate_user):
    login_window = ctk.CTk()
    login_window.title("DD Port Scanner")

    # Calcoliamo la posizione per centrare la finestra
    window_width = 800
    window_height = 600
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    login_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    frame_width = int(window_width * 0.6)  # 60% della larghezza
    frame_height = int(window_height * 0.6)  # 60% dell'altezza

    main_frame = ctk.CTkFrame(login_window, width=frame_width, height=frame_height)
    main_frame.pack_propagate(False)  # Blocca il ridimensionamento automatico
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Carica l'immagine del logo
    logo_image = Image.open("assets/logo.webp")  # Carica l'immagine
    logo_photo = CTkImage(logo_image, size=(100, 100))  # Specifica la dimensione

    img = Image.open("assets/logo.png")
    img_tk = ImageTk.PhotoImage(img)

    # Imposta l'icona
    login_window.iconphoto(False, img_tk)


    # Aggiungi il logo all'interno del frame
    logo_label = ctk.CTkLabel(main_frame, image=logo_photo, text="")
    logo_label.image = logo_photo  # Mantieni il riferimento all'immagine
    logo_label.pack(pady=10)

    # Label e Entry per Username
    username_label = ctk.CTkLabel(main_frame, text="Username:")
    username_label.pack(pady=5)
    username_entry = ctk.CTkEntry(main_frame)
    username_entry.pack(pady=5)

    # Label e Entry per Password
    password_label = ctk.CTkLabel(main_frame, text="Password:")
    password_label.pack(pady=5)
    password_entry = ctk.CTkEntry(main_frame, show="*")
    password_entry.pack(pady=5)

    # Pulsante per effettuare il login
    login_button = ctk.CTkButton(main_frame, text="Login", command=lambda: login(username_entry, password_entry, authenticate_user, login_window))
    login_button.pack(pady=20)

    login_window.mainloop()
