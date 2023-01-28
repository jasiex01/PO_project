import sqlite3
from flask import Flask, request, render_template,Markup
from datetime import datetime, timedelta

app = Flask(__name__)

def add_to_tables():
    conn = connect_db()
    c = conn.cursor()
    #c.execute("UPDATE rezerwacje SET DataStartuPobytu=? WHERE NrRezerwacji=?", ("25.01.2023", 4))
    #c.execute("INSERT INTO rabaty (NrRabatu,Status,Obnizka,DataWaznosci) VALUES (?,?,?,?)", (1234, 0, 20, "30.12.2023"))
    #c.execute("INSERT INTO rabaty (NrRabatu,Status,Obnizka,DataWaznosci) VALUES (?,?,?,?)", (1111, 0, 20, "30.12.2023"))
    #c.execute("INSERT INTO rabaty (NrRabatu,Status,Obnizka,DataWaznosci) VALUES (?,?,?,?)", (2222, 0, 20, "30.12.2023"))
    #c.execute("INSERT INTO rabaty (NrRabatu,Status,Obnizka,DataWaznosci) VALUES (?,?,?,?)", (3333, 0, 20, "30.12.2023"))
    #c.execute("INSERT INTO rabaty (NrRabatu,Status,Obnizka,DataWaznosci) VALUES (?,?,?,?)", (4444, 0, 20, "30.12.2023"))
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
    return sqlite3.connect('test.db')

@app.route('/')
def index():
    #add_to_tables()
    return render_template('main.html')

@app.route('/stars', methods=['GET', 'POST'])
def stars():
    if request.method == 'POST':     
        print(request.form)
    #add_to_tables()
    return render_template('stars.html')

@app.route('/hotelsRate', methods=['GET', 'POST'])
def hotelsRate():
    popup = (False, '')
    
    conn = connect_db()
    c = conn.cursor()
    if request.method == 'POST':     
        
        print(request.form)
        
        hotel_id = request.form["hotel_id"]
        description = request.form["description"]
        stars = request.form["stars"]
        #print("hotel_id=", hotel_id, "| desc=" , description, "| stars=", stars)
        date = datetime.now()
        stringDate = str(date.day) + '.' + str(date.month) + '.' + str(date.year)
        c.execute("INSERT INTO oceny (IdHotelu,IdUzytkownika,Data,Gwiazdki,Opis) VALUES (?,?,?,?,?)",
                  (hotel_id, 2, stringDate, stars, description)) #id uzytkownika na sztywno (2)
        conn.commit()
        # TODO: Domcio, popup if add rate was successful (later)              
        popup = (True, 'Pomyślnie dodano nową ocenę.')
    #select hotele gdzie uzytkownik mial rezerwacje
    c.execute("SELECT hotele.IdHotelu, Nazwa, Opis FROM hotele INNER JOIN pokoje ON hotele.IdHotelu = pokoje.IdHotelu INNER JOIN rezerwacje_pokojow ON pokoje.IdPokoju = rezerwacje_pokojow.IdPokoju INNER JOIN rezerwacje ON rezerwacje_pokojow.NrRezerwacji = rezerwacje.NrRezerwacji   WHERE IdKlienta = 2")
    rows = c.fetchall()
    conn.close()
    return render_template('hotelsRate.html', hotels=rows, popup=popup)
    

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

@app.route('/hotelsResSelect')
def hotelsResSelect():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT hotele.IdHotelu, Nazwa, Opis FROM hotele")
    rows = c.fetchall()
    # print(rows)
    conn.commit()
    conn.close()
    return render_template('hotelsResSelect.html', hotels=rows)


