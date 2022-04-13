# Concrete Subject to be observed
from RaspberryPi.src.door_controller.door_control_handler.subject import Subject

"""
Ist Teil des Beobachter-Design-Patterns. Es realisiert ein konkretes Subjekt, das beobachtet werden kann.
Classes:
    UserListUpdatesNotifier: Diese Klasse erbt von der abstrakten Klasse Subject. Sie ist dafür zuständig,
        bei einer Änderung der Liste der Nutzer und zugehörigen Tokens alle Beobachter zu benachrichtigen.
        
@author Lukas Wittenzellner
@version 1.0
"""


class UserListUpdatesNotifier(Subject):
    """
    Diese Klasse erbt von der abstrakten Klasse Subject. Sie ist dafür zuständig,
    bei einer Änderung der Liste der Nutzer und zugehörigen Tokens alle Beobachter zu benachrichtigen.

    Methods:
        setState: Informiert die Beobachter dieses Subjektes, dass es eine Änderung stattfand.
    """

    def setState(self) -> None:
        """
        Informiert die Beobachter dieses Subjektes, dass es eine Änderung stattfand.
        """
        super().notifyObservers()
