from simple_websocket_server import WebSocketServer, WebSocket
from volume import GlobalVolume
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
                    os.system("./say.sh 'Mince, aucune lettre né détectée'")
                    os.system("./say.sh 'Pose les cubes et compose ton mot'")
                else:
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
    listOfWords = ["caliner", "lancer", "racine", "acier", "caler", "clair", "calin",
                   "crane", "liane", "nacre", "ciel", "nier", "rien", "cire",
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
                os.system("./say.sh 'Mince, tu na rentré aucune lettre.'")
                os.system("./say.sh 'Écris le mot, " + self.wordToCreate + "' ")
            else:
                lengthWordEnterVsWordToCreate = len(self.word) - len(self.wordToCreate)
                if lengthWordEnterVsWordToCreate > 0:
                    os.system("./say.sh 'Tu as mis " + str(lengthWordEnterVsWordToCreate) + " lettres en trop.' ")
                else:
                    os.system("./say.sh 'Il te manque " + str(-lengthWordEnterVsWordToCreate) + " lettres.' ")
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
                os.system("./say.sh 'Tu as fait une erreur dans la case numéro " + str(self.tabError[i] + 1) + ".' ")
                os.system("./say.sh 'Tu as mis un'")
                os.system("./say.sh '" + str(self.word[self.tabError[i]]) + "'")
                os.system("./say.sh 'au lieu dun'")
                os.system("./say.sh '" + str(self.wordToCreate[self.tabError[i]]) + "'")
            os.system("./say.sh 'Essaye à nouveau' ")


class Mode:
    actualMode = "libre"
    startingModeVerification = False

    def sayActualMode(self):
        return os.system("./say.sh 'Vous êtes en mode " + self.actualMode + "'")

    def instructionPratiqueMode(self):
        return os.system("./say.sh ' Faites le mot '"), os.system(
            "./say.sh '" + word.wordToCreate + "'")

    def goodWord(self):
        return os.system("./say.sh 'Bravo tu as réalisé le mot " + word.wordToCreate + "'"), os.system(
            "./say.sh 'Passons au prochain mot'")

    def endPraticeMode(self):
        return os.system("./say.sh 'Tu tes bien entraîné, tu peux repasser en mode libre'")


class Instruction:
    verificationInstruction = False

    def askQuestion(self):
        return os.system("./say.sh 'Pour lancer les consignes, appuis sur le bouton en haut à gauche'")

    def tellInstructions(self):
        return os.system("./say.sh 'Tu es bien dans les consignes, je vais texpliquer mon fonctionnement.'"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Tu trouveras des cubes dans la partie rangement, qui se détache avec les scratchs, situés sur les tranches de la tablette.'"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Chaque cube contient une lettre en braille, et il faudra que tu les places dans les cases creuses, situées au milieu de la tablette.'"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Avant déssayer, je vais texpliquer les deux modes qui me composent.'"), os.system(
            "sleep 0.8"), os.system(
            "./say.sh 'Le premier mode est le mode libre. En le choisissant, tu pourras apprendre individuellement les lettres en braille. En effet, lorsque tu placeras un cube dans le bon sense dans une des cases, tu pourras appuyer sur le gros bouton valider à droite des creux, et je tindiquerai quelle lettre sé. Tu n’as plus ka la mémoriser ! Tu peux également mettre plusieurs lettres et même composer des mots.'"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Le second mode est le mode pratique, tu vas pouvoir téxercer et voir si tu as bien mémorisé les lettres. En effet, je vais te dire un mot, et il faudra que tu le reconstitue avec les cubes correspondants, lettre par lettre. Lorsque tu appuiera sur le bouton valider, je tindiquerai si c’est correct ou non et où sont les erreurs !'"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Pour choisir ton mode, c’est lintérrupteur en haut à droite sur la surface de la tablette. '"), os.system(
            "sleep 0.5"), os.system(
            "./say.sh 'Tu es là pour apprendre, avances à ton rythme !'")
        # return os.system("./say.sh 'Voici les consignes, bla bla bla'")


class Sound:

    volume = GlobalVolume.globalVolume

    def start(self):
        return os.system("play -v " + str((self.volume/100)) + " sounds/start.wav")

    def correct(self):
        return os.system("play -v " + str((self.volume/100)) + " sounds/correct.wav")

    def confirmation(self):
        return os.system("play -v " + str((self.volume/100)) + " sounds/confirmation.wav")

    def wrong(self):
        return os.system("play -v " + str((self.volume/100)) + " sounds/wrong.wav")


class CancelActions:
    f = open("check.json", "r")
    data = json.load(f)
    f.close()

    def true(self):
        self.data["cancelActions"] = 1
        self.updateJson()

    def false(self):
        self.data["cancelActions"] = 0
        self.updateJson()

    def updateJson(self):
        f = open("check.json", "w")
        json.dump(self.data, f)
        f.close()


buttons = Buttons()
letter = Letter()
word = Word()
mode = Mode()
instructions = Instruction()
sound = Sound()
cancelActions = CancelActions()
globalVolume = GlobalVolume()

server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()
