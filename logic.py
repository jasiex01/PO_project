import requests
import json

def post_json(route, json_data):
    headers = {'Content-type': 'application/json'}
    try:
        response = requests.post(route, data=json.dumps(json_data), headers=headers)
        if response.status_code != 201:
            raise ValueError(response.text)
    except requests.exceptions.RequestException as e:
        print(e)

def add_user(typ_uzytkownika, login, haslo, email, imienazwisko, saldo):
    json_data = json.dumps({"TypUzytkownika": typ_uzytkownika,"Login": login,"Haslo": haslo,"Email": email,"ImieNazwisko": imienazwisko,"Saldo": saldo })
    post_json('http://localhost:5000/insert_user', json_data)

#TODO add to other tables

