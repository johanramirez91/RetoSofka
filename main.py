import cv2 as cv
import csv
import time
import random
import cvzone
from cvzone.HandTrackingModule import HandDetector

cam = cv.VideoCapture(0)
cam.set(3, 1900)
cam.set(4, 1400)
detector = HandDetector(detectionCon=0.8)


class Game:
    def __init__(self, data):
        self._question = data[0]
        self._option1 = data[1]
        self._option2 = data[2]
        self._option3 = data[3]
        self._option4 = data[4]
        self._answer = int(data[5])
        self._userAnswer = None

    def update(self, cursors, boxes):
        for i, box in enumerate(boxes):
            op1, op2, op3, op4 = box
            if op1 < cursors[0] < op3 and op2 < cursors[1] < op4:
                self._userAnswer = i+1
                cv.rectangle(img, (op1, op3), (op2, op4), (0, 255, 0), cv.FILLED)

    @property
    def useranswer(self):
        return self._userAnswer

    @property
    def answer(self):
        return self._answer

    @property
    def question(self):
        return self._question

    @property
    def option1(self):
        return self._option1

    @property
    def option2(self):
        return self._option2

    @property
    def option3(self):
        return self._option3

    @property
    def option4(self):
        return self._option4


class Player:
    def dataPlayer(self, playername, playerlastname, score):
        with open('Players.csv', 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Player Name", "Player Last Name", "Score"])
            writer.writerow([playername, playerlastname, score])


# Import csv file
path = "Questions.csv"
with open(path, newline='\n') as file:
    reader = csv.reader(file)
    allData = list(reader)[1:]

# Objects of question

numQuestion = random.randint(1, 5)
levelQuest = []
for i in allData:
    levelQuest.append(Game(i))

player = Player()
name = str(input("Enter player name: \n"))
lastName = str(input("Enter player Last name: \n"))

while True and player:
    succes, img = cam.read()
    img = cv.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if numQuestion < len(allData):
        quest = levelQuest[numQuestion]
        img, box = cvzone.putTextRect(img, quest.question, [40, 80], 1.3, 2, offset=30, border=2, colorR=0)
        img, box1 = cvzone.putTextRect(img, quest.option1, [60, 200], 1.3, 2, offset=30, border=2, colorR=0)
        img, box2 = cvzone.putTextRect(img, quest.option2, [350, 200], 1.3, 2, offset=30, border=2, colorR=0)
        img, box3 = cvzone.putTextRect(img, quest.option3, [60, 300], 1.3, 2, offset=30, border=2, colorR=0)
        img, box4 = cvzone.putTextRect(img, quest.option4, [350, 300], 1.3, 2, offset=30, border=2, colorR=0)

        if hands:
            finger = hands[0]['lmList']
            cursor = finger[8]
            length, info = detector.findDistance(finger[8], finger[12])
            if length < 20:
                score = 0
                quest.update(cursor, [box1, box2, box3, box4])
                if quest.useranswer is not None:
                    time.sleep(0.6)
                    if quest.answer == quest.useranswer:
                        numQuestion += 5
                        score += 50
                    else:
                        numQuestion += 28

    else:
        score = 0
        for q in levelQuest:
            if quest.answer == quest.useranswer:
                score += 50
                player.dataPlayer(name, lastName, score)
            else:
                img, _ = cvzone.putTextRect(img, "Game Over", [200, 250], 2, 2, offset=50, colorR=150)
                score = 0
                player.dataPlayer(name, lastName, score)
        img, _ = cvzone.putTextRect(img, "Quiz Completed", [200, 100], 1.5, 2, offset=50, colorR=0)
        img, _ = cvzone.putTextRect(img, f'Your Score: {score/5}', [200, 400], 1.5, 2, offset=50, colorB=100)

    cv.imshow("Imagen", img)
    cv.waitKey(1)
