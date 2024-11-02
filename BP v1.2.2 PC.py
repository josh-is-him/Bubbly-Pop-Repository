import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1200, 690))
clock = pygame.time.Clock()
white = (255, 255, 255)
gray = (127, 127, 127)
black = (0, 0, 0)
red = (180, 80, 80)
orange = (255, 150, 20)
yellow = (255, 230, 0)
green = (10, 200, 0)
blue = (50, 130, 230)
cyan = (0, 149, 149)
brown = (100, 70, 30)
score = 0
gincrement = 0
colors = (red, green, blue, yellow, orange, brown, black)
bluePossibilities = (red, green)
ballAmount = 0
allBalls = []
modGreenBalls = []
YellowBalls = []
OrangeBalls = []
dragging = False
operators = ("-", "+", "x")
tnyFont = pygame.font.SysFont('lucidabright', 20)
smlFont = pygame.font.SysFont('lucidabright', 45)
medFont = pygame.font.SysFont('lucidabright', 90)
bigFont = pygame.font.SysFont('lucidabright', 135)
scores = []
menu = True
tutorial = False
menuTime = 0
displayCleanSlate = False
dcsTime = 0
dcsDuration = 0
run = True

cleanSlateText = smlFont.render('Fuiyoh! +5', True, black)
cleanSlateText.set_alpha(100)
cleanSlateRect = cleanSlateText.get_rect(center=(600, 280))

class Ball:                                     #Ball Class

    def __init__(self, x, y, color, xvel, yvel):
        self.x = x
        self.y = y
        self.color = color
        self.xvel = xvel
        self.yvel = yvel
        self.rect = pygame.Rect(x-60, y-60, 120, 120)
        self.graydius = 0
    def drawBall(self, x, y, color):
        pygame.draw.circle(screen, color, (x, y), 60)
        pygame.draw.circle(screen, gray, (x, y), (self.graydius / 6))
    def updateRect(self, x, y):
        self.rect = pygame.Rect(x-60, y-60, 120, 120)
    def updateGraydius(self):
        self.graydius += (1 + gincrement)/2

class RedBall(Ball):                                        #Red Ball

    def __init__(self, x, y, color, xvel, yvel):
        super().__init__(x, y, color, xvel, yvel)
        self.color = red
        self.new = True
        self.creationTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)
    def Action(self):
        global score, ballAmount, menu, menuTime
        if self.new == False:
            scores.insert(0, score)
            for ball in allBalls:
                allBalls.remove(ball)
            ballAmount = 0
            score = 0
            menu = True
            menuTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)
    def Graction(self):
        global ballAmount
        allBalls.remove(ball)
        ballAmount -= 1
        return ballAmount
    
class GreenBall(Ball):                                      #Green Ball

    def __init__(self, x, y, color, xvel, yvel):
        super().__init__(x, y, color, xvel, yvel)
        self.color = green
    def Action(self):
        global score, ballAmount, displayCleanSlate, dcsTime
        score += 1
        allBalls.remove(ball)
        ballAmount -= 1
        if ballAmount == 0:
            displayCleanSlate = True
            dcsTime = pygame.time.get_ticks()
        return score, ballAmount, displayCleanSlate, dcsTime
    def Graction(self):
        global score, ballAmount, menu, menuTime
        scores.insert(0, score)
        for ball in allBalls:
            allBalls.remove(ball)
        ballAmount = 0
        score = 0
        menu = True
        menuTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)
    
class CyanBall(Ball):                                       #Saturn Ball

    def __init__(self, x, y, color, xvel, yvel):
        super().__init__(x, y, color, xvel, yvel)
        self.color = cyan
        self.rings = 2
    def Action(self):
        global score, ballAmount, displayCleanSlate, dcsTime
        if self.rings > 0:
            self.rings -= 1
        elif self.rings == 0:
            score += 1
            allBalls.remove(ball)
            ballAmount -= 1
            if ballAmount == 0:
                displayCleanSlate = True
                dcsTime = pygame.time.get_ticks()
        return score, ballAmount, displayCleanSlate, dcsTime
    def Graction(self):
        global score, ballAmount, menu, menuTime
        scores.insert(0, score)
        for ball in allBalls:
            allBalls.remove(ball)
        ballAmount = 0
        score = 0
        menu = True
        menuTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)
    def showRings(self, x, y):
        if self.rings > 0:
            pygame.draw.circle(screen, black, (x, y), 65, 3)
        if self.rings > 1:
            pygame.draw.circle(screen, black, (x, y), 70, 3)
    
