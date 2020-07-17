from modules.webserver import webserver
import com
from threading import Thread


def updateLED():
    com.send(webserver.buffer)


t = Thread(target=updateLED)
t.daemon = True
t.start()
