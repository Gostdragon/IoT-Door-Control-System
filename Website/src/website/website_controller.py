import cv2
from flask import Flask, render_template, redirect, Response
import requests
import sys

# Hier Pfad einfügen:
sys.path.append("")

from Website.src.data_model.configuration import CameraConfiguration
from Website.src.data_model.configuration import PiConfiguration

app = Flask(__name__)
cam_conf = CameraConfiguration()
pi_conf = PiConfiguration()

"""Ist die URL der WLAN Kamera"""
camera_link = "rtsp://" + cam_conf.username[0].firstName.firstName + ":" + cam_conf.password[0].password + "@" + \
              cam_conf.ip_address[0] + ":554/stream1"


def gen_frames():
        """Diese Methode generiert den Videostream für die Webseite aus camera"""
        camera = cv2.VideoCapture(camera_link)
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def main():
    """Diese Methode zeigt die Ansicht der Webseite"""
    return render_template('main.html')


@app.route('/camera_feed')
def camera_feed():
    """Diese Methode zeigt die Ansicht des Videostreams"""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/button/', methods=["POST"])
def button():
    """Diese Methode sendet das Signal von der Webseite an den DoorOpener um die Tür zu öffnen"""
    open_door()
    return redirect('/')


def open_door():
    """Diese Methode sendet das Signal von der Webseite an den DoorOpener um die Tür zu öffnen"""
    requests.get("http://" + pi_conf.ip_address + ":5000/opendoor")
    return 200


if __name__ == '__main__':
    app.run(host="0.0.0.0")