@app.route('/hotelResView/<hotel_id>', methods=['GET', 'POST'])
def hotelResView(hotel_id=None):
    popup = (False, '')
    
    conn = connect_db()
    c = conn.cursor()
    if request.method == 'POST':
        room_id = request.form["room_id"]
        date = request.form["date"]
        days = request.form["days"]
        discount_code = request.form["discount_code"]
        
        print("REQUEST FORM = ", request.form)

        if date != 1 and days != '':
            cena = 200.0 + 15.0 * float(room_id) + 60.0 * float(days)
            today = datetime.now().strftime("%d.%m.%Y")
            if discount_code != '':
                c.execute("SELECT Obnizka FROM rabaty WHERE NrRabatu=? AND Status = 0 AND dataWaznosci > ? ",(discount_code, today))
                obnizka = c.fetchall()
                print("OBNIZKA: ", obnizka)
                if len(obnizka) != 0:
                    cena = cena - obnizka[0][0]/100.0 * cena
                    c.execute("INSERT INTO rezerwacje (IdKlienta, Cena, DataDokonaniaRezerwacji, DataStartuPobytu, IloscNoclegow) VALUES (?,?,?,?,?)",(2, cena, today, date, days))
                    c.execute("INSERT INTO rezerwacje_pokojow (NrRezerwacji,IdPokoju) VALUES (?,?)", (c.lastrowid, room_id))
                    c.execute("UPDATE rabaty SET Status=1 WHERE NrRabatu=?", (discount_code, ))
                    print("Dokonano rezerwacji z rabatem")
                    popup = (True, "Dokonano rezerwacji z rabatem")
                else:
                    print("Blad rezerwacji")
                    popup = (True, "Niepoprawny kod rabatowy")
            else:
                c.execute("INSERT INTO rezerwacje (IdKlienta, Cena, DataDokonaniaRezerwacji, DataStartuPobytu, IloscNoclegow) VALUES (?,?,?,?,?)",(2, cena, today, date, days))
                c.execute("INSERT INTO rezerwacje_pokojow (NrRezerwacji,IdPokoju) VALUES (?,?)", (c.lastrowid, room_id))
                print("Dokonano rezerwacji")
                popup = (True, "Pomyślnie dokonano rezerwacji")
        else:
            print("Blad rezerwacji")
            popup = (True, "Powinny być wprowadzone dane")

    c.execute("SELECT IdOceny, ImieNazwisko, Gwiazdki, oceny.Opis FROM hotele INNER JOIN oceny ON hotele.IdHotelu = oceny.IdHotelu INNER JOIN uzytkownicy ON uzytkownicy.IdUzytkownika = oceny.IdUzytkownika WHERE hotele.IdHotelu = ?",(hotel_id,))
    ratesRows = c.fetchall()
    c.execute("SELECT hotele.IdHotelu, Nazwa, Opis FROM hotele WHERE hotele.IdHotelu = ?", (hotel_id,))
    hotelInfo = c.fetchone()
    c.execute("SELECT AVG(Gwiazdki) FROM oceny WHERE IdHotelu = ?", (hotel_id,))
    avgRating = c.fetchone()[0]
    if avgRating:
        avgRating = (int)(avgRating)
    else:
        avgRating = 0

    c.execute("SELECT IloscDoroslych,IloscDzieci,Balkon,Klimatyzacja,Minibar,Lazienka,Czajnik,Wifi,Telewizor, IdPokoju FROM pokoje WHERE IdHotelu = ?",(hotel_id,))
    roomsInfo = c.fetchall()
    roomsArray = []
    i = 0
    for room in roomsInfo:
        roomTuple = ()
        i = i + 1
        roomTuple = roomTuple + (str(room[9]), str('Pokój ' + str(i)),)
        infoArray = []
        for x in range(7):
            if room[x + 2] == 0:
                infoArray.append('Nie')
            else:
                infoArray.append('Tak')

        text = 'Ilość dorosłych: ' + str(room[0]) + ' Ilość dzieci: ' + str(room[1]) + '<br>Balkon: ' + infoArray[
            0] + ' Klimatyzacja: ' + infoArray[1] + '<br>Minibar: ' + infoArray[2] + ' Łazienka: ' + infoArray[
                   3] + '<br>Czajnik: ' + infoArray[4] + ' Wi-fi: ' + infoArray[5] + '<br>Telewizor: ' + infoArray[
                   6]
        roomTuple = roomTuple + (Markup(text),)
        roomsArray.append(roomTuple)
    print(roomsArray)
    #TODO popupy
    conn.commit()
    conn.close()

    #TODO: Dominik, jesli popupy zadzialaja po POST, to pododawac

    return render_template('hotelResView.html', hotel=hotelInfo, average=avgRating,  rooms=roomsArray, rates=ratesRows, popup=popup)

# TO BEDZIE TYLKO WYSWIETLANIE OCEN HOTELU
@app.route('/hotelView/<hotel_id>')
def hotelView(hotel_id=None):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT IdOceny, ImieNazwisko, Gwiazdki, oceny.Opis FROM hotele INNER JOIN oceny ON hotele.IdHotelu = oceny.IdHotelu INNER JOIN uzytkownicy ON uzytkownicy.IdUzytkownika = oceny.IdUzytkownika WHERE hotele.IdHotelu = ?", (hotel_id,))
    ratesRows = c.fetchall()
    c.execute("SELECT hotele.IdHotelu, Nazwa, Opis FROM hotele WHERE hotele.IdHotelu = ?", (hotel_id,))
    hotelInfo = c.fetchone()
    c.execute("SELECT AVG(Gwiazdki) FROM oceny WHERE IdHotelu = ?", (hotel_id,)) 
    avgRating = c.fetchone()[0]
    print(avgRating)
    if avgRating:
        avgRating = (int) (avgRating)
    else:
        avgRating = 0
    
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

# jest blad po usunieciu rezerwacji i probie odswiezenia strony
# ale nie jest bardzo istotny
@app.route('/hotelsRemoveReservation', methods=['GET', 'POST'])
def hotelRemoveReservation():
    
    popup = (False, '') # popup

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
            
            popup = (True, 'Rezerwacja została usunięta.')
        else:
            print("Nie da się usunąć rezerwacji")
            
            popup = (True, 'Rezerwacja nie została usunięta.')

    c.execute("SELECT rezerwacje.NrRezerwacji, Nazwa, Opis FROM hotele INNER JOIN pokoje ON hotele.IdHotelu = pokoje.IdHotelu INNER JOIN rezerwacje_pokojow ON pokoje.IdPokoju = rezerwacje_pokojow.IdPokoju INNER JOIN rezerwacje ON rezerwacje_pokojow.NrRezerwacji = rezerwacje.NrRezerwacji   WHERE IdKlienta = 2") #podawanie id na sztywno - nie mamy logowania
    rows = c.fetchall()
    #print(rows)
    conn.commit()
    conn.close()
    
    return render_template('hotelsRemoveReservation.html', hotels=rows, popup=popup)

if __name__ == '__main__':
    app.run(debug=True)
