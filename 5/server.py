from simple_websocket_server import WebSocketServer, WebSocket
from typing import List
import os
import random
import json


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

        if not mode.startingModeVerification:

            if protocolDecodeur.getKey() == 'startingMode':
                instructions.askQuestion()
                if protocolDecodeur.getValue() == '0':
                    mode.sayActualMode()
                mode.startingModeVerification = True
            letter.resetLetter()

        if protocolDecodeur.getKey() == 'letter':
            letter.changeLetter(protocolDecodeur.getValue())

        if protocolDecodeur.getValue() == 'ON':
            key: int = int(protocolDecodeur.getKey())
            if letter.verificationLetter:
                buttons.tabButtons[key] = letter.getLetter()
                letter.resetLetter()
                sound.confirmation()
            else:
                buttons.tabButtons[key] = ""

        if protocolDecodeur.getKey() == 'mode':
            cancelActions.true()
            if protocolDecodeur.getValue() == 'LIBRE':
                mode.actualMode = "libre"
                mode.sayActualMode()
            else:
                mode.actualMode = "pratique"
                mode.sayActualMode()
                word.createWordToMake()
                mode.instructionPratiqueMode()
                letter.resetLetter()
            buttons.resetButtons()
            cancelActions.false()

        if protocolDecodeur.getKeyValue() == ['validation', 'ACTIVATE']:
            cancelActions.true()
            word.createWord()
            print("Mot actuel : " + word.word)
            if mode.actualMode == "libre":
                if len(word.word) == 0:
                    os.system("./say.sh 'Mince, aucune lettre n?? d??tect??e'")
                    os.system("./say.sh 'Pose les cubes et compose ton mot'")
                else:
                    os.system("./say.sh '" + word.word + "'")
                buttons.resetButtons()
            else:
                print("Mot ?? refaire : " + word.wordToCreate)
                if word.word == word.wordToCreate:
                    sound.correct()
                    led.checkCurrentTabButtons()
                    word.spellWord()
                    led.cleanTabButtonsLed()
                    mode.goodWord()
                    buttons.resetButtons()
                    if len(word.listOfWords) == 0:
                        mode.endPraticeMode()
                    else:
                        word.createWordToMake()
                        mode.instructionPratiqueMode()
                else:
                    sound.wrong()
                    led.checkCurrentTabButtons()
                    word.spellWord()
                    word.checkTheWord()
                    led.cleanTabButtonsLed()
            cancelActions.false()

        if protocolDecodeur.getKeyValue() == ['instruction', 'ACTIVATE']:
            cancelActions.true()
            instructions.tellInstructions()
            cancelActions.false()

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

    def getLetter(self):
        return self.puckLetter

    def resetLetter(self):
        self.puckLetter = " "
        self.verificationLetter = False


class Buttons:
    tabButtons = ["", "", "", "", "", "", ""]

    def resetButtons(self):
        self.tabButtons = ["", "", "", "", "", "", ""]


class Word:
    word = ""
    wordToCreate = ""
    nbOfLetterMissing: int
    nbOfError: int
    tabError = []
    listOfWords = ["lancer", "racine", "acier", "caler", "clair", "calin",
                   "crane", "liane", "ciel", "rien", "cire",
                   "lier", "rail", "cri", "lac"]

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

            if len(self.word) == 0:
                os.system("./say.sh 'Mince, tu na rentr?? aucune lettre.'")
                os.system("./say.sh '??cris le mot, " + self.wordToCreate + "' ")
            else:
                lengthWordEnterVsWordToCreate = len(self.word) - len(self.wordToCreate)
                if lengthWordEnterVsWordToCreate > 0:
                    os.system("./say.sh 'Tu as mis " + str(lengthWordEnterVsWordToCreate) + " lettres en trop.' ")
                else:
                    os.system("./say.sh 'Il te manque " + str(-lengthWordEnterVsWordToCreate) + " lettres.' ")
                os.system("./say.sh 'R??essaye' ")

        else:
            self.nbOfError = 0
            self.tabError = []
            for i in range(len(self.word)):
                if self.word[i] != self.wordToCreate[i]:
                    self.nbOfError = self.nbOfError + 1
                    self.tabError.append(i)

            if self.nbOfError == 1:
                os.system("./say.sh 'Mince tu tes tromp?? une fois' ")
            else:
                os.system("./say.sh 'Mince tu tes tromp?? " + str(self.nbOfError) + " fois.' ")

            for i in range(len(self.tabError)):
                os.system("./say.sh 'Tu as fait une erreur dans la case num??ro " + str(self.tabError[i] + 1) + ".' ")
                os.system("./say.sh 'Tu as mis un'")
                os.system("./say.sh '" + str(self.word[self.tabError[i]]) + "'")
                os.system("./say.sh 'au lieu dun'")
                os.system("./say.sh '" + str(self.wordToCreate[self.tabError[i]]) + "'")
            os.system("./say.sh 'Essaye ?? nouveau' ")


