import paho.mqtt.client as mqtt
from RaspberryPi.src.data_model.configuration import MQTTProtocolConfiguration

"""
Dieses Modul kapselt Klassen, mithilfe deren Signale zwischen bestimmten (physischen)
Komponenten im Türsteuerungssystem (z.B. dem Hauptcontroller und dem Controller
für die akustische Klingel) übers WLAN gesendet werden können.
Diese Klassen realisieren das Message Queuing Telemetry Transport (MQTT) Client-Server-Protokoll 
für Machine-to-Machine-Kommunikation, das die Übertragung von Daten in Form von Nachrichten 
zwischen Geräten ermöglicht.

Classes: 
    MQTTClient: Repräsentiert einen MQTT-Client, der die Rolle eines Subscribers und/oder
                eines Publishers einnehmen und Signale an andere MQTT-Clients über einen Vermittler 
                (sogenannten "Broker") senden bzw. Signale von anderen MQTT-Clients empfangen kann. 
    MQTTPublisher: Repräsentiert einen MQTT-Client, der über den Broker Nachrichten 
                   zu einem bestimmten Topic an alle MQTT-Clients senden kann, die dieses Topic abonniert haben.
    MQTTSubscriber: Repräsentiert einen MQTT-Client, der ein (oder mehrere) Topics abonnieren kann 
                    und dann automatisch vom Server (Broker) benachrichtigt wird, sobald ein MQTT-Publisher
                    eine Nachricht zu einem dieser Topics publiziert hat. 

@author Ahmad Eynawi
@version 16.02.2022
"""


class MQTTClient:
    """
    Diese Klasse repräsentiert einen MQTT-Client.

    Ein MQTT-Client kann Nachrichten an andere MQTT-Clients übers MQTT-Protokoll senden
    und/oder benachrichtigt werden, wenn andere MQTT-Clients Nachrichten zu bestimmten
    Topics über den MQTT-Broker gesendet haben.

    Attributes:
        mqttConfig (:class:`~configuration.MQTTProtocolConfiguration`):
                    Die Konfigurationsdaten des MQTT-Protokolls für diesen MQTT-Client.
        on_connect ((client, userdata, flags, resultCode) -> None):
                    Diese Methode definiert die Aktionen, die der Client ausführt, wenn er
                    eine CONNACK-Antwort (Verbindungsaufbau-Bestätigung) vom MQTT-Broker erhält.
        on_message ((client, userdata, message) -> None):
                    Diese Methode definiert die Aktionen, die der MQTT-Client ausführt, wenn er
                    eine Nachricht zu einem der von ihm abonnierten Topics erhält.

    Methods:
        run: Startet den MQTT-Client mit einer Endlosschleife, in der auf das Eintreffen
             von Nachrichten zu bestimmten Topics gewartet bzw. reagiert wird.
        __init__: Konstruktor der Klasse :class:`~mqtt_protocol.MQTTClient`
    """

    def __init__(self, mqttConfig: MQTTProtocolConfiguration, on_connect, on_message=None):
        """
        Konstruktor der Klasse :class:`~mqtt_protocol.MQTTClient`.

        Erstellt und initialisiert einen neuen MQTT-Client, der Nachrichten mit anderen MQTT-Clients
        übers MQTT-Protokoll austauschen kann.

        @param mqttConfig: Die Konfigurationsdaten des MQTT-Protokolls für diesen MQTT-Client.
        @type mqttConfig: :class:`~configuration.MQTTProtocolConfiguration`
        @param on_connect: Diese Methode definiert die Anweisungen, die ausgeführt werden müssen, wenn
                           der Client sich nach einem Verbindungsaufbauwunsch erfolgreich mit dem Server (Broker)
                           verbinden konnte.
        @type on_connect: on_connect(client, userdata, flags, resultCode) -> None
        """
        self._mqttConfig = mqttConfig

        # Erstellt einen MQTT-Client und weist ihm die entsprechenden Funktionen zu.
        self._client = mqtt.Client()
        self._client.on_connect = on_connect
        self._client.on_message = on_message
        self._client.username_pw_set(mqttConfig.username, mqttConfig.password)
        self._client.connect(mqttConfig.broker, mqttConfig.port,
                             mqttConfig.keepalive)

    def run(self):
        """
        Startet den MQTT-Client mit einer Endlosschleife, in der auf das Eintreffen
        von Nachrichten zu bestimmten Topics gewartet bzw. reagiert wird.

        Diese Methode ruft bestimmte Netzwerkschleifenfunktionen in einer endlosen Sperrschleife auf
        und sendet entsprechende Rückrufe, wenn der Client z.B. eine Nachricht zu einem
        der von ihm abonnierten Topics bekommt.
        Sie sorgt auch für Wiederverbindung im Falle einer Verbindungsunterbrechung.
        """
        self._client.loop_forever()


