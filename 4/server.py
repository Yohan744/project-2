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


class SimpleEcho(WebSocket):

    def handle(self):

        protocolDecodeur = ProtocolDecodeur(msg=self.data)
        print(protocolDecodeur.getKeyValue())

        if protocolDecodeur.getKey() == 'letter':
            letter.changeLetter(protocolDecodeur.getValue())

        if protocolDecodeur.getValue() == 'ON':
            key: int = int(protocolDecodeur.getKey())
            if letter.verificationLetter:
                buttons.tabButtons[key] = letter.getLetter()
                letter.resetLetter()
            else:
                buttons.tabButtons[key] = " "

        print("")
        print(buttons.tabButtons)
        print("")

        self.send_message(self.data)

    def connected(self):
        print(self.address, 'connected')

    def handle_close(self):
        print(self.address, 'closed')


class Letter:
    puckLetter = " "
    verificationLetter = False

    def changeLetter(self, letter):
        self.puckLetter = letter
        self.verificationLetter = True
        print("Letter is " + self.puckLetter)

    def getLetter(self):
        return self.puckLetter

    def resetLetter(self):
        self.puckLetter = " "
        self.verificationLetter = False


class Buttons:
    tabButtons = ["0", "0", "0", "0", "0", "0", "0", "0"]


buttons = Buttons()
letter = Letter()

server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()
