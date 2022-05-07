from simple_websocket_server import WebSocketServer, WebSocket
from typing import List


class ProtocolDecodeur:

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def getKey(self) -> str:
        return self.msg.split(":")[0]

    def getValue(self) -> str:
        return self.msg.split(":")[1]

    def getKeyValue(self) -> List[str]:
        return self.msg.split(":")


class Buttons:
    one = 0
    two = 0
    three = 0

    def __init__(self, one, two, three):
        self.one = one
        self.two = two
        self.three = three


buttons = Buttons(one=0, two=0, three=0)


class SimpleEcho(WebSocket):

    def handle(self):

        protocolDecodeur = ProtocolDecodeur(msg=self.data)
        print(protocolDecodeur.getKeyValue())

        if protocolDecodeur.getKeyValue() == ['one', 'ON']:
            buttons.one = 1
        elif protocolDecodeur.getKeyValue() == ['one', 'OFF']:
            buttons.one = 0

        if protocolDecodeur.getKeyValue() == ['two', 'ON']:
            buttons.two = 1
        elif protocolDecodeur.getKeyValue() == ['two', 'OFF']:
            buttons.two = 0

        if protocolDecodeur.getKeyValue() == ['three', 'ON']:
            buttons.three = 1
        elif protocolDecodeur.getKeyValue() == ['three', 'OFF']:
            buttons.three = 0

        print("")
        # print(buttons.one, buttons.two, buttons.three)
        print("")

        self.send_message(self.data)

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')


server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()
