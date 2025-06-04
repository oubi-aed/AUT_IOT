from tinydb import TinyDB, where

class Database:
    """
    Eine einfache TinyDB-Wrapper-Klasse zum Speichern von JSON-/Dict-Daten.
    """
    def __init__(self, db_path: str = 'db.json'):
        """
        Initialisiert die TinyDB-Datenbank.

        :param db_path: Pfad zur JSON-Datei, die als Datenbank dient.
        """
        self.db = TinyDB(db_path)

    def insert(self, data: dict) -> int:
        """
        Fügt einen neuen Datensatz in die Datenbank ein.

        :param data: Ein Dictionary, das in die Datenbank eingefügt werden soll.
        :return: Die ID des eingefügten Datensatzes.
        """
        return self.db.insert(data)

    def insert_multiple(self, data_list: list) -> list:
        """
        Fügt mehrere Datensätze gleichzeitig ein.

        :param data_list: Eine Liste von Dictionaries, die eingefügt werden sollen.
        :return: Eine Liste der IDs der eingefügten Datensätze.
        """
        return self.db.insert_multiple(data_list)

    def get_all(self) -> list:
        """
        Gibt alle Datensätze in der Datenbank zurück.

        :return: Liste aller Datensätze als Dictionaries.
        """
        return self.db.all()

    def search(self, field: str, value) -> list:
        """
        Sucht nach Datensätzen, bei denen field == value.

        :param field: Der Feldname, nach dem gesucht werden soll.
        :param value: Der Wert, nach dem das Feld durchsucht werden soll.
        :return: Liste der gefundenen Datensätze.
        """
        return self.db.search(where(field) == value)

    def update(self, field: str, value, key: str, new_value) -> int:
        """
        Aktualisiert Datensätze, bei denen field == value: Setzt key auf new_value.

        :param field: Feldname für die Suche.
        :param value: Suchwert.
        :param key: Der Feldname, der aktualisiert werden soll.
        :param new_value: Neuer Wert für das Feld.
        :return: Anzahl der aktualisierten Datensätze.
        """
        return self.db.update({key: new_value}, where(field) == value)

    def remove(self, field: str, value) -> int:
        """
        Entfernt Datensätze, bei denen field == value.

        :param field: Feldname für die Suche.
        :param value: Suchwert.
        :return: Anzahl der entfernten Datensätze.
        """
        return self.db.remove(where(field) == value)

    def close(self):
        """
        Schließt die Datenbank.
        """
        self.db.close()

if __name__ == "__main__":
    # Beispielverwendung der Database-Klasse
    db = Database('db.json')
    
    # Einfügen eines Datensatzes
    data_id = db.insert({'name': 'Alice', 'age': 30})
    print(f'Datensatz eingefügt mit ID: {data_id}')
    db.insert({'name': 'Alice', 'age': 30})
    
    # Einfügen mehrerer Datensätze
    ids = db.insert_multiple([{'name': 'Bob', 'age': 25}, {'name': 'Charlie', 'age': 35}])
    print(f'Mehrere Datensätze eingefügt mit IDs: {ids}')
    
    # Alle Datensätze abrufen
    all_data = db.get_all()
    print('Alle Datensätze:', all_data)
    
    # Suchen nach einem Datensatz
    search_result = db.search('name', 'Alice')
    print('Suchergebnis:', search_result)
    
    # Aktualisieren eines Datensatzes
    updated_count = db.update('name', 'Alice', 'age', 31)
    print(f'Anzahl aktualisierter Datensätze: {updated_count}')
    
    # Entfernen eines Datensatzes
    removed_count = db.remove('name', 'Bob')
    print(f'Anzahl entfernter Datensätze: {removed_count}')
    
    # Schließen der Datenbank
    db.close()
