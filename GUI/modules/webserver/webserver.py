from flask import Flask
from threading import Thread
import threading
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(__file__))))
import com


buffer = ['<1,255,0,32>',
          '<1,0,0,255>']


def inBuffer(command):
    com.inBuffer(command)


def updateLED():
    com.synced()


def create_app():
    t = Thread(target=updateLED, name='Updater')
    t.daemon = True
    t.start()
    app = Flask(__name__)

    from main import bp_main
    app.register_blueprint(bp_main)

    from modules import bp_modules
    app.register_blueprint(bp_modules)

    app.run(host='0.0.0.0', port='5000')


if __name__ == '__main__':
    create_app()
