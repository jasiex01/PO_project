import unittest
from app import app, createRoomArray
from flask import Markup

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    #test funkcjonalny
    def test_hotelResView_get(self): #dynamiczny link - sprawdzam czy strona istnieje
        result = self.client.get('/hotelView/2')
        self.assertEqual(result.status_code, 200)

    #test jednostkowy
    def test_createRoomArray(self):
        expected = [('1', 'Pokój 1', Markup('Ilość dorosłych: 2 Ilość dzieci: 2<br>Balkon: Tak Klimatyzacja: Nie<br>Minibar: Nie Łazienka: Tak<br>Czajnik: Tak Wi-fi: Tak<br>Telewizor: Tak')), ('2', 'Pokój 2', Markup('Ilość dorosłych: 2 Ilość dzieci: 0<br>Balkon: Tak Klimatyzacja: Nie<br>Minibar: Nie Łazienka: Tak<br>Czajnik: Tak Wi-fi: Tak<br>Telewizor: Tak'))]
        result = createRoomArray([(2, 2, 1, 0, 0, 1, 1, 1, 1), (2, 0, 1, 0, 0, 1, 1, 1, 1)])
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()