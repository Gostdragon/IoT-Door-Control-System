# Observer Interface
from abc import abstractmethod, ABC

"""
Dieses Modul ist für die Implementierung des Beobachter-Design_Pattern da.
Ein Beobachter kann über Neuigkeiten eines Subjektes informiert werden.
Classes:
    Observer: Diese abstrakte Klasse ist der Grundbaustein für das Beobachter-Design-Pattern.
        Ein konkreter Beobachter implementiert diese Klasse und ihre Methoden.
@author Lukas Wittenzellner
@version 1.0
"""


class Observer(ABC):
    """
    Diese abstrakte Klasse ist der Grundbaustein für das Beobachter-Design-Pattern.
    Ein konkreter Beobachter implementiert diese Klasse und ihre Methoden.

    Methods:
        update: Diese abstrakte Methode wird aufgerufen,
        sobald eine Veränderung in der Instanz des zu beobachtenden Objektes stattfand.
    """

    @abstractmethod
    def update(self):
        """
        Diese abstrakte Methode wird aufgerufen,
        sobald eine Veränderung in der Instanz des zu beobachtenden Objektes stattfand.
        """
        pass
