# MediDepot - Medizinische Lagerverwaltung 🏥

Eine benutzerfreundliche Desktop-Anwendung zur Verwaltung von medizinischen Lagerbeständen in Praxen und Kliniken.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Funktionen

- **Lagerverwaltung**: Einfache Verwaltung von medizinischen Artikeln
- **Bestandsüberwachung**: Automatische Warnung bei niedrigen Beständen
- **Zugänge & Abgänge**: Einfache Erfassung von Warenein- und ausgängen
- **Doppelklick-Navigation**: Grid-Doppelklick für schnelle Artikelauswahl
- **Passwort-Management**: Sichere Anmeldung mit Passwort-System
- **Datenbank**: Automatische SQLite-Datenbank mit Beispieldaten
- **Desktop-App**: Standalone DMG-Datei für einfache Installation
- **Benutzerfreundlich**: Intuitive GUI mit klarer Struktur

## 🚀 Installation

### Voraussetzungen

- Python 3.6 oder höher
- Tkinter (meist bereits mit Python installiert)

### Setup

1. **Repository klonen:**
```bash
git clone https://github.com/ihr-username/MediDepot.git
cd MediDepot
```

2. **Programm starten:**
```bash
python medidepot.py
```

Das war's! Die Datenbank wird automatisch beim ersten Start erstellt.

## 📖 Verwendung

### Ersten Start
Beim ersten Programmstart wird automatisch eine SQLite-Datenbank mit Beispieldaten erstellt. Sie können sofort beginnen!

### Neue Artikel hinzufügen
1. Füllen Sie die Felder unter "Neue Zugänge" aus
2. Klicken Sie auf "Zugang hinzufügen"
3. Der Artikel wird automatisch zur Datenbank hinzugefügt

### Abgänge registrieren
1. Geben Sie den Artikelnamen und die Anzahl unter "Abgänge" ein
2. Klicken Sie auf "Abgang registrieren"
3. Der Bestand wird automatisch reduziert

### Artikel löschen
1. Wählen Sie einen Artikel in der Tabelle aus
2. Klicken Sie auf "Artikel löschen"
3. Bestätigen Sie die Sicherheitsabfrage

## 📁 Projektstruktur

```
MediDepot/
├── medidepot.py          # Hauptprogramm
├── datenbank_erstellen.py # Datenbank-Setup (optional)
├── passwort.py           # Passwort-Funktionen
├── unit_test.py          # Unit Tests
├── praxislager.db        # SQLite-Datenbank (wird automatisch erstellt)
├── requirements.txt      # Python-Abhängigkeiten
├── daten_bilder/         # Dokumentation und Bilder
│   ├── Bild.png
│   └── logo_image.png
├── build/                # Build-Dateien (PyInstaller)
├── dist/                 # Distribution-Dateien
├── MediDepot.dmg         # macOS Installer
├── medidepot.spec        # PyInstaller Konfiguration
├── LICENSE               # MIT Lizenz
└── README.md             # Diese Datei
```

## 🔧 Technische Details

### Datenbank-Schema
```sql
CREATE TABLE artikel (
    artikel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    produktname TEXT,
    aktuellerbestand INTEGER,
    mindestbestand INTEGER,
    einheit TEXT,
    lagerort TEXT,
    datum TEXT,
    Kürzel TEXT
);
```

### Funktionen im Detail

#### `get_writable_path(filename)`
Findet den korrekten Speicherort für die Datenbank:
- Entwicklung: Aktueller Ordner
- App-Bundle: Application Support Ordner

#### `erstelle_datenbank_falls_nicht_vorhanden()`
Erstellt automatisch eine neue Datenbank mit Beispieldaten beim ersten Start.

#### `tabelle_neu_laden()`
Lädt die Tabelle neu und prüft automatisch auf niedrige Bestände.

## ⚠️ Bestandswarnungen

Das System warnt automatisch wenn:
- Aktueller Bestand ≤ Mindestbestand
- Warnsymbol (⚠️) wird in der Tabelle angezeigt
- Popup-Warnung erscheint beim Neuladen

## 🧪 Tests

Tests ausführen:
```bash
python unit_test.py
```

## 📱 App-Bundle erstellen

### Windows
```bash
# PyInstaller installieren
pip install pyinstaller

# Executable erstellen
pyinstaller --onefile --windowed medidepot.py
# Ergebnis: dist/medidepot.exe
```

### macOS
```bash
# PyInstaller installieren
pip install pyinstaller

# App-Bundle erstellen
pyinstaller medidepot.spec
# Ergebnis: dist/medidepot.app

# DMG-Installer erstellen (optional)
# Mit Disk Utility oder create-dmg
```

**Hinweis:** Die mitgelieferte `MediDepot.dmg` wurde auf macOS erstellt.

## 🤝 Beitragen

Wir freuen uns über Beiträge! So können Sie helfen:

1. Fork das Repository
2. Erstellen Sie einen Feature-Branch (`git checkout -b feature/NeuesFunktion`)
3. Committen Sie Ihre Änderungen (`git commit -am 'Neue Funktion hinzugefügt'`)
4. Push zum Branch (`git push origin feature/NeuesFunktion`)
5. Erstellen Sie einen Pull Request

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

## 👨‍💻 Autor

**Esra Güler**
- Erstellt: 28.05.2025
- Beschreibung: Lagerverwaltungssystem für medizinische Praxen

## 📞 Support

Bei Fragen oder Problemen:
1. Erstellen Sie ein [Issue](https://github.com/ihr-username/MediDepot/issues)
2. Beschreiben Sie das Problem detailliert
3. Fügen Sie Screenshots hinzu (wenn hilfreich)

## 🔄 Changelog

### Version 1.2 (Aktuell)
- Grid-Doppelklick Funktionalität hinzugefügt
- Passwort-System implementiert  
- macOS DMG-Installer erstellt
- Code-Bereinigung und Optimierung

### Version 1.1
- PyInstaller Integration
- Build-System optimiert
- Zusätzliche Spec-Dateien

### Version 1.0
- Grundlegende Lagerverwaltung
- Automatische Datenbankererstellung
- Bestandswarnungen
- GUI mit Tkinter
- SQLite-Integration

---

**Hinweis für Anfänger:** Dieser Code ist ausführlich kommentiert und als Lernprojekt geeignet. Jede Funktion ist erklärt und der Code folgt Python-Standards.