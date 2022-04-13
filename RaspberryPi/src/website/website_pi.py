import sys

# Hier Pfad einfügen:
sys.path.append("")

import socket
from flask import Flask

app = Flask(__name__)


@app.route('/opendoor/')
def openDoor():
    """Sendet das OpenDoor Signal mit Unix Sokets an das Main Programm."""
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect(("localhost", 10000))
    s.send(str.encode("send_open"))
    s.close()

    return "Open Door"


@app.route('/clear_history_info/', methods=['Post', 'Get'])
def log_clear_history_info():
    """Löscht den Verlauf des Logs mit der Stufe info."""
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect(("localhost", 10000))
    s.send(str.encode("info"))
    s.close()

    return "Clear info"


@app.route('/clear_history_error/', methods=['Post', 'Get'])
def log_clear_history_error():
    """Löscht den Verlauf des Logs mit der Stufe error."""
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect(("localhost", 10000))
    s.send(str.encode("error"))
    s.close()

    return "Clear error"


@app.route('/clear_history_fatal/', methods=['Post', 'Get'])
def log_clear_history_fatal():
    """Löscht den Verlauf des Logs mit der Stufe fatal."""
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect(("localhost", 10000))
    s.send(str.encode("fatal"))
    s.close()

    return "Clear fatal"


if __name__ == "__main__":
    app.run(host="0.0.0.0")

