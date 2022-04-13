import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest
from RaspberryPi.src.data_model.key_token import Token, NFCToken, AuthorizedNFCToken, UnauthorizedNFCToken
from RaspberryPi.src.data_model.identifier import Identifier

"""
Dieses Modul testet die Funktionalität der Klasse :class:`~key_token.Token` 
und ihrer Unterklassen mithilfe von Unittests.

Classes:
    TestKeyToken: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                  :class:`~key_token.Token` und die ihrer Unterklassen :class:`~key_token.NFCToken`,
                  :class:`~key_token.AuthorizedNFCToken` und :class:`~key_token.UnauthorizedNFCToken` 
                  testet.

@author Ahmad Eynawi
@version 03.03.2022
"""


class TestKeyToken(unittest.TestCase):

    def setUp(self) -> None:
        self.__authorizedNFCToken = AuthorizedNFCToken(Identifier("12345"))
        self.__unauthorizedNFCToken = UnauthorizedNFCToken(Identifier("12345"))

    def test_init(self):
        self.assertIsInstance(self.__authorizedNFCToken, Token)
        self.assertIsInstance(self.__authorizedNFCToken, NFCToken)
        self.assertIsInstance(self.__authorizedNFCToken, AuthorizedNFCToken)
        self.assertNotIsInstance(self.__authorizedNFCToken, UnauthorizedNFCToken)

        self.assertIsInstance(self.__unauthorizedNFCToken, Token)
        self.assertIsInstance(self.__unauthorizedNFCToken, NFCToken)
        self.assertIsInstance(self.__unauthorizedNFCToken, UnauthorizedNFCToken)
        self.assertNotIsInstance(self.__unauthorizedNFCToken, AuthorizedNFCToken)

    def test_equals(self):
        self.assertTrue(self.__authorizedNFCToken.__eq__(self.__unauthorizedNFCToken))
        self.assertEqual(self.__authorizedNFCToken, self.__unauthorizedNFCToken)

        self.__authorizedNFCToken = AuthorizedNFCToken(Identifier("67890"))

        self.assertFalse(self.__authorizedNFCToken.__eq__(self.__unauthorizedNFCToken))
        self.assertNotEqual(self.__authorizedNFCToken, self.__unauthorizedNFCToken)
