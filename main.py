from flask import Flask, render_template, request
import requests
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('db.json')
User = Query()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        ime = request.form['ime']
        drzava = request.form['drzava']
        geslo = request.form['geslo']

        response = requests.get(f'https://api.nationalize.io/?name={ime}')
        data = response.json()

        drzava_match = any(country['country_id'] == drzava for country in data['country'])

        if drzava_match:
            db.insert({'email': email, 'ime': ime, 'drzava': drzava, 'geslo': geslo})
            message = "Uspešno ste se vpisali!"
        else:
            message = "Ime in država se ne ujemata."

        return render_template('index.html', message=message)

    return render_template('index.html', message='')

if __name__ == '__main__':
    app.run(debug=True)