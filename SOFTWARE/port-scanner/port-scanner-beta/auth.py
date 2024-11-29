import requests

API_BASE_URL = "http://192.168.1.24:5000"  # Cambia con l'URL del server

def authenticate_user(username, password):
    try:
        response = requests.post(f"{API_BASE_URL}/auth", json={"username": username, "password": password})
        return response.json()
    except Exception as e:
        return {"success": False, "message": f"Errore di connessione: {e}"}
