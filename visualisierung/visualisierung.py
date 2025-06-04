# visualization.py
import os
import json
from tinydb import TinyDB, where
import plotly.graph_objects as go
import sys
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

# 8. Ein Plotly-Liniendiagramm erzeugen
fig = go.Figure(
    data=go.Scatter(
        x=list(range(len(drop_values))),
        y=drop_values,
        mode='lines+markers',
        marker=dict(size=5),
        hovertemplate="Index: %{x}<br>Wert: %{y}<extra></extra>"
    )
)
fig.update_layout(
    title="Drop Oscillation (Topic: iot1/teaching_factory/drop_oscillation)",
    xaxis_title="Index",
    yaxis_title="Wert",
    template="plotly_white",
    margin=dict(l=40, r=40, t=60, b=40)
)

# 9. Den Plotly-Chart als HTML-DIV exportieren (inkl. Plotly.js via CDN)
html_div = fig.to_html(include_plotlyjs='cdn', full_html=False)

# 10. Markdown-Datei-Pfad festlegen und Ordner anlegen
md_path = os.path.join('reports', 'drop_oscillation.md')
os.makedirs(os.path.dirname(md_path), exist_ok=True)

# 11. Markdown-Inhalt zusammenstellen
md_lines = [
    "# Drop Oscillation Plot\n\n",
    "_Topic: iot1/teaching_factory/drop_oscillation_\n\n",
    "<!-- Interaktives Plotly-Diagramm -->\n\n",
    html_div
]

# 12. In die Markdown-Datei schreiben
with open(md_path, 'w', encoding='utf-8') as f:
    f.writelines(md_lines)

print(f"Markdown mit Plotly-Chart wurde erstellt: {md_path}")

# 13. Datenbank schließen
db.close()
