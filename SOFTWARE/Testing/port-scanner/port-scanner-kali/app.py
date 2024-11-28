# app.py
from ui import create_ui
from functions import authenticate_user_fake  # Rimuovi start_scan

def main():
    print("App avviata")  # Aggiungi un print per verificare l'esecuzione
    create_ui(authenticate_user_fake)  # Crea e avvia l'interfaccia utente con un solo argomento

if __name__ == "__main__":
    main()