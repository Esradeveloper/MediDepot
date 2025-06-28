#Autor: Esra Güler
#Datum: 28.05.25
#Inhalt: Lagerverwaltung MediDEPOT
#Beschreibung: Programm zur Verwaltung von Medizin-Artikeln mit Datenbank


# Alle benötigten Module importieren
import tkinter                    # Für das Fenster und Buttons
from tkinter import ttk, messagebox  # Für Tabelle und Popup-Fenster
from datetime import datetime     # Für das aktuelle Datum
import sqlite3                   # Für die Datenbank
import os, sys                   # Für Dateipfade

print("Hauptprogramm startet...")

# Variable um zu merken ob es der erste Start ist
erster_start = False

# WICHTIGE FUNKTION: Findet den richtigen Ort für die Datenbank
def get_writable_path(filename):
    """
    Diese Funktion sorgt dafür, dass die Datenbank immer am richtigen Ort gespeichert wird.
    - Beim Programmieren: im aktuellen Ordner
    - Als App: im Application Support Ordner (wo Apps ihre Daten speichern dürfen)
    """
    if getattr(sys, 'frozen', False):  # Prüft ob es eine gepackte App ist
        # App-Version: Spezialordner für App-Daten verwenden
        app_support = os.path.expanduser("~/Library/Application Support/MediDepot")
        if not os.path.exists(app_support):  # Ordner erstellen falls er nicht existiert
            os.makedirs(app_support)
        return os.path.join(app_support, filename)
    else:
        # Entwicklungsversion: aktueller Ordner
        return filename

