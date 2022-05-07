from simple_websocket_server import WebSocketServer, WebSocket
from typing import List

from led import Led
led = Led()


class ProtocolDecodeur:

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def getKey(self) -> str:
        return self.msg.split(":")[0]

    def getValue(self) -> str:
        return self.msg.split(":")[1]

    def getKeyValue(self) -> List[str]:
        return self.msg.split(":")


class Sensor:
    button = 0
    temp = 0

    def __init__(self, button, temp):
        self.button = button
        self.temp = temp


class SimpleEcho(WebSocket):

    def handle(self):
        sensor = Sensor(button=0, temp=0)
        # echo message back to client
        protocolDecodeur = ProtocolDecodeur(msg=self.data)
        print(protocolDecodeur.getKeyValue())

        if protocolDecodeur.getKey() == "button":
            sensor.button = 1
            print("Button is on")
            led.lightLed()

        else:
            sensor.button = 0

        self.send_message(self.data)

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')


server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()
