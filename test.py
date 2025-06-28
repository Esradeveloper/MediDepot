# Tkinter importieren (für das Fenster und Buttons)
import tkinter
import os
import sys

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Funktion: Überprüft Benutzername und Passwort
def pruefen():
    # Eingaben aus den Textfeldern holen
    benutzer = etBenutzer.get()
    pw = etPasswort.get()
    
    # Prüfen ob Daten richtig sind
    if benutzer == "Praxis" and pw == "malzacher1234":
        lbAusgabe["text"] = "Zugang erlaubt"      # Erfolgsmeldung anzeigen
        buEnde["state"] = "normal"                # "Weiter"-Button aktivieren
    else:
        lbAusgabe["text"] = "Zugang nicht erlaubt" # Fehlermeldung anzeigen
        buEnde["state"] = "disabled"               # "Weiter"-Button deaktivieren
    
    # Eingabefelder leeren (für neue Eingabe)
    etBenutzer.delete(0, "end")
    etPasswort.delete(0, "end")

# Funktion: Schließt Login und öffnet Hauptprogramm
def ende():
    fenster.destroy()         # Login-Fenster schließen
    import medidepot   # Hauptprogramm starten
    

# Hauptfenster erstellen
fenster = tkinter.Tk()
fenster.title("MediDEPOT - Login")
fenster.geometry("1200x900")                     # Fenstergröße (Breite x Höhe)

# Fenster mittig positionieren
fenster.update_idletasks()  # Größe berechnen
breite = fenster.winfo_width()
hoehe = fenster.winfo_height()
x = (fenster.winfo_screenwidth() // 2) - (breite // 2)
y = (fenster.winfo_screenheight() // 2) - (hoehe // 2)
fenster.geometry(f"{breite}x{hoehe}+{x}+{y}")

fenster.resizable(True, False)                   # Größe änderbar: ja horizontal, nein vertikal
fenster.configure(bg="lightblue")                # Hintergrundfarbe des Fensters

# HINTERGRUNDBILD hinzufügen
try:
    hintergrund = tkinter.PhotoImage(file=get_resource_path("daten_bilder/Bild.png"))    # Bild laden
    hintergrund_label = tkinter.Label(fenster, image=hintergrund)  # Bild in Label
    hintergrund_label.place(x=0, y=0, relwidth=1, relheight=1)    # Über ganzes Fenster
    hintergrund_label.lower()                                      # Hintergrund nach hinten
except:
    print("Hintergrundbild nicht gefunden")                      # Falls Hintergrundbild nicht gefunden wird

# LOGO hinzufügen (links mittig, kleinere Größe)
try:
    logo_bild_original = tkinter.PhotoImage(file=get_resource_path("daten_bilder/logo_image.png"))  # Logo laden
    # Bild verkleinern (subsample macht es kleiner)
    logo_bild = logo_bild_original.subsample(2, 2)  # Halbiert die Größe
    logo_label = tkinter.Label(fenster, image=logo_bild, bg="white")  # Logo in weißem Kasten
    logo_label.place(x=150, y=350)  # Position links mittig
except:
    print("Logo nicht gefunden")
    # Falls Logo nicht gefunden, zeige Text stattdessen
    logo_label = tkinter.Label(fenster, text="MEDIDEPOT", font=("Arial", 16), 
                              bg="white", fg="lightblue", width=12, height=6)
    logo_label.place(x=150, y=350)

# LAYOUT konfigurieren (für mittige Ausrichtung)
fenster.grid_columnconfigure(0, weight=1)    # Linke Spalte: dehnbar
fenster.grid_columnconfigure(1, weight=0)    # Mittlere Spalte: feste Größe (hier sind die Login-Elemente)
fenster.grid_columnconfigure(2, weight=1)    # Rechte Spalte: dehnbar

# Alle Zeilen dehnbar machen (für vertikale Zentrierung)
for i in range(25):
    fenster.grid_rowconfigure(i, weight=1)

# LOGIN-BEREICH erstellen (engere Abstände)

# Benutzername-Eingabe
lbBenutzer = tkinter.Label(fenster, text="Benutzername:", fg="black", 
                          relief="flat", bd=0, highlightthickness=0)  # Keine Umrandung
lbBenutzer.grid(row=12, column=1, sticky="w", padx=5, pady=1)       # pady=1 (sehr eng)

etBenutzer = tkinter.Entry(fenster, width=20, bg="white", fg="black")  # Eingabefeld
etBenutzer.grid(row=13, column=1, padx=5, pady=1)                     # pady=1 (sehr eng)

# Passwort-Eingabe
lbPasswort = tkinter.Label(fenster, text="Passwort:", fg="black",
                          relief="flat", bd=0, highlightthickness=0)  # Keine Umrandung
lbPasswort.grid(row=14, column=1, sticky="w", padx=5, pady=1)        # pady=1 (sehr eng)

etPasswort = tkinter.Entry(fenster, show="*", width=20, bg="white", fg="black")  # Eingabefeld (Sterne für Passwort)
etPasswort.grid(row=15, column=1, padx=5, pady=1)                               # pady=1 (sehr eng)

# Prüfen-Button
buPruefen = tkinter.Button(fenster, text="Prüfen", command=pruefen, width=10,
                          bg="lightblue", activebackground="skyblue")      # Button zum Prüfen
buPruefen.grid(row=16, column=1, sticky="w", padx=5, pady=3)              # pady=3 (etwas mehr Platz vor Button)

# Ausgabe-Text (zeigt Erfolg oder Fehler an)
lbAusgabe = tkinter.Label(fenster, text="(leer)", fg="black",
                         relief="flat", bd=0, highlightthickness=0)        # Keine Umrandung
lbAusgabe.grid(row=17, column=1, sticky="w", padx=5, pady=1)              # pady=1 (sehr eng)

# Weiter-Button (nur aktiv nach erfolgreichem Login)
buEnde = tkinter.Button(fenster, text="Weiter", command=ende, width=10, state="disabled",
                       bg="lightblue", activebackground="skyblue")         # Button zum Weiter
buEnde.grid(row=18, column=1, padx=5, pady=1)                            # pady=1 (sehr eng)

# Fenster anzeigen und auf Benutzer-Aktionen warten
fenster.mainloop()