from simple_websocket_server import WebSocketServer, WebSocket
from typing import List
import os
import random
import time


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
                sound.start()
            else:
                buttons.tabButtons[key] = ""

        if protocolDecodeur.getKey() == 'mode':
            if protocolDecodeur.getValue() == 'LIBRE':
                mode.actualMode = "libre"
                mode.sayActualMode()
            else:
                mode.actualMode = "pratique"
                mode.sayActualMode()
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

        if protocolDecodeur.getKeyValue() == ['instruction', 'ACTIVATE']:
            instructions.tellInstructions()

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
    tabButtons = ["", "", "", "", "", "", ""]

    def resetButtons(self):
        self.tabButtons = ["", "", "", "", "", "", ""]


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
        return os.system("./say.sh 'Bravo tu as réalisé le mot'"), os.system(
            "./say.sh 'Passons au prochain mot'")

    def endPraticeMode(self):
        return os.system("./say.sh 'Tu tes bien entraîné, tu peux repasser en mode libre'")


class Instruction:
    verificationInstruction = False

    def askQuestion(self):
        return os.system("./say.sh 'Pour lancer les consignes, appuis sur le bouton en haut à gauche'")

    def tellInstructions(self):
        '''return os.system("./say.sh 'Tu es bien dans les consignes, je vais texpliquer mon fonctionnement.'"), os.system(
            "./say.sh 'Tu trouveras des cubes dans la partie rangement, qui se détache avec les scratchs situés sur les tranches de la tablette. Chaque cube contient une lettre en braille, et il faudra que tu les places dans les cases creuses situées au milieu de la tablette.'"), os.system(
            "./say.sh 'Avant déssayer, je vais texpliquer les deux modes qui me composent.'"), os.system(
            "./say.sh ''"), os.system(
            "./say.sh 'Le premier mode est le mode libre. En le choisissant, tu pourras apprendre individuellement les lettres en braille. En effet, lorsque tu placeras un cube dans le bon sens dans une des cases, tu pourras appuyer sur le gros bouton valider à droite des creux, et je tindiquerai quelle lettre c’est. Tu n’as plus quà la mémoriser ! Tu peux également mettre plusieurs lettres et même composer des mots.'"), os.system(
            "./say.sh 'Le second mode est le mode pratique, tu vas pouvoir texercer et voir si tu as bien mémorisé les lettres. En effet, je vais te dire un mot, et il faudra que tu le reconstitue avec les cubes correspondants, lettre par lettre. Lorsque tu appuiera sur le bouton valider, je tindiquerai si c’est correct ou non et où sont les erreurs !'"), os.system(
            "./say.sh 'Pour choisir ton mode, c’est la molette en haut à droite sur la surface de la tablette. '"), os.system(
            "./say.sh 'Noublie pas que tu es là pour apprendre, avances à ton rythme !'")
        '''
        return os.system("./say.sh 'Voici les consignes, bla bla bla'")


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
instructions = Instruction()
sound = Sound()

server = WebSocketServer('', 8000, SimpleEcho)
server.serve_forever()