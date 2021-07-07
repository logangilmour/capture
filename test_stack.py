import time
import picamerax
import picamerax.array
import numpy as np
from PIL import Image
import fractions

with picamerax.PiCamera() as camera:
    with picamerax.array.PiRGBArray(camera) as output:
        camera.resolution = (4056,3040)
        camera.framerate=fractions.Fraction(4,1)
        
        camera.hflip = True
        camera.vflip = True
        camera.preview_fullscreen=False
        camera.preview_window=(0, 0, 1024, 768)

        s = 250000
        camera.shutter_speed = s
        
        camera.exposure_mode = 'off'

        g = camera.awb_gains
        camera.awb_mode='off'
        camera.awb_gains = 3,1.5
        camera.analog_gain=8
        print(camera.analog_gain)


        camera.start_preview()
        q = False
        num = 0
        base = None
        count = 8
        for i in range(count):
            # camera.shutter_speed = int(s)
            camera.capture(output,'rgb')
            if base is None:
                base = output.array.astype('float32')
            else:
                base+=output.array.astype('float32')
            output.truncate(0)
        
        out = Image.fromarray(np.uint8(base))

        out.save("test_stack.jpg")
        print(camera.analog_gain)
        print(camera.digital_gain)

        camera.stop_preview()

