import os
import csv
import random
from flask import Flask, render_template, request, session
import webbrowser
import threading

## Prozeduren ##

# Prozedur dienste +1
def add_service_count(anwesende, name):
    for row in anwesende:
        if row.get("Vorname", "").lower() == name.lower():
            row["Dienste"] += 1

def get_min_Dienste(verfuegbar):
    if not verfuegbar:
        return 0
    return min([person["Dienste"] for person in verfuegbar])

def pyjamaboys_dienst_WE(aktive_dienste, pyjamaboys, anwesende):
    # Dienstzuweisung für Pyjama-Boys und Freitag Abendessen
    for dienst in ["Sonntag Wecken(Pyjama-Boys)"]:
        zuordnung[dienst] = pyjamaboys
        # Count dienste +1 for each pyjama boy in data_list
        for boy in pyjamaboys:
            add_service_count(anwesende, boy.get("Vorname", "").lower())
        if "Sonntag Wecken(Pyjama-Boys)" in aktive_dienste:
            del aktive_dienste["Sonntag Wecken(Pyjama-Boys)"]

def pyjamaboys_dienst_SE(aktive_dienste, pyjamaboys, anwesende):
    # Dienstzuweisung für Pyjama-Boys und Freitag Abendessen
    for dienst in ["Sonntag2 Wecken(Pyjama-Boys)"]:
        zuordnung[dienst] = pyjamaboys
        # Count dienste +1 for each pyjama boy in data_list
        for boy in pyjamaboys:
            add_service_count(anwesende, boy.get("Vorname", "").lower())
        if "Sonntag2 Wecken(Pyjama-Boys)" in aktive_dienste:
            del aktive_dienste["Sonntag2 Wecken(Pyjama-Boys)"]

def freitag_abenddienst(dienste_updated, anwesende, zuordnung, freitag_abenddienst_list):
    freitag_abendessen_done = []

    for name in freitag_abenddienst_list:
        match = next((person for person in anwesende if person.get("Vorname", "").lower() == name.lower()), None)
        if match:
            freitag_abendessen_done.append(match)
            # Zähle "dienste" für die Person in data_list hoch
            add_service_count(anwesende, match.get("Vorname", "").lower())


    for dienst in ["Freitag Abendessen"]:
        zuordnung[dienst] = freitag_abendessen_done
        if "Freitag Abendessen" in dienste_updated:
            del dienste_updated["Freitag Abendessen"]

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
    {"Vorname": "Christoph", "Nachname": "Hartmann", "Dienste": 0},
    {"Vorname": "Georg", "Nachname": "Paul", "Dienste": 0},
    {"Vorname": "Arndt", "Nachname": "Begrich", "Dienste": 0},
    {"Vorname": "Tobias", "Nachname": "Gebauer", "Dienste": 0},
    {"Vorname": "Joseph", "Nachname": "Sonntag", "Dienste": 0}
]

dienste_WE = {
    "Freitag Abendessen": 4,
    "Samstag Wecken": 1,
    "Samstag Frühstück": 4,
    "Samstag Mittagessen": 4,
    "Samstag Kaffee": 1,
    "Samstag Abendessen": 4,
    "Sonntag Wecken(Pyjama-Boys)": 5,
    "Sonntag Frühstück": 4,
    "Sonntag Mittagessen": 4
}

dienste_SE = {
    "Freitag Abendessen": 4,
    "Samstag Wecken": 1,
    "Samstag Frühstück": 4,
    "Samstag Mittagessen": 4,
    "Samstag Kaffee": 1,
    "Samstag Abendessen": 4,
    "Sonntag Wecken": 1,
    "Sonntag Frühstück": 4,
    "Sonntag Mittagessen": 4,
    "Montag Wecken": 1,
    "Montag Frühstück": 4,
    "Montag Mittagessen": 4,
    "Montag Kaffee": 1,
    "Montag Abendessen": 4,
    "Dienstag Wecken": 1,
    "Dienstag Frühstück": 4,
    "Dienstag Mittagessen": 4,
    "Dienstag Kaffee": 1,
    "Dienstag Abendessen": 4,
    "Mittwoch Wecken": 1,
    "Mittwoch Frühstück": 4,
    "Mittwoch Mittagessen": 4,
    "Mittwoch Kaffee": 1,
    "Mittwoch Abendessen": 4,
    "Donnerstag Wecken": 1,
    "Donnerstag Frühstück": 4,
    "Donnerstag Mittagessen": 4,
    "Donnerstag Kaffee": 1,
    "Donnerstag Abendessen": 4,
    "Freitag2 Wecken": 1,
    "Freitag2 Frühstück": 4,
    "Freitag2 Mittagessen": 4,
    "Freitag2 Kaffee": 1,
    "Freitag2 Abendessen": 4,
    "Samstag2 Wecken": 1,
    "Samstag2 Frühstück": 4,
    "Samstag2 Mittagessen": 4,
    "Samstag2 Kaffee": 1,
    "Samstag2 Abendessen": 4,
    "Sonntag2 Wecken(Pyjama-Boys)": 5,
    "Sonntag2 Frühstück": 4,
    }

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
    not_present_list = request.form.getlist('person_vornamen')

    # anwesende = alle, deren Index nicht missing_ids ist
    anwesende = [
        d for d in data_list
        if (d.get("Befreit", "").strip().lower() != "ja")
        and (d.get("Vorname", "").strip() or d.get("Nachname", "").strip())
        and (d.get("Vorname", "").strip() not in not_present_list)
    ]
    session['anwesende'] = anwesende  # Store in session for later use

    return render_template("freitagdienst.html", anwesende=anwesende)