def erstelle_datenbank_falls_nicht_vorhanden():
    """
    Erstellt automatisch eine neue Datenbank mit Beispieldaten,
    falls noch keine existiert. Wird beim Programmstart aufgerufen.
    WICHTIG: Diese Funktion sorgt dafür, dass die App auf jedem Computer funktioniert!
    """
    global erster_start
    db_path = get_writable_path("praxislager.db")
    
    try:
        # Verbindung zur Datenbank (wird erstellt falls nicht vorhanden)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Prüfen ob Tabelle "artikel" existiert
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='artikel'")
        tabelle_existiert = cursor.fetchone() is not None
        
        if tabelle_existiert:
            print("Datenbank und Tabelle gefunden - verwende existierende Datenbank")
            connection.close()
            return
        
        # Merken dass es der erste Start ist
        erster_start = True
        print("Keine Artikel-Tabelle gefunden - erstelle neue Datenbank...")
        
        # Tabelle erstellen (gleiche Struktur wie im Original)
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
        
        # Beispiel-Artikel einfügen (damit die App nicht leer ist)
        artikel = [
            ('Latexhandschuhe', 60, 10, 'Packung', 'Labor', '17.06.2025', 'MS'),
            ('Mullbinde 6cm', 18, 8, 'Packung', 'Labor', '17.06.2025', 'AB'),
            ('Desinfektionsmittel', 25, 5, 'Liter', 'Lager A', '17.06.2025', 'TK'),
            ('Einmalspritzen 5ml', 120, 20, 'Packung', 'Labor', '17.06.2025', 'MS'),
            ('Gelbe Kanüle', 6, 5, 'Stück', 'Labor', '17.06.2025', 'EG'),
            ('Urbason 1000mg', 3, 2, 'Stück', 'Medikamentenschrank', '17.06.2025', 'EG'),
            ('Mullkompresse 10x10', 2, 3, 'Packung', 'Labor', '17.06.2025', 'EG'),
            ('Optiskin', 2, 1, 'Stück', 'Labor', '17.06.2025', 'EG'),
            ('Leukase Puder', 1, 1, 'Stück', 'Medikamentenschrank', '17.06.2025', 'EG'),
            ('Skalpell 15 REF', 3, 2, 'Stück', 'Labor', '17.06.2025', 'EG')
        ]
        
        # Alle Artikel in die Datenbank einfügen
        cursor.executemany("""
        INSERT INTO artikel (produktname, aktuellerbestand, mindestbestand, einheit, lagerort, datum, Kürzel)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, artikel)
        
        connection.commit()  # Änderungen speichern
        connection.close()   # Datenbank schließen
        
        print("Neue Datenbank mit Beispieldaten erstellt!")
        
    except Exception as e:
        print(f"Fehler beim Erstellen der Datenbank: {e}")
        messagebox.showerror("Datenbank-Fehler", 
                           f"Konnte keine Datenbank erstellen:\n{e}\n\nBitte Administrator kontaktieren.")

# DATENBANK-FUNKTIONEN (Hier wird mit der Datenbank gearbeitet)


def daten_aus_db_laden():
    """
    Lädt alle Artikel aus der Datenbank und gibt sie zurück.
    Wird verwendet um die Tabelle zu füllen.
    """
    try:
        # Datenbank öffnen
        db_path = get_writable_path("praxislager.db")  # Richtigen Pfad holen
        conn = sqlite3.connect(db_path)               # Verbindung zur Datenbank
        cursor = conn.cursor()                        # Cursor zum Ausführen von Befehlen
        
        # SQL-Befehl: Alle Artikel aus der Tabelle holen
        cursor.execute("SELECT artikel_id, produktname, aktuellerbestand, mindestbestand, einheit, lagerort, Kürzel, datum FROM artikel")
        daten = cursor.fetchall()                     # Alle Ergebnisse holen
        conn.close()                                  # Datenbank schließen
        
        print(f"{len(daten)} Artikel aus Datenbank geladen")
        return daten                                  # Daten zurückgeben
        
    except Exception as e:
        # Falls ein Fehler auftritt (z.B. Datenbank nicht gefunden)
        print(f"Datenbank-Fehler: {e}")
        messagebox.showerror("Datenbank-Fehler", "Kann nicht aus Datenbank laden!")
        return []                                     # Leere Liste zurückgeben

def tabelle_neu_laden():
    """
    Löscht alle Einträge aus der Tabelle und lädt sie neu aus der Datenbank.
    Wird nach jedem Hinzufügen/Löschen/Ändern aufgerufen.
    NEUE FUNKTION: Prüft auch ob Bestände zu niedrig sind.
    """
    # Schritt 1: Alte Einträge aus der Tabelle löschen
    for item in treeview.get_children():
        treeview.delete(item)
    
    # Schritt 2: Neue Daten aus Datenbank holen und in Tabelle einfügen
    daten = daten_aus_db_laden()
    niedrige_bestaende = []  # Liste für Artikel mit niedrigem Bestand
    
    for eintrag in daten:
        # Eintrag in Tabelle einfügen
        item = treeview.insert('', 'end', values=eintrag)
        
        # Bestand prüfen: Position 2 = aktueller Bestand, Position 3 = Mindestbestand
        aktueller_bestand = int(eintrag[2])
        mindest_bestand = int(eintrag[3])
        artikel_name = eintrag[1]
        
        # Wenn aktueller Bestand <= Mindestbestand, dann Warnung
        if aktueller_bestand <= mindest_bestand:
            # Zeile mit Warnsymbol markieren
            treeview.set(item, 'Aktueller Bestand', f"{aktueller_bestand} ⚠️")
            niedrige_bestaende.append(f"• {artikel_name}: {aktueller_bestand} (Minimum: {mindest_bestand})")
    
    # Warnung anzeigen wenn Bestände niedrig sind (aber nicht beim ersten Start)
    if niedrige_bestaende and not erster_start:
        warnung_text = "WARNUNG: Folgende Artikel haben niedrige Bestände:\n\n" + "\n".join(niedrige_bestaende)
        warnung_text += "\n\nBitte Nachbestellung prüfen!"
        messagebox.showwarning("Niedrige Bestände!", warnung_text)

def hinzufugen():
    """
    Fügt einen neuen Artikel zur Datenbank hinzu.
    Wird aufgerufen wenn der grüne "Zugang hinzufügen" Button geklickt wird.
    """
    # Schritt 1: Werte aus den Eingabefeldern holen
    artikel_name = artikel_feld.get()    # Text aus dem Artikelname-Feld
    anzahl_name = anzahl_feld.get()      # Text aus dem Anzahl-Feld  
    einheit_name = einheit_feld.get()    # Text aus dem Einheit-Feld
    ort_name = ort_feld.get()            # Text aus dem Ort-Feld
    kuerzel_name = kuerzel_feld.get()    # Text aus dem Kürzel-Feld
    datum_name = datum_feld.get()        # Text aus dem Datum-Feld
    
    # Schritt 2: Prüfen ob alle Felder ausgefüllt sind
    if not all([artikel_name, anzahl_name, einheit_name, ort_name, kuerzel_name, datum_name]):
        messagebox.showwarning("Warnung", "Bitte füllen Sie alle Felder aus!")
        return  # Funktion beenden wenn Felder leer sind
    
    # Schritt 3: Neuen Artikel in die Datenbank speichern
    try:
        # Datenbank öffnen
        db_path = get_writable_path("praxislager.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # SQL-Befehl: Neuen Artikel einfügen (mindestbestand = 5 als Standard)
        cursor.execute("""
            INSERT INTO artikel (produktname, aktuellerbestand, mindestbestand, einheit, lagerort, Kürzel, datum)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (artikel_name, anzahl_name, 5, einheit_name, ort_name, kuerzel_name, datum_name))
        
        conn.commit()  # Änderungen speichern
        conn.close()   # Datenbank schließen
        
        # Schritt 4: Eingabefelder leeren für nächste Eingabe
        artikel_feld.delete(0, tkinter.END)
        anzahl_feld.delete(0, tkinter.END)
        einheit_feld.delete(0, tkinter.END)
        ort_feld.delete(0, tkinter.END)
        kuerzel_feld.delete(0, tkinter.END)
        datum_feld.delete(0, tkinter.END)
        datum_feld.insert(0, datetime.now().strftime("%d.%m.%Y"))  # Heutiges Datum einfügen
        
        # Schritt 5: Tabelle neu laden und Erfolg anzeigen
        tabelle_neu_laden()
        messagebox.showinfo("Erfolg", "Zugang wurde erfolgreich hinzugefuegt!")
        
    except Exception as e:
        # Falls beim Speichern ein Fehler auftritt
        messagebox.showerror("Datenbank-Fehler", f"Konnte nicht speichern: {e}")

