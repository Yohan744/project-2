from websocket import create_connection
import RPi.GPIO as GPIO
import time

ws = create_connection("ws://localhost:8000")


class ProtocolGenerator:

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def create(self) -> str:
        return f"{self.key}:{self.value}"


protocolGenerator = ProtocolGenerator(key="button", value="ON")


def button_callback(channel):
    print("")
    print('-------------------')
    print('-                 -')
    print('-  BUTTON PUSHED  -')
    ws.send(protocolGenerator.create())
    result = ws.recv()
    print('-                 -')
    print('-   Received as   -')
    print("-   '%s'" % result + "   -")
    print('-------------------')
    waitingButton()


def waitingButton():
    print("")
    print("    -> Waiting for button")


GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(40, GPIO.RISING, callback=button_callback)

waitingButton()

while True:
    pass