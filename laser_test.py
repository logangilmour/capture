import time
import picamera
import serial


with picamera.PiCamera() as camera:
    laser = serial.Serial(
        port='/dev/ttyS0',
        baudrate='19200',
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    laser.write(b'O')
    laser.flush()
    print(laser.readline())
    laser.write(b'D')
    laser.flush()
    print(laser.readline())