class Mode:
    actualMode = "libre"
    startingModeVerification = False

    def sayActualMode(self):
        return os.system("./say.sh 'Vous ??tes en mode " + self.actualMode + "'")

    def instructionPratiqueMode(self):
        return os.system("./say.sh ' Faites le mot '"), os.system(
            "./say.sh '" + word.wordToCreate + "'")

    def goodWord(self):
        return os.system("./say.sh 'Bravo tu as r??alis?? le mot " + word.wordToCreate + "'"), os.system(
            "./say.sh 'Passons au prochain mot'")

    def endPraticeMode(self):
        return os.system("./say.sh 'Tu tes bien entra??n??, tu peux repasser en mode libre'")


class Instruction:
    verificationInstruction = False

    def askQuestion(self):
        return os.system("./say.sh 'Pour lancer les consignes, appuis sur le bouton en haut ?? gauche'")

    def tellInstructions(self):
        return os.system("./say.sh 'Tu es bien dans les consignes, je vais texpliquer mon fonctionnement.'"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Tu trouveras des cubes dans la partie rangement, qui se d??tache avec les scratchs, situ??s sur les tranches de la tablette.'"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Chaque cube contient une lettre en braille, et il faudra que tu les places dans les cases creuses, situ??es au milieu de la tablette.'"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Avant d??ssayer, je vais texpliquer les deux modes qui me composent.'"), os.system(
            "sleep 0.8"), os.system(
            "./say.sh 'Le premier mode est le mode libre. En le choisissant, tu pourras apprendre individuellement les lettres en braille. En effet, lorsque tu placeras un cube dans le bon sense dans une des cases, tu pourras appuyer sur le gros bouton valider ?? droite des creux, et je tindiquerai quelle lettre s??. Tu n???as plus ka la m??moriser ! Tu peux ??galement mettre plusieurs lettres et m??me composer des mots.'"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Le second mode est le mode pratique, tu vas pouvoir t??xercer et voir si tu as bien m??moris?? les lettres. En effet, je vais te dire un mot, et il faudra que tu le reconstitue avec les cubes correspondants, lettre par lettre. Lorsque tu appuiera sur le bouton valider, je tindiquerai si c???est correct ou non et o?? sont les erreurs !'"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Pour choisir ton mode, c???est lint??rrupteur en haut ?? droite sur la surface de la tablette. '"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Tu es l?? pour apprendre, avances ?? ton rythme !'")


class Sound:
    volume = 100

    def start(self):
        self.getActualVolume()
        return os.system("play -v " + str((self.volume / 100)) + " sounds/start.wav")

    def correct(self):
        self.getActualVolume()
        return os.system("play -v " + str((self.volume / 100)) + " sounds/correct.wav")

    def confirmation(self):
        self.getActualVolume()
        return os.system("play -v " + str((self.volume / 100)) + " sounds/confirmation.wav")

    def wrong(self):
        self.getActualVolume()
        return os.system("play -v " + str((self.volume / 100)) + " sounds/wrong.wav")

    def getActualVolume(self):
        f = open("variables.json", "r")
        data = json.load(f)
        f.close()
        self.volume = data["volume"]


class CancelActions:
    data = ""

    def openFile(self):
        f = open("variables.json", "r")
        self.data = json.load(f)
        f.close()

    def true(self):
        self.openFile()
        self.data["cancelActions"] = 1
        self.updateJson()

    def false(self):
        self.openFile()
        self.data["cancelActions"] = 0
        self.updateJson()

    def updateJson(self):
        f = open("variables.json", "w")
        f.seek(0)
        f.write(json.dumps(self.data))
        f.truncate()
        f.close()


class Led:
    tabButtonsLed = ""
    data = ""

    def checkCurrentTabButtons(self):
        self.cleanTabButtonsLed()
        for i in range(len(word.wordToCreate)):
            if len(word.word) == len(word.wordToCreate):
                if word.word[i] != word.wordToCreate[i]:
                    print("0")
                    self.tabButtonsLed = self.tabButtonsLed + str(0)
                else:
                    print("1")
                    self.tabButtonsLed = self.tabButtonsLed + str(1)
            else:
                print("0")
        self.sendTabButtonsLed()

    def openLedFile(self):
        f = open("variableLed.json", "r")
        self.data = json.load(f)
        f.close()

    def sendTabButtonsLed(self):
        self.openLedFile()
        self.data["tabButtonsLed"] = self.tabButtonsLed
        f = open("variableLed.json", "w")
        f.seek(0)
        f.write(json.dumps(self.data))
        f.truncate()
        f.close()

    def cleanTabButtonsLed(self):
        self.openLedFile()
        self.tabButtonsLed = ""
        self.data["tabButtonsLed"] = ""
        f = open("variableLed.json", "w")
        f.seek(0)
        f.write(json.dumps(self.data))
        f.truncate()
        f.close()


buttons = Buttons()
letter = Letter()
word = Word()
mode = Mode()
instructions = Instruction()
sound = Sound()
cancelActions = CancelActions()
led = Led()

cancelActions.false()
led.cleanTabButtonsLed()

server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()
