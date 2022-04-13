import requests.exceptions
from pytapo import Tapo
import time
from abc import ABC, abstractmethod

from RaspberryPi.src.exceptions.exception import ConnectionException
from RaspberryPi.src.door_controller.entities.log import LogFatal
from RaspberryPi.src.data_model.configuration import CameraConfiguration

"""
Die Klasse in diesem Modul repräsentiert ein Kamera-Objekt für eine ferngesteuerte Tür.

Classes: 
    Camera: Repräsentiert ein Kamera-Objekt für die gesteuerte Beobachtung einer ferngesteuerten Tür. 
    TapoCamera: Eine Unterklasse von Camera, repräsentiert eine Tapo Kamera.
    
@author Fabian Schiekel
@version 05.03.2022
"""


class Camera(ABC):
    __ip_address = ""
    __idx = -1

    def __init__(self, ip_address: str, idx: int):
        self.__ip_address = ip_address
        self.__idx = idx

    @abstractmethod
    def ringEvent(self) -> int:
        """
        Diese Methode signalisiert der Kamera, dass sie sich in Position begeben soll und den Livestream übertragen
        soll.

        @return: 1 Wenn die Kamera sich in Position gebracht hat und den Livestream übertragen konnte.
                -1 Wenn die Kamera sich nicht in Position bringen konnte oder den Livestream nicht übertragen konnte.
        @rtype: int

        @raise: SyntaxException: Wenn die übergebene Zeitspann negativ oder gleich null ist.
        """
        pass

    @property
    def ip_address(self) -> str:
        """
        Getter für die IP-Adresse der Kamera.

        @return: Die Ip-Adresse.
        @rtype: str
        """
        return self.__ip_address

    @property
    def idx(self) -> int:
        """
        Getter für den Index der Attribute der Kamera in dem Config-Modul.

        @return: Der Index der Kamera.
        @rtype: str
        """
        return self.__idx


class TapoCamera(Camera):
    """
    Repräsentiert ein Kamera-Objekt für die gesteuerte Beobachtung einer ferngesteuerten Tür.

    Methods:
        event: Diese Methode signalisiert der Kamera, dass sie sich in Position begeben soll und den Livestream
            übertragen soll.
    """
    def __init__(self, idx: int):
        """
        Der Konstruktor für die Klasse:class:`~Camera.Camera`.

        Erstellt und initialisert ein Camera-Objekt. Dieses Objekt speichert die IP-Adresse, Benutzernamen sowie das
        Passwort für die Kamera, die dieses Objekt repräsentiert. Es werden bei der Kamera diverse unerwünschte
        Funktionen abgeschaltet.

        @param idx: Der Index der Kameraattribute in der Configurations Datei.

        @type idx: int
        """
        try:
            if idx < 0 | len(CameraConfiguration().rot_angle) <= idx:
                LogFatal.get_instance().send_log_msg("Der Index: " + idx.__repr__() + " ist nicht valide!")

            super().__init__(CameraConfiguration().ip_address[idx], idx)
            self.__tapo = Tapo(self.ip_address, user=CameraConfiguration().username[self.idx].firstName.firstName,
                               password=CameraConfiguration().password[self.idx].password)
            self.__tapo.setPrivacyMode(False)

            self.__tapo.calibrateMotor()
            time.sleep(CameraConfiguration().time_cam_calibration[self.idx])
            # Dreht die Kamera initial weg von der Tür.
            self.__tapo.moveMotor(CameraConfiguration().rot_angle[self.idx], 0)

            self.__tapo.setPrivacyMode(True)
            self.__tapo.setMotionDetection(False)
            self.__tapo.setAlarm(False)
            self.__tapo.setAutoTrackTarget(False)
        except requests.exceptions.ConnectionError as e:
            LogFatal.get_instance().send_log_msg("Das System kann nicht mit der Kamera verbunden werden!\n"
                                                 + "Fehlernachricht: " + e.__repr__())
            raise ConnectionException("Es konnte keine Verbindung zur Kamera hergestellt werden, siehe LogFatal.")

    def ringEvent(self) -> int:
        self.__tapo.setPrivacyMode(False)
        self.__tapo.moveMotor(CameraConfiguration().rot_angle[self.idx], 0)
        time.sleep(CameraConfiguration().time_cam_aktiv[self.idx] + CameraConfiguration().time_cam_rot[self.idx])
        self.__tapo.moveMotor(-CameraConfiguration().rot_angle[self.idx], 0)
        time.sleep(CameraConfiguration().time_cam_rot[self.idx])
        self.__tapo.setPrivacyMode(True)
        return 1
