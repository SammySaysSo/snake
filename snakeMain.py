# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 17:09:50 2021

@author: sambr
"""
import pygame, sys, random
from pygame.math import Vector2

class Central:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        
    def update(self):
        self.snake.moveSnake()
        self.checkCollision()
        self.checkFail()
        
    def drawElements(self):
        self.drawGrass()
        self.fruit.drawFruit()
        self.snake.drawSnake()
        self.drawScore()
        if self.snake.direction.x == 0 and self.snake.direction.y == 0: self.drawOtherText()
        
    def checkCollision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomizePos()
            self.snake.addBlock()
            self.snake.playCrunchSound()
        for bod in self.snake.body[1:]:
            if bod == self.fruit.pos: self.fruit.randomizePos()
    
    def checkFail(self):
        if self.snake.body[0].x >= cellNumber or self.snake.body[0].x < 0 or self.snake.body[0].y >= cellNumber or self.snake.body[0].y < 0:
            self.gameOver()
        for bod in self.snake.body[1:]:
            if bod == self.snake.body[0]: self.gameOver()
        
    def gameOver(self):
        self.snake.reset()
        
    def drawGrass(self):
        for row in range(cellNumber):
            if row % 2 == 0:
                for col in range(cellNumber):
                    if col % 2 == 0: pygame.draw.rect(screen, (167, 209, 61), (col*cellSize, row*cellSize, cellSize, cellSize))
            else:
                for col in range(cellNumber):
                    if col % 2 != 0: pygame.draw.rect(screen, (167, 209, 61), (col*cellSize, row*cellSize, cellSize, cellSize))

    def drawScore(self):
        scoreText = 'Score: ' + str((len(self.snake.body)-3)*10)
        scoreSurface = gameFont.render(scoreText, True, (56, 74, 12)) #antialias = more smoother(not much differnce)
        screen.blit(scoreSurface, (10, 10, 100, 100))

    def drawOtherText(self):
        titleText = 'SNAKE'
        creditText = 'Made by Sam Brey'
        playText = 'Eat apples to get bigger'
        rulesText = 'You lose by running into yourself'
        rulesText2 = 'You lose by running into the walls'
        rulesText3 = 'Start by pressing the arrow/wsad keys'
        rulesText4 = 'Have fun'
        titleSurface = titleFont.render(titleText, True, (56, 74, 12))
        textSurface1 = otherFont.render(creditText, True, (56, 74, 12))
        textSurface2 = otherFont.render(playText, True, (56, 74, 12))
        textSurface3 = otherFont.render(rulesText, True, (56, 74, 12))
        textSurface4 = otherFont.render(rulesText2, True, (56, 74, 12))
        textSurface5 = otherFont.render(rulesText3, True, (56, 74, 12))
        textSurface6 = otherFont.render(rulesText4, True, (56, 74, 12))
        screen.blit(titleSurface, (100, 250, 100, 100))
        screen.blit(textSurface1, (100, 450, 100, 100))
        screen.blit(textSurface2, (100, 500, 100, 100))
        screen.blit(textSurface3, (100, 550, 100, 100))
        screen.blit(textSurface4, (100, 600, 100, 100))
        screen.blit(textSurface5, (100, 650, 100, 100))
        screen.blit(textSurface6, (100, 700, 100, 100))
    
class Snake():
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.c = 1
        
        self.headUp = pygame.image.load('headUp.png').convert_alpha()
        self.headDown = pygame.image.load('headDown.png').convert_alpha()
        self.headLeft = pygame.image.load('headLeft.png').convert_alpha()
        self.headRight = pygame.image.load('headRight.png').convert_alpha()
        
        self.tailUp = pygame.image.load('tailUp.png').convert_alpha()
        self.tailDown = pygame.image.load('tailDown.png').convert_alpha()
        self.tailRight = pygame.image.load('tailRight.png').convert_alpha()
        self.tailLeft = pygame.image.load('tailLeft.png').convert_alpha()
        
        self.bodyVertical = pygame.image.load('bodyVertical.png').convert_alpha()
        self.bodyHorizontal = pygame.image.load('bodyHorizontal.png').convert_alpha()
        
        self.bodyTR = pygame.image.load('bodyTR.png').convert_alpha()
        self.bodyTL = pygame.image.load('bodyTL.png').convert_alpha()
        self.bodyBR = pygame.image.load('bodyBR.png').convert_alpha()
        self.bodyBL = pygame.image.load('bodyBL.png').convert_alpha()
        
        self.crunchSound = pygame.mixer.Sound('soundCrunch.wav')
        
    def drawSnake(self):
        for index, bod in enumerate(self.body): #enumerate gives us the index on what object we are in inside the list
            blockRect = (int(bod.x*cellSize), int(bod.y*cellSize), cellSize, cellSize)
            if index == 0: #always going to be the head
                screen.blit(self.updateHeadGraphic(), blockRect)
            elif index == len(self.body)-1:
                screen.blit(self.updateTailGraphic(), blockRect)
            else:
                previouseBlock = self.body[index + 1] - bod
                nextBlock = self.body[index-1] - bod
                if previouseBlock.x == nextBlock.x: screen.blit(self.bodyVertical, blockRect)
                if previouseBlock.y == nextBlock.y: screen.blit(self.bodyHorizontal, blockRect)
                else:
                    if previouseBlock.x == -1 and nextBlock.y == -1 or previouseBlock.y == -1 and nextBlock.x == -1: screen.blit(self.bodyTL, blockRect)
                    if previouseBlock.x == -1 and nextBlock.y == 1 or previouseBlock.y == 1 and nextBlock.x == -1: screen.blit(self.bodyBL, blockRect)
                    if previouseBlock.x == 1 and nextBlock.y == -1 or previouseBlock.y == -1 and nextBlock.x == 1: screen.blit(self.bodyTR, blockRect)
                    if previouseBlock.x == 1 and nextBlock.y == 1 or previouseBlock.y == 1 and nextBlock.x == 1: screen.blit(self.bodyBR, blockRect)                
    
    def updateHeadGraphic(self):
        if self.direction.x == 1: return self.headRight
        if self.direction.x == -1: return self.headLeft
        if self.direction.y == 1: return self.headDown
        if self.direction.y == -1: return self.headUp
        return self.headRight
    
    def updateTailGraphic(self):
        cx = self.body[len(self.body)-2].x - self.body[len(self.body)-1].x
        cy = self.body[len(self.body)-2].y - self.body[len(self.body)-1].y
        if cx > 0 and cy == 0: return self.tailLeft
        if cx < 0 and cy == 0: return self.tailRight
        if cy > 0 and cx == 0: return self.tailUp
        if cy < 0 and cx == 0: return self.tailDown
        
    def moveSnake(self):
        bodyCopy = self.body[:-1]
        bodyCopy.insert(0, bodyCopy[0] + self.direction)
        self.body = bodyCopy[:]
        
    def addBlock(self):
        self.body.append(Vector2(self.body[len(self.body)-2].x, self.body[len(self.body)-2].y))

    def playCrunchSound(self):
        self.crunchSound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        
    def music(self):
        if self.body == [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)] and len(self.body) == 3: 
            pygame.mixer.music.stop()
            self.c = 1
        elif self.c == 1: 
            pygame.mixer.music.play(-1)
            self.c += 1

class Fruit():
    def __init__(self):
        self.x = random.randint(0, cellNumber-1)
        self.y = random.randint(0, cellNumber-1)
        self.pos = Vector2(self.x, self.y)
        
    def drawFruit(self):
        screen.blit(apple, pygame.Rect((int(self.pos.x*cellSize), int(self.pos.y*cellSize), cellSize, cellSize)))
    
    def randomizePos(self):
        self.x = random.randint(0, cellNumber-1)
        self.y = random.randint(0, cellNumber-1)
        self.pos = Vector2(self.x, self.y)
        # test out int & pos

pygame.mixer.pre_init(44100, -16, 2, 512) #does this do anything?
pygame.init()
clock = pygame.time.Clock()

cellSize = 40
cellNumber = 20
screen = pygame.display.set_mode((cellSize * cellNumber, cellSize * cellNumber))

apple = pygame.image.load('apple.png').convert_alpha()
gameFont = pygame.font.Font(None, 50) #change font by download of githum if u want
titleFont = pygame.font.Font(None, 200)
otherFont = pygame.font.Font(None, 50)

gold = (175, 215, 70)

def main():
    mainGame = Central()
    screenUpdate = pygame.USEREVENT #these 2 lines of code is a timer
    pygame.time.set_timer(screenUpdate, 150)
    pygame.mixer.music.load('heroesTonight.wav')
    pygame.mixer.music.play(-1)
    run = True
    while run:
        screen.fill(gold)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            if event.type == screenUpdate: #snake always moves every 150ms
                mainGame.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if mainGame.snake.direction.y != 1: mainGame.snake.direction = Vector2(0, -1)  
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if mainGame.snake.direction.y != -1: mainGame.snake.direction = Vector2(0, 1) 
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if mainGame.snake.direction.x != 1: mainGame.snake.direction = Vector2(-1, 0) 
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if mainGame.snake.direction.x != -1: mainGame.snake.direction = Vector2(1, 0) 
            
          
        mainGame.drawElements()
        mainGame.snake.music()
        
        clock.tick(60)
        pygame.display.update()

main()