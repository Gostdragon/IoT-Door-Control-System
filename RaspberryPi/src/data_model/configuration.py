from typing_extensions import Final
from RaspberryPi.src.data_model.user import AuthenticatedUser
from RaspberryPi.src.data_model.user import Name, Password, Identifier
from RaspberryPi.src.data_model.name import FirstName, LastName
from RaspberryPi.src.data_model.key_token import BotIDToken, BotChannelToken

"""
Dieses Modul kapselt alle Klassen, die für die Speicherung von Konfigurationsdaten 
im Türsteuerungssystem zuständig sind.

Classes: 
    Configuration: Repräsentiert eine Datenhaltungsklasse, welche die Speicherung 
                   und Verwaltung von Konstanten und Konfigurationsdaten für Komponenten des 
                   Türsteuerungssystems ermöglicht und in sich kapselt.
    MQTTProtocolConfiguration: Repräsentiert eine Datenhaltungsklasse, welche alle
                               Daten und Konstanten, die für die Konfigurierung des 
                               MQTT-Protokolls erforderlich sind, speichert und den Zugriff
                               darauf ermöglicht.
    BotConfiguration: Repräsentiert eine Datenhaltungsklasse, welche alle relevanten Daten und Konstanten
                    zu den benötigten Bots in sich kapselt.
    CameraConfiguration: Repräsentiert eine Datenhaltungsklasse, welche alle relevanten Daten und Konstanten
                    zu den benötigten Kameras in sich kapselt.
    PiConfiguration: Repräsentiert eine Datenhaltungsklasse, welche alle relevanten Daten und Konstanten
                    zu dem benötigten Pi in sich kapselt.

@author Ahmad Eynawi
@version 24.02.2022

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


class MQTTProtocolConfiguration(Configuration):
    """
    Diese Klasse ist eine Unterklasse der Klasse :class:`~configuration.Configuration`
    und repräsentiert eine Datenhaltungsklasse, in der Konstanten und
    Konfigurationsdaten für die Realisierung des MQTT-Netzwerkprotokolls gekapselt werden.

    Die meisten Attribute in dieser Klasse haben Standardwerte, die mit den als Klassenvariablen
    definierten (nicht veränderbaren) Konstanten identisch sind.

    Attributes:
        topic (str): Das Thema, das für die Klassifizierung von Nachrichten im MQTT-Protokoll
                     verwendet wird.
        payload (str): Der eigentliche Inhalt einer MQTT-Nachricht.
        broker (str): Der Hostname oder die IP-Adresse des Remote-Brokers, der
                      die Kommunikation zwischen den MQTT-Clients steuert.
        username (str): Der Benutzername für die Broker-Authentifizierung.
        password (str): Das Passwort für die Broker-Authentifizierung.
        willPayload (str): Der Inhalt der sogenannten Will-Nachricht.
                           Diese Testament-Nachricht wird durch den Broker an andere
                           MQTT-Clients gesendet, wenn ein MQTT-Client (z.B. aufgrund
                           einer Verbindungsunterbrechung) inaktiv wird.
        keepalive (int): Der maximale Zeitraum in Sekunden zwischen den Kommunikationsversuchen
                         mit dem Broker. Wenn keine anderen Nachrichten ausgetauscht werden,
                         steuert dies die Rate, mit der der Client Ping-Nachrichten an
                         den Broker sendet.
        port (int): Der Netzwerkport des Serverhosts (MQTT-Broker), zu dem
                    eine Verbindung hergestellt werden soll.

    Methods:
        topic: Get-Methode für das Thema, zu dem im MQTT-Protokoll Nachrichten ausgetauscht
               werden.
        payload: Get-Methode für den eigentlichen Inhalt einer MQTT-Nachricht.
        broker: Get-Methode für den MQTT-Broker.
        username: Get-Methode für den zur Authentifizierung verwendeten Benutzernamen.
        password: Get-Methode für das zur Authentifizierung verwendete Passwort.
        willPayload: Get-Methode für die Testament-Nachricht, die vom Broker
                     an andere MQTT-Clients gesendet wird, wenn der Client
                     unerwartet die Verbindung verliert.
        keepalive: Get-Methode für den maximalen Zeitraum (in Sekunden) zwischen
                   aufeinanderfolgenden Kommunikationsversuchen mit dem Broker.
        port: Get-Methode für den Netzwerkport des MQTT-Brokers.
        __init__: Konstruktor der Klasse :class:`~configuration.MQTTProtocolConfiguration`
    """

    __BROKER: Final[str] = "10.12.180.128"
    __USERNAME: Final[str] = "rapi_zerow"
    __PASSWORD: Final[str] = "rapi#zerow#mqtt"
    __WILL_PAYLOAD: Final[str] = "Der MQTT-Client hat die Verbindung mit dem MQTT-Broker verloren!"
    __KEEPALIVE: Final[int] = 60
    __PORT: Final[int] = 1883

    def __init__(self, topic, payload, broker=__BROKER, username=__USERNAME, password=__PASSWORD,
                 willPayload=__WILL_PAYLOAD, keepalive=__KEEPALIVE, port=__PORT):
        """
        Konstruktor der Klasse :class:`~configuration.MQTTProtocolConfiguration`.

        Erstellt und initialisiert ein Konfigurationsobjekt, in dem die Konfigurationsdaten
        des MQTT-Protokolls für die Kommunikation zwischen dem WLAN-Türöffnertaster, der Klingel
        und der Türsteuerung gekapselt werden.

        @param topic: Das Thema, das für die Klassifizierung von Nachrichten im MQTT-Protokoll
                      verwendet wird.
        @type topic: str
        @param payload: Der eigentliche Inhalt einer MQTT-Nachricht.
        @type payload: str
        @param broker: Der Hostname oder die IP-Adresse des Remote-Brokers, der
                       die Kommunikation zwischen den MQTT-Clients steuert.
        @type broker: str
        @param username: Der Benutzername für die Broker-Authentifizierung.
        @type username: str
        @param password: Das Passwort für die Broker-Authentifizierung.
        @type password: str
        @param willPayload: Der Inhalt der sogenannten Will-Nachricht.
                            Diese Testament-Nachricht wird durch den Broker an andere
                            MQTT-Clients gesendet, wenn ein MQTT-Client (z.B. aufgrund
                            einer Verbindungsunterbrechung) inaktiv wird.
        @type willPayload: str
        @param keepalive: Der maximale Zeitraum in Sekunden zwischen den Kommunikationsversuchen
                          mit dem Broker. Wenn keine anderen Nachrichten ausgetauscht werden,
                          steuert dies die Rate, mit der der Client Ping-Nachrichten an
                          den Broker sendet.
        @type keepalive: int
        @param port: Der Netzwerkport des Serverhosts (MQTT-Broker), zu dem
                     eine Verbindung hergestellt werden soll.
        @type port: int
        """
        super().__init__()
        self.__topic = topic
        self.__payload = payload
        self.__broker = broker
        self.__username = username
        self.__password = password
        self.__willPayload = willPayload
        self.__keepalive = keepalive
        self.__port = port

    @property
    def topic(self):
        """
        Gibt das Thema zurück, zu dem Nachrichten übers MQTT-Protokoll ausgetauscht werden.

        @return: Das Thema für die Klassifizierung von Nachrichten im MQTT-Protokoll.
        @rtype: str
        """
        return self.__topic

    @property
    def payload(self):
        """
        Gibt den eigentlichen Inhalt der MQTT-Nachricht zurück.

        @return: Die eigentliche Nachricht, die übers MQTT-Protokoll gesendet wird.
        @rtype: str
        """
        return self.__payload

    @property
    def broker(self):
        """
        Gibt die IP-Adresse des MQTT-Brokers zurück.

        @return: Die IP-Adresse des MQTT-Servers.
        @rtype: str
        """
        return self.__broker

    @property
    def username(self):
        """
        Gibt den Benutzernamen zurück, der zur Authentifizierung beim Aufbau einer Verbindung mit
        dem MQTT-Broker benutzt wird.

        @return: Den Benutzernamen für die Broker-Authentifizierung.
        @rtype: str
        """
        return self.__username

    @property
    def password(self):
        """
        Gibt das Passwort zurück, das zur Authentifizierung beim Aufbau einer Verbindung mit
        dem MQTT-Broker benutzt wird.

        @return: Das Passwort für die Broker-Authentifizierung.
        @rtype: str
        """
        return self.__password

    @property
    def willPayload(self):
        """
        Gibt den Inhalt der sogenannten Will-Nachricht zurück, die durch den Broker
        an andere MQTT-Clients gesendet wird, wenn der MQTT-Client unerwartet inaktiv wird.

        @return: Die "Testament-Nachricht" des MQTT-Clients.
        @rtype: str
        """
        return self.__willPayload

    @property
    def keepalive(self):
        """
        Gibt den maximalen Zeitraum in Sekunden zwischen aufeinanderfolgenden Kommunikationsversuchen
        mit dem Broker. Wenn keine anderen Nachrichten ausgetauscht werden,
        steuert dies die Rate, mit welcher der Client Ping-Nachrichten an den Broker sendet.

        @return: Den maximalen Zeitraum (in Sekunden) zwischen aufeinanderfolgenden
        Kommunikationsversuchen mit dem MQTT-Broker.

        @rtype: int
        """
        return self.__keepalive

    @property
    def port(self):
        """
        Gibt die Nummer des Netzwerkports des Serverhosts (MQTT-Broker) zurück, zu dem
        eine Verbindung hergestellt werden soll.

        Der Standardwert des MQTT-Ports ist 1883.

        @return: Den Port des MQTT-Brokers.
        @rtype: int
        """
        return self.__port


class BotConfiguration(Configuration):
    """
    Diese Klasse ist eine Unterklasse der Klasse :class:`~configuration.Configuration`
    und repräsentiert eine Datenhaltungsklasse, in der Konstanten und
    Konfigurationsdaten für die Realisierung des Bots gekapselt werden.

    Alle Attribute in dieser Klasse haben Standardwerte, die mit den als Klassenvariablen
    definierten (nicht veränderbaren) Konstanten identisch sind.

        Attributes:
            bot_channel_id(list[BotChannelToken]): Die Channel IDs der Bots,
                welche bei einem Klingelereignis aktiv werden.
            bot_token(list[BotIDToken] Die Token IDs der Bots, welche bei einem Klingelereignis aktiv werden.
            bot_msg([str]): Die Nachrichten, welche bei einem Klingelereignis gesendet werden sollen.
            bot_log_token(BotIDToken): Die ID des Bots, welche alle Log-Nachrichten sendet.
            bot_f_channel_id(BotChannelToken): Die Channel ID des Channels,
                welcher das Log mit der Log Stufe Fatal darstellt.
            bot_e_channel_id(BotChannelToken):Die Channel ID des Channels,
                welcher das Log mit der Log Stufe Error darstellt.
            bot_i_channel_id(BotChannelToken):Die Channel ID des Channels,
                welcher das Log mit der Log Stufe Info darstellt.
            bot_msg_visible(int): Die Zeitspanne, in der die Nachrichten bei einem Klingelereignis sichtbar sein sollen.

        Methods:
            bot_channel_id: Getter für die Channel IDs.
            bot_token: Getter für die Bot Tokens.
            bot_msg: Getter für die Bot Nachrichten
            bot_log_token: Getter für den Log-Bot Token
            bot_f_channel_id: Getter für die Fatal-Log Channel-ID
            bot_e_channel_id: Getter für die Error-Log Channel-ID
            bot_i_channel_id: Getter für die Info-Log Channel-ID
            bot_msg_visible: Getter für die Zeitspanne der Bot Nachrichten.
            __init__: Konstruktor der Klasse :class:`~configuration.BotConfiguration`
    """

    # Ein Slack-Bot konnte mithilfe eines Tokens angesprochen und der entsprechende Channel mittels
    # Channel-Token angesprochen werden. Für den Fall, dass ein anderer Bot benutzt wird, muss bei Bedarf dieses
    # Muster angepasst werden.
    __BOT_RING_CHANNEL_ID: Final[list[BotChannelToken]] = [BotChannelToken(Identifier(''))]
    __BOT_RING_TOKEN: Final[list[BotIDToken]] = [BotIDToken(Identifier(''))]
    __BOT_RING_MESSAGE: Final[list[str]] = [""]
    __BOT_LOG_TOKEN: Final[BotIDToken] = BotIDToken(Identifier(''))
    __BOT_LOG_CHANNEL_ID_FATAL: Final[BotChannelToken] = BotChannelToken(Identifier(""))
    __BOT_LOG_CHANNEL_ID_ERROR: Final[BotChannelToken] = BotChannelToken(Identifier(""))
    __BOT_LOG_CHANNEL_ID_INFO: Final[BotChannelToken] = BotChannelToken(Identifier(""))
    __TIME_BOT_MESSAGE_VISIBLE: Final[int] = 60

    def __init__(self, bot_channel_id=None, bot_token=None, bot_msg=None, bot_log_token=__BOT_LOG_TOKEN,
                 bot_f_channel_id=__BOT_LOG_CHANNEL_ID_FATAL, bot_e_channel_id=__BOT_LOG_CHANNEL_ID_ERROR,
                 bot_i_channel_id=__BOT_LOG_CHANNEL_ID_INFO, bot_msg_visible=__TIME_BOT_MESSAGE_VISIBLE):
        super().__init__()
        if bot_msg is None:
            bot_msg = self.__BOT_RING_MESSAGE
        if bot_token is None:
            bot_token = self.__BOT_RING_TOKEN
        if bot_channel_id is None:
            bot_channel_id = self.__BOT_RING_CHANNEL_ID

        self.__bot_channel_id = bot_channel_id
        self.__bot_token = bot_token
        self.__bot_msg = bot_msg
        self.__bot_log_token = bot_log_token
        self.__bot_fat_channel_id = bot_f_channel_id
        self.__bot_err_channel_id = bot_e_channel_id
        self.__bot_inf_channel_id = bot_i_channel_id
        self.__bot_msg_visible = bot_msg_visible

    @property
    def bot_channel_id(self) -> list[BotChannelToken]:
        """
        Gibt die IDs der Channel zurück, in die bei einem Klingelereignis eine Nachricht gesendet werden soll.

        Diese Liste muss genauso lang sein, wie die der Bot Tokens und Nachrichten.
        Der Bot an Index i pusht die i-te Nachricht in den Channel mit Index i.

        @return: Die IDs der Channel, welche bei einem Klingelereignis eine Nachricht pushen sollen.
        @rtype: list[BotChannelToken]
        """
        return self.__bot_channel_id

    @property
    def bot_token(self) -> list[BotIDToken]:
        """
        Gibt die IDs der Bots zurück, die bei einem Klingelereignis eine Nachricht senden sollen.

        Diese Liste muss genauso lang sein, wie die der Channel Tokens und Nachrichten.
        Der Bot an Index i pusht die i-te Nachricht in den Channel mit Index i.

        @return: Die IDs der Bots, welche eine Nachricht pushen sollen.
        @rtype: list[BotIDToken]
        """
        return self.__bot_token

    @property
    def bot_msg(self) -> list[str]:
        """
        Gibt die Nachrichten zurück, welche bei einem Klingelereignis von den jeweiligen Bots in die jeweiligen Channel
        gepusht werden sollen.

        Diese Liste muss genauso lang sein, wie die der Bot Tokens und Channel Tokens.
        Der Bot an Index i pusht die i-te Nachricht in den Channel mit Index i.

        @return: Die Nachrichten, welche gesendet werden sollen.
        @rtype: list[str]
        """
        return self.__bot_msg

    @property
    def bot_log_token(self) -> BotIDToken:
        """
        Gibt die ID des Bots zurück, welcher alle Log Nachrichten senden soll.

        @return: Die ID des Logbot
        @rtype: BotIDToken
        """
        return self.__bot_log_token

    @property
    def bot_fat_id(self) -> BotChannelToken:
        """
        Git die ID des Channels zurück, welche das Log mit dem Log-Level Fatal darstellt.

        @return: Die ID des Fatal-Log Channel
        @rtype: BotChannelToken
        """
        return self.__bot_fat_channel_id

    @property
    def bot_err_id(self) -> BotChannelToken:
        """
        Git die ID des Channels zurück, welche das Log mit dem Log-Level Error darstellt.

        @return: Die ID des Error-Log Channel
        @rtype: BotChannelToken
        """
        return self.__bot_err_channel_id

    @property
    def bot_inf_id(self) -> BotChannelToken:
        """
        Git die ID des Channels zurück, welche das Log mit dem Log-Level Info darstellt.

        @return: Die ID des Info-Log Channel
        @rtype: BotChannelToken
        """
        return self.__bot_inf_channel_id

    @property
    def bot_msg_visible(self) -> int:
        """
        Gibt die Zeitspanne an, in der die Nachrichten über das Klingelereignis angezeigt werden sollen.

        @return: Die Zeitspanne, in der die Nachrichten über das Klingelereignis angezeigt werden sollen.
        @rtype: int
        """
        return self.__bot_msg_visible


class CameraConfiguration(Configuration):
    """
    Diese Klasse ist eine Unterklasse der Klasse :class:`~configuration.Configuration`
    und repräsentiert eine Datenhaltungsklasse, in der Konstanten und
    Konfigurationsdaten für die Realisierung der Kamera gekapselt werden.

    Alle Attribute in dieser Klasse haben Standardwerte, die mit den als Klassenvariablen
    definierten (nicht veränderbaren) Konstanten identisch sind.

        Attributes:
            ip_address(list[String]): Die IP-Adresse der Kamera.
            username(list[Name]): Den Usernamen der Kamera.
            password(list[Password]): Das Password der Kamera.
            time_cam_active(list[int]): Die Zeitspanne, die die Kamera bei einem Klingelereignis den Livestream senden soll.
            time_cam_rot(list[int]): Die Zeitspanne, die die Kamera für eine 40 Grad Drehung benötigt.
            time_cam_calibration(list[int]): Die Zeitspanne, die die Kamera für die initiale Kalibrierung benötigt.
            rot_angle(list[int]): Der Winkel, um den sich die Kamera bei einem Klingelereignis drehen soll.

        Methods:
            ip_address: Getter für die IP-Adresse der Kamera.
            username: Getter für den Usernamen der Kamera.
            password: Getter für das Passwort der Kamera.
            time_cam_active: Getter für die Zeitspanne, in der die Kamera den Livestream übertragen soll.
            time_cam_rot: Getter für die Zeitspanne, die die Kamera für eine 40 Grad Drehung benötigt.
            time_cam_calibration: Getter für die Zeitspanne, die die Kamera für die initiale Kalibrierung benötigt.
            rot_angle: Getter für den Drehwinkel der Kamera.
            __init__: Konstruktor der Klasse :class:`~configuration.CameraConfiguration`
    """
    __IP_ADDRESS: Final[list[str]] = ['']
    # Der Username wird im Firstname gespeichert.
    __USERNAME: Final[list[Name]] = [Name(FirstName(''), LastName("leer"))]
    __PASSWORD: Final[list[Password]] = [Password("")]
    __TIME_CAMERA_ACTIVE: Final[list[int]] = [60]
    # Die Nachfolgenden drei Werte sind für eine Tapo Kamera Tapo C200.
    __TIME_ROTATION_CAMERA: Final[list[int]] = [3]
    __TIME_CALIBRATION_CAMERA: Final[list[int]] = [27]
    __ROTATION_ANGLE: Final[list[int]] = [40]

    def __init__(self, ip_address=None, username=None, password=None, time_cam_active=None, time_cam_rot=None,
                 time_cam_calibration=None, rot_angle=None):
        super().__init__()

        if ip_address is None:
            ip_address = self.__IP_ADDRESS
        if username is None:
            username = self.__USERNAME
        if password is None:
            password = self.__PASSWORD
        if time_cam_active is None:
            time_cam_active = self.__TIME_CAMERA_ACTIVE
        if time_cam_rot is None:
            time_cam_rot = self.__TIME_ROTATION_CAMERA
        if time_cam_calibration is None:
            time_cam_calibration = self.__TIME_CALIBRATION_CAMERA
        if rot_angle is None:
            rot_angle = self.__ROTATION_ANGLE
        self.__ip_address = ip_address
        self.__username = username
        self.__password = password
        self.__time_cam_aktiv = time_cam_active
        self.__time_cam_rot = time_cam_rot
        self.__time_cam_calibration = time_cam_calibration
        self.__rot_angle = rot_angle

    @property
    def ip_address(self) -> list[str]:
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

    @property
    def time_cam_aktiv(self) -> list[int]:
        """
        Gibt die Zeitspanne zurück, in der die Kamera bei einem Klingelereignis aktiv sein soll.

        @return: Die Zeitspanne, die die Kamera bei einem Klingelereignis aktiv sein soll.
        @rtype: list[int]
        """
        return self.__time_cam_aktiv

    @property
    def time_cam_rot(self) -> list[int]:
        """
        Gibt die Zeitspanne zurück, die die Kamera für eine 40 Grad Drehung benötigt.
        Die Zeitspanne ist Abhängig von dem Winkel, um den sich die Kamera bei einem Klingelereignis drehen soll.
        Wenn die beiden Werte nicht zusammen passen, ist es möglich, dass das Programm nicht funktioniert.

        @return: Die Zeitspanne, die die Kamera für eine 40 Grad Drehung benötigt.
        @rtype: list[int]
        """
        return self.__time_cam_rot

    @property
    def time_cam_calibration(self) -> list[int]:
        """
        Gibt die Zeitspanne zurück, die die Kamera für die Kalibrierung benötigt.

        @return: Die Zeitspanne, die die Kamera für die Kalibrierung benötigt.
        @rtype: list[int]
        """
        return self.__time_cam_calibration

    @property
    def rot_angle(self) -> list[int]:
        """
        Gibt den Winkel zurück, um den sich die Kamera bei einem Klingelereignis drehen soll.
        Der Wert time_cam_rot ist Abhängig von dem rot_angle. Wenn die beiden Werte nicht zusammen passen, ist es
        möglich, dass das Programm nicht funktioniert.

        @return: Den Winkel, um den sich die Kamera drehen soll.
        @rtype: list[int]
        """
        return self.__rot_angle


class PiConfiguration(Configuration):
    """
    Diese Klasse ist eine Unterklasse der Klasse :class:`~configuration.Configuration`
    und repräsentiert eine Datenhaltungsklasse, in der Konstanten und
    Konfigurationsdaten für die Realisierung der Ausgänge auf dem Pi gekapselt werden.

    Alle Attribute in dieser Klasse haben Standardwerte, die mit den als Klassenvariablen
    definierten (nicht veränderbaren) Konstanten identisch sind.

        Attributes:
            button(int): Die Pinnummer des Buttons.
            pin_red(int): Die Pinnummer der roten LED.
            pin_green(int): Die Pinnummer der grünen LED.
            pin_yellow(int): Die Pinnummer der gelben LED.
            sleep_after_ring(int): Die Zeitspanne nach einem Klingelereignis, in der kein weiteres
                Klingelereignis auftreten soll.
            admin(AuthenticatedUser): Der Admin, welcher auf den Server zugreifen kann.
            path_to_project(str): Der Pfad zu dem Verzeichnis mit dem Projektordner.
            path_to_cert_pem(str): Der Pfad zu der .pem Datei.
            path_to_cert_key(str): Der Pfad zu der .key Datei.
            ip_address(str): Die IP-Addresse des Pi.
            path_valid_tokens(str): Der Pfad zu den validen Tokens.
            app_socket_port(int): Der Port über den Anfragen an den Server entgegengenommen werden.
            app_request_pattern(str): Der Redex dem eine Anfrage an den Server genügen muss.
            app_encoding(str): String-Kodierung mit der Anfragen an den Server kodiert sind.
            app_socket_buf_size(int): Die maximale Anzahl an Byte die eine Anfrage an den Server haben darf.
            command_search(str): Das Schlüsselwort mit dem eine Suchanfrage an den Server beginnt.
            command_add_token(str): Das Schlüsselwort mit dem eine Anfrage an den Server zum Hinzufügen von Tokens
                beginnt.
            command_delete_token(str): Das Schlüsselwort mit dem eine Anfrage an den Server zum Löschen eines einzelnen
                Tokens beginnt.
            command_delete_all(str): Das Schlüsselwort mit dem eine Anfrage an den Server zum Löschen aller Token eines
                Nutzers beginnt
            no_firstname(str): Zeichenkette die verwendet wird um einen Namen mit unbekanntem Vornamen zu erstellen.
            no_lastname(str): Zeichenkette die verwendet wird um einen Namen mit unbekanntem Nachnamen zu erstellen.

        Methods:
            button: Getter für die Pinnummer des Buttons.
            pin_red: Getter für die Pinnummer der roten LED.
            pin_green: Getter für die Pinnummer der grünen LED.
            pin_yellow: Getter für die Pinnummer der gelben LED.
            sleep_after_ring: Getter für die Zeitspanne, in der kein weiteres Klingelereignis auftreten soll.
            path_project: Getter für den Pfad zu dem Verzeichnis mit dem Projektordner.
            path_cert_pem: Getter für den Pfad zu der .pem Datei.
            path_cert_key: Getter für den Pfad zu der .key Datei.
            ip_address: Getter für die IP-Address des Pi.
            path_valid_tokens: Getter für den Pfad zu den validen Tokens.
            app_socket_port: Getter für den Port über den Anfragen an den Server gestellt werden können.
            app_request_pattern: Getter für den Redex dem eine Anfrage an den Server genügen muss
            app_encoding: Getter für die Kodierung mit welcher die Anfragen an den Server kodiert sein müssen.
            app_socket_buf_size: Getter für die maximale Anzahl an Byte die eine Anfrage an den Server haben darf.
            command_search: Getter für das Schlüsselwort, mit dem eine Suchanfrage an den Server beginnt.
            command_add_token: Getter für das Schlüsselwort, mit dem eine Anfrage an den Server zum Hinzufügen eines
                Tokens beginnt.
            command_delete_token: Getter für das Schlüsselwort, mit dem eine Anfrage an den Server zum Löschen eines
                Tokens beginnt.
            command_delete_all: Getter für das Schlüsselwort, mit dem eine Anfrage an den Server zum Löschen aller
                Tokens eines Nutzers beginnt.
            no_firstname: Getter für den Vornamen der Verwendet wird um einen Namen mit unbekanntem Vornamen zu
                erstellen.
            no_lastname: Getter für den Nachnamen der Verwendet wird um einen Namen mit unbekanntem Vornamen zu
                erstellen.
            __init__: Konstruktor der Klasse :class:`~configuration.PiConfiguration`
    """

    __PIN_NUMBER_BUTTON: Final[int] = 4
    __LED_RED: Final[int] = 23
    __LED_GREEN: Final[int] = 18
    __LED_YELLOW: Final[int] = 14
    __SLEEP_AFTER_RING: Final[int] = 5
    __PATH_TO_PROJECT: Final[str] = ""
    __IP_ADDRESS: Final[str] = ""

    # Nachfolgendes nicht verändern!!
    __PATH_TO_CERT_PEM: Final[str] = "/RaspberryPi/Certifications/app.cert.crt"
    __PATH_TO_CERT_KEY: Final[str] = "/RaspberryPi/Certifications/app.cert.key"
    __PATH_TO_VALID_TOKENS: Final[str] = "/RaspberryPi/src/ValidTokens.txt"
    __ADMIN: Final[AuthenticatedUser] = AuthenticatedUser(Name(FirstName("admin"), LastName("admin")),
                                                          Identifier("admin"), Password("admin"))
    __APP_SOCKET_PORT: Final[int] = 5001
    __APP_REQUEST_PATTERN: Final[str] = "(search|addToken|deleteToken|deleteAll)\\$([^$]+)\\$([^$]+)\\$([^$]+)" \
                                        "(?:\\$([^$]+))?"
    __APP_ENCODING: Final[str] = "utf-8"
    __APP_SOCKET_BUF_SIZE: Final[int] = 1024
    __COMMAND_SEARCH: Final[str] = "search"
    __COMMAND_ADD_TOKEN: Final[str] = "addToken"
    __COMMAND_DELETE_TOKEN: Final[str] = "deleteToken"
    __COMMAND_DELETE_ALL: Final[str] = "deleteAll"
    __NO_FIRSTNAME: Final[str] = 'a'
    __NO_LASTNAME: Final[str] = 'a'

    def __init__(self, button=__PIN_NUMBER_BUTTON, pin_red=__LED_RED, pin_green=__LED_GREEN, pin_yellow=__LED_YELLOW,
                 sleep_after_ring=__SLEEP_AFTER_RING, admin=__ADMIN, path_project=__PATH_TO_PROJECT, path_pem=__PATH_TO_CERT_PEM,
                 path_key=__PATH_TO_CERT_KEY, ip_address=__IP_ADDRESS, path_valid_tokens=__PATH_TO_VALID_TOKENS,
                 app_socket_port=__APP_SOCKET_PORT, app_request_pattern=__APP_REQUEST_PATTERN,
                 app_encoding=__APP_ENCODING, app_socket_buf_size=__APP_SOCKET_BUF_SIZE,
                 command_search=__COMMAND_SEARCH,command_add_token=__COMMAND_ADD_TOKEN,
                 command_delete_token=__COMMAND_DELETE_TOKEN,command_delete_all=__COMMAND_DELETE_ALL,
                 no_firstname=__NO_FIRSTNAME, no_lastname=__NO_LASTNAME):
        super().__init__()
        self.__button = button
        self.__pin_red = pin_red
        self.__pin_green = pin_green
        self.__pin_yellow = pin_yellow
        self.__sleep_after_ring = sleep_after_ring
        self.__admin = admin
        self.__path_project = path_project
        self.__path_pem = path_pem
        self.__path_key = path_key
        self.__ip_address = ip_address
        self.__path_valid_tokens = path_valid_tokens
        self.__app_socket_port = app_socket_port
        self.__app_request_pattern = app_request_pattern
        self.__app_encoding = app_encoding
        self.__app_socket_buf_size = app_socket_buf_size
        self.__command_search = command_search
        self.__command_add_token = command_add_token
        self.__command_delete_token = command_delete_token
        self.__command_delete_all = command_delete_all
        self.__no_firstname = no_firstname
        self.__no_lastname = no_lastname

    @property
    def button(self) -> int:
        """
        Gibt die Pinnummer zurück, an welcher der Button angeschlossen ist.
        Mit diesem Button kann ein Klingelereignis simuliert werden.

        @return: Die Pinnummer an welcher der Button angeschlossen ist.
        @rtype: int
        """
        return self.__button

    @property
    def pin_red(self) -> int:
        """
        Gibt die Pinnummer zurück, an welcher die rote LED angeschlossen ist.

        @return: Die Pinnummer an welcher die rote LED angeschlossen ist.
        @rtype: int
        """
        return self.__pin_red

    @property
    def pin_green(self) -> int:
        """
        Gibt die Pinnummer zurück, an welcher die grüne LED angeschlossen ist.

        @return: Die Pinnummer an welcher die grüne LED angeschlossen ist.
        @rtype: int
        """
        return self.__pin_green

    @property
    def pin_yellow(self) -> int:
        """
        Gibt die Pinnummer zurück, an welcher die gelbe LED angeschlossen ist.

        @return: Die Pinnummer an welcher die gelbe LED angeschlossen ist.
        @rtype: int
        """
        return self.__pin_yellow

    @property
    def sleep_after_ring(self) -> int:
        """
        Gibt die Zeitspanne zurück, in der nach einem Klingelereignis bei betätigung des Klingeltasters kein weiteres
        Klingelereignis ausgelöst werden soll.

        @return: Die Zeitspanne, in der kein weiteres Klingelereignis auftreten soll.
        @rtype: int
        """
        return self.__sleep_after_ring

    @property
    def admin(self) -> AuthenticatedUser:
        """
        Gibt den Admin wieder, welcher auf den Server zugreifen kann.

        @return: Admin wieder, welcher auf den Server zugreifen kann.
        @rtype: AuthenticatedUser
        """
        return self.__admin

    @property
    def path_project(self) -> str:
        """
        Gibt den Pfad zu dem Verzeichnis mit dem Projektordner wieder.

        @return: Der Pfad zu dem Projektordner.
        @rtype: str
        """
        return self.__path_project

    @property
    def path_pem(self) -> str:
        """
        Gibt den Pfad zu der .pem Datei wieder.

        @return: Der Pfad zu der .pem Datei.
        @rtype: str
        """
        return self.__path_project + self.__path_pem

    @property
    def path_key(self) -> str:
        """
        Gibt den Pfad zu der .key Datei wieder.

        @return: Der Pfad zu der .key Datei.
        @rtype: str
        """
        return self.__path_project + self.__path_key

    @property
    def ip_address(self) -> str:
        """
        Gibt die IP-Adresse des Pi wieder.

        @return: Die IP-Adresse des Pis.
        @rtype: str
        """
        return self.__ip_address

    @property
    def path_valid_tokens(self) -> str:
        """
        Gibt den Pfad zu der txt Datei mit den validen Tokens wieder.

        @return: Der Pfad zu den validen Tokens.
        @rtype: str
        """
        return self.__path_project + self.__path_valid_tokens


    @property
    def app_socket_port(self) -> int:
        """
        Gibt den Port des Sockets zurück, über den Anfragen an den ServerAdapterFromPythonFilemanager gestellt werden
        können.

        @return: Den Port des Sockets, über den Anfragen an den ServerAdapterFromPythonFilemanager gestellt werden
        können
        @rtype: int
        """
        return self.__app_socket_port

    @property
    def app_request_pattern(self) -> str:
        """
        Gibt den Regex zurück welchem eine Anfrage an den ServerAdapterFromPythonFilemanager genügen muss.

        @return: den Regex für eine Anfrage an dem ServerAdapterFromPythonFilemanager
        @rtype: str
        """
        return self.__app_request_pattern

    @property
    def app_encoding(self) -> str:
        """
        Gibt die Kodierung zurück mit dem eine Anfrage an dem ServerAdapterFromPythonFilemanager codiert wird.

        @return: die Kodierung für eine Anfrage an dem ServerAdapterFromPythonFilemanager
        @rtype: str
        """
        return self.__app_encoding

    @property
    def app_socket_buf_size(self) -> int:
        """
        Gibt die Buffergröße für eine Anfrage an dem ServerAdapterFromPythonFilemanager zurück

        @return: die Buffergröße für eine Anfrage an dem ServerAdapterFromPythonFilemanager
        @rtype: int
        """
        return self.__app_socket_buf_size

    @property
    def command_search(self) -> str:
        """
        Gibt das Kommando für das Suchen nach einem Nutzer in dem ServerAdapterFromPythonFilemanager zurück.

        @return: das Kommando für das Suchen nach einem Nutzer in dem ServerAdapterFromPythonFilemanager
        @rtype: str
        """
        return self.__command_search

    @property
    def command_add_token(self) -> str:
        """
        Gibt das Kommando für das Hinzufügen von einem Token zu einem Nutzer in dem ServerAdapterFromPythonFilemanager
        zurück.

        @return: das Kommando für das Hinzufügen von einem Token zu einem Nutzer in dem
        ServerAdapterFromPythonFilemanager
        @rtype: str
        """
        return self.__command_add_token

    @property
    def command_delete_token(self) -> str:
        """
        Gibt das Kommando für das Entfernen eines Tolkens von einem Nutzer in dem ServerAdapterFromPythonFilemanager
        zurück.

        @return: das Kommando für das Entfernen eines Tolkens von einem Nutzer in dem
        ServerAdapterFromPythonFilemanager
        @rtype: str
        """
        return self.__command_delete_token

    @property
    def command_delete_all(self) -> str:
        """
        Gibt das Kommando für das Entfernen aller Tolkens eines Nutzers in dem ServerAdapterFromPythonFilemanager
        zurück.

        @return: das Kommando für das Entfernen aller Tolkens eines Nutzers in dem
        ServerAdapterFromPythonFilemanager
        @rtype: str
        """
        return self.__command_delete_all

    @property
    def no_firstname(self) -> str:
        """
        Gibt die Repräsentation für einen nicht vorhandenen Vornamen zurück.

        @return: die Repräsentation für einen nicht vorhandenen Vornamen
        @rtype: str
        """
        return self.__no_firstname

    @property
    def no_lastname(self) -> str:
        """
        Gibt die Repräsentation für einen nicht vorhandenen Nachnamen zurück.

        @return: die Repräsentation für einen nicht vorhandenen Nachnamen
        @rtype: str
        """
        return self.__no_lastname
