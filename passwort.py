
# MEDIDEPOT LOGIN-PROGRAMM

# Autor: Esra Güler
# Datum: 28.05.25
# Beschreibung: Login-System für MediDEPOT Lagerverwaltung
#               Überprüft Benutzername und Passwort, startet dann das Hauptprogramm

# Alle benötigten Module importieren
import tkinter                    # Für das Fenster, Buttons und Eingabefelder
import os                        # Für Dateipfade
import sys                       # Für Systeminformationen

def get_resource_path(relative_path):
    """ 
    Findet den richtigen Pfad zu Bildern und anderen Dateien.
    WICHTIG: Diese Funktion sorgt dafür, dass Bilder sowohl beim Programmieren
    als auch in der fertigen App gefunden werden.
    """
    try:
        # PyInstaller erstellt einen temporären Ordner und speichert den Pfad in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Falls nicht als App gepackt, verwende aktuellen Ordner
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


# FUNKTIONEN FÜR DAS LOGIN-SYSTEM


def pruefen():
    """
    Diese Funktion wird aufgerufen wenn der "Prüfen"-Button geklickt wird.
    Sie überprüft ob Benutzername und Passwort richtig sind.
    """
    # Schritt 1: Eingaben aus den Textfeldern holen
    benutzer = etBenutzer.get()      # Text aus dem Benutzername-Feld
    pw = etPasswort.get()            # Text aus dem Passwort-Feld
    
    # Schritt 2: Prüfen ob die Daten richtig sind
    # HIER STEHEN DIE LOGIN-DATEN: Benutzername "demo", Passwort "demo123"
    if benutzer == "demo" and pw == "demo123":
        # ERFOLG: Login-Daten sind korrekt
        lbAusgabe["text"] = "Zugang erlaubt"      # Erfolgsmeldung anzeigen
        buEnde["state"] = "normal"                # "Weiter"-Button aktivieren (anklickbar machen)
    else:
        # FEHLER: Login-Daten sind falsch
        lbAusgabe["text"] = "Zugang nicht erlaubt" # Fehlermeldung anzeigen
        buEnde["state"] = "disabled"               # "Weiter"-Button deaktivieren (nicht anklickbar)
    
    # Schritt 3: Eingabefelder leeren (für neue Eingabe bereit machen)
    etBenutzer.delete(0, "end")      # Benutzername-Feld leeren
    etPasswort.delete(0, "end")      # Passwort-Feld leeren

def ende():
    """
    Diese Funktion wird aufgerufen wenn der "Weiter"-Button geklickt wird.
    Sie schließt das Login-Fenster und startet das Hauptprogramm.
    """
    fenster.destroy()         # Login-Fenster schließen (komplett entfernen)
    import medidepot         # Hauptprogramm (Lagerverwaltung) starten

# HAUPTFENSTER ERSTELLEN UND KONFIGURIEREN


# Hauptfenster erstellen
fenster = tkinter.Tk()
fenster.title("MediDEPOT - Login")               # Titel des Fensters
fenster.geometry("1200x900")                     # Fenstergröße: 1200 Pixel breit, 900 Pixel hoch

