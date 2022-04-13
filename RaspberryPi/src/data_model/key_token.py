from __future__ import annotations
from abc import ABC, abstractmethod
from RaspberryPi.src.data_model.identifier import Identifier

"""
Dieses Modul kapselt alle Klassen, die die verschiedenen Typen von Schlüsseltokens modellieren.
Die hier modellierten Tokens werden im Türsteuerungssystem für das Öffnen der 
elektrisch ansteuerbaren Tür verwendet.

Classes:
    Token: Repräsentiert einen generischen Schlüsseltoken (abstrakte Klasse).
    NFCToken: Repräsentiert einen NFC-Schlüsseltoken (abstrakte Klasse).
    AuthorizedNFCToken: Repräsentiert einen autorisierten NFC-Schlüsseltoken.
    UnauthorizedNFCToken: Repräsentiert einen unautorisierten NFC-Schlüsseltoken.
    BotIDToken. Repräsentiert einen Bot-ID-Token.
    BotChannelToken: Repräsentiert einen Slack-Channel-Token.
    
@author Ahmad Eynawi
@version 30.01.2022

@author Fabian Schiekel
@version 02.03.2022
"""


class Token(ABC):
    """
    Diese abstrakte Klasse modelliert einen Schlüsseltoken, der zur Identifizierung von Nutzern
    durch das im Steuerungssystem integrierte NFC-Lesegerät verwendet wird.

    Attributes:
        identifier (:class:`~identifier.Identifier`): Der eindeutige Identifikator
                                                      dieses Schlüsseltokens.

    Methods:
        identifier: Gibt den Identifikator eines Tokens zurück.
        __init__: Konstruktor der Klasse :class:`~key_token.Token`.
        __repr__: Gibt eine String-Repräsentation für dieses Token-Objekt zurück.
        __eq__: Vergleicht dieses Token-Objekt mit einem anderen Objekt.
        __hash__: Berechnet einen Hashwert für dieses Token-Objekt.
    """

    @abstractmethod
    def __init__(self, identifier: Identifier):
        """
        Konstruktor der Klasse :class:`~key_token.Token`.

        @param identifier: Der eindeutige Identifikator dieses Tokens.
        @type identifier: :class:`~identifier.Identifier`
        """
        self._identifier = identifier

    @property
    def identifier(self):
        """
        Get-Methode für den eindeutigen Identifikator dieses Tokens.

        @return: Den Identifikator dieses Tokens.
        @rtype: :class:`~identifier.Identifier`
        """
        return self._identifier

    def __repr__(self):
        """
        Erzeugt eine textuelle Darstellung für dieses Token-Objekt und gibt diese
        Darstellung als String zurück.

        @return: Die String-Repräsentation dieses Token-Objekts.
        @rtype: str
        """
        return f"{self._identifier}"

    def __eq__(self, other: Token):
        """
        Vergleicht dieses Token-Objekt mit dem Objekt `other`.

        Zwei Token-Objekte werden als gleich betrachtet, wenn sie den gleichen
        Identifikator speichern.

        @param other: Das Objekt, das mit diesem Token-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn beide Token-Objekte den gleichen Identifikator haben;
                 andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return self.identifier == other.identifier

    def __hash__(self):
        """
        Gibt einen Hashwert für dieses Token-Objekt zurück.

        Der Hashwert wird anhand des in diesem Token-Objekt gespeicherten
        Identifikators berechnet.

        @return: Den für dieses Token-Objekt berechneten Hashwert.
        @rtype: int
        """
        return hash(self.identifier)


class NFCToken(Token):
    """
    Diese abstrakte Klasse modelliert einen Schlüsseltoken, der die NFC-Technik (Near Field Communication)
    zum kontaktlosen Austausch von Daten benutzt.
    NFC-Tokens werden im Steuerungssystem verwendet, um die gesteuerte Tür durch
    autorisierte Nutzer zu öffnen.

    Attributes:
        identifier (:class:`~identifier.Identifier`): Der eindeutige Identifikator
                                                      dieses NFC-Tokens.

    Methods:
        __init__: Konstruktor der Klasse :class:`~key_token.NFCToken`.
    """

    @abstractmethod
    def __init__(self, identifier: Identifier):
        """
        Konstruktor der Klasse :class:`~key_token.NFCToken`.

        @param identifier: Der eindeutige Identifikator dieses NFC-Tokens.
        @type identifier: :class:`~identifier.Identifier`
        """
        super().__init__(identifier)


class AuthorizedNFCToken(NFCToken):
    """
    Diese Klasse modelliert einen autorisierten NFC-Schlüsseltoken.
    Die elektrisch gesteuerte Tür kann nur mit autorisierten NFC-Tokens geöffnet werden.

    Attributes:
        identifier (:class:`~identifier.Identifier`): Der eindeutige Identifikator
                                                      dieses autorisierten NFC-Tokens.

    Methods:
        __init__: Konstruktor der Klasse :class:`~key_token.AuthorizedNFCToken`.
    """

    def __init__(self, identifier: Identifier):
        """
        Konstruktor der Klasse :class:`~key_token.AuthorizedNFCToken`.

        Erstellt und initialisiert einen autorisierten NFC-Token mit einem
        eindeutigen Identifikator.
        Ein autorisierter Token gehört immer zu genau einem autorisierten Nutzer.

        @param identifier: Der eindeutige Identifikator dieses autorisierten NFC-Tokens.
        @type identifier: :class:`~identifier.Identifier`
        """
        super().__init__(identifier)


class UnauthorizedNFCToken(NFCToken):
    """
    Diese Klasse modelliert einen nicht autorisierten NFC-Schlüsseltoken.
    Nicht autorisierte Tokens werden vom Türsteuerungssystem automatisch erkannt,
    sodass man mit einem nicht autorisierten Tokens die Tür nicht öffnen kann.

    Attributes:
        identifier (:class:`~identifier.Identifier`): Der eindeutige Identifikator
                                                      dieses unautorisierten NFC-Tokens.

    Methods:
        __init__: Konstruktor der Klasse :class:`~key_token.UnauthorizedNFCToken`.
    """

    def __init__(self, identifier: Identifier):
        """
        Konstruktor der Klasse :class:`~key_token.UnauthorizedNFCToken`.

        Erstellt und initialisiert einen nicht autorisierten NFC-Token mit einem eindeutigen Identifikator.
        Mit nicht autorisierten Tokens kann die gesteuerte Tür nicht geöffnet werden.

        @param identifier: Der eindeutige Identifikator dieses unautorisierten NFC-Tokens.
        @type identifier: :class:`~identifier.Identifier`
        """
        super().__init__(identifier)


class BotIDToken(Token):
    """
    Diese Klasse modelliert einen ID-Token für einen Bot. Damit kann der Bot eindeutig identifiziert werden.

    Attributes:
        identifier (:class:`~identifier.Identifier`): Der eindeutige Identifikator des Bots.

    Methods:
        __init__: Konstruktor der Klasse :class:`~key_token.BotIDToken`.
    """
    def __init__(self, id:Identifier):
        """
        Konstruktor der Klasse :class:`~key_token.BotIDToken`.

        Erstellt und initialisiert einen BotIDToken mit einem eindeutigen Identifikator.
        Durch diesen ist der Bot eindeutig zu identifizieren.

        @param identifier: Der eindeutige Identifikator dieses BotIDTokens.
        @type identifier: :class:`~identifier.Identifier`
        """
        super().__init__(id)

    def __eq__(self, other: Token):
        """
        Vergleicht dieses Token-Objekt mit dem Objekt `other`.

        Zwei Token-Objekte werden als gleich betrachtet, wenn sie den gleichen
        Identifikator speichern.

        @param other: Das Objekt, das mit diesem Token-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn beide Token-Objekte den gleichen Identifikator haben;
                 andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return isinstance(other, self.__class__) and self.identifier == other.identifier


