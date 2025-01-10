import customtkinter as ctk
from tkinter import messagebox, filedialog
from customtkinter import CTkImage
import requests
import sys
import os
from tkinter import PhotoImage
from PIL import Image, ImageTk

# # Funzione di login tramite API
# def login(username_entry, password_entry, login_window):
#     username = username_entry.get()
#     password = password_entry.get()

#     url = "http://localhost:5000/auth"  # Assumiamo che il backend API sia in ascolto su questa porta
#     data = {"username": username, "password": password}

#     try:
#         response = requests.post(url, json=data)
#         if response.status_code == 200 and response.json().get("success"):
#             login_window.destroy()
#             show_main_window()
#         else:
#             messagebox.showerror("Errore", "Credenziali non valide.")
#     except requests.exceptions.RequestException as e:
#         messagebox.showerror("Errore di Connessione", f"Impossibile connettersi al backend: {str(e)}")

def fake_login(username_entry, password_entry, login_window):
    username = username_entry.get()
    password = password_entry.get()

    # Login fittizio con username e password "admin"
    if username == "admin" and password == "admin":
        login_window.destroy()
        show_main_window()
    else:
        messagebox.showerror("Errore", "Credenziali non valide.")

# Funzione per inviare le richieste HTTP
def send_requests(url_entry, selected_methods, headers_entry, body_entry, response_box, error_box):
    url = url_entry.get()
    headers = headers_entry.get()
    body = body_entry.get()
    
    response_box.delete(1.0, ctk.END)
    error_box.delete(1.0, ctk.END)

    if not url:
        messagebox.showerror("Errore", "Inserire un URL valido.")
        return

    for method in selected_methods:
        try:
            response = requests.request(method, url, headers=eval(headers) if headers else None, data=body)
            response_box.insert(ctk.END, f"Metodo {method}:\n{response.status_code} {response.reason}\n{response.text}\n\n")
        except Exception as e:
            error_box.insert(ctk.END, f"Metodo {method}:\nErrore: {str(e)}\n\n")

def save_logs(response_box, error_box):
    folder_path = filedialog.askdirectory(title="Seleziona cartella di destinazione")
    if not folder_path:
        return  # L'utente ha annullato la selezione

    file_path = f"{folder_path}/log.txt"
    
    try:
        with open(file_path, "w") as file:
            file.write("=== Risposte ===\n")
            file.write(response_box.get(1.0, ctk.END))
            file.write("\n=== Errori ===\n")
            file.write(error_box.get(1.0, ctk.END))
        messagebox.showinfo("Salvataggio", f"Log salvato con successo in: {file_path}")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il salvataggio: {str(e)}")


# Funzione per mostrare la finestra principale
def show_main_window():
    main_window = ctk.CTk()

    # Configurazione finestra principale
    main_window.geometry("900x800")
    main_window.title("DD HTTP Request Tester")

    # Layout principale: Colonne
    left_frame = ctk.CTkFrame(main_window)
    left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    right_frame = ctk.CTkFrame(main_window)
    right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    # Sezione input
    url_label = ctk.CTkLabel(left_frame, text="URL:")
    url_label.pack(pady=5)
    url_entry = ctk.CTkEntry(left_frame, width=300)
    url_entry.pack(pady=5)

    headers_label = ctk.CTkLabel(left_frame, text="Headers (formato dizionario):")
    headers_label.pack(pady=5)
    headers_entry = ctk.CTkEntry(left_frame, width=300)
    headers_entry.pack(pady=5)

    body_label = ctk.CTkLabel(left_frame, text="Body:")
    body_label.pack(pady=5)
    body_entry = ctk.CTkEntry(left_frame, width=300)
    body_entry.pack(pady=5)

    # Aggiungi i checkbox per i metodi HTTP
    methods_frame = ctk.CTkFrame(left_frame)
    methods_frame.pack(pady=10)

    methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "TRACE"]
    selected_methods = []

    def on_method_change():
        selected_methods.clear()
        for method, var in checkboxes.items():
            if var.get():
                selected_methods.append(method)

    checkboxes = {}
    for method in methods:
        var = ctk.BooleanVar()
        checkbox = ctk.CTkCheckBox(methods_frame, text=method, variable=var, command=on_method_change)
        checkbox.pack(anchor="w", pady=5)
        checkboxes[method] = var

    # Funzione per selezionare/deselezionare tutti i metodi
    def toggle_select_all():
        select_all = select_all_var.get()
        if select_all:
            select_all_checkbox.configure(text="Deseleziona Tutti")
        else:
            select_all_checkbox.configure(text="Seleziona Tutti")
        for method, var in checkboxes.items():
            var.set(select_all)
        on_method_change()

    # Variabile per la checkbox "Seleziona Tutti"
    select_all_var = ctk.BooleanVar(value=False)

    # Checkbox "Seleziona Tutti/Deseleziona Tutti"
    select_all_checkbox = ctk.CTkCheckBox(
        methods_frame,
        text="Seleziona Tutti",
        variable=select_all_var,
        command=toggle_select_all
    )
    select_all_checkbox.pack(anchor="w", pady=5)

    # Pulsante per inviare le richieste
    send_button = ctk.CTkButton(left_frame, text="Invia Richieste", 
                                command=lambda: send_requests(url_entry, selected_methods, headers_entry, body_entry, response_box, error_box))
    send_button.pack(pady=20)

    # Sezione output
    response_label = ctk.CTkLabel(right_frame, text="Risposta:")
    response_label.pack(pady=5)
    response_box = ctk.CTkTextbox(right_frame, width=400, height=200)
    response_box.pack(pady=5)

    error_label = ctk.CTkLabel(right_frame, text="Errori:")
    error_label.pack(pady=5)
    error_box = ctk.CTkTextbox(right_frame, width=400, height=200)
    error_box.pack(pady=5)

    # Pulsante per salvare i log
    save_button = ctk.CTkButton(left_frame, text="Salva Log", 
                                command=lambda: save_logs(response_box, error_box))
    save_button.pack(pady=10)

    # Layout ridimensionabile
    main_window.grid_rowconfigure(0, weight=1)
    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_columnconfigure(1, weight=1)

    main_window.mainloop()

# Funzione di login con API
def create_ui():
    login_window = ctk.CTk()
    login_window.title("DD HTTP Request Tester - Login")

    # Configurazione finestra di login
    login_window.geometry("900x800")
    frame_width = 500
    frame_height = 500

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

    # Pulsante di login
    # login_button = ctk.CTkButton(main_frame, text="Login", 
    #                              command=lambda: login(username_entry, password_entry, login_window))
    login_button = ctk.CTkButton(main_frame, text="Login", 
                                 command=lambda: fake_login(username_entry, password_entry, login_window))
    login_button.pack(pady=20)

    login_window.mainloop()

create_ui()
