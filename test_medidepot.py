# =============================================================================
# UNIT TESTS FÜR MEDIDEPOT HAUPTPROGRAMM
# =============================================================================
# Autor: Esra Güler
# Datum: 28.05.25
# Beschreibung: Tests für die Datenbank-Funktionen der Lagerverwaltung

import unittest
import sqlite3
import os
import tempfile
from datetime import datetime

# Testfunktionen aus dem Hauptprogramm (ohne GUI)
def get_test_db_path():
    """Erstellt eine temporäre Test-Datenbank"""
    return "test_praxislager.db"

def test_datenbank_erstellen():
    """Erstellt eine Test-Datenbank mit der gleichen Struktur"""
    db_path = get_test_db_path()
    
    # Alte Test-DB löschen falls vorhanden
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Neue Test-Datenbank erstellen
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabelle erstellen (gleiche Struktur wie im Hauptprogramm)
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
    conn.commit()
    conn.close()
    return db_path

def test_artikel_hinzufuegen(produktname, bestand, mindest, einheit, ort, kuerzel, datum):
    """Fügt einen Artikel zur Test-Datenbank hinzu"""
    db_path = get_test_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO artikel (produktname, aktuellerbestand, mindestbestand, einheit, lagerort, Kürzel, datum)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (produktname, bestand, mindest, einheit, ort, kuerzel, datum))
    
    conn.commit()
    artikel_id = cursor.lastrowid  # ID des eingefügten Artikels
    conn.close()
    return artikel_id

def test_artikel_laden():
    """Lädt alle Artikel aus der Test-Datenbank"""
    db_path = get_test_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT artikel_id, produktname, aktuellerbestand, mindestbestand, einheit, lagerort, Kürzel, datum FROM artikel")
    daten = cursor.fetchall()
    conn.close()
    return daten

def test_artikel_loeschen(artikel_id):
    """Löscht einen Artikel aus der Test-Datenbank"""
    db_path = get_test_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM artikel WHERE artikel_id = ?", (artikel_id,))
    conn.commit()
    geloeschte_zeilen = cursor.rowcount
    conn.close()
    return geloeschte_zeilen

def test_bestand_aendern(artikel_id, neuer_bestand):
    """Ändert den Bestand eines Artikels"""
    db_path = get_test_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE artikel SET aktuellerbestand = ? WHERE artikel_id = ?", (neuer_bestand, artikel_id))
    conn.commit()
    geaenderte_zeilen = cursor.rowcount
    conn.close()
    return geaenderte_zeilen

# =============================================================================
# UNIT TEST KLASSE
# =============================================================================

