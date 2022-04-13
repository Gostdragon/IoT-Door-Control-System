from RaspberryPi.src.data_model.door import DoorDataStorage
from RaspberryPi.src.door_controller.door_control_handler.oberver import Observer
from RaspberryPi.src.door_controller.server_adapter.server_adapter import ServerAdapter
from RaspberryPi.src.data_model.configuration import PiConfiguration
from RaspberryPi.src.data_model.user import UnauthenticatedUser

"""
Dieses Modul ist Teil des Beobachter-Design-Patterns. Es implementiert einen konkreten Beobachter.
Classes:
    TokenUpdater: Diese Klasse ist dafür zuständig die Liste der für eine Tür autorisierten Tokens zu aktualisieren.
        Sie implementiert die abstrakte Klasse Observer und alle abstrakten Methoden dieser.

@author Lukas Wittenzellner
@version 1.0
"""


class TokenUpdater(Observer):
    """
    Diese Klasse ist dafür zuständig die Liste der für eine Tür autorisierten Tokens zu aktualisieren.
    Sie implementiert die abstrakte Klasse Observer und alle abstrakten Methoden dieser
    Methods:
        update: Aktualisiert die Liste der Tokens der zugehörigen Tür
        getValidTokens: gibt die Liste der autorisierten Tokens einer Tür zurück
    """

    def __init__(self, doorDataStorage: DoorDataStorage, serverAdapter: ServerAdapter):
        """
        Konstruktor für eine TokenUpdater Instanz. Beim Erstellen muss eine der Datenspeicher einer Tür übergeben werden.
        :param doorDataStorage: Ist der Datenspeicher zu einer zugehörigen Tür.
        :type doorDataStorage: DoorDataStorage.
        """
        self.doorDataStorage = doorDataStorage
        self.serverAdapter = serverAdapter

    def update(self) -> None:
        """
        Aktualisiert die Liste der Tokens der zugehörigen Tür
        """
        xor = set(self.doorDataStorage.doorTokens) ^ set(self.getValidTokens())
        for x in xor:
            if x in self.doorDataStorage.doorTokens:
                self.doorDataStorage.deleteToken(x)
            else:
                self.doorDataStorage.addToken(x)

    def getValidTokens(self) -> list:
        """
        Gibt die Liste der autorisierten Tokens einer Tür zurück.
        :return: Eine Liste aller Tokens.
        :rtype: Liste von Tokens.
        """
        admin = PiConfiguration().admin
        return self.serverAdapter.get_all_valid_tokens(UnauthenticatedUser(admin.name, admin.identifier),
                                                       admin.password)