class BlueBall(Ball):                                       #Blue Ball

    def __init__(self, x, y, color, xvel, yvel):
        super().__init__(x, y, color, xvel, yvel)
        self.color = blue
    def Action(self):
        global score, ballAmount
        score += 1
        allBalls.remove(ball)
        ballAmount -= 1
        blueBallAction(self.x, self.y)
        blueBallAction(self.x, self.y)
        blueBallAction(self.x, self.y)
        return score, ballAmount
    def Graction(self):
        global score, ballAmount, menu, menuTime
        scores.insert(0, score)
        for ball in allBalls:
            allBalls.remove(ball)
        ballAmount = 0
        score = 0
        menu = True
        menuTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)

class YellowBall(Ball):                                     #Yellow Ball

    def __init__(self, x, y, color, xvel, yvel):
        super().__init__(x, y, color, xvel, yvel)
        self.color = yellow
        self.ring = True
        self.beingDragged = False
    def Action(self):
        global score, ballAmount, displayCleanSlate, dcsTime
        score += 1
        allBalls.remove(ball)
        ballAmount -= 1
        if ballAmount == 0:
            displayCleanSlate = True
            dcsTime = pygame.time.get_ticks()
        return score, ballAmount, displayCleanSlate, dcsTime
    def Graction(self):
        global score, ballAmount, menu, menuTime
        scores.insert(0, score)
        for ball in allBalls:
            allBalls.remove(ball)
        ballAmount = 0
        score = 0
        menu = True
        menuTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)
    def showRing(self, x, y):
        if self.ring:
            yellowRing = pygame.draw.circle(screen, black, (x, y), 180, 3)
        return yellowRing

class OrangeBall(Ball):                                     #Orange Ball

    def __init__(self, x, y, color, xvel, yvel):
        super().__init__(x, y, color, xvel, yvel)
        self.color = orange
        self.beingDragged = False
    def Action(self):
        global score, ballAmount, displayCleanSlate, dcsTime
        score += 1
        allBalls.remove(ball)
        ballAmount -= 1
        if ballAmount == 0:
            displayCleanSlate = True
            dcsTime = pygame.time.get_ticks()
        return score, ballAmount, displayCleanSlate, dcsTime
    def Graction(self):
        global score, ballAmount, menu, menuTime
        scores.insert(0, score)
        for ball in allBalls:
            allBalls.remove(ball)
        ballAmount = 0
        score = 0
        menu = True
        menuTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)

class BrownBall(Ball):                                      #Brown Ball

    def __init__(self, x, y, color, xvel, yvel):
        super().__init__(x, y, color, xvel, yvel)
        self.color = brown
        self.new = True
        self.creationTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)
    def Action(self):
        global score, ballAmount, displayCleanSlate, dcsTime
        if self.new == False:
            score += 1
            allBalls.remove(ball)
            ballAmount -= 1
            if ballAmount == 0:
                displayCleanSlate = True
                dcsTime = pygame.time.get_ticks()
        return score, ballAmount, displayCleanSlate, dcsTime
    def Graction(self):
        global score, ballAmount, menu, menuTime
        scores.insert(0, score)
        for ball in allBalls:
            allBalls.remove(ball)
        ballAmount = 0
        score = 0
        menu = True
        menuTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)
    def GetEquation(self, font):
        numberOne = random.randint(1, 9)
        numberTwo = random.randint(1, 9)
        operator = random.choice(operators)
        self.temp = f'{numberOne}{operator}{numberTwo}'
        self.shownOperator = random.choice(operators)
        self.equation = self.temp[0]+self.shownOperator+self.temp[2]
        if self.shownOperator == "-":
            self.shownAnswer = str(random.choice((int(self.temp[0])-int(self.temp[2]), int(self.temp[0])+int(self.temp[2]))))
        elif self.shownOperator == "+":
            self.shownAnswer = str(random.choice((int(self.temp[0])+int(self.temp[2]), int(self.temp[0])*int(self.temp[2]))))
        elif self.shownOperator == "x":
            self.shownAnswer = str(random.choice((int(self.temp[0])+int(self.temp[2]), int(self.temp[0])*int(self.temp[2]))))
        self.equationText = font.render(self.temp, True, black)
        self.equationTextRect = self.equationText.get_rect()
        self.equationTextRect.center = (self.x, self.y-30)
        self.shownAnswerText = font.render(self.shownAnswer, True, black)
        self.shownAnswerTextRect = self.shownAnswerText.get_rect()
        self.shownAnswerTextRect.center = (self.x, self.y+30)
        return self.temp, self.shownOperator, self.equation, self.shownAnswer, self.equationText, self.equationTextRect, self.shownAnswerText, self.shownAnswerTextRect

