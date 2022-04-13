#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import hashlib

"""
Dieses Modul ist für das Einlesen und Beschreiben von NFC-Tokens zuständig

Attributes:
    reader: SimpleMFRC522(): Ist das NFC-Lesegerät, das zum lesen und schreiben benutzt wird
    
@author Lukas Wittenzellner
"""

reader = SimpleMFRC522()


class NFCReader:
    """
    Diese Klasse repräsentiert ein physisches NFC-Lesegerät

    Methods:
        readToken: Beim Aufruf dieser Methode fängt das Lesegerät zu lesen
    """

    def readToken(self):
        """
        Beim Aufruf dieser Methode fängt das Lesegerät zu lesen. Die gelesene Token-Id wird dann gehasht.
        Falls das Lesen fehlschlägt, wird eine Fehlermeldung weitergegeben.

        @returns: die gelesene und gehashte id des Tokens als Hashobjekt
        """
        token_id, text = reader.read()
        token_id_hex = hex(int(token_id.__repr__()))
        # readToken() ließt 2 Stellen zu viel, deshalb wird das verkürzt.
        token_id_hex_s = token_id_hex[2: len(token_id_hex.__repr__()) - 4: 1]
        obj_256 = hashlib.sha256(token_id_hex_s.encode())

        return obj_256


