from RaspberryPi.src.data_model.key_token import Token
from RaspberryPi.src.data_model.door import DoorDataStorage

"""
Dieses Modul kapselt alle Klassen, die für die Validierung von Schlüsseltokens
im Türsteuerungssystem zuständig sind.

Classes: 
    TokenValidation: Repräsentiert ein Validierungsmittel, mithilfe dessen die Gültigkeit
                     von Schlüsseltokens im Türsteuerungssystem geprüft werden kann.
                     
@author Ahmad Eynawi
@version 17.02.2022
"""


class TokenValidation:
    """
    Diese Klasse repräsentiert ein Validierungsmittel, mithilfe dessen die Gültigkeit
    von Schlüsseltokens im Türsteuerungssystem geprüft werden kann.

    Attributes:
        doorDataStorage (:class:`~door.DoorDataStorage`): Der Datenspeicher für eine ferngesteuerte Tür.

    Methods:
        doorDataStorage (Getter): Get-Methode für den Datenspeicher, der den Identifikator
                                  sowie eine Liste aller mit einer Tür assoziierten Tokens
                                  speichert.
        validateToken: Prüft, ob ein Schlüsseltoken im Türsteuerungssystem registriert
                       bzw. gültig ist,
        __init__: Konstruktor der Klasse :class:`~TokenValidation.TokenValidation`
    """

    def __init__(self, doorDataStorage: DoorDataStorage):
        """
        Konstruktor der Klasse :class:`~TokenValidation.TokenValidation`.

        Erstellt und initialisiert ein Tokenvalidierungsobjekt für eine ferngesteuerte Tür.
        Dieses Validierungsobjekt bietet Methoden für die Feststellung der Gültigkeit
        von Schlüsseltokens im Türsteuerungssystem.

        @param doorDataStorage: Der Datenspeicher für die Tür, der für die Überprüfung
                                der Zugehörigkeit von Schlüsseltokens zu dieser Tür
                                benötigt wird.
        @type doorDataStorage: :class:`~door.DoorDataStorage`
        """
        self.__doorDataStorage = doorDataStorage

    @property
    def doorDataStorage(self):
        """
        Gibt den mit diesem Tokenvalidierungsobjekt assoziierten Datenspeicher zurück.

        Dieser Datenspeicher speichert den Identifikator der Tür sowie die Liste der
        mit dieser Tür assoziierten Schlüsseltokens.

        @return: Den Datenspeicher für die Tür, der für die Validierung von Schlüsseltokens
                 verwendet wird.
        @rtype: :class:`~door.DoorDataStorage`
        """
        return self.__doorDataStorage

    def validateToken(self, keyToken: Token):
        """
        Gibt `True` zurück, wenn der als Parameter übergebene Schlüsseltoken für die Tür
        registriert ist, die mit diesem TokenValidation-Objekt assoziiert ist;
        andernfalls wird `False` zurückgegeben.

        @param keyToken: Der Schlüsseltoken, dessen Zugehörigkeit zu einer Tür im
                         Türsteuerungssystem geprüft werden soll.
        @type keyToken: :class:`~token.Token`

        @return: `True`, wenn der gegebene Schlüsseltoken im Türsteuerungssystem
                 registriert ist, andernfalls `False`.
        @rtype: bool
        """
        return self.__doorDataStorage.hasToken(keyToken)
