#Autor:Esra Güler
#Datum:28.05.25
#Inhalt: Datenbank von Lagerverwaltung (PyInstaller-kompatibel)

import os, sys, sqlite3

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def get_writable_path(filename):
    """ Get path to writable directory for database """
    if getattr(sys, 'frozen', False):
        # App ist als .app gepackt - verwende App Support Ordner
        app_support = os.path.expanduser("~/Library/Application Support/MediDepot")
        if not os.path.exists(app_support):
            os.makedirs(app_support)
        return os.path.join(app_support, filename)
    else:
        # Entwicklungsumgebung - verwende aktuellen Ordner
        return filename

# Datenbankpfad festlegen
db_path = get_writable_path("praxislager.db")

# Datenbank löschen falls vorhanden (für Neustart)
if os.path.exists(db_path):
    print("Alte Datenbank wird gelöscht...")
    os.remove(db_path)

print("Neue Datenbank wird erstellt...")
print(f"Datenbankpfad: {db_path}")

# Neue Datenbank erstellen
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Tabelle erstellen
sql = "CREATE TABLE artikel(" \
      "artikel_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
      "produktname TEXT, " \
      "aktuellerbestand INTEGER, " \
      "mindestbestand INTEGER, " \
      "einheit TEXT, " \
      "lagerort TEXT, " \
      "datum TEXT, " \
      "Kürzel TEXT)"
cursor.execute(sql)

print("Tabelle 'artikel' erstellt...")

# Liste mit Artikeln für die Praxis
artikel = [
    ('Latexhandschuhe', 60, 10, 'Packung', 'Labor', '28.05.2025', 'MS'),
    ('Mullbinde 6cm', 18, 8, 'Packung', 'Labor', '29.05.2025', 'AB'),
    ('Desinfektionsmittel', 25, 5, 'Liter', 'Lager A', '30.05.2025', 'TK'),
    ('Einmalspritzen 5ml', 120, 20, 'Packung', 'Labor', '31.05.2025', 'MS'),
    ('Gelbe Kanüle', 6, 5, 'Stück', 'Labor', '01.06.2025', 'EG'),
    ('Urbason 1000mg', 3, 2, 'Stück', 'Medikamentenschrank', '01.06.2025', 'EG'),
    ('Xyclocain Pump', 1, 1, 'Stück', 'Labor', '01.06.2025', 'EG'),
    ('Mullkompresse 10x10', 2, 3, 'Packung', 'Labor', '01.06.2025', 'EG'),
    ('Optiskin', 2, 1, 'Stück', 'Labor', '01.06.2025', 'EG'),
    ('Leukase Puder', 1, 1, 'Stück', 'Medikamentenschrank', '01.06.2025', 'EG'),
    ('Skalpell 15 REF', 3, 2, 'Stück', 'Labor', '01.06.2025', 'EG'),
    ('ES-Kompressen 5cmx5cm', 2, 3, 'Packung', 'Labor', '01.06.2025', 'EG'),
    ('ALK Lancet', 2, 2, 'Stück', 'Labor', '01.06.2025', 'EG'),
    ('DracoFixiermull', 1, 1, 'Stück', 'Labor', '01.06.2025', 'EG'),
    ('Fixomull 10cmx10cm', 8, 3, 'Stück', 'Labor', '01.06.2025', 'EG'),
    ('Fucidine Creme 100g', 8, 2, 'Stück', 'Medikamentenschrank', '01.06.2025', 'EG'),
    ('Fucicort Creme 60g', 11, 3, 'Stück', 'Medikamentenschrank', '01.06.2025', 'EG'),
    ('BetaGalen Creme 100g', 6, 2, 'Stück', 'Medikamentenschrank', '01.06.2025', 'EG'),
    ('Leukoplast Pflaster 8cmx5m', 4, 2, 'Stück', 'Labor', '01.06.2025', 'EG'),
    ('Leukoplast Pflaster 4cmx5m', 5, 2, 'Stück', 'Labor', '01.06.2025', 'EG'),
    ('Leukoplast Pflaster 6cmx5m', 3, 2, 'Stück', 'Labor', '01.06.2025', 'EG')
]

print("Artikel werden eingefügt...")

# Alle Artikel auf einmal einfügen
cursor.executemany("""
INSERT INTO artikel (produktname, aktuellerbestand, mindestbestand, einheit, lagerort, datum, Kürzel)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", artikel)

# Änderungen speichern
connection.commit()

# Kontrolle: Anzahl eingefügter Artikel anzeigen
cursor.execute("SELECT COUNT(*) FROM artikel")
anzahl = cursor.fetchone()[0]
print(f" {anzahl} Artikel erfolgreich eingefuegt!")

# Verbindung schließen
connection.close()

print(" Datenbank erfolgreich erstellt: praxislager.db")
print(" Jetzt kannst du dein Hauptprogramm starten!")

# Funktion zum Exportieren des Datenbankpfads (für andere Module)
def get_database_path():
    """Gibt den korrekten Datenbankpfad zurück - für Import in anderen Modulen"""
    return get_writable_path("praxislager.db")