# from flask import Flask, request, jsonify # type: ignore
# from pymongo import MongoClient # type: ignore
# import socket

# # Configurazioni
# from config import DB_URI, DB_NAME

# # Connessione a MongoDB
# client = MongoClient(DB_URI)
# db = client[DB_NAME]
# users_collection = db["usernames"]

# app = Flask(__name__)

# # Endpoint per autenticazione
# @app.route('/auth', methods=['POST'])
# def authenticate():
#     data = request.json
#     username = data.get("username")
#     password = data.get("password")
    
#     user = users_collection.find_one({"username": username, "password": password})
#     if user:
#         return jsonify({"success": True, "message": "Login effettuato con successo"})
#     else:
#         return jsonify({"success": False, "message": "Username o password errati"}), 401

# # Endpoint per scansione porte
# @app.route('/scan', methods=['POST'])
# def port_scan():
#     data = request.json
#     target_ip = data.get("target_ip")
#     start_port = data.get("start_port")
#     end_port = data.get("end_port")
    
#     if not (target_ip and start_port and end_port):
#         return jsonify({"success": False, "message": "Parametri mancanti"}), 400

#     open_ports = []
#     for port in range(start_port, end_port + 1):
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.settimeout(1)
#         result = sock.connect_ex((target_ip, port))
#         if result == 0:
#             open_ports.append(port)
#         sock.close()
    
#     return jsonify({"success": True, "open_ports": open_ports})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
