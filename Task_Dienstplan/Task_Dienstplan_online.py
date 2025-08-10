import os
import csv
import pandas as pd
import random
import io
import sharepy

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

def Freitag_Abendessen(aktive_dienste, anwesende, zuordnung):
    # freitag Abendessen
    freitag_abendessen_done = []
    print("\nBitte geben Sie die Vornamen der Personen ein, die bereits Freitag Abendessen Dienst gemacht haben (durch Kommas getrennt):")
    input_names = input("Vornamen: ")
    input_names_list = [name.strip() for name in input_names.split(",") if name.strip()]
    for name in input_names_list:
        match = next((person for person in anwesende if person.get("Vorname", "").lower() == name.lower()), None)
        if match:
            freitag_abendessen_done.append(match)
            # Zähle "dienste" für die Person in data_list hoch
            add_service_count(data_list, match.get("Vorname", "").lower())


    for dienst in ["Freitag Abendessen"]:
        zuordnung[dienst] = freitag_abendessen_done
        if "Freitag Abendessen" in aktive_dienste:
            del aktive_dienste["Freitag Abendessen"]

def Wochenende(verfuegbar, zuordnung):

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

    pyjamaboys_dienst(dienste_WE, pyjamaboys)

    Freitag_Abendessen(dienste_WE, anwesende, zuordnung)

    # Dienste werden gleichmäßig und zufällig auf alle verfügbaren Personen verteilt,
    # ohne Begrenzung der maximalen Dienste pro Person.
    aktive_Dienste = {dienst: anzahl for dienst, anzahl in dienste_WE.items()}

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


    print("\nZufällige Dienst-Zuordnung fürs Wochenende:")
    for dienst, personen in zuordnung.items():
        print(f"{dienst}: ", end="")
        print(", ".join(f"{p.get('Vorname', '')} {p.get('Nachname', '')}" for p in personen))

def Sommerreise(verfuegbar, zuordnung):

    dienste_SE = {
    "Freitag Abendessen": 4,
    "Samstag Wecken": 1,
    "Samstag Frühstück": 4,
    "Samstag Mittagessen": 4,
    "Samstag Kaffee": 1,
    "Samstag Abendessen": 4,
    "Sonntag Wecken": 1,  # Annahme: 1 Person, ggf. anpassen
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
    "Sonntag Wecken (Pyjama-Boys)": 5,
    "Sonntag2 Frühstück": 4,
    }

    pyjamaboys_dienst(dienste_SE, pyjamaboys)

    Freitag_Abendessen(dienste_SE, anwesende, zuordnung)
    
    # Dienste werden gleichmäßig und zufällig auf alle verfügbaren Personen verteilt,
    # ohne Begrenzung der maximalen Dienste pro Person.
    aktive_Dienste = {dienst: anzahl for dienst, anzahl in dienste_SE.items()}

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

    print("\nZufällige Dienst-Zuordnung fürs Wochenende:")
    for dienst, personen in zuordnung.items():
        print(f"{dienst}: ", end="")
        print(", ".join(f"{p.get('Vorname', '')} {p.get('Nachname', '')}" for p in personen))

URL = 'https://taskev.sharepoint.com/'
FILE_URL = 'https://taskev.sharepoint.com/sites/main/Adresslisten/Forms/Task-Adressliste.xlsx'
SHAREPOINT_USER = 'jokacello@gmail.com'
SHAREPOINT_PASSWORD = 'ms5426_EIM8380!'

s = sharepy.connect(URL, username=SHAREPOINT_USER, password=SHAREPOINT_PASSWORD)
r = s.get(URL+FILE_URL)
f = io.BytesIO(r.content)
df = pd.read_csv(f)

# Einlesen der Adressliste
#base_path = os.path.dirname(os.path.abspath(__file__))
#os.chdir(base_path)
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


for data in data_list:
    print(data)

# Beispiel: Auswahl der anwesenden Personen (hier alle, die nicht "Befreit" sind)
print("\nWelche Personen sind nicht anwesend?")
input_not_present = input("Vornamen (durch Kommas getrennt): ")
not_present_list = [name.strip() for name in input_not_present.split(",") if name.strip()]
anwesende = [
    d for d in data_list
    if d.get("Befreit", "").strip().lower() != "ja"
    and (d.get("Vorname", "").strip() or d.get("Nachname", "").strip())
    and (d.get("Vorname", "").strip() not in not_present_list)
]
print("\nAnwesende Personen:")
print(anwesende)

# Kopie der anwesenden Personen, damit wir sie nicht mehrfach zuweisen
verfuegbar = anwesende.copy()

# Pyjama-Boys
pyjamaboys = [
    {"Vorname": "Christoph"},
    {"Vorname": "Georg"},
    {"Vorname": "Arndt"},
    {"Vorname": "Tobias"},
    {"Vorname": "Joseph"}
]

print("\nWochenende oder Sommerreise?")
input_choice = input("Bitte wählen Sie (W für Wochenende, S für Sommerreise): ").strip().upper()
if input_choice == "W":
    Wochenende(verfuegbar, zuordnung)
elif input_choice == "S":
    Sommerreise(verfuegbar, zuordnung)