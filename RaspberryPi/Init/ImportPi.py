"""
Importiert die notwendigen Biliotheken und überprüft, ob der import erfolgreich war.
"""

try:
    import ssl
    import sys
    import ast
    import urllib.error
    from gpiozero import Button, LED
    import time
    import threading
    import socket
    import slack
    from slack.errors import SlackApiError
    import re
    import paho.mqtt.client as mqtt
    from typing_extensions import Final
    from mfrc522 import SimpleMFRC522
    import hashlib
    from abc import ABC, abstractmethod
    import os
    import pygame
    import threading
    import requests
    import socket
    from flask import Flask

except:
    print("Fehlende Bibliothek(n): \n", sys.exc_info())
    raise
print("Installieren der Bibliotheken abgeschlossen.")
