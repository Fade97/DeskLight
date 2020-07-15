import serial
import sys


def send(buffer):
    ser = serial.Serial('COM8', 115200)
    ch = b''
    while(True):
        while (ch.find(b'XON') <= 0):
            ch = ser.read()
            if (ch == b'<'):
                ch2 = b''
                while (ch2 != b'>'):
                    ch2 = ser.read()
                    ch += ch2
                if (ch != b'<XON>' and ch != b'<XOFF>'):
                    print(ch)

        while (ch.find(b'XOFF') <= 0):
            if (len(buffer) > 0):
                ser.write(buffer[0].encode('ASCII'))
                # print(buffer[0])
                buffer.remove(buffer[0])
            ch = ser.read()
            if (ch == b'<'):
                ch2 = b''
                while (ch2 != b'>'):
                    ch2 = ser.read()
                    ch += ch2
                if (ch != b'<XON>' and ch != b'<XOFF>'):
                    print(ch)
