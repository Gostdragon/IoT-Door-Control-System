import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest
import hashlib

from RaspberryPi.src.door_controller.door_control_handler.token_validation import TokenValidation
from RaspberryPi.src.data_model.door import DoorDataStorage
from RaspberryPi.src.data_model.key_token import AuthorizedNFCToken
from RaspberryPi.src.data_model.identifier import Identifier

"""
Dieses Modul testet die Funktionalität der Klasse :class:`~token_validation.TokenValidation` 
mithilfe von Unittests.

Classes:
    TestTokenValidation: Repräsentiert eine Testklasse, welche die Methoden der Klasse
                         :class:`~token_validation.TokenValidation` testet.

@author Ahmad Eynawi
@version 03.03.2022
"""


class TestTokenValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.__tokenValidation = TokenValidation(DoorDataStorage([AuthorizedNFCToken(Identifier("123")),
                                                                  AuthorizedNFCToken(Identifier("456"))]))

    def test_init(self):
        self.assertIsInstance(self.__tokenValidation, TokenValidation)

    def test_validateToken(self):
        self.assertTrue(self.__tokenValidation.validateToken(AuthorizedNFCToken(Identifier("123"))))
        self.assertFalse(self.__tokenValidation.validateToken(AuthorizedNFCToken(Identifier("789"))))

        firstEncryptedToken = AuthorizedNFCToken(Identifier(hashlib.sha256(hex(int("1122")).encode()).hexdigest()))
        secondEncryptedToken = AuthorizedNFCToken(Identifier(hashlib.sha256(hex(int("3344")).encode()).hexdigest()))

        self.__tokenValidation.doorDataStorage.addToken(firstEncryptedToken)
        self.assertTrue(self.__tokenValidation.validateToken(firstEncryptedToken))
        self.assertFalse(self.__tokenValidation.validateToken(secondEncryptedToken))
