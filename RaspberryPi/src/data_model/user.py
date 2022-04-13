from abc import ABC, abstractmethod

from RaspberryPi.src.data_model.name import Name
from RaspberryPi.src.data_model.identifier import Identifier
from RaspberryPi.src.data_model.key_token import Token
from RaspberryPi.src.data_model.password import Password


"""
Dieses Modul kapselt alle Klassen, die für die Modellierung von Nutzern
im Türsteuerungssystem zuständig sind.
Nutzer sind in diesem Zusammenhang alle Personen, welche die durch das Steuerungssystem 
gesteuerte Tür benutzen.

Classes:
    User: Repräsentiert einen generischen Nutzer mit einem Namen, einem Identifikator 
          und einer eventuell leeren Token-Liste (abstrakte Klasse).
    AuthenticatedUser: Repräsentiert einen authentifizierten Nutzer, der neben
                       einem Namen und einem Identifikator ein Passwort 
                       zur Authentifizierung besitzt.
    UnauthenticatedUser: Repräsentiert einen unauthentifizierten Nutzer mit einem Namen und
                         einem Identifikator aber ohne Passwort.

@author Ahmad Eynawi
@version 26.01.2022
"""


class User(ABC):
    """
    Diese abstrakte Klasse modelliert einen generischen Nutzer.
    Nutzer sind in diesem Kontext alle Personen, welche die gesteuerte Tür
    mit registrierten NFC-Tokens oder über die Webseite zur Türsteuerung öffnen können.

    Attributes:
        name (:class:`~name.Name`): Der vollständige Name (bestehend aus dem Vor- und Nachnamen)
                                    des Nutzers.
        identifier (:class:`~identifier.Identifier`): Der eindeutige Identifikator des Nutzers.
        tokens (list): Die Liste der Tokens, die sich aktuell im Besitz dieses Nutzers befinden.

    Methods:
        name: Gibt den Namen (bestehend aus dem Vor- und Nachnamen) des Nutzers zurück.
        identifier: Gibt den Identifikator dieses Nutzers zurück.
        tokens (Getter): Gibt die Token-Liste dieses Nutzers zurück.
        tokens (Setter): Fügt die gegebene Liste von Tokens zu diesem Nutzer hinzu.
        addToken: Fügt einen neuen Token zur Liste der mit diesem Nutzer assoziierten Tokens hinzu.
        deleteToken: Entfernt einen Token aus der Liste der mit diesem Nutzer assoziierten Tokens.
        hasToken: Prüft, ob der gegebene Schlüsseltoken sich aktuell im Besitz dieses Nutzers befindet.
        clear: Entfernt alle Tokens, die dieser Nutzer aktuell besitzt.
        __init__: Konstruktor der Klasse :class:`~user.User`
    """

    @abstractmethod
    def __init__(self, name: Name, identifier: Identifier, tokens=[]):
        """
        Konstruktor der Klasse :class:`~user.User`.

        @param name: Der vollständige Name (bestehend aus dem Vor- und Nachnamen) des Nutzers.
        @type name: :class:`~name.Name`
        @param identifier: Der Identifikator, der für die eindeutige Identifizierung dieses Nutzers
                           im Türsteuerungssystem verwendet wird.
        @type identifier: :class:`~identifier.Identifier`
        @param tokens: Die Liste der mit diesem Nutzer bereits assoziierten Tokens.
                       Wird hierfür kein Argument übergeben, wird das entsprechende Attribut
                       defaultmäßig mit einer neuen leeren Liste initialisiert.
        @type tokens: list
        """
        self._name = name
        self._identifier = identifier
        self._tokens = tokens

    @property
    def name(self):
        """
        Gibt den Namen (bestehend aus dem Vor- und Nachnamen) des Nutzers zurück.

        @return: Den vollständigen Namen dieses Nutzers.
        @rtype: :class:`~name.Name`
        """
        return self._name

    @property
    def identifier(self):
        """
        Gibt den eindeutigen Identifikator des Nutzers als Identifier-Objekt zurück.

        @return: Den Identifikator dieses Nutzers.
        @rtype: :class:`~identifier.Identifier`
        """
        return self._identifier

    @property
    def tokens(self):
        """
        Gibt eine unveränderliche Referenz auf die Liste, welche die mit diesem Nutzer assoziierten
        Schlüsseltokens speichert.

        @return: Die Token-Liste dieses Nutzers als unveränderliches Tupel.
        @rtype: tuple
        """
        return tuple(self._tokens)

    @tokens.setter
    def tokens(self, tokens: list):
        """
        Set-Methode für die Schlüsseltokens, die zum Besitz dieses Nutzers hinzugefügt
        werden sollen.

        @param tokens: Die Schlüsseltokens, die mit diesem Nutzer assoziiert werden sollen.
        @type tokens: list
        """
        self._tokens = list(tokens)

    def addToken(self, token: Token):
        """
        Fügt einen Schlüsseltoken zur Token-Liste dieses Nutzers hinzu.
        Ein Nutzer kann also mehr als einen Token besitzen.

        Ist der als Parameter übergebene Token bereits in der Liste der mit
        diesem Nutzer assoziierten Tokens enthalten, wird er nicht hinzugefügt und
        es wird `False` zurückgegeben; andernfalls wird `True` zurückgegeben.

        @param token: Der Schlüsseltoken, der zur Token-Liste dieses Nutzers hinzugefügt werden soll.
        @type token: :class:`~token.Token`
        @return: `True`, wenn der als Parameter übergebene Token nicht bereits mit dem Nutzer assoziiert ist
                 und somit erfolgreich zur Token-Liste hinzugefügt wurde; andernfalls `False`.
        @rtype: bool
        """
        if not self._tokens.__contains__(token):
            self._tokens.append(token)
            return True
        else:
            return False

    def deleteToken(self, token: Token):
        """
        Entfernt einen Schlüsseltoken aus der Token-Liste dieses Nutzers.

        Ist der als Parameter übergebene Token nicht in der Liste der mit diesem Nutzer assoziierten Tokens enthalten,
        wird die Token-Liste nicht verändert und es wird `False` zurückgegeben; andernfalls wird `True` zurückgegeben.

        @param token: Der Schlüsseltoken, der aus der Liste der mit diesem Nutzer
                      assoziierten Tokens entfernt werden soll.
        @type token: :class:`~token.Token`
        @return: `True`, wenn der als Parameter übergebene Token bereits mit diesem Nutzer assoziiert war
                 und somit erfolgreich aus der Token-Liste entfernt wurde; andernfalls `False`.
        @rtype: bool
        """
        if self._tokens.__contains__(token):
            self._tokens.remove(token)
            return True
        else:
            return False

    def hasToken(self, keyToken: Token):
        """
        Gibt `True` zurück, wenn dieser Nutzer den als Parameter übergebenen
        Token aktuell besitzt; andernfalls wird `False` zurückgegeben.

        @param keyToken: Der Schlüsseltoken, dessen Zugehörigkeit zu diesem Nutzer
                         geprüft werden soll.
        @type keyToken: :class:`~token.Token`
        @return: `True`, wenn der gegebene Schlüsseltoken sich im Besitz dieses Nutzers befindet,
                 andernfalls `False`.
        @rtype: bool
        """
        return self._tokens.__contains__(keyToken)

    def clearTokens(self):
        """
        Entfernt alle Tokens, die sich aktuell im Besitz dieses Nutzers befinden.
        """
        self._tokens.clear()


