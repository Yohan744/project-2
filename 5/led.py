from websocket import create_connection
import RPi.GPIO as GPIO
import time
import json

ws = create_connection("ws://localhost:8000")

'''

LETTER | ON | OFF
0 | 7 | 11
1 | 13 | 15
2 | 35 | 37
3 | 8 | 10
4 | 12 | 16
5 | 18 | 22
6 | 32 | 36

'''

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)

GPIO.output(7, GPIO.LOW)
GPIO.output(11, GPIO.LOW)
GPIO.output(13, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
GPIO.output(35, GPIO.LOW)
GPIO.output(37, GPIO.LOW)
GPIO.output(8, GPIO.LOW)
GPIO.output(10, GPIO.LOW)
GPIO.output(12, GPIO.LOW)
GPIO.output(16, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(32, GPIO.LOW)
GPIO.output(36, GPIO.LOW)

GPIO.cleanup()


class Led:

    def on0(self):
        GPIO.output(11, GPIO.LOW)
        GPIO.output(7, GPIO.HIGH)

    def off0(self):
        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.HIGH)

    def on1(self):
        GPIO.output(15, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)

    def off1(self):
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.HIGH)

    def on2(self):
        print("2 ON")
        GPIO.output(37, GPIO.LOW)
        GPIO.output(35, GPIO.HIGH)

    def off2(self):
        print("2 OFF")
        GPIO.output(35, GPIO.LOW)
        GPIO.output(37, GPIO.HIGH)

    def on3(self):
        print("3 ON")
        GPIO.output(10, GPIO.LOW)
        GPIO.output(8, GPIO.HIGH)

    def off3(self):
        print("3 off")
        GPIO.output(8, GPIO.LOW)
        GPIO.output(10, GPIO.HIGH)

    def on4(self):
        print("4 on")
        GPIO.output(16, GPIO.LOW)
        GPIO.output(12, GPIO.HIGH)

    def off4(self):
        print("4 off")
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.HIGH)

    def on5(self):
        print("5 on")
        GPIO.output(22, GPIO.LOW)
        GPIO.output(18, GPIO.HIGH)

    def off5(self):
        print("5 off")
        GPIO.output(18, GPIO.LOW)
        GPIO.output(22, GPIO.HIGH)

    def on6(self):
        print("6 on")
        GPIO.output(36, GPIO.LOW)
        GPIO.output(32, GPIO.HIGH)

    def off6(self):
        print("6 off")
        GPIO.output(32, GPIO.LOW)
        GPIO.output(36, GPIO.HIGH)


led = Led()

while True:

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    f = open("variableLed.json", "r")
    data = json.load(f)
    f.close()

    if data["tabButtonsLed"] != "":
        for i in range(len(data["tabButtonsLed"])):
            time.sleep(0.85)
            if data["tabButtonsLed"][i] == "1":
                if i == 0:
                    led.on0()
                if i == 1:
                    led.on1()
                if i == 2:
                    led.on2()
                if i == 3:
                    led.on3()
                if i == 4:
                    led.on4()
                if i == 5:
                    led.on5()
                if i == 6:
                    led.on6()
            else:
                if i == 0:
                    led.off0()
                if i == 1:
                    led.off1()
                if i == 2:
                    led.off2()
                if i == 3:
                    led.off3()
                if i == 4:
                    led.off4()
                if i == 5:
                    led.off5()
                if i == 6:
                    led.off6()
    else:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup(37, GPIO.OUT)
        GPIO.setup(35, GPIO.OUT)
        GPIO.setup(8, GPIO.OUT)
        GPIO.setup(10, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(32, GPIO.OUT)
        GPIO.setup(36, GPIO.OUT)

        GPIO.output(7, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(15, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(37, GPIO.LOW)
        GPIO.output(8, GPIO.LOW)
        GPIO.output(10, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(32, GPIO.LOW)
        GPIO.output(36, GPIO.LOW)

    time.sleep(0.15)