def abgang_hinzufugen():
    """
    Registriert einen Abgang (Verbrauch) von Artikeln.
    Wird aufgerufen wenn der rote "Abgang registrieren" Button geklickt wird.
    """
    # Schritt 1: Werte aus den Abgang-Eingabefeldern holen
    artikel_name = abgang_artikel_feld.get()
    anzahl_str = abgang_anzahl_feld.get()
    einheit_name = abgang_einheit_feld.get()
    kuerzel_name = abgang_kuerzel_feld.get()
    datum_name = abgang_datum_feld.get()
    
    # Schritt 2: Prüfen ob alle Felder ausgefüllt sind
    if not all([artikel_name, anzahl_str, einheit_name, kuerzel_name, datum_name]):
        messagebox.showwarning("Warnung", "Bitte füllen Sie alle Abgang-Felder aus!")
        return
    
    # Schritt 3: Anzahl in Zahl umwandeln
    try:
        anzahl = int(anzahl_str)
    except ValueError:
        messagebox.showerror("Fehler", "Anzahl muss eine Zahl sein!")
        return
    
    # Schritt 4: Artikel in der Tabelle suchen und Bestand reduzieren
    for item in treeview.get_children():
        values = list(treeview.item(item, 'values'))
        if values[1].lower() == artikel_name.lower():  # Artikelname vergleichen (nicht case-sensitive)
            artikel_id = values[0]
            aktueller_bestand = int(values[2])
            
            # Prüfen ob genug Bestand vorhanden ist
            if aktueller_bestand < anzahl:
                messagebox.showerror("Fehler", f"Nicht genug Bestand! Verfuegbar: {aktueller_bestand}")
                return
            
            # Bestand reduzieren
            neuer_bestand = aktueller_bestand - anzahl
            
            # In Datenbank aktualisieren
            try:
                db_path = get_writable_path("praxislager.db")
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("UPDATE artikel SET aktuellerbestand = ? WHERE artikel_id = ?", (neuer_bestand, artikel_id))
                conn.commit()
                conn.close()
                
                # Abgang-Felder leeren
                abgang_artikel_feld.delete(0, tkinter.END)
                abgang_anzahl_feld.delete(0, tkinter.END)
                abgang_einheit_feld.delete(0, tkinter.END)
                abgang_kuerzel_feld.delete(0, tkinter.END)
                abgang_datum_feld.delete(0, tkinter.END)
                abgang_datum_feld.insert(0, datetime.now().strftime("%d.%m.%Y"))
                
                # Tabelle neu laden
                tabelle_neu_laden()
                messagebox.showinfo("Erfolg", f"Abgang von {anzahl} {einheit_name} wurde erfolgreich registriert!")
                return
                
            except Exception as e:
                messagebox.showerror("Datenbank-Fehler", f"Konnte nicht aktualisieren: {e}")
                return
    
    # Falls Artikel nicht gefunden wurde
    messagebox.showerror("Fehler", f"Artikel '{artikel_name}' nicht gefunden!")

