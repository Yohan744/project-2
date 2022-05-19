from RPi import GPIO
from time import sleep
import alsaaudio

# Change the following pins based on your application or HAT in use

encoder_data = 36
encoder_clk = 38

GPIO.setmode(GPIO.BOARD)
GPIO.setup(encoder_clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoder_data, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

m = alsaaudio.Mixer('Headphone')

# Set desired minimum and maximum values
min = 74
max = 100

# Set the volume change step size
volume_step_size = 2

volume = m.getvolume()[0]

print("Volume: " + str(volume))
print("")
clkLastState = GPIO.input(encoder_clk)

try:
    while True:
        clkState = GPIO.input(encoder_clk)
        dtState = GPIO.input(encoder_data)
        if clkState != clkLastState:
            if dtState != clkState:
                volume += volume_step_size / 2
                if volume > max:
                    volume = max
            else:
                volume -= volume_step_size / 2
                if volume < min:
                    volume = min
            if clkState == 1:
                print("Volume: " + str(int(volume)))
                print("")
                m.setvolume(int(volume))
        clkLastState = clkState
finally:
    GPIO.cleanup()
