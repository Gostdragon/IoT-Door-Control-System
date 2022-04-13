import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest

from RaspberryPi.src.data_model.door import DoorDataStorage
from RaspberryPi.src.data_model.identifier import Identifier
from RaspberryPi.src.data_model.key_token import AuthorizedNFCToken, UnauthorizedNFCToken

"""
Dieses Modul testet die Funktionalität der Klasse :class:`~door.DoorDataStorage` 
mithilfe von Unittests.

Classes:
    TestDoorDataStorage: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                         :class:`~door.DoorDataStorage` testet.
                         
@author Ahmad Eynawi
@version 03.03.2022
"""


class TestDoorDataStorage(unittest.TestCase):

    def setUp(self) -> None:
        self.__doorDataStorage = DoorDataStorage()
        self.__authorizedNFCToken = AuthorizedNFCToken(Identifier("12345"))
        self.__unauthorizedNFCToken = UnauthorizedNFCToken(Identifier("67890"))

    def tearDown(self) -> None:
        self.__doorDataStorage.clear()

    def test_init(self):
        self.assertIsInstance(self.__doorDataStorage, DoorDataStorage)

    def test_addToken(self):
        self.assertTrue(self.__doorDataStorage.addToken(self.__authorizedNFCToken))
        self.assertTrue(self.__doorDataStorage.addToken(self.__unauthorizedNFCToken))

        self.assertIn(self.__authorizedNFCToken, self.__doorDataStorage.doorTokens)
        self.assertIn(self.__unauthorizedNFCToken, self.__doorDataStorage.doorTokens)

    def test_deleteToken(self):
        self.assertTrue(self.__doorDataStorage.addToken(self.__authorizedNFCToken))
        self.assertTrue(self.__doorDataStorage.addToken(self.__unauthorizedNFCToken))

        self.assertTrue(self.__doorDataStorage.deleteToken(self.__authorizedNFCToken))
        self.assertTrue(self.__doorDataStorage.deleteToken(self.__unauthorizedNFCToken))

        self.assertNotIn(self.__authorizedNFCToken, self.__doorDataStorage.doorTokens)
        self.assertNotIn(self.__unauthorizedNFCToken, self.__doorDataStorage.doorTokens)

    def test_hasToken(self):
        self.assertTrue(self.__doorDataStorage.addToken(self.__authorizedNFCToken))
        self.assertTrue(self.__doorDataStorage.addToken(self.__unauthorizedNFCToken))

        self.assertTrue(self.__doorDataStorage.hasToken(self.__authorizedNFCToken))
        self.assertTrue(self.__doorDataStorage.hasToken(self.__unauthorizedNFCToken))

    def test_equals(self):
        self.assertFalse(self.__doorDataStorage.__eq__(DoorDataStorage()))

    def test_clear(self):
        self.assertTrue(self.__doorDataStorage.addToken(self.__authorizedNFCToken))
        self.assertTrue(self.__doorDataStorage.addToken(self.__unauthorizedNFCToken))
        self.assertEqual(self.__doorDataStorage.doorTokens.__len__(), 2)

        self.__doorDataStorage.clear()

        self.assertEqual(self.__doorDataStorage.doorTokens.__len__(), 0)
