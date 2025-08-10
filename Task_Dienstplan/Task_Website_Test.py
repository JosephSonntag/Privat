import os
import csv
import pandas as pd
import random
from flask import Flask, render_template, request, session

## Prozeduren ##

# Prozedur dienste +1
def add_service_count(data_list, name):
    for row in data_list:
        if row.get("Vorname", "").lower() == name.lower():
            row["Dienste"] += 1

def get_min_Dienste(verfuegbar):
    if not verfuegbar:
        return 0
    return min([person["Dienste"] for person in verfuegbar])

def pyjamaboys_dienst(aktive_dienste, pyjamaboys):
    # Dienstzuweisung für Pyjama-Boys und Freitag Abendessen
    for dienst in ["Sonntag Wecken (Pyjama-Boys)"]:
        zuordnung[dienst] = pyjamaboys
        # Count dienste +1 for each pyjama boy in data_list
        for boy in pyjamaboys:
            add_service_count(data_list, boy.get("Vorname", "").lower())
        if "Sonntag Wecken (Pyjama-Boys)" in aktive_dienste:
            del aktive_dienste["Sonntag Wecken (Pyjama-Boys)"]

def freitag_abenddienst(aktive_dienste, anwesende, zuordnung):
    freitag_abendessen_list = session.get('freitag_abendessen_list', [])
    freitag_abendessen_done = []

    for name in freitag_abendessen_list:
        match = next((person for person in anwesende if person.get("Vorname", "").lower() == name.lower()), None)
        if match:
            freitag_abendessen_done.append(match)
            # Zähle "dienste" für die Person in data_list hoch
            add_service_count(data_list, match.get("Vorname", "").lower())


    for dienst in ["Freitag Abendessen"]:
        zuordnung[dienst] = freitag_abendessen_done
        if "Freitag Abendessen" in aktive_dienste:
            del aktive_dienste["Freitag Abendessen"]

# Prozedur Wochenende
def Wochenende(verfuegbar, zuordnung):

    anwesende = session.get('anwesende', [])
    dienste_WE = {
    "Freitag Abendessen": 4,
    "Samstag Wecken": 1,
    "Samstag Frühstück": 4,
    "Samstag Mittagessen": 4,
    "Samstag Kaffee": 1,
    "Samstag Abendessen": 4,
    "Sonntag Wecken (Pyjama-Boys)": 5,  # Annahme: 1 Person, ggf. anpassen
    "Sonntag Frühstück": 4,
    "Sonntag Mittagessen": 4
    }

    aktive_Dienste = {dienst: anzahl for dienst, anzahl in dienste_WE.items()}

    freitag_abenddienst(aktive_Dienste, verfuegbar, zuordnung)

    pyjamaboys_dienst(dienste_WE, pyjamaboys)

    for dienst, anzahl in aktive_Dienste.items():
        ausgewaehlt = []
        for _ in range(anzahl):
            # Finde Personen mit minimaler Dienstanzahl
            min_Dienste = get_min_Dienste(verfuegbar)
            kandidaten = [p for p in verfuegbar if p["Dienste"] == min_Dienste]
            if kandidaten:
                person = random.choice(kandidaten)
                ausgewaehlt.append(person)
                person["Dienste"] += 1
            else:
                # Falls keine Kandidaten mehr verfügbar sind, wähle zufällig aus allen anwesenden
                person = random.choice(anwesende)
                ausgewaehlt.append(person)
                person["Dienste"] += 1
        zuordnung[dienst] = ausgewaehlt

# Einlesen der Adressliste
base_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_path)
filename = "Task_Adressliste.csv"
fields = []
rows = []
data_list = []
columns_to_read = ['Vorname', 'Nachname', 'Befreit']
# Hier könnte die zufällige Zuteilung der dienste erfolgen
zuordnung = {}

with open(filename, 'r', encoding='utf-8') as csvfile:
    #csvreader = pd.read_csv(csvfile, delimiter=';', usecols=['Vorname', 'Nachname', 'Befreit'])
    csvreader = csv.DictReader(csvfile, delimiter=';')

    for row in csvreader:
        filtered_row = {key: row[key] for key in columns_to_read if key in row}
        data_list.append(filtered_row)

    # delete rows with empty Vorname
    data_list = [row for row in data_list if row.get("Vorname", "").strip()]

for row in data_list:
    row['Dienste'] = 0

# Pyjama-Boys
pyjamaboys = [
    {"Vorname": "Christoph"},
    {"Vorname": "Georg"},
    {"Vorname": "Arndt"},
    {"Vorname": "Tobias"},
    {"Vorname": "Joseph"}
]

## Flask App Setup ##
app = Flask(__name__, template_folder='website')
app.secret_key = "dein-geheimes-schluessel"  # notwendig für Sessions


## Flask Server ##
@app.route('/')

def index():
    return render_template("index.html", data_list=data_list)

@app.route('/submitfehlend', methods=['POST'])
def submitfehlend():
    # IDs der fehlenden Peronen (Checkboxen)
    missing_ids = request.form.getlist('person_ids')
    missing_ids = list(map(int, missing_ids))       # to int

    # anwesende = alle, deren Index nicht missing_ids ist
    anwesende = [person for idx, person in enumerate(data_list) if idx not in missing_ids]

    session['anwesende'] = anwesende  # Store in session for later use

    print("Anwesende Personen:", anwesende)

    return render_template("freitagdienst.html", anwesende=anwesende)

@app.route('/submitabenddienst', methods=['POST'])
def submitabenddienst():

    anwesende = session.get('anwesende', [])

    # IDs der fehlenden Peronen (Checkboxen)
    abenddienst_ids = request.form.getlist('person_ids')
    abenddienst_ids = list(map(int, abenddienst_ids))       # to int

    # anwesende = alle, deren Index nicht missing_ids ist
    freitag_abenddienst_list = [person for idx, person in enumerate(data_list) if idx not in abenddienst_ids]

    session['freitag_abenddienst_list'] = freitag_abenddienst_list  # Store in session for later use

    return render_template("result.html", anwesende=anwesende)

if __name__ == "__main__":
    app.run(debug=True)