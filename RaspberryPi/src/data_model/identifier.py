"""
Dieses Modul kapselt alle Klassen, die für die Darstellung und Überprüfung
der im Türsteuerungssystem verwendeten Identifikatoren zuständig sind.

Classes:
    Identifier: Repräsentiert den Identifikator für eine eindeutig identifizierbare
    Entität (z.B. Schlüsseltoken oder Türnutzer) im Türsteuerungssystem.

@author Ahmad Eynawi
@version 26.01.2022
"""


class Identifier:
    """
    Diese Klasse kapselt einen Identifikator zur manipulationssicheren Identifikation
    von Entitäten (z.B. Schlüsseltoken oder Türnutzer) im Türsteuerungssystem.
    Erstellte Identifier-Objekte können nach der Initialisierung nicht mehr verändert werden.

    Attributes:
        identifier (str): Der String, der einen Nutzer eindeutig identifiziert
                          und den Identifikator eines Nutzers bildet.

    Methods:
        identifier: Gibt den als String gespeicherten Identifikator zurück.
        __init__: Konstruktor der Klasse :class:`~identifier.Identifier`
        __repr__: Gibt eine String-Repräsentation für dieses Identifier-Objekt zurück.
        __eq__: Vergleicht dieses Identifier-Objekt mit einem anderen Objekt.
        __hash__: Berechnet einen Hashwert für dieses Identifier-Objekt.
    """

    def __init__(self, identifier: str):
        """
        Konstruktor der Klasse :class:`~identifier.Identifier`.

        Erstellt und initialisiert einen neuen Identifikator, mit dem eine Entität
        im Türsteuerungssystem eindeutig identifiziert werden kann.

        @param identifier: Der String, der eine Entität im Türsteuerungssystem eindeutig
                           identifiziert.
        @type identifier: str
        """
        self.__identifier = identifier

    @property
    def identifier(self):
        """
        Get-Methode für den in diesem Identifier-Objekt gespeicherten Identifikationsstring.

        @return: Den in diesem Identifier-Objekt gespeicherten Identifikationsstring.
        @rtype: str
        """
        return self.__identifier

    def __repr__(self):
        """
        Erzeugt eine textuelle Darstellung für dieses Identifier-Objekt und gibt diese
        Darstellung als String zurück.

        @return: Die String-Repräsentation dieses Identifier-Objekts.
        @rtype: str
        """
        return f"{self.__identifier}"

    def __eq__(self, other: object):
        """
        Vergleicht dieses Identifier-Objekt mit dem Objekt `other`.

        Zwei Identifier-Objekte werden als gleich betrachtet, wenn sie den gleichen
        Identifikationsstring speichern.

        @param other: Das Objekt, das mit diesem Identifier-Objekt verglichen werden soll.
        @type other: object
        @return: `True`, wenn das Objekt `other` auch eine Instanz der Klasse
        :class:`~identifier.Identifier` ist und die beiden Objekte im oben genannten Sinne
        gleich sind; andernfalls `False`.
        @rtype: bool
        """
        if self is other:
            return True
        return isinstance(other, Identifier) and self.identifier == other.identifier

    def __hash__(self):
        """
        Gibt einen Hashwert für dieses Identifier-Objekt zurück.

        Der Hashwert wird anhand des in diesem Identifier-Objekt gespeicherten
        Identifikationsstrings berechnet.

        @return: Den für dieses Identifier-Objekt berechneten Hashwert.
        @rtype: int
        """
        return hash(self.identifier)

