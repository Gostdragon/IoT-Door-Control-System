"""
Importiert die notwendigen Biliotheken und überprüft, ob der import erfolgreich war.
"""

try:
    import cv2
    from flask import Flask, render_template, redirect, Response
    import requests
    import sys
except:
    print("Fehlende Bibliothek(n): \n", sys.exc_info())
    raise
print("Installieren der Bibliotheken abgeschlossen.")
