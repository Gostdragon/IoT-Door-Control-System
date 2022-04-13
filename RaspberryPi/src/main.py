import ssl
import sys
import ast

# Hier Pfad einfügen:
sys.path.append("")

import urllib.error
from gpiozero import Button, LED
import time
import threading
import socket
import slack
from slack.errors import SlackApiError
import re

from RaspberryPi.src.data_model.key_token import UnauthorizedNFCToken
from RaspberryPi.src.door_controller.bell_push_handler import BotNotifier
from RaspberryPi.src.door_controller.bell_push_handler import CameraNotifier
from RaspberryPi.src.door_controller.bell_push_handler import BellPushEventHandler
from RaspberryPi.src.door_controller.bell_push_handler import DoorbellNotifier
from RaspberryPi.src.door_controller.door_control_handler.token_validation import TokenValidation
from RaspberryPi.src.door_controller.door_control_handler.door_opener import DoorOpener
from RaspberryPi.src.door_controller.door_control_handler.nfc_reader import NFCReader
from RaspberryPi.src.door_controller.door_control_handler.user_list_updates_notifier import UserListUpdatesNotifier
from RaspberryPi.src.data_model.door import DoorDataStorage
from RaspberryPi.src.door_controller.server_adapter.server_adapter_from_python_filemanager import ServerAdapterFromPythonFilemanager
from RaspberryPi.src.data_model.identifier import Identifier
from RaspberryPi.src.door_controller.door_control_handler.token_updater import TokenUpdater
from RaspberryPi.src.door_controller.entities.log import LogFatal, LogInfo, LogError
from RaspberryPi.src.exceptions.exception import SyntaxException, ConnectionException
from RaspberryPi.src.data_model.configuration import BotConfiguration, CameraConfiguration, PiConfiguration
from RaspberryPi.src.data_model.configuration import MQTTProtocolConfiguration
from RaspberryPi.src.door_controller.entities.button import DoorOpenButtonObserver
from RaspberryPi.src.data_model.user import UnauthenticatedUser, Name
from RaspberryPi.src.data_model.name import LastName, FirstName
from RaspberryPi.src.data_model.password import Password
from RaspberryPi.src.door_controller.entities.bot import SlackBot
from RaspberryPi.src.door_controller.entities.camera import TapoCamera

"""
Dieses Modul enthält die Main Klasse, welche als Einstiegspunkt in das Türsteuerungssystem dient. 

Classes:
    Main: Die Main Klasse, welche als Einstiegspunkt in das Projekt dient.

@author Fabian Schiekel
@version 05.03.2022

@author Ahmad Eynawi
@version 19.02.2022
"""


