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
threeON = ProtocolGenerator(key="3", value="ON")
threeOFF = ProtocolGenerator(key="3", value="OFF")
fourON = ProtocolGenerator(key="4", value="ON")
fourOFF = ProtocolGenerator(key="4", value="OFF")
fiveON = ProtocolGenerator(key="5", value="ON")
fiveOFF = ProtocolGenerator(key="5", value="OFF")
sixON = ProtocolGenerator(key="6", value="ON")
sixOFF = ProtocolGenerator(key="6", value="OFF")
modeON = ProtocolGenerator(key="mode", value="PRATIQUE")
modeOFF = ProtocolGenerator(key="mode", value="LIBRE")
validationON = ProtocolGenerator(key="validation", value="ACTIVATE")
validationOFF = ProtocolGenerator(key="validation", value="DEACTIVATE")
instructionON = ProtocolGenerator(key="instruction", value="ACTIVATE")
instructionOFF = ProtocolGenerator(key="instruction", value="DEACTIVATE")

startingModeLibre = ProtocolGenerator(key="startingMode", value="0")
startingModePratique = ProtocolGenerator(key="startingMode", value="1")


def waitingButton():
    print("")
    print("    -> Waiting for button")


GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

waitingButton()

tempory_state0 = False
tempory_state1 = False
tempory_state2 = False
tempory_state3 = False
tempory_state4 = False
tempory_state5 = False
tempory_state6 = False
tempory_stateM = False
tempory_stateV = False
tempory_stateI = False

current_stateM = GPIO.input(40)
if current_stateM == 0:
    ws.send(startingModeLibre.create())
else :
    ws.send(startingModePratique.create())

while True:

    current_state0 = GPIO.input(37)
    current_state1 = GPIO.input(35)
    current_state2 = GPIO.input(33)
    current_state3 = GPIO.input(31)
    current_state4 = GPIO.input(29)
    current_state5 = GPIO.input(23)
    current_state6 = GPIO.input(21)
    current_stateM = GPIO.input(40)
    current_stateV = GPIO.input(19)
    current_stateI = GPIO.input(26)

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

    if current_state3:
        if current_state3 != tempory_state3:
            print("BOUTON 3 : ON")
            ws.send(threeON.create())
    else:
        if current_state3 != tempory_state3:
            print("BOUTON 3 : OFF")
            ws.send(threeOFF.create())

    if current_state4:
        if current_state4 != tempory_state4:
            print("BOUTON 4 : ON")
            ws.send(fourON.create())
    else:
        if current_state4 != tempory_state4:
            print("BOUTON 4 : OFF")
            ws.send(fourOFF.create())

    if current_state5:
        if current_state5 != tempory_state5:
            print("BOUTON 5 : ON")
            ws.send(fiveON.create())
    else:
        if current_state5 != tempory_state5:
            print("BOUTON 5 : OFF")
            ws.send(fiveOFF.create())

    if current_state6:
        if current_state6 != tempory_state6:
            print("BOUTON 6 : ON")
            ws.send(sixON.create())
    else:
        if current_state6 != tempory_state6:
            print("BOUTON 6 : OFF")
            ws.send(sixOFF.create())

    if current_stateM:
        if current_stateM != tempory_stateM:
            print("MODE : PRATIQUE")
            ws.send(modeON.create())
    else:
        if current_stateM != tempory_stateM:
            print("MODE : LIBRE")
            ws.send(modeOFF.create())

    if current_stateV:
        if current_stateV != tempory_stateV:
            print("VALIDATION : ON")
            ws.send(validationON.create())
    else:
        if current_stateV != tempory_stateV:
            print("VALIDATION : OFF")
            ws.send(validationOFF.create())

    if current_stateI:
        if current_stateI != tempory_stateI:
            print("INSTRUCTION : ON")
            ws.send(instructionON.create())
    else:
        if current_stateI != tempory_stateI:
            print("INSTRUCTION : OFF")
            ws.send(instructionOFF.create())

    tempory_state0 = current_state0
    tempory_state1 = current_state1
    tempory_state2 = current_state2
    tempory_state3 = current_state3
    tempory_state4 = current_state4
    tempory_state5 = current_state5
    tempory_state6 = current_state6
    tempory_stateM = current_stateM
    tempory_stateV = current_stateV
    tempory_stateI = current_stateI

    time.sleep(0.3)
