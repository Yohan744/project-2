import websocket
from websocket import create_connection
import RPi.GPIO as GPIO
import time
import json

ws = create_connection("ws://localhost:8000")


class Led:

    def on0(self):
        print("0 on")
        GPIO.setup(3, GPIO.OUT)
        GPIO.output(3, GPIO.HIGH)

    def off0(self):
        print("0 off")
        GPIO.setup(5, GPIO.OUT)
        GPIO.output(5, GPIO.HIGH)

    def on1(self):
        print("1 on")
        GPIO.setup(7, GPIO.OUT)
        GPIO.output(7, GPIO.HIGH)

    def off1(self):
        print("1 off")
        GPIO.setup(11, GPIO.OUT)
        GPIO.output(11, GPIO.HIGH)

    def on2(self):
        print("2 on")
        GPIO.setup(13, GPIO.OUT)
        GPIO.output(13, GPIO.HIGH)

    def off2(self):
        print("2 off")
        GPIO.setup(15, GPIO.OUT)
        GPIO.output(15, GPIO.HIGH)

    def on3(self):
        print("3 on")

    def off3(self):
        print("3 off")

    def on4(self):
        print("4 on")

    def off4(self):
        print("4 off")

    def on5(self):
        print("5 on")

    def off5(self):
        print("5 off")

    def on6(self):
        print("6 on")

    def off6(self):
        print("6 off")


led = Led()

while True:

    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)

    f = open("variableLed.json", "r")
    data = json.load(f)
    f.close()

    if data["tabButtonsLed"] != "":
        print("VALUE IS " + str(data["tabButtonsLed"]))

        for i in range(len(data["tabButtonsLed"])):
            time.sleep(0.75)
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
                if i == 7:
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

    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, GPIO.LOW)

    GPIO.setup(5, GPIO.OUT)
    GPIO.output(5, GPIO.LOW)

    GPIO.setup(7, GPIO.OUT)
    GPIO.output(7, GPIO.LOW)

    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11, GPIO.LOW)

    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, GPIO.LOW)

    GPIO.setup(15, GPIO.OUT)
    GPIO.output(15, GPIO.LOW)

    GPIO.cleanup()
    time.sleep(5)