def loeschen():
    """
    Löscht einen Artikel komplett aus der Datenbank.
    Wird aufgerufen wenn der orange "Artikel löschen" Button geklickt wird.
    """
    # Schritt 1: Ausgewählten Eintrag ermitteln
    ausgewaehlt = treeview.selection()
    
    if not ausgewaehlt:
        messagebox.showwarning("Warnung", "Bitte wählen Sie einen Eintrag zum Löschen aus!")
        return
    
    # Schritt 2: Artikelname und ID holen
    item = ausgewaehlt[0]
    values = treeview.item(item, 'values')
    artikel_id = values[0]
    artikel_name = values[1]
    
    # Schritt 3: Sicherheitsabfrage
    antwort = messagebox.askyesno("Löschen bestätigen", 
                                 f"Möchten Sie den Artikel '{artikel_name}' wirklich löschen?")
    
    if antwort:
        # Schritt 4: Aus Datenbank löschen
        try:
            db_path = get_writable_path("praxislager.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM artikel WHERE artikel_id = ?", (artikel_id,))
            conn.commit()
            conn.close()
            
            # Tabelle neu laden
            tabelle_neu_laden()
            messagebox.showinfo("Erfolg", f"Artikel '{artikel_name}' wurde geloescht!")
            
        except Exception as e:
            messagebox.showerror("Datenbank-Fehler", f"Konnte nicht loeschen: {e}")

print("Erstelle GUI...")


# HAUPTFENSTER ERSTELLEN UND KONFIGURIEREN


# Hauptfenster erstellen
fenster = tkinter.Tk()
fenster.title("MediDEPOT - Lagerverwaltung")
fenster.geometry("1200x900")                    # Fenstergröße: 1200 Pixel breit, 900 Pixel hoch

# Fenster mittig auf dem Bildschirm positionieren
fenster.update_idletasks()                      # Größe berechnen lassen
breite = fenster.winfo_width()                  # Fensterbreite holen
hoehe = fenster.winfo_height()                  # Fensterhöhe holen
x = (fenster.winfo_screenwidth() // 2) - (breite // 2)    # X-Position berechnen (mittig horizontal)
y = (fenster.winfo_screenheight() // 2) - (hoehe // 2)   # Y-Position berechnen (mittig vertikal)
fenster.geometry(f"{breite}x{hoehe}+{x}+{y}")  # Fenster neu positionieren

fenster.resizable(True, False)                  # Größe änderbar: horizontal ja, vertikal nein

# =============================================================================
# OBERER BEREICH: EINGABEFELDER FÜR ZUGÄNGE UND ABGÄNGE
# =============================================================================

# Hauptframe für Eingabebereiche
haupt_eingabe_frame = tkinter.Frame(fenster)
haupt_eingabe_frame.pack(side=tkinter.TOP, fill=tkinter.X, padx=10, pady=10)

# ZUGÄNGE BEREICH (LINKS)
eingabe_frame = tkinter.Frame(haupt_eingabe_frame)
eingabe_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=(0, 5))

zugaenge = tkinter.Label(eingabe_frame, text="Neue Zugänge", font=("Arial", 12, "bold"), fg="green")
zugaenge.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 15))

# Eingabefelder für Zugänge
artikel = tkinter.Label(eingabe_frame, text="Artikelname:")
artikel.grid(row=1, column=0, sticky="w", padx=20, pady=5)
artikel_feld = tkinter.Entry(eingabe_frame, width=25)
artikel_feld.grid(row=1, column=1, padx=10, pady=5, sticky="w")

anzahl = tkinter.Label(eingabe_frame, text="Anzahl:")
anzahl.grid(row=2, column=0, sticky="w", padx=20, pady=5)
anzahl_feld = tkinter.Entry(eingabe_frame, width=25)
anzahl_feld.grid(row=2, column=1, padx=10, pady=5, sticky="w")

einheit = tkinter.Label(eingabe_frame, text="Einheit:")
einheit.grid(row=3, column=0, sticky="w", padx=20, pady=5)
einheit_feld = tkinter.Entry(eingabe_frame, width=25)
einheit_feld.grid(row=3, column=1, padx=10, pady=5, sticky="w")

ort = tkinter.Label(eingabe_frame, text="Ort:")
ort.grid(row=4, column=0, sticky="w", padx=20, pady=5)
ort_feld = tkinter.Entry(eingabe_frame, width=25)
ort_feld.grid(row=4, column=1, padx=10, pady=5, sticky="w")

kuerzel = tkinter.Label(eingabe_frame, text="Kürzel:")
kuerzel.grid(row=5, column=0, sticky="w", padx=20, pady=5)
kuerzel_feld = tkinter.Entry(eingabe_frame, width=25)
kuerzel_feld.grid(row=5, column=1, padx=10, pady=5, sticky="w")

datum_label = tkinter.Label(eingabe_frame, text="Datum:")
datum_label.grid(row=6, column=0, sticky="w", padx=20, pady=5)
datum_feld = tkinter.Entry(eingabe_frame, width=25)
datum_feld.grid(row=6, column=1, padx=10, pady=5, sticky="w")
datum_feld.insert(0, datetime.now().strftime("%d.%m.%Y"))