class AuthenticatedUser(User):
    """
    Diese Klasse modelliert einen authentifizierten Nutzer.
    Ein authentifizierter Nutzer ist in diesem Kontext eine Person, die neben einem Namen,
    einem eindeutigen Identifikator und (mindestens) einem Schlüsseltoken ein Passwort
    zur Authentifizierung und Anmeldung in der Admin-App zur Tokenverwaltung besitzt.

    Attributes:
        name (:class:`~name.Name`): Der vollständige Name (bestehend aus dem Vor- und Nachnamen)
                                    des authentifizierten Nutzers.
        identifier (:class:`~identifier.Identifier`): Der eindeutige Identifikator des authentifizierten Nutzers.
        tokens (list): Die Liste der Tokens, die sich aktuell im Besitz dieses
                       authentifizierten Nutzers befinden.

    Methods:
        password: Gibt das Admin-App-Password dieses authentifizierten Nutzers zurück.
        __init__: Konstruktor der Klasse :class:`~user.AuthenticatedUser`.
        __repr__: Gibt eine String-Repräsentation für dieses AuthenticatedUser-Objekt zurück.
        __eq__: Vergleicht dieses AuthenticatedUser-Objekt mit einem anderen Objekt.
        __hash__: Berechnet einen Hashwert für dieses AuthenticatedUser-Objekt.
    """

    def __init__(self, name: Name, identifier: Identifier, password: Password, tokens=[]):
        """
        Konstruktor der Klasse :class:`~user.AuthenticatedUser`.

        Erstellt und initialisiert einen neuen authentifizierten Nutzer, der neben
        einem Namen und einem Identifikator ein Passwort zur Authentifizierung und
        Anmeldung in der Admin-App zur Tokenverwaltung besitzt.

        @param name: Der vollständige Name (bestehend aus dem Vor- und Nachnamen)
                     des authentifizierten Nutzers.
        @type name: :class:`~name.Name`
        @param identifier: Der eindeutige Identifikator des authentifizierten Nutzers.
        @type identifier: :class:`~identifier.Identifier`
        @param password: Das Passwort, mit dem sich der authentifizierte Nutzer in
                         der Admin-App für die Tokenverwaltung anmelden kann.
        @type password: :class:`~password.Password`.
        @param tokens: Die Liste der mit diesem authentifizierten Nutzer bereits assoziierten Tokens.
                       Wird hierfür kein Argument übergeben, wird das entsprechende Attribut
                       defaultmäßig mit einer neuen leeren Liste initialisiert.
        @type tokens: list
        """
        super().__init__(name, identifier, tokens)
        self.__password = password

    @property
    def password(self):
        """
        Gibt das aktuelle Passwort des authentifizierten Nutzers zurück.

        @return: Das Passwort für die Anmeldung in der Admin-App zur Tokenverwaltung.
        @rtype: :class:`~password.Password`.
        """
        return self.__password

    def __repr__(self):
        """
        Erzeugt eine textuelle Darstellung für dieses AuthenticatedUser-Objekt und gibt diese
        Darstellung als String zurück.

        @return: Die String-Repräsentation dieses AuthenticatedUser-Objekts.
        @rtype: str
        """
        return f"{self.__class__.__name__}(Name: {self._name}, Identifier: {self._identifier}, Tokens: {self._tokens})"

    def __eq__(self, other: object):
        """
        Vergleicht dieses AuthenticatedUser-Objekt mit dem Objekt `other`.

        Zwei AuthenticatedUser-Objekte werden als gleich betrachtet, wenn beide Nutzer
        den gleichen Identifikator haben.

        @param other: Das Objekt, das mit diesem AuthenticatedUser-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn das Objekt `other` auch eine Instanz der Klasse
        :class:`~user.AuthenticatedUser` ist und die beiden Objekte im oben genannten Sinne
        gleich sind; andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return isinstance(other, self.__class__) and self.identifier == other.identifier

    def __hash__(self):
        """
        Gibt einen Hashwert für dieses AuthenticatedUser-Objekt zurück.

        Der Hashwert wird anhand des in diesem AuthenticatedUser-Objekt gespeicherten
        Identifikators, des vollständigen Namen und des Passwortes berechnet.

        @return: Den für dieses AuthenticatedUser-Objekt berechneten Hashwert.
        @rtype: int
        """
        return hash((self.name, self.identifier, self.password))


class UnauthenticatedUser(User):
    """
    Diese Klasse modelliert einen nicht authentifizierten Nutzer.
    Ein nicht authentifizierter Nutzer unterscheidet sich von einem authentifizierten Nutzer
    in diesem Kontext dahingehend, dass der unauthentifizierte Nutzer kein Passwort
    zur Authentifizierung bzw. zur Anmeldung in der Admin-App für die Tokenverwaltung besitzt.

    Attributes:
        name (:class:`~name.Name`): Der vollständige Name (bestehend aus dem Vor- und Nachnamen)
                                    des unauthentifizierten Nutzers.
        identifier (:class:`~identifier.Identifier`): Der eindeutige Identifikator des unauthentifizierten Nutzers.
        tokens (list): Die Liste der Tokens, die sich aktuell im Besitz dieses
                       unauthentifizierten Nutzers befinden.

    Methods:
        __init__: Konstruktor der Klasse :class:`~user.UnauthenticatedUser`.
        __repr__: Gibt eine String-Repräsentation für dieses UnauthenticatedUser-Objekt zurück.
        __eq__: Vergleicht dieses UnauthenticatedUser-Objekt mit einem anderen Objekt.
        __hash__: Berechnet einen Hashwert für dieses UnauthenticatedUser-Objekt.
    """

    def __init__(self, name: Name, identifier: Identifier, tokens=[]):
        """
        Konstruktor der Klasse :class:`~user.UnauthenticatedUser`.

        Erstellt und initialisiert einen neuen unauthentifizierten Nutzer mit einem Namen
        und einem Identifikator aber ohne Passwort.

        @param name: Der vollständige Name (bestehend aus dem Vor- und Nachnamen)
                     des unauthentifizierten Nutzers.
        @type name: :class:`~name.Name`
        @param identifier: Der eindeutige Identifikator des unauthentifizierten Nutzers.
        @type identifier: :class:`~identifier.Identifier`
        @param tokens: Die Liste der mit diesem unauthentifizierten Nutzer bereits assoziierten Tokens.
                       Wird hierfür kein Argument übergeben, wird das entsprechende Attribut
                       defaultmäßig mit einer neuen leeren Liste initialisiert.
        @type tokens: list
        """
        super().__init__(name, identifier, tokens)

    def __repr__(self):
        """
        Erzeugt eine textuelle Darstellung für dieses UnauthenticatedUser-Objekt und gibt diese
        Darstellung als String zurück.

        @return: Die String-Repräsentation dieses UnauthenticatedUser-Objekts.
        @rtype: str
        """
        return f"{self.__class__.__name__}(Name: {self._name}, Identifier: {self._identifier}, Tokens: {self._tokens})"

    def __eq__(self, other: object):
        """
        Vergleicht dieses UnauthenticatedUser-Objekt mit dem Objekt `other`.

        Zwei UnauthenticatedUser-Objekte werden als gleich betrachtet, wenn beide Nutzer
        den gleichen Identifikator haben.

        @param other: Das Objekt, das mit diesem UnauthenticatedUser-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn das Objekt `other` auch eine Instanz der Klasse
        :class:`~user.UnauthenticatedUser` ist und die beiden Objekte im oben genannten Sinne
        gleich sind; andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return isinstance(other, self.__class__) and self.identifier == other.identifier

    def __hash__(self):
        """
        Gibt einen Hashwert für dieses UnauthenticatedUser-Objekt zurück.

        Der Hashwert wird anhand des in diesem UnauthenticatedUser-Objekt gespeicherten
        Identifikators und des vollständigen Namen des Nutzers berechnet.

        @return: Den für dieses UnauthenticatedUser-Objekt berechneten Hashwert.
        @rtype: int
        """
        return hash((self.name, self.identifier))

