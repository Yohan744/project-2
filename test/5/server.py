from simple_websocket_server import WebSocketServer, WebSocket
from typing import List
import os
import random

os.system("play sounds/start.wav")


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
                sound.start()
            else:
                buttons.tabButtons[key] = ""

        if protocolDecodeur.getKey() == 'mode':
            if protocolDecodeur.getValue() == 'LIBRE':
                mode.actualMode = "libre"
                os.system("./say.sh 'Vous êtes en mode " + mode.actualMode + "'")
            else:
                mode.actualMode = "pratique"
                os.system("./say.sh 'Vous êtes en mode " + mode.actualMode + "'")
                word.createWordToMake()
                mode.instructionPratiqueMode()
            buttons.resetButtons()

        if protocolDecodeur.getKeyValue() == ['validation', 'ACTIVATE']:
            word.createWord()
            print("Mot actuel : " + word.word)
            if mode.actualMode == "libre":
                os.system("./say.sh '" + word.word + "'")
                buttons.resetButtons()
            else:
                print("Mot à refaire : " + word.wordToCreate)
                if word.word == word.wordToCreate:
                    sound.correct()
                    word.spellWord()
                    mode.goodWord()
                    buttons.resetButtons()
                    if len(word.listOfWords) == 0:
                        mode.endPraticeMode()
                    else:
                        word.createWordToMake()
                        mode.instructionPratiqueMode()

                else:
                    sound.wrong()
                    word.spellWord()
                    word.checkTheWord()

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
    tabButtons = ["", "", "", "", "", "", "", ""]

    def resetButtons(self):
        self.tabButtons = ["", "", "", "", "", "", "", ""]


class Word:
    word = ""
    wordToCreate = ""
    nbOfLetterMissing: int
    nbOfError: int
    tabError = []
    listOfWords = ["caliner", "lancer", "racine", "acier", "ancre", "caler", "clair", "lacer", "calin",
                   "crane", "laine", "liane", "nacre", "aile", "ciel", "clan", "lien", "nier", "rien", "cane", "cire",
                   "lier", "rail", "rein", "rein", "ail", "cri", "lac", "air", "arc", "cil"]

    def createWord(self):
        self.word = "".join(map(str, buttons.tabButtons))
        return self.word

    def spellWord(self):
        for i in range(len(self.word)):
            print(self.word[i])
            os.system("./say.sh '" + self.word[i] + "' ")

    def createWordToMake(self):
        pickNumber = random.randrange(0, len(self.listOfWords))
        self.wordToCreate = self.listOfWords[pickNumber]
        print("WORD TO DO : " + self.wordToCreate)
        del self.listOfWords[pickNumber]
        return self.wordToCreate

    def checkTheWord(self):
        nbOfError: int

        if len(self.word) != len(self.wordToCreate):
            if len(self.word) - len(self.wordToCreate) > 0:
                os.system("./say.sh 'Tu as mis " + str(
                    len(self.word) - len(self.wordToCreate)) + " lettres en trop.' ")
            else:
                os.system("./say.sh 'Il te manque " + str(
                    len(self.word) - len(self.wordToCreate)) + " lettres.' ")
            os.system("./say.sh 'Réessaye' ")
        else:
            self.nbOfError = 0
            self.tabError = []
            for i in range(len(self.word)):
                if self.word[i] != self.wordToCreate[i]:
                    self.nbOfError = self.nbOfError + 1
                    self.tabError.append(i)

            if self.nbOfError == 1:
                os.system("./say.sh 'Mince tu tes trompé une fois' ")
            else:
                os.system("./say.sh 'Mince tu tes trompé " + str(self.nbOfError) + " fois.' ")

            for i in range(len(self.tabError)):
                os.system("./say.sh 'Tu as fait une erreur dans la case numéro " + str(
                    self.tabError[i] + 1) + ".' ")
                os.system(
                    "./say.sh 'Tu as mis un         " + str(self.word[self.tabError[
                        i]]) + "                        au lieu dun                        " + str(
                        self.wordToCreate[self.tabError[i]]) + ".        ' ")

            os.system("./say.sh 'Essaye à nouveau' ")


class Mode:
    actualMode = ""

    def instructionPratiqueMode(self):
        return os.system("./say.sh ' Faites le mot '"), os.system(
            "./say.sh '" + word.wordToCreate + "'")

    def goodWord(self):
        return os.system("./say.sh 'Bravo tu as réalisé le mot'"), os.system(
            "./say.sh 'Passons au prochain mot'")

    def endPraticeMode(self):
        return os.system("./say.sh 'Tu tes bien entraîné, tu peux repasser en mode libre'")


class Sound:

    def start(self):
        return os.system("play sounds/start.wav")

    def correct(self):
        return os.system("play sounds/correct.wav")

    def wrong(self):
        return os.system("play sounds/wrong.wav")


buttons = Buttons()
letter = Letter()
word = Word()
mode = Mode()
sound = Sound()

server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()