class TestMediDepot(unittest.TestCase):
    
    def setUp(self):
        """Wird vor jedem Test ausgeführt - erstellt saubere Test-Datenbank"""
        print("\n--- Neuer Test startet ---")
        test_datenbank_erstellen()
    
    def tearDown(self):
        """Wird nach jedem Test ausgeführt - löscht Test-Datenbank"""
        db_path = get_test_db_path()
        if os.path.exists(db_path):
            os.remove(db_path)
        print("--- Test beendet ---")
    
    def test_datenbank_erstellen_erfolgreich(self):
        """Test: Datenbank wird korrekt erstellt"""
        db_path = get_test_db_path()
        self.assertTrue(os.path.exists(db_path))
        print("✓ Datenbank erfolgreich erstellt")
    
    def test_artikel_hinzufuegen_erfolgreich(self):
        """Test: Artikel wird korrekt hinzugefügt"""
        artikel_id = test_artikel_hinzufuegen(
            "Test-Handschuhe", 50, 10, "Packung", "Labor", "TH", "17.06.2025"
        )
        
        # Prüfen ob Artikel eingefügt wurde
        self.assertIsNotNone(artikel_id)
        self.assertGreater(artikel_id, 0)
        
        # Prüfen ob Artikel in Datenbank ist
        artikel = test_artikel_laden()
        self.assertEqual(len(artikel), 1)
        self.assertEqual(artikel[0][1], "Test-Handschuhe")  # produktname
        self.assertEqual(artikel[0][2], 50)                 # aktuellerbestand
        print("✓ Artikel erfolgreich hinzugefügt")
    
    def test_mehrere_artikel_hinzufuegen(self):
        """Test: Mehrere Artikel hinzufügen"""
        # Artikel 1
        test_artikel_hinzufuegen("Mullbinde", 20, 5, "Stück", "Lager A", "MB", "17.06.2025")
        # Artikel 2  
        test_artikel_hinzufuegen("Desinfektionsmittel", 15, 3, "Liter", "Lager B", "DM", "17.06.2025")
        
        artikel = test_artikel_laden()
        self.assertEqual(len(artikel), 2)
        print("✓ Mehrere Artikel erfolgreich hinzugefügt")
    
    def test_artikel_loeschen_erfolgreich(self):
        """Test: Artikel wird korrekt gelöscht"""
        # Erst Artikel hinzufügen
        artikel_id = test_artikel_hinzufuegen("Test-Löschung", 10, 2, "Stück", "Test", "TL", "17.06.2025")
        
        # Prüfen dass Artikel da ist
        artikel_vorher = test_artikel_laden()
        self.assertEqual(len(artikel_vorher), 1)
        
        # Artikel löschen
        geloeschte = test_artikel_loeschen(artikel_id)
        self.assertEqual(geloeschte, 1)
        
        # Prüfen dass Artikel weg ist
        artikel_nachher = test_artikel_laden()
        self.assertEqual(len(artikel_nachher), 0)
        print("✓ Artikel erfolgreich gelöscht")
    
    def test_bestand_aendern_erfolgreich(self):
        """Test: Bestand wird korrekt geändert"""
        # Artikel hinzufügen
        artikel_id = test_artikel_hinzufuegen("Test-Bestand", 100, 10, "Stück", "Test", "TB", "17.06.2025")
        
        # Bestand ändern (Abgang von 25 Stück)
        neuer_bestand = 75
        geaendert = test_bestand_aendern(artikel_id, neuer_bestand)
        self.assertEqual(geaendert, 1)
        
        # Prüfen ob Bestand korrekt geändert wurde
        artikel = test_artikel_laden()
        self.assertEqual(artikel[0][2], 75)  # aktuellerbestand sollte 75 sein
        print("✓ Bestand erfolgreich geändert")
    
    def test_leere_datenbank_laden(self):
        """Test: Leere Datenbank laden"""
        artikel = test_artikel_laden()
        self.assertEqual(len(artikel), 0)
        print("✓ Leere Datenbank korrekt geladen")
    
    def test_artikel_mit_leerem_namen(self):
        """Test: Artikel mit leerem Namen (sollte funktionieren, wird aber später validiert)"""
        artikel_id = test_artikel_hinzufuegen("", 10, 2, "Stück", "Test", "LN", "17.06.2025")
        self.assertIsNotNone(artikel_id)
        
        artikel = test_artikel_laden()
        self.assertEqual(artikel[0][1], "")  # produktname ist leer
        print("✓ Artikel mit leerem Namen eingefügt (GUI sollte das aber verhindern)")
    
    def test_negativer_bestand(self):
        """Test: Negativer Bestand (sollte funktionieren, wird aber später validiert)"""
        artikel_id = test_artikel_hinzufuegen("Test-Negativ", -5, 10, "Stück", "Test", "TN", "17.06.2025")
        artikel = test_artikel_laden()
        self.assertEqual(artikel[0][2], -5)  # aktuellerbestand ist -5
        print("✓ Negativer Bestand eingefügt (GUI sollte das aber verhindern)")

# =============================================================================
# TESTS AUSFÜHREN
# =============================================================================

if __name__ == "__main__":
    print("=== MediDEPOT UNIT TESTS ===")
    print("Teste die Datenbank-Funktionen der Lagerverwaltung...")
    unittest.main(verbosity=2)