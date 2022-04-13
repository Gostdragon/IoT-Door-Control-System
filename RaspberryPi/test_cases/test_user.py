import sys

sys.path.append('/home/pi/src-Building-Security-System')
import unittest

from RaspberryPi.src.data_model.user import User, AuthenticatedUser, UnauthenticatedUser
from RaspberryPi.src.data_model.name import FirstName, LastName, Name
from RaspberryPi.src.data_model.key_token import AuthorizedNFCToken, UnauthorizedNFCToken
from RaspberryPi.src.data_model.password import Password
from RaspberryPi.src.data_model.identifier import Identifier

"""
Dieses Modul testet die Funktionalität der Klasse :class:`~user.User` 
und ihrer Unterklassen mithilfe von Unittests.

Classes:
    TestUser: Repräsentiert eine Testklasse, welche die Methoden der Klasse
              :class:`~user.User` und die ihrer Unterklassen :class:`~user.AuthenticatedUser`
              und :class:`~user.UnauthenticatedUser` testet.

@author Ahmad Eynawi
@version 03.03.2022
"""


class TestUser(unittest.TestCase):

    def setUp(self) -> None:
        self.__authenticatedUser = AuthenticatedUser(Name(FirstName("Albert"), LastName("Einstein")),
                                                     Identifier("123"), Password("abc123"))
        self.__unauthenticatedUser = UnauthenticatedUser(Name(FirstName("Isaac"), LastName("Newton")),
                                                         Identifier("456"))
        self.__authorizedToken = AuthorizedNFCToken(Identifier("1122"))
        self.__unauthorizedToken = UnauthorizedNFCToken(Identifier("3344"))

    def tearDown(self) -> None:
        self.__authenticatedUser.clearTokens()
        self.__unauthenticatedUser.clearTokens()

    def test_init(self):
        self.assertIsInstance(self.__authenticatedUser, User)
        self.assertIsInstance(self.__authenticatedUser, AuthenticatedUser)

        self.assertIsInstance(self.__unauthenticatedUser, User)
        self.assertIsInstance(self.__unauthenticatedUser, UnauthenticatedUser)

    def test_equals(self):
        self.assertFalse(self.__authenticatedUser.__eq__(self.__unauthenticatedUser))

        secondAuthenticatedUser = AuthenticatedUser(Name(FirstName("Albert"), LastName("Einstein")),
                                                    Identifier("123"), Password("abc123"))
        self.assertTrue(self.__authenticatedUser.__eq__(secondAuthenticatedUser))
        thirdAuthenticatedUser = AuthenticatedUser(Name(FirstName("Bassel"), LastName("Safadi")),
                                                   Identifier("7788"), Password("abc123"))
        self.assertFalse(self.__authenticatedUser.__eq__(thirdAuthenticatedUser))

        secondUnauthenticatedUser = UnauthenticatedUser(Name(FirstName("Isaac"), LastName("Newton")),
                                                        Identifier("456"))
        self.assertTrue(self.__unauthenticatedUser.__eq__(secondUnauthenticatedUser))
        thirdUnauthenticatedUser = UnauthenticatedUser(Name(FirstName("Bill"), LastName("Gates")),
                                                       Identifier("123"))
        self.assertFalse(self.__unauthenticatedUser.__eq__(thirdUnauthenticatedUser))

        self.assertFalse(self.__authenticatedUser.__eq__(secondUnauthenticatedUser))
        self.assertFalse(self.__authenticatedUser.__eq__(thirdUnauthenticatedUser))

    def test_addToken(self):
        self.__authenticatedUser.addToken(self.__authorizedToken)
        self.assertIn(self.__authorizedToken, self.__authenticatedUser.tokens)

        self.__unauthenticatedUser.addToken(self.__unauthorizedToken)
        self.assertIn(self.__unauthorizedToken, self.__unauthenticatedUser.tokens)

    def test_deleteToken(self):
        self.__authenticatedUser.addToken(self.__authorizedToken)
        self.assertIn(self.__authorizedToken, self.__authenticatedUser.tokens)
        self.__authenticatedUser.deleteToken(self.__authorizedToken)
        self.assertNotIn(self.__authorizedToken, self.__authenticatedUser.tokens)

        self.__unauthenticatedUser.addToken(self.__unauthorizedToken)
        self.assertIn(self.__unauthorizedToken, self.__unauthenticatedUser.tokens)
        self.__unauthenticatedUser.deleteToken(self.__unauthorizedToken)
        self.assertNotIn(self.__unauthorizedToken, self.__unauthenticatedUser.tokens)

    def test_hasToken(self):
        self.__authenticatedUser.addToken(self.__authorizedToken)
        self.__authenticatedUser.hasToken(self.__authorizedToken)
        self.assertIn(self.__authorizedToken, self.__authenticatedUser.tokens)

        self.__unauthenticatedUser.addToken(self.__unauthorizedToken)
        self.__unauthenticatedUser.hasToken(self.__unauthorizedToken)
        self.assertIn(self.__unauthorizedToken, self.__unauthenticatedUser.tokens)

    def test_clearTokens(self):
        self.assertTrue(self.__authenticatedUser.addToken(self.__authorizedToken))
        self.assertTrue(self.__authenticatedUser.addToken(self.__unauthorizedToken))
        self.assertEqual(self.__authenticatedUser.tokens.__len__(), 2)
        self.__authenticatedUser.clearTokens()
        self.assertEqual(self.__authenticatedUser.tokens.__len__(), 0)
