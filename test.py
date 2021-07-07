import time
import picamera
import serial
from fractions import Fraction

with picamera.PiCamera() as camera:
    
    laser = serial.Serial(
        port='/dev/ttyS0',
        baudrate='19200',
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    camera.exposure_mode = 'auto'

    camera.resolution = (4056,3040)
    camera.preview_fullscreen=False
    camera.preview_window=(0, 0, 1024, 768)
    
    camera.hflip = True
    camera.vflip = True
    camera.iso=800
    camera.framerate=Fraction(1,4)
    
    s = 1000000
    camera.exposure_mode = 'off'

    camera.shutter_speed = s
    
    g = camera.awb_gains
    print(g)
    camera.awb_mode='off'
    camera.awb_gains = 3,1.5
    print(camera.iso)
   
    camera.start_preview()
    laser.write(b'O')
    laser.flush()
    print(laser.readline())
    q = False
    num = 0
    while not q:
        ch = input("")
        if ch == 'q' or ch=='Q':

            q = True
        else:

            for i in range(3):
                m = 2**((i-1)*2)
                print(m)
                print(camera.framerate)
                camera.framerate = 1/(int(s*m)/1000000)
                camera.shutter_speed = int(s*m)
                
                print(camera.shutter_speed)
                camera.capture(f'im{num}_{i}.jpg')
            num+=1



            laser.write(b'D')
            laser.flush()
            print(laser.readline())
            time.sleep(1)
            laser.write(b'O')
            laser.flush()
            print(laser.readline())

    laser.write(b'D')
    laser.flush()
    
    print(laser.readline())
    camera.stop_preview()