class BotChannelToken(Token):
    """
    Diese Klasse modelliert einen ID-Token für einen Slack-Channel, in welchen dann ein Bot eine Nachricht senden kann.
    Damit kann der Slack-Channel eindeutig identifiziert werden.

    Attributes:
        identifier (:class:`~identifier.Identifier`): Der eindeutige Identifikator des Bots.

    Methods:
        __init__: Konstruktor der Klasse :class:`~key_token.BotChannelToken`.
    """
    def __init__(self, id: Identifier):
        """
        Konstruktor der Klasse :class:`~key_token.BotChannelToken`.

        Erstellt und initialisiert einen BotChannelToken mit einem eindeutigen Identifikator.
        Durch diesen ist der Slack-Channel eindeutig zu identifizieren.

        @param identifier: Der eindeutige Identifikator dieses Slack-Channels.
        @type identifier: :class:`~identifier.Identifier`
        """
        super().__init__(id)

    def __eq__(self, other: Token):
        """
        Vergleicht dieses Token-Objekt mit dem Objekt `other`.

        Zwei Token-Objekte werden als gleich betrachtet, wenn sie den gleichen
        Identifikator speichern.

        @param other: Das Objekt, das mit diesem Token-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn beide Token-Objekte den gleichen Identifikator haben;
                 andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return isinstance(other, self.__class__) and self.identifier == other.identifier
