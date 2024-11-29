from ui import create_ui
from auth import authenticate_user  # Importa la funzione di autenticazione

def main():
    print("App avviata")
    create_ui(authenticate_user)

if __name__ == "__main__":
    main()
