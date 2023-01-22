import sqlite3
from flask import Flask, request, render_template
from datetime import datetime, timedelta
import logic

app = Flask(__name__)

def add_to_tables():
    conn = connect_db()
    c = conn.cursor()
    c.execute("UPDATE rezerwacje SET DataStartuPobytu=? WHERE NrRezerwacji=?", ("25.01.2023", 4))
    #c.execute("DELETE FROM oceny WHERE 1=1")
    conn.commit()
    conn.close()
    return 'Success'

# do testow
DEFALUT_HOTELS = [(1, "Pod akacjami", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam aliquet tortor quis nulla sollicitudin, vitae aliquet ante pulvinar. Nam ultricies laoreet posuere. Cras mattis neque ante, a fermentum neque tincidunt in. Cras commodo blandit odio, a varius lorem venenatis eget. Nulla arcu neque, venenatis ac metus nec, pulvinar volutpat tellus. Integer in aliquam nisi, nec mollis urna. Vivamus volutpat nunc eget tellus aliquet, in hendrerit urna semper. Donec elit justo, dapibus sed luctus sit amet, rhoncus ac nunc. Integer commodo justo nec posuere iaculis. Nunc viverra eros et dui pharetra, ut interdum orci molestie."),
        (2, "Różany zaułek", "Curabitur at turpis magna. Proin rhoncus nisl quis libero bibendum tempor vitae volutpat sapien. Integer arcu risus, malesuada non convallis eu, commodo a justo. Sed sed feugiat erat. Nam sodales ex sem, sit amet tincidunt sem tincidunt quis. Nunc convallis auctor tortor a aliquet. Duis id auctor nulla, sit amet varius lectus. Quisque dictum, neque eu fringilla porttitor, ipsum odio dictum nulla, id maximus tellus mauris a sapien. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Quisque euismod placerat mauris ac porta. Nunc consectetur ipsum at velit mollis laoreet."),
        (3, "Kasztanowe noclegi", "Morbi vel nisl convallis, dignissim quam sit amet, consequat leo. Etiam blandit mi tellus, vitae pretium velit aliquam vel. Phasellus ipsum arcu, faucibus a risus a, convallis scelerisque felis. Suspendisse finibus non turpis sit amet semper. Quisque scelerisque justo vitae mauris consectetur, eget pretium purus efficitur. Nam a commodo urna. In sed odio fringilla, pharetra enim at, malesuada leo."),
        (4, "Spa & Deluxe", "Vivamus posuere ex sed tristique suscipit. Nulla scelerisque, eros et lacinia blandit, diam nisl scelerisque velit, eget faucibus est justo ac ipsum. Curabitur in lorem sem. Fusce sit amet sapien volutpat, lobortis lacus eget, tincidunt turpis. Curabitur vitae aliquam quam. Ut ut libero velit. Cras ac nisi posuere, elementum augue ut, placerat dolor. Vivamus ullamcorper mauris ex, quis ultricies risus venenatis non. Quisque consequat tortor ac felis eleifend, id elementum lorem tincidunt. Nunc porttitor vitae nunc non scelerisque.")]

DEFAULT_ROOMS = [
    (1, "Room1", "Best room"),
    (1, "Room2", "This one is the best"),
    (3, "Room3", "And this with long descr. Vivamus posuere ex sed tristique suscipit. Nulla scelerisque, eros et lacinia blandit, diam nisl scelerisque velit, eget faucibus est justo ac ipsum. Curabitur in lorem sem. Fusce sit amet sapien volutpat, lobortis lacus eget, tincidunt turpis. Curabitur vitae aliquam quam. Ut ut libero velit. Cras ac nisi posuere, elementum augue ut, placerat dolor. Vivamus ullamcorper mauris ex, quis ultricies risus venenatis non. Quisque consequat tortor ac felis eleifend, id elementum lorem tincidunt. Nunc porttitor vitae nunc non scelerisque.")
]

DEFAULT_RATES = [
    #id, name, stars, desc
    (1, "user1", 2, "Good hotel"),
    (2, "user2", 4, "Very good hotel"),
    (3, "user3", 5, "Excelent hotel")
]

def connect_db():
    return sqlite3.connect('C:/Users/herna/PycharmProjects/aplikacja_hotel/test.db')

@app.route('/')
def index():
    add_to_tables()
    return "Hello, Worldy!"

@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/hotelsRate', methods=['GET', 'POST'])
def hotelsRate():
    conn = connect_db()
    c = conn.cursor()
    if request.method == 'POST':     
        hotel_id = request.form["hotel_id"]
        description = request.form["description"]
        stars = request.form["stars"]
        print("hotel_id=", hotel_id, "| desc=" , description, "| stars=", stars)
        date = datetime.now()
        stringDate = str(date.day) + '.' + str(date.month) + '.' + str(date.year)
        c.execute("INSERT INTO oceny (IdHotelu,IdUzytkownika,Data,Gwiazdki,Opis) VALUES (?,?,?,?,?)",
                  (hotel_id, 2, stringDate, stars, description)) #id uzytkownika na sztywno (2)
        conn.commit()
        # TODO: Domcio, popup if add rate was successful (later)
    #select hotele gdzie uzytkownik mial rezerwacje
    c.execute("SELECT hotele.IdHotelu, Nazwa, Opis FROM hotele INNER JOIN pokoje ON hotele.IdHotelu = pokoje.IdHotelu INNER JOIN rezerwacje_pokojow ON pokoje.IdPokoju = rezerwacje_pokojow.IdPokoju INNER JOIN rezerwacje ON rezerwacje_pokojow.NrRezerwacji = rezerwacje.NrRezerwacji   WHERE IdKlienta = 2")  # podawanie id na sztywno - nie mamy logowania
    rows = c.fetchall()
    conn.close()
    return render_template('hotelsRate.html', hotels=rows)

@app.route('/hotelsRateConfirm', methods=['GET', 'POST'])
def hotelsRateConfirm():
    if request.method == 'POST':
        name = request.form["name"]
        
        print(request.form["name"])
        print(request.form["email"])
        return render_template('hotelsRateConfirm.html', name=name)

    return render_template('hotelsRateConfirm.html')
    
    

@app.route('/hotels')
def hotels():
    return render_template('hotels.html')

@app.route('/hotelsSelect')
def hotelsSelect():
    return render_template('hotelsSelect.html', hotels=DEFALUT_HOTELS)

@app.route('/hotelView/<hotel_id>', methods=['GET', 'POST'])
def hotelView(hotel_id=None):    
    # co jeśli hotel_id nie jest już w bazie danych?
    
    if request.method == 'POST':
        print("POST")
        room_id = request.form["room_id"]
        date = request.form["room_id"]
        days = request.form["days"]
        discount_code = request.form["discount_code"]
        
        print(request.form)
        
    #TODO: db operations
    
    #TODO: Dominik, jesli popupy zadzialaja po POST, to pododawac
    #TODO: jakis rodzaj walidacji
    
    return render_template('hotelView.html', hotel=DEFALUT_HOTELS[0], average=3,  rooms=DEFAULT_ROOMS, rates=DEFAULT_RATES)

@app.route('/hotelsRemoveReservation', methods=['GET', 'POST'])
def hotelRemoveReservation():

    conn = connect_db()
    c = conn.cursor()
    if request.method == 'POST':
        reservationToDelete = request.form["delete"]
        c.execute("SELECT DataStartuPobytu FROM rezerwacje WHERE NrRezerwacji=?",(reservationToDelete,))
        startDate = c.fetchone()[0].strip()
        lastTimeToCancel = datetime.strptime(startDate, '%d.%m.%Y') - timedelta(days=7)
        now = datetime.now()
        if lastTimeToCancel > now:
            c.execute("DELETE FROM rezerwacje WHERE NrRezerwacji=?", (reservationToDelete,))
            c.execute("DELETE FROM rezerwacje_pokojow WHERE NrRezerwacji=?", (reservationToDelete,))
        else:
            print("Nie da się usunąć rezerwacji")
            #TODO popup

    c.execute("SELECT rezerwacje.NrRezerwacji, Nazwa, Opis FROM hotele INNER JOIN pokoje ON hotele.IdHotelu = pokoje.IdHotelu INNER JOIN rezerwacje_pokojow ON pokoje.IdPokoju = rezerwacje_pokojow.IdPokoju INNER JOIN rezerwacje ON rezerwacje_pokojow.NrRezerwacji = rezerwacje.NrRezerwacji   WHERE IdKlienta = 2") #podawanie id na sztywno - nie mamy logowania
    rows = c.fetchall()
    #print(rows)
    conn.commit()
    conn.close()
    
    return render_template('hotelsRemoveReservation.html', hotels=rows)

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