zugang_button = tkinter.Button(eingabe_frame, text="Zugang hinzufügen", command=hinzufugen, width=20,
                              background="green", foreground="black", font=("Arial", 10, "bold"))
zugang_button.grid(row=7, column=0, columnspan=2, pady=15)

# ABGÄNGE BEREICH (RECHTS)
abgang_frame = tkinter.Frame(haupt_eingabe_frame)
abgang_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True, padx=(5, 0))

abgaenge = tkinter.Label(abgang_frame, text="Abgänge", font=("Arial", 12, "bold"), fg="red")
abgaenge.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 15))

# Eingabefelder für Abgänge
abgang_artikel_label = tkinter.Label(abgang_frame, text="Artikelname:")
abgang_artikel_label.grid(row=1, column=0, sticky="w", padx=20, pady=5)
abgang_artikel_feld = tkinter.Entry(abgang_frame, width=25)
abgang_artikel_feld.grid(row=1, column=1, padx=10, pady=5, sticky="w")

abgang_anzahl_label = tkinter.Label(abgang_frame, text="Anzahl:")
abgang_anzahl_label.grid(row=2, column=0, sticky="w", padx=20, pady=5)
abgang_anzahl_feld = tkinter.Entry(abgang_frame, width=25)
abgang_anzahl_feld.grid(row=2, column=1, padx=10, pady=5, sticky="w")

abgang_einheit_label = tkinter.Label(abgang_frame, text="Einheit:")
abgang_einheit_label.grid(row=3, column=0, sticky="w", padx=20, pady=5)
abgang_einheit_feld = tkinter.Entry(abgang_frame, width=25)
abgang_einheit_feld.grid(row=3, column=1, padx=10, pady=5, sticky="w")

abgang_kuerzel_label = tkinter.Label(abgang_frame, text="Kürzel:")
abgang_kuerzel_label.grid(row=4, column=0, sticky="w", padx=20, pady=5)
abgang_kuerzel_feld = tkinter.Entry(abgang_frame, width=25)
abgang_kuerzel_feld.grid(row=4, column=1, padx=10, pady=5, sticky="w")

abgang_datum_label = tkinter.Label(abgang_frame, text="Datum:")
abgang_datum_label.grid(row=5, column=0, sticky="w", padx=20, pady=5)
abgang_datum_feld = tkinter.Entry(abgang_frame, width=25)
abgang_datum_feld.grid(row=5, column=1, padx=10, pady=5, sticky="w")
abgang_datum_feld.insert(0, datetime.now().strftime("%d.%m.%Y"))

abgang_button = tkinter.Button(abgang_frame, text="Abgang registrieren", command=abgang_hinzufugen, width=20,
                              background="red", foreground="black", font=("Arial", 10, "bold"))
abgang_button.grid(row=6, column=0, columnspan=2, pady=15)

# LÖSCHEN BUTTON
buLoeschen = tkinter.Button(fenster, text="Artikel löschen", command=loeschen, width=20,
                           background="orange", foreground="black", font=("Arial", 10, "bold"))
buLoeschen.pack(pady=10)

# TRENNLINIE
separator = ttk.Separator(fenster, orient='horizontal')
separator.pack(fill=tkinter.X, padx=10, pady=5)

# TABELLENBEREICH
tabelle_frame = tkinter.Frame(fenster)
tabelle_frame.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

tabelle_titel = tkinter.Label(tabelle_frame, text="Lagerbestand Übersicht", font=("Arial", 12, "bold"))
tabelle_titel.pack(pady=(0, 10))

# TABELLE ERSTELLEN
columns = ['ID', 'Artikelname', 'Aktueller Bestand', 'Mindestbestand', 'Einheit', 'Lagerort', 'Kürzel', 'Hinzugefügt am']
treeview = ttk.Treeview(tabelle_frame, columns=columns, show='headings', height=15)

# Spaltenüberschriften setzen
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=100, minwidth=50)

treeview.pack(fill=tkinter.BOTH, expand=True)

print("Lade Daten aus Datenbank...")

# WICHTIG: Datenbank erstellen falls sie nicht existiert (für erste Benutzung)
erstelle_datenbank_falls_nicht_vorhanden()

# DATEN AUS DATENBANK LADEN (anstatt Beispieldaten)
tabelle_neu_laden()

# Willkommensnachricht nur beim ersten Start zeigen
if erster_start:
    messagebox.showinfo("Willkommen", "Willkommen bei MediDEPOT!")

print("Starte GUI...")
fenster.mainloop()
print("Programm beendet!")