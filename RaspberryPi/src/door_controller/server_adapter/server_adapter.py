"""
Dieses Modul dient als Grundgerüst für alle Adapter Klassen.
Es enthält alle für das Programm relevanten Klassen und Methoden, die ein Adapter implementieren muss.
Classes:
    ServerAdapter(ABC): Diese abtsrakte Klasse gibt alle relevanten
        Methoden für einen Adapter als abstrakte Methoden vor.
@author Lukas Wittenzellner
@version 1.0
"""

from abc import abstractmethod, ABC
from RaspberryPi.src.data_model.user import UnauthenticatedUser, AuthenticatedUser
from RaspberryPi.src.data_model.key_token import Token
from RaspberryPi.src.data_model.password import Password


class ServerAdapter(ABC):
    """
    Diese abstrakte Klasse gibt alle relevanten Methoden für einen Adapter als abstrakte Methoden vor.
    Methods:
        add_token_to_user: Fügt einem Nutzer einen Token hinzu.
        delete_token_from_user: Löscht einen Token von einem Nutzer.
        delete_all_tokens_from_user: Löscht alle Tokens eines Nutzers.
        get_user: Gibt die Daten eines Nutzers zurück.
        get_all_valid_tokens: Gibt eine Liste aller validen Token zurück.
    """
    @abstractmethod
    def add_token_to_user(self, admin: UnauthenticatedUser, password: Password, user: UnauthenticatedUser,
                          token: Token):
        """
        Fügt einem Nutzer einen Token hinzu.
        :param admin: Ist der Nutzer, der diese Methode durchführen möchte.
        :type admin: UnauthenticatedUser.
        :param password: Ist das Passwort des Nutzers, der diese Operation durchführen möchte.
        :type password: Password.
        :param user: Ist der Nutzer, dem ein Token hinzugefügt werden soll.
        :type user: UnauthenticatedUser.
        :param token: Ist der Token, der dem Nutzer hinzugefügt werden soll.
        :type token: Token.
        """
        pass

    @abstractmethod
    def delete_token_from_user(self, admin: UnauthenticatedUser, password: Password, user: UnauthenticatedUser,
                               token: Token):
        """
        Löscht einen Token von einem Nutzer.
        :param admin: Ist der Nutzer, der diese Methode durchführen möchte.
        :type admin: UnauthenticatedUser.
        :param password: Ist das Passwort des Nutzers, der diese Operation durchführen möchte.
        :type password: Password.
        :param user: Ist der Nutzer, von dem ein Token geläscht werden soll.
        :type user: UnauthenticatedUser.
        :param token: Ist der Token, der gelöscht werden soll.
        :type token: Token.
        """
        pass

    @abstractmethod
    def delete_all_tokens_from_user(self, admin: UnauthenticatedUser, password: Password, user: UnauthenticatedUser):
        """
        Löscht alle Tokens eines Nutzers.

        :param admin: Ist der Nutzer, der diese Methode durchführen möchte.
        :type admin: UnauthenticatedUser
        :param password: Ist das Passwort des Nutzers, der diese Operation durchführen möchte.
        :type password: Password.
        :param user: Ist der Nutzer, von dem alle Token gelöscht werden sollen.
        :type user: UnauthenticatedUser.
        """
        pass

    @abstractmethod
    def get_user(self, admin: UnauthenticatedUser, password: Password, user: UnauthenticatedUser):
        """
        Gibt die Daten eines Nutzers zurück.

        :param admin: Ist der Nutzer, der diese Methode durchführen möchte.
        :type admin: UnauthenticatedUser.
        :param password: Ist das Passwort des Nutzers, der diese Operation durchführen möchte.
        :type password: Password.
        :param user: Ist der Nutzer, dessen Daten zurückgegeben werden sollen.
        :type user: UnauthenticatedUser.
        :return: Den Nutzer und dessen Daten.
        """
        pass

    @abstractmethod
    def get_all_valid_tokens(self, admin: UnauthenticatedUser, password: Password):
        """
        Gibt eine Liste aller validen Token zurück.

        :param admin: Ist der Nutzer, der diese Methode durchführen möchte.
        :type admin: UnauthenticatedUser.
        :param password: Ist das Passwort des Nutzers, der diese Operation durchführen möchte.
        :type password: Password.
        :return: Liste aller validen Tokens.
        :rtype: Liste von Tokens.
        """
        pass
