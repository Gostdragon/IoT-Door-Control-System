import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest
from RaspberryPi.src.data_model.key_token import BotIDToken, BotChannelToken, Token
from RaspberryPi.src.data_model.identifier import Identifier

"""
Dieses Modul testet die Funktionalität der Klassen :class:`~key_token.BotIDToken`, :class:`~key_token.BotChannelToken`
mithilfe von Unittests.

Classes:
    TestBotToken: Repräsentiert eine Testklasse, welche die Methoden der Klassen
                  :class:`~key_token.BotIDToken`, :class:`~key_token.BotChannelToken` testet.

@author Fabian Schiekel
@version 11.03.2022
"""


class TestBotToken(unittest.TestCase):

    def setUp(self) -> None:
        self.__botToken = BotIDToken(Identifier("12345"))

        self.__channelToken = BotChannelToken(Identifier("56789"))

    def test_init(self):
        self.assertIsInstance(self.__botToken, Token)
        self.assertIsInstance(self.__botToken, BotIDToken)
        self.assertNotIsInstance(self.__botToken, BotChannelToken)

        self.assertIsInstance(self.__channelToken, Token)
        self.assertIsInstance(self.__channelToken, BotChannelToken)
        self.assertNotIsInstance(self.__channelToken, BotIDToken)

    def test_equals(self):
        self.assertTrue(self.__botToken.__eq__(BotIDToken(Identifier("12345"))))
        self.assertTrue(self.__channelToken.__eq__(BotChannelToken(Identifier("56789"))))

        self.assertFalse(self.__botToken.__eq__(self.__channelToken))
        self.assertFalse(self.__botToken.__eq__(BotChannelToken(Identifier("12345"))))
