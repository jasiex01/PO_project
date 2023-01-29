import sys
import unittest
sys.path.append('..')
from app import app, starsToNum
from flask import Markup

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    #test funkcjonalny
    def test_hotelsRate_get(self):
        result = self.client.get('/hotelsRate')
        self.assertEqual(result.status_code, 200)
        
    #test jednostkowy
    def test_hotelsRate_validateData(self):
        starsInText = ['jedna gwiazdka', 'dwie gwiazdki', 'trzy gwiazdki','cztery gwiazdki', 'piec gwiazdek']
        result = [starsToNum(star) for star in starsInText]
        
        self.assertEqual(result[0], 1)

if __name__ == '__main__':
    unittest.main()