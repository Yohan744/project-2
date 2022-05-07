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


zeroON = ProtocolGenerator(key="0", value="ON")
zeroOFF = ProtocolGenerator(key="0", value="OFF")
oneON = ProtocolGenerator(key="1", value="ON")
oneOFF = ProtocolGenerator(key="1", value="OFF")
twoON = ProtocolGenerator(key="2", value="ON")
twoOFF = ProtocolGenerator(key="2", value="OFF")


def waitingButton():
    print("")
    print("    -> Waiting for button")


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

waitingButton()

tempory_state0 = False
tempory_state1 = False
tempory_state2 = False

while True:

    current_state0 = GPIO.input(36)
    current_state1 = GPIO.input(38)
    current_state2 = GPIO.input(40)

    if current_state0:
        if current_state0 != tempory_state0:
            print("BOUTON 0 : ON")
            ws.send(zeroON.create())
    else:
        if current_state0 != tempory_state0:
            print("BOUTON 0 : OFF")
            ws.send(zeroOFF.create())

    if current_state1:
        if current_state1 != tempory_state1:
            print("BOUTON 1 : ON")
            ws.send(oneON.create())
    else:
        if current_state1 != tempory_state1:
            print("BOUTON 1 : OFF")
            ws.send(oneOFF.create())

    if current_state2:
        if current_state2 != tempory_state2:
            print("BOUTON 2 : ON")
            ws.send(twoON.create())
    else:
        if current_state2 != tempory_state2:
            print("BOUTON 2 : OFF")
            ws.send(twoOFF.create())

    print("")
    print("---------------------")
    print("")

    tempory_state0 = current_state0
    tempory_state1 = current_state1
    tempory_state2 = current_state2

    time.sleep(0.5)
