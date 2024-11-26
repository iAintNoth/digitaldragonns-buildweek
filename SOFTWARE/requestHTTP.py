import requests # type:ignore

def check_metodi():
    url=input("Inserisci l'url da verificare: ").strip()
    methods=["GET","POST","PUT","DELETE","OPTIONS","HEAD","PATCH"]
    for method in methods:
        try:
            response=requests.request(method,url)
            print(f"Metodo {method}: {response.status_code} {response.reason}")
        except requests.exceptions.HTTPError as http_err:
            print(f"Errore HTTP con il metodo {method}: {http_err}")

if __name__=="__main__":
    check_metodi()