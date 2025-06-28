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
import csv                       # Für CSV-Export

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

def bearbeiten():
    """
    VERBESSERTE BEARBEITEN-FUNKTION für Anfänger
    Mit besserer Anordnung und sichtbaren Buttons
    """
    print("Bearbeiten-Button wurde geklickt!")  # Debug-Ausgabe
    
    # SCHRITT 1: Prüfen ob ein Artikel ausgewählt ist
    ausgewaehlt = treeview.selection()  # Welcher Artikel ist markiert?
    
    if not ausgewaehlt:  # Falls kein Artikel markiert ist
        messagebox.showwarning("Achtung", "Bitte klicken Sie erst auf einen Artikel in der Tabelle!")
        return  # Funktion beenden
    
    print("Artikel ist ausgewählt - starte Bearbeitung")  # Debug
    
    # SCHRITT 2: Die Daten vom ausgewählten Artikel holen
    item = ausgewaehlt[0]  # Den ersten (und einzigen) ausgewählten Artikel nehmen
    values = treeview.item(item, 'values')  # Alle Daten von diesem Artikel holen
    
    # Die einzelnen Werte in Variablen speichern (macht es übersichtlicher)
    artikel_id = values[0]          # Die ID (brauchen wir zum Speichern)
    alter_name = values[1]          # Der aktuelle Artikelname
    alter_bestand = values[2]       # Der aktuelle Bestand
    alter_mindest = values[3]       # Der aktuelle Mindestbestand
    alte_einheit = values[4]        # Die aktuelle Einheit
    alter_ort = values[5]           # Der aktuelle Lagerort
    altes_kuerzel = values[6]       # Das aktuelle Kürzel
    altes_datum = values[7]         # Das aktuelle Datum
    
    print(f"Bearbeite Artikel: {alter_name}")  # Debug
    
    # SCHRITT 3: Neues Fenster erstellen (GRÖSSER!)
    bearbeiten_fenster = tkinter.Toplevel(fenster)  # Neues Fenster erstellen
    bearbeiten_fenster.title(f"Artikel ändern: {alter_name}")  # Fenstertitel
    bearbeiten_fenster.geometry("500x550")  # GRÖSSER: 500 breit, 550 hoch
    bearbeiten_fenster.resizable(False, False)  # Größe nicht änderbar
    
    # Das neue Fenster soll über dem Hauptfenster erscheinen
    bearbeiten_fenster.transient(fenster)
    bearbeiten_fenster.grab_set()  # Hauptfenster blockieren bis wir fertig sind
    
    # SCHRITT 4: Überschrift im neuen Fenster
    titel = tkinter.Label(bearbeiten_fenster, text="Artikel bearbeiten", 
                         font=("Arial", 16, "bold"), fg="blue")
    titel.pack(pady=15)  # Oben anzeigen mit 15 Pixel Abstand
    
    # SCHRITT 5: FRAME für die Eingabefelder (LINKSBÜNDIG!)
    eingabe_frame = tkinter.Frame(bearbeiten_fenster)
    eingabe_frame.pack(padx=30, pady=10, fill="both", expand=True)
    
    # Artikelname ändern
    tkinter.Label(eingabe_frame, text="Artikelname:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", pady=8)
    neuer_name_feld = tkinter.Entry(eingabe_frame, width=35, font=("Arial", 11))
    neuer_name_feld.grid(row=0, column=1, padx=15, pady=8, sticky="w")
    neuer_name_feld.insert(0, alter_name)  # Aktuellen Namen einfügen
    
    # Bestand ändern
    tkinter.Label(eingabe_frame, text="Bestand:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky="w", pady=8)
    neuer_bestand_feld = tkinter.Entry(eingabe_frame, width=35, font=("Arial", 11))
    neuer_bestand_feld.grid(row=1, column=1, padx=15, pady=8, sticky="w")
    # Falls ein ⚠️ Symbol da ist, entfernen wir es
    sauberer_bestand = str(alter_bestand).replace(' ⚠️', '')
    neuer_bestand_feld.insert(0, sauberer_bestand)
    
    # Mindestbestand ändern
    tkinter.Label(eingabe_frame, text="Mindestbestand:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky="w", pady=8)
    neuer_mindest_feld = tkinter.Entry(eingabe_frame, width=35, font=("Arial", 11))
    neuer_mindest_feld.grid(row=2, column=1, padx=15, pady=8, sticky="w")
    neuer_mindest_feld.insert(0, alter_mindest)
    
    # Einheit ändern
    tkinter.Label(eingabe_frame, text="Einheit:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w", pady=8)
    neue_einheit_feld = tkinter.Entry(eingabe_frame, width=35, font=("Arial", 11))
    neue_einheit_feld.grid(row=3, column=1, padx=15, pady=8, sticky="w")
    neue_einheit_feld.insert(0, alte_einheit)
    
    # Lagerort ändern
    tkinter.Label(eingabe_frame, text="Lagerort:", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky="w", pady=8)
    neuer_ort_feld = tkinter.Entry(eingabe_frame, width=35, font=("Arial", 11))
    neuer_ort_feld.grid(row=4, column=1, padx=15, pady=8, sticky="w")
    neuer_ort_feld.insert(0, alter_ort)
    
    # Kürzel ändern
    tkinter.Label(eingabe_frame, text="Kürzel:", font=("Arial", 12, "bold")).grid(row=5, column=0, sticky="w", pady=8)
    neues_kuerzel_feld = tkinter.Entry(eingabe_frame, width=35, font=("Arial", 11))
    neues_kuerzel_feld.grid(row=5, column=1, padx=15, pady=8, sticky="w")
    neues_kuerzel_feld.insert(0, altes_kuerzel)
    
    # Datum ändern
    tkinter.Label(eingabe_frame, text="Datum:", font=("Arial", 12, "bold")).grid(row=6, column=0, sticky="w", pady=8)
    neues_datum_feld = tkinter.Entry(eingabe_frame, width=35, font=("Arial", 11))
    neues_datum_feld.grid(row=6, column=1, padx=15, pady=8, sticky="w")
    neues_datum_feld.insert(0, altes_datum)
    
    # SCHRITT 6: SPEICHERN-BUTTON (das Wichtigste!)
    def speichern_klick():
        """
        Das passiert wenn Sie auf "Speichern" klicken
        """
        print("Speichern wurde geklickt!")  # Debug
        
        # Die neuen Werte aus den Feldern holen
        neuer_name = neuer_name_feld.get()          # Text aus dem Namen-Feld
        neuer_bestand_text = neuer_bestand_feld.get()    # Text aus dem Bestand-Feld
        neuer_mindest_text = neuer_mindest_feld.get()    # Text aus dem Mindest-Feld
        neue_einheit = neue_einheit_feld.get()          # Text aus dem Einheit-Feld
        neuer_ort = neuer_ort_feld.get()                # Text aus dem Ort-Feld
        neues_kuerzel = neues_kuerzel_feld.get()        # Text aus dem Kürzel-Feld
        neues_datum = neues_datum_feld.get()            # Text aus dem Datum-Feld
        
        # PRÜFUNG 1: Sind alle Felder ausgefüllt?
        if not all([neuer_name, neuer_bestand_text, neuer_mindest_text, neue_einheit, neuer_ort, neues_kuerzel, neues_datum]):
            messagebox.showwarning("Fehler", "Bitte füllen Sie alle Felder aus!")
            return  # Nicht speichern, zurück zum Bearbeiten
        
        # PRÜFUNG 2: Sind die Zahlen wirklich Zahlen?
        try:
            neuer_bestand = int(neuer_bestand_text)     # Text in Zahl umwandeln
            neuer_mindest = int(neuer_mindest_text)     # Text in Zahl umwandeln
        except:
            messagebox.showerror("Fehler", "Bestand und Mindestbestand müssen Zahlen sein!\nZ.B. 10, 25, 100")
            return  # Nicht speichern, zurück zum Bearbeiten
        
        print(f"Speichere: {neuer_name}, Bestand: {neuer_bestand}")  # Debug
        
        # PRÜFUNG 3: In die Datenbank speichern
        try:
            # Datenbank öffnen (genauso wie in den anderen Funktionen)
            db_path = get_writable_path("praxislager.db")
            verbindung = sqlite3.connect(db_path)
            cursor = verbindung.cursor()
            
            # SQL-Befehl: Artikel mit dieser ID aktualisieren
            cursor.execute("""
                UPDATE artikel SET 
                produktname = ?, 
                aktuellerbestand = ?, 
                mindestbestand = ?, 
                einheit = ?, 
                lagerort = ?,
                Kürzel = ?,
                datum = ?
                WHERE artikel_id = ?
            """, (neuer_name, neuer_bestand, neuer_mindest, neue_einheit, neuer_ort, neues_kuerzel, neues_datum, artikel_id))
            
            verbindung.commit()  # Änderungen speichern
            verbindung.close()   # Datenbank schließen
            
            print("Erfolgreich gespeichert!")  # Debug
            
            # Die Tabelle im Hauptfenster neu laden (damit Sie die Änderungen sehen)
            tabelle_neu_laden()
            
            # Das Bearbeiten-Fenster schließen
            bearbeiten_fenster.destroy()
            
            # Erfolgsmeldung anzeigen
            messagebox.showinfo("Gespeichert!", f"Artikel '{neuer_name}' wurde erfolgreich geändert!")
            
        except Exception as fehler:
            # Falls beim Speichern etwas schiefgeht
            print(f"Speicher-Fehler: {fehler}")  # Debug
            messagebox.showerror("Speicher-Fehler", f"Konnte nicht speichern: {fehler}")
    
    # SCHRITT 7: ABBRECHEN-BUTTON
    def abbrechen_klick():
        """
        Das passiert wenn Sie auf "Abbrechen" klicken
        """
        print("Abbrechen wurde geklickt")  # Debug
        bearbeiten_fenster.destroy()  # Fenster einfach schließen ohne zu speichern
    
    # SCHRITT 8: BUTTON-BEREICH (UNTEN IM FENSTER!)
    button_bereich = tkinter.Frame(bearbeiten_fenster)  # Bereich für die Buttons
    button_bereich.pack(side="bottom", pady=25)  # UNTEN anzeigen mit viel Abstand
    
    # Grüner Speichern-Button (GRÖSSER!)
    speichern_button = tkinter.Button(button_bereich, text="SPEICHERN", 
                                    command=speichern_klick,  # Was passiert beim Klick
                                    bg="green", fg="black", 
                                    font=("Arial", 13, "bold"), width=18, height=2)
    speichern_button.pack(side="left", padx=15)  # Links anzeigen mit Abstand
    
    # Grauer Abbrechen-Button (GRÖSSER!)
    abbrechen_button = tkinter.Button(button_bereich, text="ABBRECHEN", 
                                     command=abbrechen_klick,  # Was passiert beim Klick
                                     bg="gray", fg="black", 
                                     font=("Arial", 13, "bold"), width=18, height=2)
    abbrechen_button.pack(side="left", padx=15)  # Rechts anzeigen mit Abstand
    
    print("Bearbeiten-Fenster ist bereit!")  # Debug

def einfache_inventur_exportieren():
    """
    SUPER EINFACHE VERSION für Anfänger
    Exportiert alle Artikel als CSV-Datei für die Inventur
    Speichert auf dem Schreibtisch (deutscher Mac)
    """
    print("Starte Inventur-Export...")  # Debug-Ausgabe
    
    try:
        # SCHRITT 1: Datenbank öffnen (genau wie in deinen anderen Funktionen)
        db_path = get_writable_path("praxislager.db")
        verbindung = sqlite3.connect(db_path)
        cursor = verbindung.cursor()
        
        # SCHRITT 2: Alle Artikel holen
        cursor.execute("SELECT * FROM artikel")
        alle_artikel = cursor.fetchall()
        verbindung.close()
        print(f"Gefunden: {len(alle_artikel)} Artikel")  
        
        # SCHRITT 3: Schreibtisch-Pfad finden 
        try:
            schreibtisch_pfad = os.path.expanduser("~/Desktop")  
            if not os.path.exists(schreibtisch_pfad):
                # Fallback: Benutzerordner
                schreibtisch_pfad = os.path.expanduser("~")
        except:
            schreibtisch_pfad = os.path.expanduser("~")
        
        # SCHRITT 4: Dateiname mit Schreibtisch-Pfad erstellen
        heute = datetime.now().strftime('%Y%m%d_%H%M')  # z.B. 20250623_1430
        dateiname = f"MediDEPOT_Inventur_{heute}.csv"
        vollstaendiger_pfad = os.path.join(schreibtisch_pfad, dateiname)
        
        print(f"Speichere auf Schreibtisch: {vollstaendiger_pfad}")  # Debug
        
        # SCHRITT 5: CSV-Datei schreiben
        with open(vollstaendiger_pfad, 'w', newline='', encoding='utf-8') as datei:
            csv_writer = csv.writer(datei, delimiter=';')
            
            # Header (Spaltenüberschriften)
            csv_writer.writerow([
                'ID', 'Artikelname', 'Bestand', 'Mindestbestand', 
                'Einheit', 'Lagerort', 'Datum', 'Kürzel'
            ])
            
            # Alle Artikel schreiben
            for artikel in alle_artikel:
                csv_writer.writerow(artikel)
        
        # SCHRITT 6: Deutsche Erfolgsmeldung
        messagebox.showinfo("Erfolg!", 
                           f"Inventur erfolgreich exportiert!\n\n"
                           f"📁 Datei: {dateiname}\n"
                           f"🖥️ Gespeichert auf dem Schreibtisch\n\n"
                           f"Sie finden die Datei auf Ihrem Schreibtisch!")
        print("Export erfolgreich auf Schreibtisch!")  # Debug
        
        # Schreibtisch automatisch öffnen
        try:
            import subprocess
            subprocess.call(["open", schreibtisch_pfad])
        except:
            pass  # Falls das nicht funktioniert, ist es nicht schlimm
        
    except Exception as fehler:
        # Falls etwas schiefgeht
        print(f"Fehler: {fehler}")  # Debug
        messagebox.showerror("Fehler!", f"Export fehlgeschlagen: {fehler}")

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

zugang_button = tkinter.Button(eingabe_frame, text="➕ Zugang hinzufügen", command=hinzufugen, width=20,
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

abgang_button = tkinter.Button(abgang_frame, text="➖ Abgang registrieren", command=abgang_hinzufugen, width=20,
                              background="red", foreground="black", font=("Arial", 10, "bold"))
abgang_button.grid(row=6, column=0, columnspan=2, pady=15)

# LÖSCHEN BUTTON
buLoeschen = tkinter.Button(fenster, text="🗑️ Artikel löschen", command=loeschen, width=20,
                           background="orange", foreground="black", font=("Arial", 10, "bold"))
buLoeschen.pack(pady=10)

# BEARBEITEN BUTTON - NEU!
bearbeiten_button = tkinter.Button(fenster, text="✏️ Artikel bearbeiten", 
                                 command=bearbeiten, width=20,
                                 background="lightgreen", foreground="black", 
                                 font=("Arial", 10, "bold"))
bearbeiten_button.pack(pady=5)

# INVENTUR BUTTON
inventur_button = tkinter.Button(
    fenster,
    text="📋 Inventur exportieren",
    command=einfache_inventur_exportieren,
    width=20,
    background="lightblue",
    foreground="black",
    font=("Arial", 10, "bold")
)
inventur_button.pack(pady=5)

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

# Bu kodu treeview.pack() satırından hemen ÖNCE ekleyin:

# ÇİFT TIKLAMA OLAYI EKLE
def on_double_click(event):
    """Çift tıklama olayı - bearbeiten() fonksiyonunu çağırır"""
    item = treeview.selection()
    if item:
        bearbeiten()  # Mevcut bearbeiten fonksiyonunu çağır

# Çift tıklama olayını treeview'e bağla
treeview.bind("<Double-1>", on_double_click)


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