class BlackBall(Ball):                                      #Black Ball

    def __init__(self, x, y, color, xvel, yvel):
        super().__init__(x, y, color, xvel, yvel)
        self.color = black
        self.beingDragged = False
    def Action(self):
        global score, ballAmount, displayCleanSlate, dcsTime
        score += 1
        allBalls.remove(ball)
        ballAmount -= 1
        if ballAmount == 0:
            displayCleanSlate = True
            dcsTime = pygame.time.get_ticks()
        return score, ballAmount, displayCleanSlate, dcsTime
    def Graction(self):
        global score, ballAmount, menu, menuTime
        scores.insert(0, score)
        for ball in allBalls:
            allBalls.remove(ball)
        ballAmount = 0
        score = 0
        menu = True
        menuTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)
    def showRing(self):
        pygame.draw.circle(screen, black, (self.x, self.y), 180, 3)

def blueBallAction(x, y):
    global ballAmount

    color = random.choice(bluePossibilities)
    ballXPossibilities = [x-120, x+120]
    ballYPossibilities = [y-120, y+120]
    ballX = random.choice(ballXPossibilities)
    ballY = random.choice(ballYPossibilities)
    if ballX < 60:
        ballX = 1140
    if ballY < 60:
        ballY = 630
    if ballX > 1140:
        ballX = 60
    if ballY > 630:
        ballY = 60
    if color == red:
        ball = RedBall(ballX, ballY, red, random.randint(-20, 20), random.randint(-20, 20))
    elif color == green:
        ball = GreenBall(ballX, ballY, green, random.randint(-20, 20), random.randint(-20, 20))
    allBalls.append(ball)
    ballAmount += 1

def checkCollision(ballOne, ballTwo):
    distance = math.sqrt((ballTwo.x-ballOne.x) ** 2 + (ballTwo.y-ballOne.y) ** 2)
    if 0 < distance < 120:
        overlap = 120 - distance
        dx = (ballTwo.x - ballOne.x) / distance
        dy = (ballTwo.y - ballOne.y) / distance
        ballOne.x -= overlap * dx
        ballOne.y -= overlap * dy
        ballTwo.x += overlap * dx
        ballTwo.y += overlap * dy
        xv, yv = ballTwo.xvel, ballTwo.yvel
        ballTwo.xvel, ballTwo.yvel = ballOne.xvel, ballOne.yvel
        ballOne.xvel, ballOne.yvel = xv, yv
    elif distance == 0:
        ballOne.x -= 1
        xv, yv = ballTwo.xvel, ballTwo.yvel
        ballTwo.xvel, ballTwo.yvel = ballOne.xvel, ballOne.yvel
        ballOne.xvel, ballOne.yvel = xv, yv
    return distance

def drag(ball):
    ball.x = mousex
    ball.y = mousey

def showMenu():
    global ballAmount
    for ball in allBalls:
        allBalls.remove(ball)
    ballAmount = 0
    screen.fill(white)
    titleText = bigFont.render('Bubbly Pop!', True, black)
    titleText.set_alpha(100)
    titleRect = titleText.get_rect(center=(600, 150))
    screen.blit(titleText, (titleRect))
    clickAnywhereText = medFont.render('Click anywhere to play', True, black)
    clickAnywhereText.set_alpha(100)
    clickAnywhereRect = clickAnywhereText.get_rect(center=(600, 310))
    screen.blit(clickAnywhereText, (clickAnywhereRect))
    if len(scores) == 0:
        mScoreText = medFont.render('Score: --', True, black)
    else:
        mScoreText = medFont.render(f'Score: {scores[0]}', True, black)
    mScoreText.set_alpha(100)
    mScoreRect = mScoreText.get_rect(center=(600, 500))
    screen.blit(mScoreText, (mScoreRect))
    viewTutorialText = tnyFont.render('Press T to view tutorial', True, black)
    viewTutorialText.set_alpha(100)
    viewTutorialRect = viewTutorialText.get_rect()
    viewTutorialRect.center = (600, 640)
    screen.blit(viewTutorialText, viewTutorialRect)