class MQTTPublisher(MQTTClient):
    """
    Diese Klasse repräsentiert einen MQTT-Publisher.

    Ein MQTT-Publisher kann Nachrichten zu bestimmten Topics übers MQTT-Protokoll publizieren,
    die dann durch den Broker an alle Clients, die diese Topics abonniert haben,
    weitergeleitet werden.

    Attributes:
        mqttConfig (:class:`~configuration.MQTTProtocolConfiguration`):
                    Die Konfigurationsdaten des MQTT-Protokolls für diesen MQTT-Publisher.
        on_connect (on_connect(client, userdata, flags, resultCode) -> None):
                    Diese Methode definiert die Aktionen, die der MQTT-Publisher ausführt, wenn er
                    eine CONNACK-Antwort (Verbindungsaufbau-Bestätigung) vom MQTT-Broker erhält.

    Methods:
        publish: Veröffentlicht eine Nachricht zu einem Topic. Dies bewirkt,
                 dass diese Nachricht an den Broker und anschließend von dem Broker an
                 alle Clients gesendet wird, die dieses Topic bereits abonniert haben.
        __init__: Konstruktor der Klasse :class:`~mqtt_protocol.MQTTPublisher`
    """

    def __init__(self, mqttConfig: MQTTProtocolConfiguration, on_connect):
        """
        Konstruktor der Klasse :class:`~mqtt_protocol.MQTTPublisher`.

        Erstellt und initialisiert einen neuen MQTT-Publisher, der Nachrichten an MQTT-Clients
        zu bestimmten Topics übers MQTT-Protokoll senden kann.

        @param mqttConfig: Die Konfigurationsdaten des MQTT-Protokolls für diesen MQTT-Publisher.
        @type mqttConfig: :class:`~configuration.MQTTProtocolConfiguration`
        @param on_connect: Diese Methode definiert die Anweisungen, die ausgeführt werden müssen, wenn
                           der MQTT-Publisher sich nach einem Verbindungsaufbauwunsch erfolgreich
                           mit dem Server (Broker) verbinden konnte.
        @type on_connect: (client, userdata, flags, resultCode) -> None
        """
        super().__init__(mqttConfig, on_connect)

    def publish(self, topic: str, payload: str, qualityOfService=0, retainMessage=False):
        """
        Veröffentlicht eine Nachricht vom MQTT-Publisher zu einem Topic.

        Wird eine Nachricht von einem MQTT-Publisher publiziert, dann leitet der Broker
        diese Nachricht an alle Clients weiter, die dieses Topic bereits abonnieren haben.

        @param topic: Thema: Das Thema, zu dem die Nachricht veröffentlicht werden soll.
        @type topic: str
        @param payload: Die tatsächlich zu sendende Nachricht. Wenn nicht angegeben oder auf
                        "None" gesetzt, wird eine Nachricht mit der Länge Null verwendet.
        @type payload: str
        @param qualityOfService: Das zu verwendende Dienstgüteniveau. Das kann die Werte 0, 1
                                 oder 2 annehmen.
                                 Hierbei bedeutet die Dienstgüte 0, dass der Empfänger den Empfang
                                 der Nachricht nicht bestätigt und dass die Nachricht höchstens einmal vom Absender
                                 gesendet und danach nicht gespeichert oder erneut übertragen wird.
                                 Dienstgüte 1 garantiert, dass eine Nachricht mindestens einmal
                                 beim Empfänger ankommt, wobei es möglich ist, dass eine Nachricht mehrmals gesendet
                                 oder zugestellt wird.
                                 Dienstgüte 2 ist die höchste Dienstebene im MQTT-Protokoll und garantiert,
                                 dass jede Nachricht nur einmal von den beabsichtigten Empfängern empfangen wird.
        @type qualityOfService: int
        @param retainMessage: Wenn auf `True` gesetzt, wird die Nachricht als "letzte bekannte gute/beibehaltene"
                              Nachricht für das Topic festgelegt.
        @type retainMessage: bool
        """
        self._client.publish(topic, payload=payload, qos=qualityOfService, retain=retainMessage)