# Fenster mittig auf dem Bildschirm positionieren
fenster.update_idletasks()                       # Größe berechnen lassen
breite = fenster.winfo_width()                   # Fensterbreite holen
hoehe = fenster.winfo_height()                   # Fensterhöhe holen
x = (fenster.winfo_screenwidth() // 2) - (breite // 2)     # X-Position berechnen (mittig horizontal)
y = (fenster.winfo_screenheight() // 2) - (hoehe // 2)     # Y-Position berechnen (mittig vertikal)
fenster.geometry(f"{breite}x{hoehe}+{x}+{y}")   # Fenster neu positionieren

fenster.resizable(True, False)                   # Größe änderbar: horizontal ja, vertikal nein
fenster.configure(bg="lightblue")                # Hintergrundfarbe des Fensters (hellblau)


# HINTERGRUNDBILD UND LOGO HINZUFÜGEN


# HINTERGRUNDBILD hinzufügen (falls vorhanden)
try:
    # Versuche das Hintergrundbild zu laden
    hintergrund = tkinter.PhotoImage(file=get_resource_path("daten_bilder/Bild.png"))
    hintergrund_label = tkinter.Label(fenster, image=hintergrund)  # Bild in ein Label packen
    hintergrund_label.place(x=0, y=0, relwidth=1, relheight=1)    # Über das ganze Fenster strecken
    hintergrund_label.lower()                                      # Hintergrund nach hinten legen
except:
    # Falls Hintergrundbild nicht gefunden wird, einfach weitermachen
    print("Hintergrundbild nicht gefunden")

# LOGO hinzufügen (links mittig, kleinere Größe)
try:
    # Versuche das Logo zu laden und zu verkleinern
    logo_bild_original = tkinter.PhotoImage(file=get_resource_path("daten_bilder/logo_image.png"))
    logo_bild = logo_bild_original.subsample(2, 2)  # Bild halbieren (subsample macht es kleiner)
    logo_label = tkinter.Label(fenster, image=logo_bild, bg="white")  # Logo in weißen Kasten
    logo_label.place(x=150, y=350)                  # Position: 150 Pixel von links, 350 von oben
except:
    # Falls Logo nicht gefunden wird, zeige Text stattdessen
    print("Logo nicht gefunden")
    logo_label = tkinter.Label(fenster, text="MEDIDEPOT", font=("Arial", 16), 
                              bg="white", fg="lightblue", width=12, height=6)
    logo_label.place(x=150, y=350)


# LAYOUT KONFIGURIEREN (Für mittige Ausrichtung der Login-Elemente)


# Grid-System konfigurieren: 3 Spalten für mittige Ausrichtung
fenster.grid_columnconfigure(0, weight=1)       # Linke Spalte: dehnbar (leer)
fenster.grid_columnconfigure(1, weight=0)       # Mittlere Spalte: feste Größe (hier sind die Login-Elemente)
fenster.grid_columnconfigure(2, weight=1)       # Rechte Spalte: dehnbar (leer)

# Alle Zeilen dehnbar machen (für vertikale Zentrierung)
for i in range(25):                             # 25 Zeilen erstellen
    fenster.grid_rowconfigure(i, weight=1)      # Jede Zeile dehnbar machen


# LOGIN-BEREICH ERSTELLEN (Eingabefelder und Buttons)


# BENUTZERNAME-EINGABE
# Label (Beschriftung) für Benutzername
lbBenutzer = tkinter.Label(fenster, text="Benutzername:", fg="black", 
                          relief="flat", bd=0, highlightthickness=0)  # Keine Umrandung
lbBenutzer.grid(row=12, column=1, sticky="w", padx=5, pady=1)        # Position: Zeile 12, Spalte 1

# Eingabefeld für Benutzername
etBenutzer = tkinter.Entry(fenster, width=20, bg="white", fg="black")  # 20 Zeichen breit, weißer Hintergrund
etBenutzer.grid(row=13, column=1, padx=5, pady=1)                     # Position: Zeile 13, Spalte 1

# PASSWORT-EINGABE
# Label (Beschriftung) für Passwort
lbPasswort = tkinter.Label(fenster, text="Passwort:", fg="black",
                          relief="flat", bd=0, highlightthickness=0)  # Keine Umrandung
lbPasswort.grid(row=14, column=1, sticky="w", padx=5, pady=1)        # Position: Zeile 14, Spalte 1

# Eingabefeld für Passwort (mit Sternchen statt Buchstaben)
etPasswort = tkinter.Entry(fenster, show="*", width=20, bg="white", fg="black")  # show="*" macht Sternchen
etPasswort.grid(row=15, column=1, padx=5, pady=1)                               # Position: Zeile 15, Spalte 1

# PRÜFEN-BUTTON
# Button zum Überprüfen der Login-Daten
buPruefen = tkinter.Button(fenster, text="Prüfen", command=pruefen, width=10,
                          bg="lightblue", activebackground="skyblue")      # command=pruefen bedeutet: rufe pruefen() auf
buPruefen.grid(row=16, column=1, sticky="w", padx=5, pady=3)              # Position: Zeile 16, Spalte 1

# AUSGABE-TEXT (zeigt Erfolg oder Fehler an)
# Label das anzeigt ob Login erfolgreich war oder nicht
lbAusgabe = tkinter.Label(fenster, text="(leer)", fg="black",
                         relief="flat", bd=0, highlightthickness=0)        # Keine Umrandung
lbAusgabe.grid(row=17, column=1, sticky="w", padx=5, pady=1)              # Position: Zeile 17, Spalte 1

# WEITER-BUTTON (nur aktiv nach erfolgreichem Login)
# Button zum Starten des Hauptprogramms (anfangs deaktiviert)
buEnde = tkinter.Button(fenster, text="Weiter", command=ende, width=10, state="disabled",
                       bg="lightblue", activebackground="skyblue")         # state="disabled" = nicht anklickbar
buEnde.grid(row=18, column=1, padx=5, pady=1)                            # Position: Zeile 18, Spalte 1


# PROGRAMM STARTEN


# Fenster anzeigen und auf Benutzer-Aktionen warten
# mainloop() startet die Ereignisschleife - das Programm läuft bis das Fenster geschlossen wird
fenster.mainloop()