import pygame
import numpy

pygame.init()
pygame.font.init()
running = True  

tela = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Joguinho")

currentNote = 1
testInt = 0

screen = pygame.display.get_surface()
titleFont = pygame.font.SysFont('Comic Sans MS', 60)
feedbackProgressActionFont = pygame.font.SysFont('Comic Sans MS', 50)
keyPressFont = pygame.font.SysFont('Comic Sans MS', 30)

def render():
    screen.fill(pygame.Color("black"))

    titleText = titleFont.render('NoteGuesser', True, (255, 255, 255))
    tela.blit(titleText, (416, 50))

    listeningText = feedbackProgressActionFont.render('Listening...', True, (218, 196, 1))
    rightAnswerText = feedbackProgressActionFont.render('YOU GOT IT!', True, (1, 218, 49))
    wrongAnswerText = feedbackProgressActionFont.render('Wrong... But you can try again', True, (220, 49, 49))
    if testInt == 1:
        tela.blit(listeningText, (476, 222))

    if testInt == 2:
        tela.blit(rightAnswerText, (440, 222))

    if testInt == 3:
        tela.blit(wrongAnswerText, (239, 222))

    progressText = feedbackProgressActionFont.render('%d / 7'%currentNote, False, (218, 196, 1))
    if testInt > 0:
        tela.blit(progressText, (538, 380))

    action1Text = feedbackProgressActionFont.render('START', True, (255, 255, 255))
    action2Text = feedbackProgressActionFont.render('SKIP', True, (255, 255, 255))
    tela.blit(action1Text, (253, 538))
    tela.blit(action2Text, (798.5, 538))

    key1Text = keyPressFont.render('Press "Enter"', True, (0, 240, 255))
    key2Text = keyPressFont.render('Press "Space"', True, (0, 240, 255))
    tela.blit(key1Text, (244, 608))
    tela.blit(key2Text, (761, 608))

while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    render()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        testInt = 1
    if keys[pygame.K_SPACE]:
        currentNote += 1
        testInt = 1
    if keys[pygame.K_1]:
        testInt = 2
    if keys[pygame.K_2]:
        testInt = 3

    if currentNote >= 8:
        currentNote = 1
        testInt = 0

    pygame.display.update()