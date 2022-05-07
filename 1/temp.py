from websocket import create_connection
import RPi.GPIO as GPIO
import dht11
import time
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
# read data using pin 14
instance = dht11.DHT11(pin=20)

ws = create_connection("ws://localhost:8000")


class ProtocolGenerator:

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def create(self) -> str:
        return f"{self.key}:{self.value}"


count = 0
temp = 0
humi = 0

while True:

    count = count + 1
    if count > 25:
        temp = 0
        humi = 0

    temp = temp + 5
    humi = humi + 5

    result = instance.read()
    protocolGeneratorTemp = ProtocolGenerator(key="temperature", value=f'{temp}')
    protocolGeneratorHumi = ProtocolGenerator(key="humidity", value=f'{humi}')

    if result.is_valid():
        print("sending data")
        print("TEMPERATURE " + protocolGeneratorTemp.create())
        print("HUMIDITY " + protocolGeneratorHumi.create())
        ws.send(protocolGeneratorTemp.create())
        ws.send(protocolGeneratorHumi.create())
        print("Sent")
        result = ws.recv()
        print("Received")
    else:
        print("Error: %d" % result.error_code)
    time.sleep(3)
