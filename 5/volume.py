from RPi import GPIO
import alsaaudio
import json
from datetime import datetime

encoder_data = 24
encoder_clk = 38

GPIO.setmode(GPIO.BOARD)
GPIO.setup(encoder_clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoder_data, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

m = alsaaudio.Mixer('Headphone')

min = 74
max = 100

volume_step_size = 2

f = open("variables.json", "r")
data = json.load(f)
f.close()

# volume = m.getvolume()[0]
volume = data["volume"]

print("Volume: " + str(volume))
print("")
clkLastState = GPIO.input(encoder_clk)


class SaveVolume:
    lastSave = datetime.now()
    isSave = True

    def save(self):
        delta = datetime.now() - self.lastSave
        if int(delta.total_seconds()) > 1.5 and self.isSave == False:
            f = open("variables.json", "r")
            data = json.load(f)
            f.close()
            data["volume"] = int(volume)
            f = open("variables.json", "w")
            f.seek(0)
            f.write(json.dumps(data))
            f.truncate()
            f.close()
            self.isSave = True

    def setSave(self):
        self.isSave = False
        self.lastSave = datetime.now()


saveVolume = SaveVolume()

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
                saveVolume.setSave()
        clkLastState = clkState
        saveVolume.save()
finally:
    GPIO.cleanup()
