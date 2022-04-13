from RaspberryPi.src.data_model.identifier import Identifier
from RaspberryPi.src.data_model.key_token import Token

"""
Dieses Modul kapselt alle Klassen, die für die Speicherung und Verwaltung der Daten der
durch dieses Software-System gesteuerten Türen zuständig sind.

Classes: 
    DoorDataStorage: Repräsentiert den Datenspeicher für eine ferngesteuerte Tür. 

@author Ahmad Eynawi
@version 17.02.2022
"""


class DoorDataStorage:
    """
    Diese Klasse repräsentiert einen Datenspeicher für eine ferngesteuerte Tür.

    Dieser Datenspeicher speichert den eindeutigen Identifikator der Tür
    sowie die Liste der mit dieser Tür assoziierten Tokens.

    Attributes:
        doorIdentifier (Identifier): Der eindeutige Identifikator der ferngesteuerten Tür.
        doorTokens (list): Die Liste der mit dieser Tür assoziierten Schlüsseltokens.

    Methods:
        doorIdentifier (Getter): Gibt den eindeutigen Identifikator der Tür,
                        deren Daten in diesem :class:`~door.DoorDataStorage` gespeichert sind, zurück.
        doorTokens (Getter): Gibt die mit dieser Tür assoziierten Schlüsseltokens als Tupel zurück.
        doorTokens (Setter): Set-Methode für die Schlüsseltokens, die zum Datenspeicher dieser Tür
                             hinzugefügt werden sollen.
        addToken: Fügt einen Token zur Liste der mit dieser Tür assoziierten Tokens hinzu
                  (sofern dieser Token nicht bereits in der Liste enthalten ist).
        deleteToken: Entfernt einen Token aus der Liste der mit dieser Tür assoziierten Tokens
                     (sofern dieser Token bereits in der Liste enthalten ist).
        hasToken: Prüft, ob der gegebene Schlüsseltoken in diesem Datenspeicher bereits
                  gespeichert ist.
        clear: Entfernt alle Tokens, die in diesem Tür-Datenspeicher gespeichert sind.
        __init__: Konstruktor der Klasse :class:`~door.DoorDataStorage`
        __repr__: Gibt eine String-Repräsentation für dieses DoorDataStorage-Objekt zurück.
        __eq__: Vergleicht dieses DoorDataStorage-Objekt mit einem anderen Objekt.
        __hash__: Berechnet einen Hashwert für dieses DoorDataStorage-Objekt.
    """
    __identifier = 1

    def __init__(self, doorTokens=[]):
        """
        Konstruktor der Klasse :class:`~door.DoorDataStorage`.

        Erstellt und initialisiert einen Datenspeicher für eine bestimmte Tür. Dieser Datenspeicher speichert
        den eindeutigen Tür-Identifikator und die Liste der mit dieser Tür assoziierten Schlüsseltokens.

        @param doorTokens: Die Liste der mit dieser Tür bereits assoziierten Tokens.
                           Wird hierfür kein Argument übergeben, wird das entsprechende Attribut
                           defaultmäßig mit einer neuen leeren Liste initialisiert.
        @type doorTokens: list
        """
        self.__doorIdentifier = Identifier(str(DoorDataStorage.__identifier))
        DoorDataStorage.__identifier += 1
        self.__doorTokens = doorTokens

    @property
    def doorIdentifier(self):
        """
        Get-Methode für den Tür-Identifikator.

        @return: Den eindeutigen Identifikator der Tür,
                 deren Daten in diesem :class:`~door.DoorDataStorage` gespeichert sind.
        @rtype: :class:`~identifier.Identifier`
        """
        return self.__doorIdentifier

    @property
    def doorTokens(self):
        """
        Get-Methode für die mit dieser Tür assoziierten Schlüsseltokens.

        Diese Methode gibt eine unveränderliche Referenz (Tupel) auf die Liste der in diesem
        DoorDataStorage-Objekt gespeicherten Tokens.

        @return: Die Schlüsseltokens der Tür, deren Daten in diesem Datenspeicher gespeichert sind.
        @rtype: tuple
        """
        return tuple(self.__doorTokens)

    @doorTokens.setter
    def doorTokens(self, doorTokens: list):
        """
        Set-Methode für die Schlüsseltokens, die zum Datenspeicher dieser Tür hinzugefügt
        werden sollen.

        @param doorTokens: Die Schlüsseltokens, die mit dieser Tür assoziiert werden sollen.
        @type doorTokens: list
        """
        self.__doorTokens = list(doorTokens)

    def addToken(self, token: Token):
        """
        Fügt einen Schlüsseltoken zum Datenspeicher dieser Tür hinzu.

        Ist der als Parameter übergebene Token bereits in der Liste der mit dieser Tür assoziierten Tokens enthalten,
        wird er nicht hinzugefügt und es wird `False` zurückgegeben; andernfalls wird `True` zurückgegeben.

        @param token: Der Schlüsseltoken, der zu dieser Tür hinzugefügt werden soll.
        @type token: :class:`~token.Token`
        @return: `True`, wenn der als Parameter übergebene Token nicht bereits mit der Tür assoziiert ist
                 und somit erfolgreich zur Token-Liste hinzugefügt wurde; andernfalls `False`.
        @rtype: bool
        """
        if not self.__doorTokens.__contains__(token):
            self.__doorTokens.append(token)
            return True
        else:
            return False

    def deleteToken(self, token: Token):
        """
        Entfernt einen Schlüsseltoken aus dem Datenspeicher dieser Tür.

        Ist der als Parameter übergebene Token nicht in der Liste der mit dieser Tür assoziierten Tokens enthalten,
        wird die Token-Liste nicht verändert und es wird `False` zurückgegeben; andernfalls wird `True` zurückgegeben.

        @param token: Der Schlüsseltoken, der aus der Liste der mit dieser Tür assoziierten Tokens entfernt werden soll.
        @type token: :class:`~token.Token`
        @return: `True`, wenn der als Parameter übergebene Token bereits mit der Tür assoziiert war
                 und somit erfolgreich aus der Token-Liste entfernt wurde; andernfalls `False`.
        @rtype: bool
        """
        if self.__doorTokens.__contains__(token):
            self.__doorTokens.remove(token)
            return True
        else:
            return False

    def hasToken(self, keyToken: Token):
        """
        Gibt `True` zurück, wenn dieses DoorDataStorage-Objekt den als Parameter übergebenen
        Token aktuell speichert; andernfalls wird `False` zurückgegeben.

        @param keyToken: Der Schlüsseltoken, dessen Exitenz in diesem Datenspeicher
                         geprüft werden soll.
        @type keyToken: :class:`~token.Token`
        @return: `True`, wenn der gegebene Schlüsseltoken in diesem Datenspeicher gespeichert
                 ist, andernfalls `False`.
        @rtype: bool
        """
        return self.__doorTokens.__contains__(keyToken)

    def clear(self):
        """
        Entfernt alle Tokens, die in diesem Datenspeicher gespeichert sind.
        """
        self.__doorTokens.clear()

    def __repr__(self):
        """
        Erzeugt eine textuelle Darstellung für dieses DoorDataStorage-Objekt und gibt diese
        Darstellung als String zurück.

        @return: Die String-Repräsentation dieses DoorDataStorage-Objekts.
        @rtype: str
        """
        return f"{self.__class__.__name__}(Identifier: {self.__doorIdentifier}, Tokens: {self.__doorTokens})"

    def __eq__(self, other: object):
        """
        Vergleicht dieses DoorDataStorage-Objekt mit dem Objekt `other`.

        Zwei DoorDataStorage-Objekte werden als gleich betrachtet, wenn sie den gleichen
        Tür-Identifikator speichern.

        @param other: Das Objekt, das mit diesem DoorDataStorage-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn das other-Objekt `other` auch eine Instanz der Klasse
        :class:`~door.DoorDataStorage` ist und die beiden Objekte im oben genannten Sinne
        gleich sind; andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return isinstance(other, self.__class__) and self.doorIdentifier == other.doorIdentifier

    def __hash__(self):
        """
        Gibt einen Hashwert für dieses DoorDataStorage-Objekt zurück.

        Der Hashwert wird anhand des in diesem DoorDataStorage-Objekt gespeicherten
        Tür-Identifikator berechnet.

        @return: Den für dieses DoorDataStorage-Objekt eindeutigen Hashwert.
        @rtype: int
        """
        return hash(self.doorIdentifier)

