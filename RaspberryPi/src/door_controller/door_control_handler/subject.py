# Subject abstract Class
from abc import ABC, abstractmethod
from RaspberryPi.src.door_controller.door_control_handler.oberver import Observer
from RaspberryPi.src.door_controller.entities.log import LogError

"""
Dieses Modul dient zur Umsetzung des Beobachter-Design-Patterns. Ein Subjekt ist eine Klasse,
die von Beobachtern beobachtet werden kann.
Classes:
    Subject: Diese abstrakte Klasse ist der Grundbaustein für ein Subjekt, das beobachtet werden kann von Beobachtern.
    
@author Lukas Wittenzellner
@version 1.0
"""


class Subject(ABC):
    """
    Diese abstrakte Klasse ist der Grundbaustein für ein Subjekt, das beobachtet werden kann von Beobachtern

    Methods:
        addObserver: fügt dem Subjekt einen Beobachter hinzu
        deleteObserver: löscht einen Beobachter aus der Liste der angemeldeten Beobachter
        notifyObservers: Informiert die Beobachter, dass es eine Änderung in dem Subjekt gab

    @:param state: Ist der Zustand des Subjekts.
    @:param observers: Ist die Liste der Beobachter dieses Subjekts.
    @:type observers: Liste von Observers.
    """

    observers = []
    state = None

    def addObserver(self, observer: Observer) -> None:
        """
        Fügt dem Subjekt einen Beobachter hinzu.

        :param observer: Ist der Beobachter, der hinzugefügt werden soll
        :type observer: Observer
        """

        if observer not in self.observers:
            self.observers.append(observer)
        else:
            LogError.get_instance().send_log_msg('Hinzufügen fehlgeschlagen: {}'.format(observer))

    def deleteObserver(self, observer: Observer) -> None:
        """
        Löscht einen Beobachter aus der Liste der angemeldeten Beobachter

        :param observer: Ist der Beobachter, der aus der Liste der Beobachter des Subjekts gelöscht werden soll
        :type observer: Observer
        """

        try:
            self.observers.remove(observer)
        except ValueError:
            LogError.get_instance().send_log_msg('Löschen fehlgeschlagen: {}'.format(observer))

    def notifyObservers(self) -> None:
        """
        Informiert die Beobachter, dass es eine Änderung in dem Subjekt gab
        """

        for observer in self.observers:
            observer.update()

    @abstractmethod
    def setState(self) -> None:
        """
        Setzt den Zustand des Subjektes
        """
        pass