def showTutorial():
    screen.fill(white)
    pygame.draw.circle(screen, red, (90, 90), 60)
    redTutorialText = tnyFont.render("Don't click me!", True, black)
    redTutorialText.set_alpha(100)
    redTutorialRect = redTutorialText.get_rect()
    redTutorialRect.midleft = (160, 90)
    pygame.draw.circle(screen, green, (90, 240), 60)
    greenTutorialText = tnyFont.render("Click me!", True, black)
    greenTutorialText.set_alpha(100)
    greenTutorialRect = greenTutorialText.get_rect()
    greenTutorialRect.midleft = (160, 240)
    pygame.draw.circle(screen, blue, (90, 390), 60)
    blueTutorialText = tnyFont.render("Click me, and I'll spawn 3 bubbles!", True, black)
    blueTutorialText.set_alpha(100)
    blueTutorialRect = blueTutorialText.get_rect()
    blueTutorialRect.midleft = (160, 390)
    pygame.draw.circle(screen, cyan, (90, 540), 60)
    cyanTutorialText = tnyFont.render("Click me 3 times!", True, black)
    cyanTutorialText.set_alpha(100)
    cyanTutorialRect = cyanTutorialText.get_rect()
    cyanTutorialRect.midleft = (160, 540)
    pygame.draw.circle(screen, yellow, (600, 90), 60)
    yellowTutorialText = tnyFont.render("Drag me out of my black ring!", True, black)
    yellowTutorialText.set_alpha(100)
    yellowTutorialRect = yellowTutorialText.get_rect()
    yellowTutorialRect.midleft = (670, 90)
    pygame.draw.circle(screen, orange, (600, 240), 60)
    orangeTutorialText = tnyFont.render("Drag me to a wall!", True, black)
    orangeTutorialText.set_alpha(100)
    orangeTutorialRect = orangeTutorialText.get_rect()
    orangeTutorialRect.midleft = (670, 240)
    pygame.draw.circle(screen, brown, (600, 390), 60)
    brownTutorialText = tnyFont.render("If I'm a correct math question, click me!", True, black)
    brownTutorialText.set_alpha(100)
    brownTutorialRect = brownTutorialText.get_rect()
    brownTutorialRect.midleft = (670, 390)
    pygame.draw.circle(screen, black, (600, 540), 60)
    blackTutorialText = tnyFont.render("Click me, and I'll explode surrounding bubbles!", True, black)
    blackTutorialText.set_alpha(100)
    blackTutorialRect = blackTutorialText.get_rect()
    blackTutorialRect.midleft = (670, 540)
    exitTutorialText = tnyFont.render('Press T to exit tutorial', True, black)
    exitTutorialText.set_alpha(100)
    exitTutorialRect = exitTutorialText.get_rect()
    exitTutorialRect.center = (600, 640)
    screen.blit(redTutorialText, redTutorialRect)
    screen.blit(greenTutorialText, greenTutorialRect)
    screen.blit(blueTutorialText, blueTutorialRect)
    screen.blit(cyanTutorialText, cyanTutorialRect)
    screen.blit(yellowTutorialText, yellowTutorialRect)
    screen.blit(orangeTutorialText, orangeTutorialRect)
    screen.blit(brownTutorialText, brownTutorialRect)
    screen.blit(blackTutorialText, blackTutorialRect)
    screen.blit(exitTutorialText, exitTutorialRect)



