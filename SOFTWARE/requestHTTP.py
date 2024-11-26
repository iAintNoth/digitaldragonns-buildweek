import requests # type:ignore
import os
import datetime
import logging

desktop_path=os.path.join(os.path.expanduser("~"), "Desktop")
log_filename=datetime.now.strftime("scan_log_%Y-%m-%d_%H-%M-%S.log")
log_filepath=os.path.join(desktop_path, log_filename)
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s-%(levelname)s-%(message)s")

def check_metodi():
    url=input("Inserisci l'url da verificare: ").strip()
    methods=["GET","POST","PUT","DELETE","OPTIONS","HEAD","PATCH"]
    for method in methods:
        try:
            response=requests.request(method,url)
            log_message=f"Metodo {method}: {response.status_code} {response.reason}"
            print(f"Metodo {method}: {response.status_code} {response.reason}")
            logging.info(log_message)
        except requests.exceptions.HTTPError as http_err:
            print(f"Errore HTTP con il metodo {method}: {http_err}")
            logging.error(log_message)
            log_error=f"Errore HTTP con il metodo {method}: "

if __name__=="__main__":
    check_metodi()