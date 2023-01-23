import sqlite3
from flask import Flask, request, render_template,Markup
from datetime import datetime, timedelta

app = Flask(__name__)

def add_to_tables():
    conn = connect_db()
    c = conn.cursor()
    #c.execute("UPDATE rezerwacje SET DataStartuPobytu=? WHERE NrRezerwacji=?", ("25.01.2023", 4))
    #c.execute("DELETE FROM hotele WHERE Nazwa='Hotel Example'")
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
    return sqlite3.connect('C:/Users/ghern/PycharmProjects/PO_project/test.db')

@app.route('/')
def index():
    #add_to_tables()
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
    c.execute("SELECT hotele.IdHotelu, Nazwa, Opis FROM hotele INNER JOIN pokoje ON hotele.IdHotelu = pokoje.IdHotelu INNER JOIN rezerwacje_pokojow ON pokoje.IdPokoju = rezerwacje_pokojow.IdPokoju INNER JOIN rezerwacje ON rezerwacje_pokojow.NrRezerwacji = rezerwacje.NrRezerwacji   WHERE IdKlienta = 2")
    rows = c.fetchall()
    conn.close()
    return render_template('hotelsRate.html', hotels=rows)
"""
@app.route('/hotelsRateConfirm', methods=['GET', 'POST'])
def hotelsRateConfirm():
    if request.method == 'POST':
        name = request.form["name"]
        
        print(request.form["name"])
        print(request.form["email"])
        return render_template('hotelsRateConfirm.html', name=name)

    return render_template('hotelsRateConfirm.html')
"""
    

@app.route('/hotels')
def hotels():
    return render_template('hotels.html')

@app.route('/hotelsSelect')
def hotelsSelect():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT hotele.IdHotelu, Nazwa, Opis FROM hotele")
    rows = c.fetchall()
    # print(rows)
    conn.commit()
    conn.close()
    return render_template('hotelsSelect.html', hotels=rows)

@app.route('/hotelView/<hotel_id>', methods=['GET', 'POST'])
def hotelView(hotel_id=None):    
    # co jeśli hotel_id nie jest już w bazie danych? - jezeli hotelu nie bedzie w bazie danych to nie bedzie sie pokazywal w hotelsSelect
    #TODO: Dominik zrobic dokonywanie rezerwacji pod innym linkiem, tu jest tylko wsywietlanie ocen
    if request.method == 'POST':
        print("POST")
        room_id = request.form["room_id"]
        date = request.form["room_id"]
        days = request.form["days"]
        discount_code = request.form["discount_code"]
        
        print(request.form)

    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT IdOceny, ImieNazwisko, Gwiazdki, oceny.Opis FROM hotele INNER JOIN oceny ON hotele.IdHotelu = oceny.IdHotelu INNER JOIN uzytkownicy ON uzytkownicy.IdUzytkownika = oceny.IdUzytkownika WHERE hotele.IdHotelu = ?", (hotel_id,))
    ratesRows = c.fetchall()
    c.execute("SELECT hotele.IdHotelu, Nazwa, Opis FROM hotele WHERE hotele.IdHotelu = ?", (hotel_id,))
    hotelInfo = c.fetchone()
    c.execute("SELECT AVG(Gwiazdki) FROM oceny WHERE IdHotelu = ?", (hotel_id,))
    avgRating = c.fetchone()[0]
    c.execute("SELECT IloscDoroslych,IloscDzieci,Balkon,Klimatyzacja,Minibar,Lazienka,Czajnik,Wifi,Telewizor FROM pokoje WHERE IdHotelu = ?", (hotel_id,))
    roomsInfo = c.fetchall()
    roomsArray = []
    i = 0
    for room in roomsInfo:
        roomTuple = ()
        i = i + 1
        roomTuple = roomTuple + (str(i), str('Pokój ' + str(i)),)
        infoArray = []
        for x in range(7):
            if room[x+2] == 0:
                infoArray.append('Nie')
            else:
                infoArray.append('Tak')

        text = 'Ilość dorosłych: ' + str(room[0]) + ' Ilość dzieci: ' + str(room[1]) + '<br>Balkon: ' + infoArray[0] + ' Klimatyzacja: ' + infoArray[1] + '<br>Minibar: ' + infoArray[2] + ' Łazienka: ' + infoArray[3] + '<br>Czajnik: ' + infoArray[4] + ' Wi-fi: ' + infoArray[5] + '<br>Telewizor: ' + infoArray[6]
        roomTuple = roomTuple + (Markup(text),)
        roomsArray.append(roomTuple)

    print(roomsArray)
    conn.commit()
    conn.close()
    #TODO: Dominik, jesli popupy zadzialaja po POST, to pododawac
    #TODO: jakis rodzaj walidacji

    return render_template('hotelView.html', hotel=hotelInfo, average=avgRating,  rooms=roomsArray, rates=ratesRows)

@app.route('/hotelsRemoveReservation', methods=['GET', 'POST'])
def hotelRemoveReservation():

    conn = connect_db()
    c = conn.cursor()
    if request.method == 'POST':
        reservationToDelete = request.form["delete"]
        c.execute("SELECT DataStartuPobytu FROM rezerwacje WHERE NrRezerwacji=?", (reservationToDelete,))
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

if __name__ == '__main__':
    app.run(debug=True)
