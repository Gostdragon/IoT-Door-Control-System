from typing_extensions import Final
from Website.src.data_model.password import Password
from Website.src.data_model.name import Name, FirstName, LastName

"""
Dieses Modul kapselt alle Klassen, die für die Speicherung von Konfigurationsdaten 
im Türsteuerungssystem zuständig sind.

Classes: 
    CameraConfiguration: Repräsentiert eine Datenhaltungsklasse, welche alle relevanten Daten und Konstanten
                    zu den benötigten Kameras in sich kapselt.
    PiConfiguration: Repräsentiert eine Datenhaltungsklasse, welche alle relevanten Daten und Konstanten
                    zu dem benötigten Pi in sich kapselt.
                    
@author Fabian Schiekel
@version 19.02.2022
"""


class Configuration:
    """
    Diese Klasse repräsentiert eine Datenhaltungsklasse, in der Konstanten und
    Konfigurationsdaten für Komponenten des Türsteuerungssystems gekapselt werden.

    Attributes:
        configurationData: Ein Dictionary, in dem die initialen Konfigurationsdaten
                           gespeichert sind.

    Methods:
        getConfigurationValue: Gibt den Konfigurationswert zu einem Konfigurationselement
                               zurück.
        addConfigurationItem: Fügt ein Konfigurationselement zu diesem Konfigurationsobjekt hinzu.
        deleteConfigurationItem: Entfernt ein Konfigurationselement aus diesem Konfigurationsobjekt.
        __init__: Konstruktor der Klasse :class:`~configuration.Configuration`
    """

    def __init__(self, configurationData=dict()):
        """
        Konstruktor der Klasse :class:`~configuration.Configuration`.

        Erstellt und initialisiert ein neues Konfigurationsobjekt, in dem Konfigurationsdaten
        für andere Klassen im Türsteuerungssystem gespeichert werden.

        @param configurationData: Die initialen Konfigurationsdaten, die in diesem
                                  Konfigurationselement gespeichert werden sollen.
        @type configurationData: dict
        """
        self.__configurationData = configurationData

    def getConfigurationValue(self, configurationItemName: str):
        """
        Gibt den Konfigurationswert zu dem als Parameter übergebenen Bezeichner zurück.

        Wenn kein Konfigurationselement mit dem gegebenen Bezeichner assoziiert ist,
        wird `None` zurückgegeben.

        @param configurationItemName: Der Bezeichner, der den Konfigurationswert kennzeichnet,
                                      den die Methode zurückgeben soll, oder `None`, falls
                                      zu diesem Bezeichner kein Konfigurationselement existiert.
        @type configurationItemName: str
        @return: Den Konfigurationswert zum gegebenen Bezeichner als String.
        @rtype: str
        """
        return self.__configurationData.get(configurationItemName)

    def addConfigurationItem(self, configurationItem: dict):
        """
        Fügt das als Parameter übergebene Konfigurationselement zur Datenstruktur hinzu,
        welche die in diesem Konfigurationsobjekt gespeicherten Konfigurationsdaten speichert.

        Ein Konfigurationselement besteht hierbei aus einem Tupel der Form
        {Bezeichner: Wert}, wobei der Bezeichner den zu speichernden Konfigurationswert
        eindeutig kennzeichnen muss und für den Zugriff auf diesen Wert benötigt wird.
        Wenn das als Parameter übergebene Konfigurationselement bereits gespeichert ist,
        dann wird das Konfigurationsobjekt nicht verändert.

        @param configurationItem: Das Konfigurationselement, das zu diesem Konfigurationsobjekt
        hinzugefügt werden soll.
        @type configurationItem: dict
        """
        self.__configurationData.update(configurationItem)

    def deleteConfigurationItem(self, configurationItemName: str):
        """
        Entfernt das als Parameter übergebene Konfigurationselement aus diesem
        Konfigurationsobjekt.

        Wenn das Konfigurationselement nicht bereits gespeichert ist, wird das
        Konfigurationsobjekt nicht verändert und es wird `False` zurückgegeben;
        andernfalls wird `True` zurückgegeben.

        @param configurationItemName: Der eindeutige Bezeichner des Konfigurationselementes,
        dessen Daten entfernt werden sollen.
        @type configurationItemName: str
        @return `True`, wenn das Konfigurationselement zum gegebenen Bezeichner
        bereits gespeichert war und erfolgreich entfernt wurde; andernfalls `False`.
        @rtype bool
        """
        if self.__configurationData.__contains__(configurationItemName):
            self.__configurationData.pop(configurationItemName)
            return True
        else:
            return False


class CameraConfiguration(Configuration):
    """
    Diese Klasse ist eine Unterklasse der Klasse :class:`~configuration.Configuration`
    und repräsentiert eine Datenhaltungsklasse, in der Konstanten und
    Konfigurationsdaten für die Realisierung der Kamera gekapselt werden.

    Alle Attribute in dieser Klasse haben Standardwerte, die mit den als Klassenvariablen
    definierten (nicht veränderbaren) Konstanten identisch sind.

        Attributes:
            ip_address(str): Die IP-Adresse der Kamera.
            username(list[Name]): Den Usernamen der Kamera.
            password(list[Password]): Das Password der Kamera.

        Methods:
            ip_address: Getter für die IP-Adresse der Kamera.
            username: Getter für den Usernamen der Kamera.
            password: Getter für das Passwort der Kamera.
            __init__: Konstruktor der Klasse :class:`~configuration.CameraConfiguration`
    """
    __IP_ADDRESS: Final[str] = ['']
    __USERNAME: Final[list[Name]] = [Name(FirstName(''), LastName("leer"))]
    __PASSWORD: Final[list[Password]] = [Password("")]

    def __init__(self, ip_address=__IP_ADDRESS, username=__USERNAME, password=__PASSWORD,):
        super().__init__()
        self.__ip_address = ip_address
        self.__username = username
        self.__password = password

    @property
    def ip_address(self) -> str:
        """
        Gibt die IP-Adresse der Kamera zurück.

        @return: Die IP-Adresse der Kamera.
        @rtype: str
        """
        return self.__ip_address
    @property
    def username(self) -> list[Name]:
        """
        Gibt den Usernamen der Kamera zurück.

        @return: Den Usernamen der Kamera.
        @rtype: list[Name]
        """
        return self.__username

    @property
    def password(self) -> list[Password]:
        """
        Gibt das Passwort der Kamera zurück.

        @return: Das Passwort der Kamera.
        @rtype: list[Password]
        """
        return self.__password


class PiConfiguration(Configuration):
    """
    Diese Klasse ist eine Unterklasse der Klasse :class:`~configuration.Configuration`
    und repräsentiert eine Datenhaltungsklasse, in der Konstanten und
    Konfigurationsdaten für die Realisierung der Ausgänge auf dem Pi gekapselt werden.

    Alle Attribute in dieser Klasse haben Standardwerte, die mit den als Klassenvariablen
    definierten (nicht veränderbaren) Konstanten identisch sind.

        Attributes:
            ip_address(str): Die IP-Addresse des Pi.


        Methods:
            ip_address: Getter für die IP-Address des Pi.
            __init__: Konstruktor der Klasse :class:`~configuration.PiConfiguration`
    """

    __IP_ADDRESS: Final[str] = ""

    def __init__(self, ip_address=__IP_ADDRESS):
        super().__init__()
        self.__ip_address = ip_address

    @property
    def ip_address(self) -> str:
        """
        Gibt die IP-Adresse des Pi wieder.

        @return: Die IP-Adresse des Pis.
        @rtype: str
        """
        return self.__ip_address
