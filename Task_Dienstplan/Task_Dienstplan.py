import os
import csv
import pandas as pd

base_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_path)
filename = "Task_Adressliste.csv"
fields = []
rows = []
data_list = []
columns_to_read = ['Vorname', 'Nachname', 'Befreit']

with open(filename, 'r', encoding='utf-8') as csvfile:
    #csvreader = pd.read_csv(csvfile, delimiter=';', usecols=['Vorname', 'Nachname', 'Befreit'])
    csvreader = csv.DictReader(csvfile, delimiter=';')

    for row in csvreader:
        filtered_row = {key: row[key] for key in columns_to_read if key in row}
        data_list.append(filtered_row)

for data in data_list:
    print(data)

print(data_list.get("Vorname"))

# anzahl Personen pro Dienst festgelegt

# Auswählen, ob wochenende oder Sommerreise
# Auswählen, wie viele Dienste (Checkbox?)
# Auswählen, welche personen anwesend sind
# Auswählen, welche Personen bereits Dienst abgeschlossen haben und berücksichtigung Pyjama boys (Anwesenheit spielt dort auch eine rolle)

# zufällige Zuordnung der Vornamen zu Diensten