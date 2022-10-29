import pygame
from receive_note_and_play import receive_a_note_to_play as playNote
import random

pygame.init()
pygame.font.init()
running = True  

# setando o tamanho da tela e titulo da janela
tela = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Joguinho")

commonNotes = ["C", "G", "E", "F" , "G" , "A", "B"]
random.shuffle(commonNotes)

# in case of increasing difficulty
# the idea is to creat an array that will be used on the game,
# if we increase the difficulty we can concat these new arrays on it
flatNotes = ["Bb" , "Eb", "Ab", "Db" , "Gb", "Cb" , "Fb"]
sharpNotes = ["F#", "C#", "G#", "D#", "A#", "E#", "B#"]

# variaveis para testar a interface
currentNote = 0
testInt = 0
play = False


# setando as fontes a serem usadas
screen = pygame.display.get_surface()
titleFont = pygame.font.SysFont('Comic Sans MS', 60)
feedbackProgressActionFont = pygame.font.SysFont('Comic Sans MS', 50)
keyPressFont = pygame.font.SysFont('Comic Sans MS', 30)


def next_note(n):
    # generates sound
    # if we choose to increase difficulty we can reduce the times that the sound is repeated
    songEnded = playNote(commonNotes[n])
    print(songEnded)

# funcao que eh chamada para renderizar a tela
def render():
    screen.fill(pygame.Color("black"))

    # as variaveis com Text sao para setar o texto, e a sua cor em RGB
    # a funcao tela.blit eh para renderizar o texto na posicao x,y
    titleText = titleFont.render('NoteGuesser', True, (255, 255, 255))
    tela.blit(titleText, (416, 50))

    playingNoteText = feedbackProgressActionFont.render('Playing the Note...', True, (218, 196, 1))
    rightAnswerText = feedbackProgressActionFont.render('YOU GOT IT!', True, (1, 218, 49))
    wrongAnswerText = feedbackProgressActionFont.render('Wrong... But you can try again', True, (220, 49, 49))
    
    if testInt == 1:
        tela.blit(playingNoteText, (476, 222))

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

# loop que ficara rodando enquanto o jogo estiver aberto
while running:

    pygame.time.delay(100)

    # funcao para poder clicar no x e fechar o jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # chamada da funcao render
    render()
    
    if play:
        next_note(currentNote)
        play = False
    
    # funcao para receber input do teclado    
    keys = pygame.key.get_pressed()
    
    # aloca uma acao a cada input de teclado
    if keys[pygame.K_RETURN]:
        testInt = 1
        play = True
    if keys[pygame.K_SPACE]:
        currentNote += 1
        testInt = 1
        play = True
    if keys[pygame.K_1]:
        testInt = 2
    if keys[pygame.K_2]:
        testInt = 3

    if currentNote >= 8:
        currentNote = 1
        testInt = 0

    # atualiza o display com a nova tela renderizada
    pygame.display.update()
