'''This is the main program for the fourth version of a mini-game of football/
soccer in PyGame. Compared to the previous versions, this version enhances
players' movements.'''

import pygame, random, math
import NonplayerClasses as np
import PlayerClasses as pl

pygame.init()   # start pygame

pygame.display.set_caption('My First Game')   # game title
screenSize = 500, 500   # screen size

# create objects that will appear on the screen
bg = np.Background(screenSize)
goal = np.Goal(screenSize)
goalkeeper = pl.Goalkeeper(screenSize)
striker = pl.Outfielder(screenSize)
midfielder = pl.Outfielder(screenSize)
ball = np.Ball(screenSize)

# load objects into pygame
bg.load('grass')
goal.load('goalLeft', 'goalMiddle', 'goalRight')
goalkeeper.load('playerFoot', 'playerBody')
striker.load('playerFoot', 'playerBody')
midfielder.load('playerFoot', 'playerBody')
ball.load('ball')

# draw the objects onto the screen
bg.blit()
goal.blit()
goalkeeper.blitFeet()
striker.blitFeet()
midfielder.blitFeet()
ball.blit()
goalkeeper.blitBody()
striker.blitBody()
midfielder.blitBody()

players = goalkeeper, striker, midfielder

# list of everything on the screen
allThings = bg.things + goal.things
for player in players:
    allThings += player.things[:2]   # player's feet
allThings += ball.things
for player in players:
    allThings.append(player.things[2])   # player's body

# list of those things' positions at the start of the program
allPos = [bg.pos] + goal.getPos()
for player in players:
    allPos += player.getStartPos()[:2]   # player's feet
allPos += ball.getStartPos()
for player in players:
    allPos.append(player.getStartPos()[2])   # player's body

# turn the lists into class attributes
for thing in (ball,) + players:
    thing.allThings, thing.allPos = allThings, allPos

gkStartSpeed = goalkeeper.speed   # goalkeeper's initial speed

# keys that will initiate player movements
moveKeys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
            pygame.K_SPACE, pygame.K_RSHIFT]
pygame.key.set_repeat(1)   # control how held keys are repeated

playing = True
while playing:
    # process events in the game
    for event in pygame.event.get():
        pressedKeys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or pressedKeys[pygame.K_ESCAPE] or \
           (pressedKeys[pygame.K_LCTRL] and pressedKeys[pygame.K_w]):
            playing = False
                
    pressedKeys = pygame.key.get_pressed()
    moveType, direction = bg.processMoveKeys(pressedKeys)    
    striker.move(moveType, direction, ball)
    if striker.moved:
        striker.updateAll()
        
    goalkeeper.moveAcross(goal)
    goalkeeper.updateAll()
                        
    if pressedKeys[pygame.K_s]:
        for player in players[1:]:
            if player.getDistToBall(ball)[2]<=goalkeeper.getDistToBall(ball)[2]:
                player.kickBall(ball)
                if player.touchedBall:
                    bg.processMovements(ball, goal, players)
                    if ball.gkCaught:   # ball caught by goalkeeper
                        goalkeeper.speed = 0
                        pygame.time.wait(200)   # pause program for 200 ms
                        goalkeeper.kickBall(ball, gk=True)
                        ball.gkCaught = False   # reset
                        goalkeeper.speed = gkStartSpeed   # reset
                        bg.processMovements(ball, goal, players)
                    break
            else:
                goalkeeper.kickBall(ball, gk=True)
                if goalkeeper.touchedBall:
                    goalkeeper.speed = gkStartSpeed   # reset
                    ball.gkCaught = False
                    bg.processMovements(ball, goal, players)
        if ball.inGoal:
            ball.reset()   # return to its original position
                        
    bg.updateDisplay()

pygame.quit()