offset = pygame.time.get_ticks()
while run:
    clock.tick(100)
    ticks = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)

    mousex, mousey = pygame.mouse.get_pos()
    mousepos = (mousex, mousey)

    if menu == True:
        showMenu()
    elif menu == False and tutorial == True:
        showTutorial()

    for event in pygame.event.get():            #Event handler
        if event.type == pygame.QUIT:
            run = False
        elif (event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_s) or (event.type == pygame.KEYDOWN and event.key == pygame.K_d)) and menu == False:
            mousex, mousey = pygame.mouse.get_pos()
            mousepos = (mousex, mousey)
            for ball in allBalls:
                if ball.rect.collidepoint(mousepos):
                    if ball.color == brown and ball.new == False:
                        if ball.temp[1] == "-" and int(ball.shownAnswer) == int(ball.temp[0])-int(ball.temp[2]):
                            ball.Action()
                        elif ball.temp[1] == "+" and int(ball.shownAnswer) == int(ball.temp[0])+int(ball.temp[2]):
                            ball.Action()
                        elif ball.temp[1] == "x" and int(ball.shownAnswer) == int(ball.temp[0])*int(ball.temp[2]):
                            ball.Action()
                        else:
                            scores.insert(0, score)
                            for ball in allBalls:
                                allBalls.remove(ball)
                                ballAmount = 0
                                score = 0
                                menu = True
                                menuTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)
                    elif ball in YellowBalls or ball in OrangeBalls or ball.color == black:
                        locx, locy = ball.x, ball.y
                        heldBall = ball
                        ball.beingDragged = True
                        dragging = True
                    else:
                        ball.Action()
        elif (event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_s) or (event.type == pygame.KEYDOWN and event.key == pygame.K_d)) and menu == True:
            if ticks - menuTime >= 200:
                menu = False
        elif (event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.KEYUP and event.key == pygame.K_s) or (event.type == pygame.KEYUP and event.key == pygame.K_d)):
            if dragging:
                dragging = False
                for ball in YellowBalls:
                    if ball.beingDragged == True:
                        yelDistance = math.sqrt((mousex-locx) ** 2 + (mousey-locy) ** 2)
                        if yelDistance >= 180:
                            ball.Action()
                        elif yelDistance < 180:
                            locx, locy = ball.x, ball.y
                        ball.beingDragged = False
                for ball in OrangeBalls:
                    if ball.beingDragged == True:
                        if ball.x <= 60 or ball.x >= 1140 or ball.y <= 60 or ball.y >= 630:
                            ball.Action()
                        else:
                            locx, locy = ball.x, ball.y
                        ball.beingDragged = False
                for ball in allBalls:
                    if ball.color == black and ball.beingDragged == True:
                        for ballToCheck in allBalls:
                            if ballToCheck.color != black:
                                blackDistance = math.sqrt((ball.x-ballToCheck.x) ** 2 + (ball.y-ballToCheck.y) ** 2)
                                if blackDistance <= 180:
                                    allBalls.remove(ballToCheck)
                                    ballAmount -= 1
                        ball.Action()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t and menu == True:
            menu = False
            tutorial = True
            showTutorial()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_t and tutorial == True:
            tutorial = False
            menu = True
            showMenu()

    if dragging:
        ballDistance = math.sqrt((mousex-locx) ** 2 + (mousey-locy) ** 2)
        drag(heldBall)

    if ballAmount < 10 and menu == False:          #Make a ball
        if ticks % 66 == 0:
            color = random.choice(colors)
            if color == red:
                ball = RedBall(random.randint(60, 1140), random.randint(60, 630), red, random.randint(-20, 20), random.randint(-20, 20))
            elif color == green:
                modded = random.randint(1, 2)
                if modded == 1:
                    ball = GreenBall(random.randint(60, 1140), random.randint(60, 630), green, random.randint(-20, 20), random.randint(-20, 20))
                elif modded == 2:
                    ball = CyanBall(random.randint(60, 1140), random.randint(60, 630), green, random.randint(-20, 20), random.randint(-20, 20))
                    modGreenBalls.append(ball)
            elif color == blue:
                ball = BlueBall(random.randint(60, 1140), random.randint(60, 630), blue, random.randint(-20, 20), random.randint(-20, 20))
            elif color == yellow:
                ball = YellowBall(random.randint(60, 1140), random.randint(60, 630), yellow, random.randint(-20, 20), random.randint(-20, 20))
                YellowBalls.append(ball)
            elif color == orange:
                ball = OrangeBall(random.randint(60, 1140), random.randint(60, 630), orange, random.randint(-20, 20), random.randint(-20, 20))
                OrangeBalls.append(ball)
            elif color == brown:
                ball = BrownBall(random.randint(60, 1140), random.randint(60, 630), brown, random.randint(-20, 20), random.randint(-20, 20))
                ball.temp, ball.shownOperator, ball.equation, ball.shownAnswer, ball.equationText, ball.equationTextRect, ball.shownAnswerText, ball.shownAnswerTextRect = ball.GetEquation(smlFont)
            elif color == black:
                ball = BlackBall(random.randint(60, 1140), random.randint(60, 630), black, random.randint(-20, 20), random.randint(-20, 20))
            allBalls.append(ball)
            ballCreationTime = round(round((pygame.time.get_ticks() - offset)/1000, 2)*100)
            ballAmount += 1

    for ball in allBalls:           #Move the balls
        ball.x += ball.xvel/10
        ball.y += ball.yvel/10
    
    for i in range(len(allBalls)):          #Check every ball to ball collision
        for j in range(i + 1, len(allBalls)):
            ballOne = allBalls[i]
            ballTwo = allBalls[j]
            checkCollision(ballOne, ballTwo)

    for ball in allBalls:           #Check every ball to wall collision
        if ball.x < 60:
            ball.x = 60
            ball.xvel = abs(ball.xvel)
        if ball.x > 1140:
            ball.x = 1140
            ball.xvel = -abs(ball.xvel)
        if ball.y < 60:
            ball.y = 60
            ball.yvel = abs(ball.yvel)
        if ball.y > 630:
            ball.y = 630
            ball.yvel = -abs(ball.yvel)

    if score > 0:
        gincrement = math.sqrt(score) * 0.04

    if menu == False and tutorial == False:
        screen.fill(white)
        for ball in allBalls:
            if ball.color in (red, brown) and ball.new == True and ticks-ball.creationTime > 50:
                ball.new = False
            elif ball.color in (red, brown) and ball.new == True and ticks-ball.creationTime <= 50:
                ball.graydius = 0
            ball.updateRect(ball.x, ball.y)
            if ball.color not in (red, brown) or (ball.color in (red, brown) and ball.new == False):
                ball.updateGraydius()
            ball.drawBall(ball.x, ball.y, ball.color)
            if ball.color in (red, brown) and ball.new == True:
                pygame.draw.circle(screen, white, (ball.x, ball.y), 10)
            if ball in modGreenBalls:
                ball.showRings(ball.x, ball.y)
            elif ball in YellowBalls and not dragging:
                ball.showRing(ball.x, ball.y)
            elif ball.color == black:
                ball.showRing()
            elif ball.color == brown:
                ball.equationTextRect = ball.equationText.get_rect()
                ball.equationTextRect.center = (ball.x, ball.y-30)
                ball.shownAnswerTextRect = ball.shownAnswerText.get_rect()
                ball.shownAnswerTextRect.center = (ball.x, ball.y+30)
                screen.blit(ball.equationText, ball.equationTextRect)
                screen.blit(ball.shownAnswerText, ball.shownAnswerTextRect)
            if ball.graydius >= 360:
                if ball.color != brown:
                    ball.Graction()
                elif ball.temp[1] == "-" and int(ball.shownAnswer) == int(ball.temp[0])-int(ball.temp[2]):
                    ball.Graction()
                elif ball.temp[1] == "+" and int(ball.shownAnswer) == int(ball.temp[0])+int(ball.temp[2]):
                    ball.Graction()
                elif ball.temp[1] == "x" and int(ball.shownAnswer) == int(ball.temp[0])*int(ball.temp[2]):
                    ball.Graction()
                else:
                    allBalls.remove(ball)
                    ballAmount -= 1
        scoreText = medFont.render(f'{score}', True, black)
        scoreText.set_alpha(100)
        scoreRect = scoreText.get_rect(center=(600, 345))
        screen.blit(scoreText, (scoreRect))
        if displayCleanSlate == True:
            dcsDuration = pygame.time.get_ticks()
            score += 5
            displayCleanSlate = False
        if dcsDuration - dcsTime <= 1000 and dcsTime != 0:
            dcsDuration = pygame.time.get_ticks()
            screen.blit(cleanSlateText, (cleanSlateRect))
    pygame.display.flip()
pygame.quit()

print(f'Last score: {scores[0]}')