class MQTTSubscriber(MQTTClient):
    """
    Diese Klasse repräsentiert einen MQTT-Subscriber.

    Ein MQTT-Subscriber kann ein (oder mehrere) Topics abonnieren und wird dann automatisch
    vom Server (Broker) benachrichtigt, sobald ein MQTT-Publisher eine Nachricht zu einem dieser
    Topics publiziert hat.

    Attributes:
        mqttConfig (:class:`~configuration.MQTTProtocolConfiguration`):
                    Die Konfigurationsdaten des MQTT-Protokolls für diesen MQTT-Subscriber.
        on_connect ((client, userdata, flags, resultCode) -> None):
                    Diese Methode definiert die Aktionen, die der Subscriber ausführt, wenn er
                    eine CONNACK-Antwort (Verbindungsaufbau-Bestätigung) vom MQTT-Broker erhält.
        on_message ((client, userdata, message) -> None):
                    Diese Methode definiert die Aktionen, die der MQTT-Subscriber ausführt, wenn er
                    eine Nachricht zu einem der von ihm abonnierten Topics erhält.

    Methods:
        subscribe: Abonniert das als Parameter übergeben Topic, sodass der MQTT-Subscriber
                   benachrichtigt wird, wenn MQTT-Publisher Nachrichten zu diesem
                   Topic senden.
        __init__: Konstruktor der Klasse :class:`~mqtt_protocol.MQTTSubscriber`
    """

    def __init__(self, mqttConfig: MQTTProtocolConfiguration, on_connect, on_message):
        """
        Konstruktor der Klasse :class:`~mqtt_protocol.MQTTSubscriber`.

        Erstellt und initialisiert einen neuen MQTT-Subscriber, der Topics abonnieren
        und Nachrichten zu diesen Topics von MQTT-Publishern bekommen kann.

        @param mqttConfig: Die Konfigurationsdaten des MQTT-Protokolls für diesen MQTT-Subscriber.
        @type mqttConfig: :class:`~configuration.MQTTProtocolConfiguration`
        @param on_connect: Diese Methode definiert die Anweisungen, die ausgeführt werden müssen, wenn
                           der MQTT-Subscriber sich nach einem Verbindungsaufbauwunsch erfolgreich
                           mit dem Server (Broker) verbinden konnte.
        @type on_connect: on_connect(client, userdata, flags, resultCode) -> None
        @param on_message: Diese Methode definiert die Aktionen, die der MQTT-Subscriber ausführt,
                           wenn er eine Nachricht zu einem der von ihm abonnierten Topics erhält.
        @type on_message: (client, userdata, message) -> None
        """
        super().__init__(mqttConfig, on_connect, on_message)

    def subscribe(self, topic: str):
        """
        Abonniert das als Parameter übergebene Topic.

        Wird ein Topic von einem MQTT-Subscriber abonniert, dann erhält der Subscriber
        über den MQTT-Broker automatisch alle Nachrichten, die von MQTT-Publishern
        zu diesem abonnierten Topic gesendet werden.

        @param topic: Das Thema, das der MQTT-Subscriber abonnieren will.
        @type topic: str
        """
        self._client.subscribe(topic)