class Main:
    """
    Diese Klasse bildet den Einstiegspunkt für das Türsteuerungsprogramm.
    Methods:
        main: Diese Methode ist der Einstiegspunkt für Türsteuerungsprogramm.
    """
    def __init__(self):
        self.__log_bot_fatal = LogFatal.get_instance()
        self.__log_bot_error = LogError.get_instance()
        self.__log_bot_info = LogInfo.get_instance()
        self.__bell_push_event_handler = BellPushEventHandler()
        self.__door_opener = DoorOpener()
        self.__door_data_storage = DoorDataStorage()
        self.__token_validation = TokenValidation(self.__door_data_storage)
        self.__user_updater = UserListUpdatesNotifier()
        self.__adapter_python = ServerAdapterFromPythonFilemanager()
        self.__reader = NFCReader()
        self.__token_updater = TokenUpdater(self.__door_data_storage, self.__adapter_python)
        self.__bot_conf = BotConfiguration()
        self.__cam_conf = CameraConfiguration()
        self.__pi_conf = PiConfiguration()
        self.__mqttConfig = MQTTProtocolConfiguration(topic=DoorOpenButtonObserver.TOPIC,
                                                      payload=DoorOpenButtonObserver.DOOR_OPEN_BUTTON_SHORT_PUSH_EVENT)
        self.button = Button(self.__pi_conf.button, pull_up=False)

    def __add_bot_notifiers(self):
        if len(self.__bot_conf.bot_msg) <= 0 | len(self.__bot_conf.bot_token) <= 0 \
                | len(self.__bot_conf.bot_channel_id) <= 0:
            return

        if len(self.__bot_conf.bot_msg) != len(self.__bot_conf.bot_token) | \
           len(self.__bot_conf.bot_msg) != len(self.__bot_conf.bot_channel_id):
            raise SyntaxException("Die Argumente sind nicht gleich lang oder besitzen ungültige Länge!")

        for i in range(len(self.__bot_conf.bot_msg)):
            try:
                # Die Attribute der Bots sind in dem Config-Modul gespeichert.
                # Referenziert werden diese über ihren Index. Das i-te Element jeder Liste gehört zum i-ten Bot.
                bot = SlackBot(self.__bot_conf.bot_token[i], self.__bot_conf.bot_channel_id[i])
                bot_notifier = BotNotifier(bot, self.__bot_conf.bot_msg[i])
            except slack.errors.SlackApiError as e:
                LogFatal.get_instance().send_log_msg("Der Bot-Token und/oder die Channel-ID ist nicht valide!\n"
                                                     + "Fehlernachricht: " + e.__repr__())
                raise SyntaxException("Der Bot-Token und/oder die Channel-ID ist nicht valide, siehe LogFatal.")
            except urllib.error.URLError:
                raise ConnectionException("Es konnte keine Verbindung zum Bot hergestellt werden!")
            self.__bell_push_event_handler.addObserver(bot_notifier)

    def __add_camera_notifiers(self):
        if len(self.__cam_conf.ip_address) <= 0 | len(self.__cam_conf.username) <= 0 \
                | len(self.__cam_conf.password) <= 0:
            return

        if len(self.__cam_conf.ip_address) != len(self.__cam_conf.password) | \
           len(self.__cam_conf.ip_address) != len(self.__cam_conf.username) | \
           len(self.__cam_conf.ip_address) != len(self.__cam_conf.time_cam_calibration) | \
           len(self.__cam_conf.ip_address) != len(self.__cam_conf.rot_angle) | \
           len(self.__cam_conf.ip_address) != len(self.__cam_conf.time_cam_rot) | \
           len(self.__cam_conf.ip_address) != len(self.__cam_conf.time_cam_aktiv):
            raise SyntaxException("Die Argumente in der Konfigurationsdatei haben nicht die gleiche Länge!")

        for i in range(len(self.__bot_conf.bot_msg)):
            # Die Attribute der Kamera sind in dem Config-Modul gespeichert.
            # Referenziert werden diese über ihren Index. Das i-te Element jeder Liste gehört zur i-ten Kamera.
            cam = TapoCamera(i)
            camera_notifier = CameraNotifier(cam)

            self.__bell_push_event_handler.addObserver(camera_notifier)

    def __add_doorbell_notifiers(self):
        doorbell_notifier = DoorbellNotifier()
        self.__bell_push_event_handler.addObserver(doorbell_notifier)

    def __runDoorOpenButtonObserver(self):
        """
        Startet den mit dem Benachrichtiger des Türöffnertasters verbundenen MQTT-Subscriber mit einer Endlosschleife,
        in der auf das Eintreffen von Nachrichten zum vordefinierten Topic für das Öffnen der Tür
        gewartet bzw. reagiert wird.
        """

        def on_connect(client, userdata, flags, resultCode):
            LogInfo.get_instance().send_log_msg("Der Beobachter des Türöffnertasters hat sich mit dem MQTT-Broker "
                                                "mit Ergebniscode " + str(resultCode) + " verbunden.")
            client.subscribe(self.__mqttConfig.topic)
            LogInfo.get_instance().send_log_msg(f"Der Beobachter des Türöffnertasters hat das Topic \""
                                                + self.__mqttConfig.topic + "\" abonniert.")

        def on_message(client, userdata, message):
            messageString = message.payload.decode()
            inputDictionary = ast.literal_eval(messageString)
            LogInfo.get_instance().send_log_msg("Der Beobachter des Türöffnertasters hat die Nachricht \"" +
                                                messageString + "\" zum Thema \"" + message.topic + "\" erhalten.")
            if inputDictionary.get(DoorOpenButtonObserver.DOOR_OPEN_BUTTON_INPUT_EVENT_IDENTIFIER) == \
                    self.__mqttConfig.payload:
                self.__door_opener.openDoor()

        doorOpenButtonObserver = DoorOpenButtonObserver(self.__mqttConfig, on_connect, on_message)
        doorOpenButtonObserver.run()

    def __add_token_updater(self):
        self.__user_updater.addObserver(self.__token_updater)

    def __process_request(self, request, lock):

        # verarbeitet eine Anfrage
        match = re.fullmatch(self.__pi_conf.app_request_pattern, request)
        if not match:
            return ""

        command, admin_id, admin_password, uid, token_id = match.groups()

        admin = UnauthenticatedUser(Name(FirstName(self.__pi_conf.no_firstname), LastName(self.__pi_conf.no_lastname)),
                                    Identifier(admin_id))
        password = Password(admin_password)
        user = UnauthenticatedUser(Name(FirstName(self.__pi_conf.no_firstname), LastName(self.__pi_conf.no_lastname)),
                                   Identifier(uid))
        token = UnauthorizedNFCToken(Identifier(token_id)) if token_id is not None else None

        with lock:
            if command == self.__pi_conf.command_search:
                result = ServerAdapterFromPythonFilemanager().get_user(admin, password, user)
                return result
            elif command == self.__pi_conf.command_add_token and token is not None:
                ServerAdapterFromPythonFilemanager().add_token_to_user(admin, password, user, token)
            elif command == self.__pi_conf.command_delete_token and token is not None:
                ServerAdapterFromPythonFilemanager().delete_token_from_user(admin, password, user, token)
            elif command == self.__pi_conf.command_delete_all:
                ServerAdapterFromPythonFilemanager().delete_all_tokens_from_user(admin, password, user)
            return ""

    def __communicate(self, connection, lock):
        # verarbeitet die Kommunikation mit einer einzelnen Verbindung
        with connection:
            while True:
                try:
                    data = connection.recv(self.__pi_conf.app_socket_buf_size)
                except ConnectionResetError:
                    # Klient nicht mehr erreichbar
                    break
                if not data:
                    # Klient schließt Verbindung
                    break
                resp = self.__process_request(data.decode(self.__pi_conf.app_encoding).strip('\n'), lock)
                connection.sendall((resp + '\n').encode(self.__pi_conf.app_encoding))

    def __start_app_socket(self):
        # nimmt Anfragen der App entgegen
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(self.__pi_conf.path_pem, self.__pi_conf.path_key)
        lock = threading.Lock()
        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("", self.__pi_conf.app_socket_port))
            server_socket.listen()
            with context.wrap_socket(server_socket, server_side=True) as tls_server_socket:
                while True:
                    try:
                        connection, address = tls_server_socket.accept()
                        # die Kommunikation mit jeder Verbindung wird parallel behandelt
                        threading.Thread(target=self.__communicate, args=(connection, lock)).start()
                    except ssl.SSLError:
                        # Verifikation des Zertifikats des Klienten fehlgeschlagen
                        pass

    def main(self):
        """
        Diese Methode ist der Einstiegspunkt für Türsteuerungsprogramm. Sie fügt alle Observer den Subjekten hinzu und
        wartet anschließend auf ein Eingangssignal.

        @return: none
        """
        self.__add_bot_notifiers()
        self.__add_doorbell_notifiers()
        self.__add_camera_notifiers()

        self.__add_token_updater()
        self.__user_updater.setState()

        self.__wait_for_event()

    def __wait_for_event(self):
        door_opener = self.__door_opener
        log_bot_info = self.__log_bot_info
        log_bot_fatal = self.__log_bot_fatal
        log_bot_error = self.__log_bot_error
        door_data_storage = self.__door_data_storage
        user_updater = self.__user_updater

        class ThreadUpdateValidToken(threading.Thread):
            """
            Diese Klasse repräsentiert ein Thread, der für eine periodische Aktualisierung der validen Tokens sorgt.
            Dies ist notwendig, da die Nutzerverwaltung von außerhalb unseres Systems passiert und sich somit die Tokens
            auch ohne unser Wissen ändern können.

            Methods:
                run: Die run Methode des Threads, sie wird beim Start des Threads aufgerufen.
            """

            def __init__(self, updater: TokenUpdater):
                threading.Thread.__init__(self)
                self.daemon = False
                self.token_updater = updater

            def run(self):
                while True:
                    # Aktualisiert die validen Tokens der Tür dreimal am Tag.
                    # Hier nur die Aktualisierung der Tokens dieser Tür nicht aller über den Notifier verbundenen Türen,
                    # da diese ja selber eine Aktualisierung besitzten.
                    time.sleep(28800)
                    self.token_updater.update()

        class ThreadReadToken(threading.Thread):
            """
            Diese Klasse repräsentiert ein Thread, der den Token einließt.

            Methods:
                run: Die run Methode des Threads, sie wird beim Start des Threads aufgerufen.
            """

            def __init__(self, reader: NFCReader):
                threading.Thread.__init__(self)
                self.daemon = False
                self.reader = reader
                user_updater.setState()

            def run(self):
                log_bot_info.send_log_msg("Token lesen...")

                token = self.reader.readToken()
                user_updater.setState()
                __token_validation = TokenValidation(door_data_storage)

                valid = __token_validation.validateToken(UnauthorizedNFCToken(Identifier(token.hexdigest())))

                if valid:
                    log_bot_info.send_log_msg("Der Token ist gültig")
                    door_opener.openDoor()
                else:
                    led = LED(pin=PiConfiguration().pin_red)
                    led.on()
                    log_bot_info.send_log_msg("Der Token ist ungültig")
                    time.sleep(5)
                    led.off()
                    led.close()

                time.sleep(2)

        class ThreadSocket(threading.Thread):
            """
            Diese Klasse repräsentiert ein Thread, der auf ein Eingangssignal von dem Webserver wartet.

            Methods:
                run: Die run Methode des Threads, sie wird beim Start des Threads aufgerufen.
            """

            def __init__(self):
                threading.Thread.__init__(self)
                self.daemon = False

            def run(self):
                s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("", 10000))
                s.listen(1)

                connection, address = s.accept()
                resp = connection.recv(1024).__repr__().strip('b' '\'')

                if resp == "fatal":
                    log_bot_fatal.clear_log_history()
                elif resp == "error":
                    log_bot_error.clear_log_history()
                elif resp == "info":
                    log_bot_info.clear_log_history()
                elif resp == "send_open":
                    door_opener.openDoor()
                else:
                    LogError.get_instance().send_log_msg("Kein Log mit dieser Logstufe vorhanden!")

        # Ein Thread für das Einlesen von Tokens über den NFC-Reader
        thread_read_token = ThreadReadToken(self.__reader)
        thread_read_token.start()

        # Ein Thread für den UNIX Socket, damit das Signal über das WebsitePi Programm weiter geleitet werden kann.
        thread_socket_website = ThreadSocket()
        thread_socket_website.start()

        # Ein Thread um mit der App zu kommunizieren.
        threading.Thread(target=self.__start_app_socket, daemon=True).start()

        # Ein Thread um die validen Tokens zyklisch zu aktualisieren.
        thread_update_token = ThreadUpdateValidToken(self.__token_updater)
        thread_update_token.start()

        # Ein Thread für die Ausführung des Codes für den Türöffnertaster
        doorOpenButtonThread = threading.Thread(target=self.__runDoorOpenButtonObserver)

        # Startet einen neuen Thread, der in einer Endlosschleife auf das Eintreffen
        # eines Signals vom Türöffnertaster wartet und dann ein Signal an das Türschloss
        # zum Öffnen der Tür sendet
        doorOpenButtonThread.start()

        self.__log_bot_info.send_log_msg("Die Initialisierung des Systems wurde erfolgreich abgeschlossen.")
        while True:
            time.sleep(0.1)
            if self.button.wait_for_active(0.1):
                self.__bell_push_event_handler.setState()
                time.sleep(self.__pi_conf.sleep_after_ring)

            if not thread_read_token.is_alive():
                # Falls ein Token eingelesen wurde, wird der Thread wieder neu gestartet.
                thread_read_token = ThreadReadToken(self.__reader)
                thread_read_token.start()

            if not thread_socket_website.is_alive():
                # Falls eine Nachricht vom Webserver gesendet wurde, wird der Thread wieder neu gestartet.
                time.sleep(0.5)
                thread_socket_website = ThreadSocket()
                thread_socket_website.start()


if __name__ == '__main__':
    main = Main()
    main.main()
