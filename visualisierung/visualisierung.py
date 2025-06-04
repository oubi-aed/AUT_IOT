# visualization.py

import os
import json
import urllib.parse
import matplotlib.pyplot as plt
import sys

# Damit wir die Database-Klasse finden (eine Ebene höher, in database/database.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.database import Database

# 1. Datenbank öffnen (Pfad ggf. anpassen)
db = Database(db_path='db.json')

# 2. Nach Einträgen mit dem gesuchten Topic suchen
#    Hier: "iot1/teaching_factory/drop_oscillation"
records = db.get_by_topic('iot1/teaching_factory/drop_oscillation')

# 3. Falls kein Eintrag gefunden wurde, abbrechen
if not records:
    print("Kein Eintrag mit Topic 'iot1/teaching_factory/drop_oscillation' gefunden.")
    db.close()
    exit(1)

# 4. Den ersten passenden Datensatz nehmen
entry = records[0]

# 5. Payload-String parsen (ist JSON im String-Format)
payload_dict = json.loads(entry['payload'])

# 6. "drop_oscillation" als Liste von Strings auslesen
drop_str_list = payload_dict.get('drop_oscillation', [])

# 7. Strings in Floats umwandeln
drop_values = [float(x) for x in drop_str_list]

# 8. Mit Matplotlib einen PNG-Plot erstellen
png_dir = os.path.join('reports', 'plots')
os.makedirs(png_dir, exist_ok=True)
png_path = os.path.join(png_dir, 'drop_oscillation.png')

plt.figure(figsize=(6, 4))
plt.plot(range(len(drop_values)), drop_values, marker='o', linestyle='-', color='green')
plt.title("Drop Oscillation")
plt.xlabel("Index")
plt.ylabel("Wert")
plt.grid(True)
plt.tight_layout()
plt.savefig(png_path, format='png')
plt.close()
print(f"PNG-Datei gespeichert: {png_path}")

# 9. QuickChart-URL zusammenbauen (sampling, um URL-Länge zu begrenzen)
sample_step = 5
qc_labels = list(range(0, len(drop_values), sample_step))
qc_data = drop_values[::sample_step]

qc_config = {
    "type": "line",
    "data": {
        "labels": qc_labels,
        "datasets": [{
            "label": "Drop Oscillation (Sampled every 10th)",
            "data": qc_data,
            "borderColor": "green",
            "fill": False
        }]
    },
    "options": {
        "title": {
            "display": True,
            "text": "Drop Oscillation (QuickChart, gesampelt)"
        },
        "scales": {
            "xAxes": [{
                "scaleLabel": {
                    "display": True,
                    "labelString": "Index"
                }
            }],
            "yAxes": [{
                "scaleLabel": {
                    "display": True,
                    "labelString": "Wert"
                }
            }]
        }
    }
}

qc_json = json.dumps(qc_config, separators=(',', ':'))
qc_param = urllib.parse.quote(qc_json, safe='')
quickchart_url = f"https://quickchart.io/chart?c={qc_param}"

# 10. Markdown-Inhalt zusammenstellen (README.md im Projekt-Root)
md_path = 'README.md'
md_lines = [
    "# Drop Oscillation Plot\n\n",
    "_Topic: iot1/teaching_factory/drop_oscillation_\n\n",
    "## Lokale PNG-Datei\n\n",
    f"![Drop Oscillation PNG](https://github.com/oubi-aed/AUT_IOT/blob/main/reports/plots/drop_oscillation.png)\n\n",
    "## QuickChart-Embed (statische Grafik von quickchart.io mit Sample Step = 5)\n\n",
    f"![Drop Oscillation QuickChart]({quickchart_url})\n"
]

# 11. In die README.md schreiben (überschreibt vorhandene README.md!)
with open(md_path, 'w', encoding='utf-8') as f:
    f.writelines(md_lines)

print(f"README.md wurde erstellt/aktualisiert: {md_path}")

# 12. Datenbank schließen
db.close()
