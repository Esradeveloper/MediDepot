# Unit Test für Login
import unittest

# Die Login-Funktion
def login_pruefen(benutzername, passwort):
    """Prüft ob Login-Daten korrekt sind"""
    if benutzername == "Praxis" and passwort == "malzacher1234":
        return True
    else:
        return False

# Unit Tests
class TestLogin(unittest.TestCase):
    
    def test_korrekter_login(self):
        """Test: Praxis + malzacher1234 = erfolgreich"""
        result = login_pruefen("Praxis", "malzacher1234")
        self.assertTrue(result)
        print("Korrekter Login funktioniert")
    
    def test_falscher_benutzername(self):
        """Test: falscher Benutzername"""
        result = login_pruefen("admin", "malzacher1234")
        self.assertFalse(result)
        print("Falscher Benutzername wird abgelehnt")
    
    def test_falsches_passwort(self):
        """Test: falsches Passwort"""
        result = login_pruefen("Praxis", "123456")
        self.assertFalse(result)
        print("Falsches Passwort wird abgelehnt")
    
    def test_leere_eingaben(self):
        """Test: leere Eingaben"""
        result = login_pruefen("", "")
        self.assertFalse(result)
        print("Leere Eingaben werden abgelehnt")

# Tests ausführen
if __name__ == "__main__":
    print("Login Tests werden ausgeführt...")
    unittest.main(verbosity=2)