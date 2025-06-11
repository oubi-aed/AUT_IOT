#%%
# 
# import json
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.database import Database 

db = Database('db.json') 
#db = Database('../db.json') 
# Hole alle Daten
raw_dict = db.get_all()
#print(raw_dict)
#%%
import json
# Erstelle leere Listen für jede Spalte
bottles_data = {
    'bottle': [],
    'vibration_index_red': [],
    'fill_level_grams_red': [],
    'vibration_index_blue': [],
    'fill_level_grams_blue': [],
    'vibration_index_green': [],
    'fill_level_grams_green': [],
    'temperature_green': [],
    'temperature_red': [],
    'temperature_blue': [],
    'final_weight': []  # Nur final_weight, kein weight
}

# Temporäre Dictionaries für Temperaturen und andere Werte
temp_data = {}
bottle_data = {}
final_weights = {}  # Dictionary für finale Gewichte

for record in raw_dict:
    try:
        topic = record['topic']
        payload = json.loads(record['payload'])
        
        if 'temperature' in topic:
            dispenser = payload['dispenser']
            temp_data[f"temperature_{dispenser}"] = payload['temperature_C']
        
        elif 'dispenser' in topic:
            dispenser = payload['dispenser']
            bottle = payload['bottle']
            
            if bottle not in bottle_data:
                bottle_data[bottle] = {}
            
            bottle_data[bottle].update({
                f'vibration_index_{dispenser}': payload['vibration-index'],
                f'fill_level_grams_{dispenser}': payload['fill_level_grams']
            })
        
        elif 'scale/final_weight' in topic:
            bottle = payload['bottle']
            final_weights[bottle] = payload['final_weight']
            
    except json.JSONDecodeError as e:
        print(f"JSON Parse error in record: {record}")
        continue

# Erstelle DataFrame-Einträge
for bottle in bottle_data:
    bottles_data['bottle'].append(bottle)
    bottles_data['vibration_index_red'].append(bottle_data[bottle].get('vibration_index_red', None))
    bottles_data['fill_level_grams_red'].append(bottle_data[bottle].get('fill_level_grams_red', None))
    bottles_data['vibration_index_blue'].append(bottle_data[bottle].get('vibration_index_blue', None))
    bottles_data['fill_level_grams_blue'].append(bottle_data[bottle].get('fill_level_grams_blue', None))
    bottles_data['vibration_index_green'].append(bottle_data[bottle].get('vibration_index_green', None))
    bottles_data['fill_level_grams_green'].append(bottle_data[bottle].get('fill_level_grams_green', None))
    bottles_data['temperature_green'].append(temp_data.get('temperature_green', None))
    bottles_data['temperature_red'].append(temp_data.get('temperature_red', None))
    bottles_data['temperature_blue'].append(temp_data.get('temperature_blue', None))
    bottles_data['final_weight'].append(final_weights.get(bottle, None))

# Erstelle DataFrame
df = pd.DataFrame(bottles_data)
df = df.sort_values('bottle')  # Sortiere nach Flaschen-ID
df = df.dropna()
print("\nErste 5 Zeilen des DataFrames:")
print(df.head())

# Speichere DataFrame als CSV
df.to_csv('bottle_data.csv', index=False)
print("\nDatei 'bottle_data.csv' wurde erstellt!")