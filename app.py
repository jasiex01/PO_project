import sqlite3
from flask import Flask, request, render_template
import logic

app = Flask(__name__)

# do testow
VALUES = [(None, "Pod akacjami", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam aliquet tortor quis nulla sollicitudin, vitae aliquet ante pulvinar. Nam ultricies laoreet posuere. Cras mattis neque ante, a fermentum neque tincidunt in. Cras commodo blandit odio, a varius lorem venenatis eget. Nulla arcu neque, venenatis ac metus nec, pulvinar volutpat tellus. Integer in aliquam nisi, nec mollis urna. Vivamus volutpat nunc eget tellus aliquet, in hendrerit urna semper. Donec elit justo, dapibus sed luctus sit amet, rhoncus ac nunc. Integer commodo justo nec posuere iaculis. Nunc viverra eros et dui pharetra, ut interdum orci molestie."),
        (None, "Różany zaułek", "Curabitur at turpis magna. Proin rhoncus nisl quis libero bibendum tempor vitae volutpat sapien. Integer arcu risus, malesuada non convallis eu, commodo a justo. Sed sed feugiat erat. Nam sodales ex sem, sit amet tincidunt sem tincidunt quis. Nunc convallis auctor tortor a aliquet. Duis id auctor nulla, sit amet varius lectus. Quisque dictum, neque eu fringilla porttitor, ipsum odio dictum nulla, id maximus tellus mauris a sapien. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Quisque euismod placerat mauris ac porta. Nunc consectetur ipsum at velit mollis laoreet."),
        (None, "Kasztanowe noclegi", "Morbi vel nisl convallis, dignissim quam sit amet, consequat leo. Etiam blandit mi tellus, vitae pretium velit aliquam vel. Phasellus ipsum arcu, faucibus a risus a, convallis scelerisque felis. Suspendisse finibus non turpis sit amet semper. Quisque scelerisque justo vitae mauris consectetur, eget pretium purus efficitur. Nam a commodo urna. In sed odio fringilla, pharetra enim at, malesuada leo."),
        (None, "Spa & Deluxe", "Vivamus posuere ex sed tristique suscipit. Nulla scelerisque, eros et lacinia blandit, diam nisl scelerisque velit, eget faucibus est justo ac ipsum. Curabitur in lorem sem. Fusce sit amet sapien volutpat, lobortis lacus eget, tincidunt turpis. Curabitur vitae aliquam quam. Ut ut libero velit. Cras ac nisi posuere, elementum augue ut, placerat dolor. Vivamus ullamcorper mauris ex, quis ultricies risus venenatis non. Quisque consequat tortor ac felis eleifend, id elementum lorem tincidunt. Nunc porttitor vitae nunc non scelerisque.")]

def connect_db():
    return sqlite3.connect('C:/Users/herna/PycharmProjects/aplikacja_hotel/test.db')

@app.route('/')
def index():
    return "Hello, Worldy!"

@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/hotelsRate')
def hotelsRate():    
    return render_template('hotelsRate.html', hotels=VALUES)

@app.route('/hotels')
def hotels():
    return render_template('hotels.html')

@app.route('/hotelsSelect')
def hotelsSelect():
    return render_template('hotelsSelect.html')

@app.route('/hotelView')
def hotelView():
    return render_template('hotelView.html')

@app.route('/hotelsRemoveReservation')
def hotelRemoveReservation():
    return render_template('hotelsRemoveReservation.html')

@app.route('/insert_user', methods=['POST'])
def insert_user():
    data = request.get_json()
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS uzytkownicy (
                    IdUzytkownika INTEGER PRIMARY KEY,
                    TypUzytkownika TEXT NOT NULL,
                    Login TEXT NOT NULL,
                    Haslo TEXT NOT NULL,
                    Email TEXT NOT NULL,
                    ImieNazwisko TEXT NOT NULL,
                    Saldo REAL
                    )""")
    c.execute("INSERT INTO uzytkownicy (TypUzytkownika,Login,Haslo,Email,ImieNazwisko,Saldo) VALUES (?,?,?,?,?,?)",
              (data['TypUzytkownika'], data['Login'],data['Haslo'], data['Email'],data['ImieNazwisko'], data['Saldo']))
    conn.commit()
    conn.close()
    return "User created."

@app.route('/insert_hotel', methods=['POST'])
def insert_hotel():
    data = request.get_json()
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS hotele (
                    IdHotelu INTEGER PRIMARY KEY,
                    WlascicielHotelu INTEGER NOT NULL,
                    Nazwa TEXT NOT NULL,
                    Opis TEXT,
                    FOREIGN KEY (WlascicielHotelu) REFERENCES uzytkownicy(IdUzytkownika)
                    )""")
    c.execute("INSERT INTO hotele (WlascicielHotelu,Nazwa,Opis) VALUES (?,?,?)",
              (data['WlascicielHotelu'], data['Nazwa'], data['Opis']))
    conn.commit()
    conn.close()
    return "Hotel created."

