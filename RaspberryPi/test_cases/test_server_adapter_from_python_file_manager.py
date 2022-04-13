import sys
sys.path.append('/home/pi/src-Building-Security-System')
import os
import unittest
from RaspberryPi.src.data_model.identifier import Identifier
from RaspberryPi.src.data_model.key_token import UnauthorizedNFCToken
from RaspberryPi.src.data_model.name import Name, LastName, FirstName
from RaspberryPi.src.data_model.password import Password
from RaspberryPi.src.data_model.user import UnauthenticatedUser
from RaspberryPi.src.door_controller.server_adapter.server_adapter_from_python_filemanager import ServerAdapterFromPythonFilemanager

"""
Dieses Modul ist zum Testen des Moduls server_adapter_from_python.
Classes:
    TestServerAdapterFromPythonFileManager(unittest.TestCase): Diese Klasse implementiert Test Methoden für
        die Klasse ServerAdapterFromPython
        
@author Lukas Wittenzellner
@version 1.0
"""


class TestServerAdapterFromPythonFileManager(unittest.TestCase):
    """
    Diese Klasse testet die Methoden der Klasse ServerAdapterFromPython.

    Methods:
        setUp: Bereitet eine Reihe von Attributen vor, die von einigen Methoden verwendet werden.
            Außerdem wird ein Backup der Tokenliste erstellt, damit kein Test diese versehentlich verändert.
        tearDown: Läd das Backup der Tokenliste wieder in die Datei.
        test_init: Testet den Konstruktor des Adapters.
        test_validate_filepath: Testet die Validierung des Pfades der Datei der Tokens.
        test_add_token_to_user: Testet verschiedene Szenarien zum Hinzufügen eines Tokens zu einem Nutzer.
        test_delete_token_from_user: Testet verschiedene Szenarien zum Löschen eines Tokens eines Nutzers.
        test_delete_all_tokens_from_user: Testet verschiedene Szenarien zum Löschen aller Tokens eines Nutzers.
        test_get_user: Testet das Bekommen der gespeicherten Informationen eines Nutzers.
        test_get_all_valid_tokens: Testet das Bekommen der Liste aller gespeicherten Tokens aller Nutzer.

    """
    def setUp(self) -> None:
        """
        Bereitet eine Reihe von Attributen vor, die von einigen Methoden verwendet werden.
        Außerdem wird ein Backup der Tokenliste erstellt, damit kein Test diese versehentlich verändert.
        """
        self.server_adapter = ServerAdapterFromPythonFilemanager()
        self.path = "/home/pi/src-Building-Security-System/src/ValidTokens.txt"
        self.temp_path = "/home/pi/src-Building-Security-System/src/temp_file.txt"

        self.admin = UnauthenticatedUser(Name(FirstName("admin"), LastName("admin")), Identifier("admin"))
        self.admin_password = Password("admin")
        self.admin_string = "admin,admin;admin;admin:"

        self.example_user1 = UnauthenticatedUser(Name(FirstName("Max"), LastName("Mustermann")), Identifier("identifier1"))
        self.example_user1_string = "Max,Mustermann;identifier1;password1:"
        self.example_token1_string = "example_token1"
        self.example_token1 = UnauthorizedNFCToken(Identifier(self.example_token1_string))

        self.example_user2 = UnauthenticatedUser(Name(FirstName("John"), LastName("Doe")), Identifier("identifier2"))
        self.example_user2_string = "John,Doe;identifier2;password2:"
        self.example_token2_string = "example_token2"
        self.example_token2 = UnauthorizedNFCToken(Identifier(self.example_token2_string))

        # Erstellt ein Backup der Tokenliste unter dem angegebenen Pfad
        with open(self.temp_path, "w") as temp_file, open(self.path, "r+") as file:
            for line in file:
                temp_file.write(line)
            file.truncate(0)

    def tearDown(self) -> None:
        """
        Läd das Backup der Tokenliste wieder in die Datei.
        """
        with open(self.path, "w") as file, open(self.temp_path, "r") as temp_file:
            for line in temp_file:
                file.write(line)
        os.remove(self.temp_path)

    def test_init(self):
        """
        Testet den Konstruktor des Adapters.
        """
        self.assertIsInstance(self.server_adapter, ServerAdapterFromPythonFilemanager)

    def test_validate_filepath(self):
        """
        Testet die Validierung des Pfades der Datei der Tokens.
        """
        self.assertTrue(self.server_adapter.validate_filepath())

    def test_add_token_to_user(self):
        """
        Testet verschiedene Szenarien zum Hinzufügen eines Tokens zu einem Nutzer.
        """
        # Fügt Nutzer der temporären Datei hinzu
        with open(self.path, "w+") as file:
            file.write(self.admin_string + "\n" +
                       self.example_user1_string + "\n" +
                       self.example_user2_string)

        # Wenn das Passwort des Admins nicht stimmt
        self.server_adapter.add_token_to_user(self.admin, Password("False_Password"),
                                              self.example_user1, self.example_token1)
        self.assertEqual(self.server_adapter.get_user(self.admin, self.admin_password, self.example_user1).split(":")[1], "")

        # Wenn der Nutzer nicht existiert, dem ein Token hinzugefügt werden soll
        non_existent_user = UnauthenticatedUser(Name(FirstName("Non"), LastName("Existent")), Identifier("User"))
        self.server_adapter.add_token_to_user(self.admin, self.admin_password, non_existent_user, self.example_token1)
        self.assertEqual(self.server_adapter.get_user(self.admin,
                                                      self.admin_password, self.example_user1).split(":")[1], "")
        self.assertEqual(self.server_adapter.get_user(self.admin, self.admin_password, non_existent_user), "")

        # Fügt 2 Token einem Nutzer hinzu
        self.server_adapter.add_token_to_user(self.admin, self.admin_password, self.example_user1, self.example_token1)
        self.server_adapter.add_token_to_user(self.admin, self.admin_password, self.example_user1, self.example_token2)
        token_list = self.server_adapter.get_all_valid_tokens(self.admin, self.admin_password)
        self.assertTrue(token_list.__contains__(self.example_token1))
        self.assertTrue(token_list.__contains__(self.example_token2))

    def test_delete_token_from_user(self):
        """
        Testet verschiedene Szenarien zum Löschen eines Tokens eines Nutzers.
        """
        # Fügt Nutzer der temporären Datei hinzu
        with open(self.path, "w+") as file:
            file.write(self.admin_string + "\n" +
                       self.example_user1_string)

        # Löscht den Token eines Nutzers
        self.server_adapter.delete_token_from_user(self.admin, self.admin_password,
                                                   self.example_user1, self.example_token1)
        self.assertEqual(self.server_adapter.get_user(self.admin, self.admin_password, self.example_user1),
                        self.example_user1_string)

    def test_delete_all_tokens_from_user(self):
        """
        Testet verschiedene Szenarien zum Löschen aller Tokens eines Nutzers.
        """
        # Fügt Nutzer der temporären Datei hinzu
        with open(self.path, "w+") as file:
            file.write(self.admin_string + "\n" +
                       self.example_user1_string + self.example_token1_string + self.example_token2_string)

        # Löscht alle Tokens eines Nutzers
        self.server_adapter.delete_all_tokens_from_user(self.admin, self.admin_password, self.example_user1)
        self.assertEqual(self.server_adapter.get_user(self.admin, self.admin_password, self.example_user1),
                         self.example_user1_string)

    def test_get_user(self):
        """
        Testet das Bekommen der gespeicherten Informationen eines Nutzers.
        """
        # Fügt Nutzer der temporären Datei hinzu
        with open(self.path, "w+") as file:
            file.write(self.admin_string + "\n" +
                       self.example_user1_string + self.example_token1_string)

        # Holt die Informationen eines Nutzers
        self.assertEqual(self.server_adapter.get_user(self.admin, self.admin_password, self.example_user1),
                         self.example_user1_string + self.example_token1_string)

    def test_get_all_valid_tokens(self):
        """
        Testet das Bekommen der Liste aller gespeicherten Tokens aller Nutzer.
        """
        # Fügt Nutzer der temporären Datei hinzu
        with open(self.path, "w+") as file:
            file.write(self.admin_string + "\n" +
                       self.example_user1_string + self.example_token1_string + "\n" +
                       self.example_user2_string + self.example_token2_string)

        # Holt die Liste aller Tokens
        token_list = self.server_adapter.get_all_valid_tokens(self.admin, self.admin_password)
        self.assertTrue(token_list.__contains__(self.example_token1))
        self.assertTrue(token_list.__contains__(self.example_token2))