@app.route('/submitabenddienst', methods=['POST'])
def submitabenddienst():
    anwesende = session.get('anwesende', [])

    # IDs der fehlenden Personen (Checkboxen)
    abenddienst_ids = request.form.getlist('person_ids_2')
    abenddienst_ids = list(map(int, abenddienst_ids))  # to int

    # anwesende = alle, deren Index nicht abenddienst_ids ist
    freitag_abenddienst_list = [person for idx, person in enumerate(anwesende) if idx in abenddienst_ids]
    session['freitag_abenddienst_list'] = freitag_abenddienst_list  # Store in session for later use

    # Return JSON for AJAX to trigger popup, but don't redirect
    return render_template("sommerwoche.html")

@app.route('/submitwochensommer', methods=['POST'])
def submitwochensommer():
    wochensommer_choice = request.form['wochensommer_choice']

    if wochensommer_choice == "Wochenende":
        return render_template("wochenende.html", dienste_WE=dienste_WE)
    elif wochensommer_choice == "Sommerreise": 
        return render_template("sommerreise.html", dienste_SE=dienste_SE)

@app.route('/submitdienste_WE', methods=['POST'])
def submitdienste_WE():
    anwesende = session.get('anwesende', [])
    freitag_abenddienst_list = [
        person.get("Vorname", "")
        for person in session.get('freitag_abenddienst_list', [])
        if isinstance(person, dict)
    ]

    # Get unchecked dienst names (those that are unchecked)
    checked_dienste = request.form.getlist('dienst_WE_names')
    dienste_updated = {dienst: anzahl for dienst, anzahl in dienste_WE.items() if dienst not in checked_dienste}


    pyjamaboys_dienst_WE(dienste_updated, pyjamaboys, anwesende)
    
    freitag_abenddienst(dienste_updated, anwesende, zuordnung, freitag_abenddienst_list)

    for dienst, anzahl in dienste_updated.items():
        ausgewaehlt = []
        for _ in range(anzahl):
            # Finde Personen mit minimaler Dienstanzahl
            min_Dienste = get_min_Dienste(anwesende)
            kandidaten = [p for p in anwesende if p["Dienste"] == min_Dienste]
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

    # Redirect or render next step
    return render_template("final_dienste.html", dienste_updated=session.get('dienste_updated', {}), zuordnung=zuordnung, data_list=data_list, anwesende=session.get('anwesende', []))



@app.route('/submitdienste_SE', methods=['POST'])
def submitdienste_SE():
    anwesende = session.get('anwesende', [])
    freitag_abenddienst_list = [
        person.get("Vorname", "")
        for person in session.get('freitag_abenddienst_list', [])
        if isinstance(person, dict)
    ]

    # Get unchecked dienst names (those that are unchecked)
    checked_dienste = request.form.getlist('dienst_SE_names')
    dienste_updated = {dienst: anzahl for dienst, anzahl in dienste_SE.items() if dienst not in checked_dienste}


    pyjamaboys_dienst_SE(dienste_updated, pyjamaboys, anwesende)
    
    freitag_abenddienst(dienste_updated, anwesende, zuordnung, freitag_abenddienst_list)

    for dienst, anzahl in dienste_updated.items():
        ausgewaehlt = []
        for _ in range(anzahl):
            # Finde Personen mit minimaler Dienstanzahl
            min_Dienste = get_min_Dienste(anwesende)
            kandidaten = [p for p in anwesende if p["Dienste"] == min_Dienste]
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

    # Redirect or render next step
    return render_template("final_dienste.html", dienste_updated=session.get('dienste_updated', {}), zuordnung=zuordnung, data_list=data_list, anwesende=session.get('anwesende', []))




@app.route('/final_dienste', methods=['POST'])
def final_dienste():
    zuordnung = session.get('zuordnung', {})

    # Prepare data for rendering in final_dienste.html
    dienst_zuordnung_list = []
    for dienst, personen in zuordnung.items():
        personen_namen = ", ".join(f"{p.get('Vorname', '')} {p.get('Nachname', '')}" for p in personen)
        dienst_zuordnung_list.append({"dienst": dienst, "personen": personen_namen})
    
    return render_template("final_dienste.html", zuordnung=zuordnung, data_list=data_list, dienst_zuordnung_list=dienst_zuordnung_list)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")  # or your host/port if different

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.0, open_browser).start()
    app.run(debug=True)