@app.route('/insert_room', methods=['POST'])
def insert_room():
    data = request.get_json()
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS pokoje (
                    IdPokoju INTEGER PRIMARY KEY,
                    IdHotelu INTEGER NOT NULL,
                    IloscDoroslych INTEGER NOT NULL,
                    IloscDzieci INTEGER NOT NULL,
                    Balkon INTEGER NOT NULL,
                    Klimatyzacja INTEGER NOT NULL,
                    Minibar INTEGER NOT NULL,
                    Lazienka INTEGER NOT NULL,
                    Czajnik INTEGER NOT NULL,
                    Wifi INTEGER NOT NULL,
                    Telewizor INTEGER NOT NULL,
                    FOREIGN KEY (IdHotelu) REFERENCES hotele(IdHotelu)
                    )""")
    c.execute("INSERT INTO pokoje (IdHotelu,IloscDoroslych,IloscDzieci,Balkon,Klimatyzacja,Minibar,Lazienka,Czajnik,Wifi,Telewizor) VALUES (?,?,?,?,?,?,?,?,?,?)",
              (data['IdHotelu'], data['IloscDoroslych'],data['IloscDzieci'], data['Balkon'],data['Klimatyzacja'],data['Minibar'],data['Lazienka'],data['Czajnik'],data['Wifi'],data['Telewizor']))
    conn.commit()
    conn.close()
    return "Room created."

@app.route('/insert_address', methods=['POST'])
def insert_address():
    data = request.get_json()
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS adresy (
                    IdAdresu INTEGER PRIMARY KEY,
                    IdHotelu INTEGER NOT NULL,
                    KodPocztowy TEXT NOT NULL,
                    Miasto TEXT NOT NULL,
                    Numer INTEGER NOT NULL,
                    Ulica TEXT NOT NULL,
                    FOREIGN KEY (IdHotelu) REFERENCES hotele(IdHotelu)
                    )""")
    c.execute("INSERT INTO adresy (IdHotelu,KodPocztowy,Miasto,Numer,Ulica) VALUES (?,?,?,?,?)",
              (data['IdHotelu'], data['KodPocztowy'],data['Miasto'], data['Numer'],data['Ulica']))
    conn.commit()
    conn.close()
    return "Address created."

@app.route('/insert_rating', methods=['POST'])
def insert_rating():
    data = request.get_json()
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS oceny (
                    IdOceny INTEGER PRIMARY KEY,
                    IdHotelu INTEGER NOT NULL,
                    IdUzytkownika INTEGER NOT NULL,
                    Data TEXT NOT NULL,
                    Gwiazdki INTEGER NOT NULL,
                    Opis TEXT NOT NULL,
                    FOREIGN KEY (IdHotelu) REFERENCES hotele(IdHotelu),
                    FOREIGN KEY (IdUzytkownika) REFERENCES uzytkownicy(IdUzytkownika)
                    )""")
    c.execute("INSERT INTO oceny (IdHotelu,IdUzytkownika,Data,Gwiazdki,Opis) VALUES (?,?,?,?,?)",
              (data['IdHotelu'], data['IdUzytkownika'],data['Data'], data['Gwiazdki'],data['Opis']))
    conn.commit()
    conn.close()
    return "Rating created."

@app.route('/insert_discount', methods=['POST'])
def insert_discount():
    data = request.get_json()
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS rabaty (
                    NrRabatu INTEGER PRIMARY KEY,
                    Status INTEGER NOT NULL,
                    Obnizka REAL NOT NULL,
                    DataWaznosci TEXT NOT NULL
                    )""")
    c.execute("INSERT INTO rabaty (NrRabatu, Status, Obnizka, DataWaznosci) VALUES (?,?,?,?)",
              (data['NrRabatu'], data['Status'], data['Obnizka'], data['DataWaznosci']))
    conn.commit()
    conn.close()
    return "Discount created."

@app.route('/insert_reservation', methods=['POST'])
def insert_reservation():
    data = request.get_json()
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS rezerwacje (
                    NrRezerwacji INTEGER PRIMARY KEY,
                    IdKlienta INTEGER NOT NULL,
                    Cena REAL NOT NULL,
                    DataDokonaniaRezerwacji TEXT NOT NULL,
                    DataStartuPobytu TEXT NOT NULL,
                    IloscNoclegow INTEGER NOT NULL,
                    FOREIGN KEY (IdKlienta) REFERENCES uzytkownicy(IdUzytkownika)
                    )""")
    c.execute("INSERT INTO rezerwacje (IdKlienta, Cena, DataDokonaniaRezerwacji, DataStartuPobytu, IloscNoclegow) VALUES (?,?,?,?,?)",
              (data['IdKlienta'], data['Cena'], data['DataDokonaniaRezerwacji'], data['DataStartuPobytu'], data['IloscNoclegow']))
    conn.commit()
    conn.close()
    return "Reservation created."

@app.route('/insert_reservation_room', methods=['POST'])
def insert_reservation_room():
    data = request.get_json()
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS rezerwacje_pokojow (
                    NrRezerwacji INTEGER NOT NULL,
                    IdPokoju INTEGER NOT NULL,
                    PRIMARY KEY (NrRezerwacji, IdPokoju),
                    FOREIGN KEY (NrRezerwacji) REFERENCES rezerwacje(NrRezerwacji),
                    FOREIGN KEY (IdPokoju) REFERENCES pokoje(IdPokoju)
                    )""")
    c.execute("INSERT INTO rezerwacje_pokojow (NrRezerwacji, IdPokoju) VALUES (?,?)",
              (data['NrRezerwacji'], data['IdPokoju']))
    conn.commit()
    conn.close()
    return "Reservation room created."

if __name__ == '__main__':
    app.run(debug=True)
