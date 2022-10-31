from operator import truediv
from xmlrpc.client import boolean
import pygame
from receive_note_and_play import receive_a_note_to_play as playNote
import random

pygame.init()
pygame.font.init()
running = True  

# setando o tamanho da tela e titulo da janela
tela = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Joguinho")

# variaveis para testar a interface
currentNote = 0
noteIndex = 1
gameState = 0
play = False

noteDictionary = {
  "C": "DO",
  "D": "RE",
  "E": "MI",
  "F": "FA",
  "G": "SOL",
  "A": "LA",
  "B": "SI",
}

commonNotes = ["C", "D", "E", "F" , "G" , "A", "B"]
random.shuffle(commonNotes)

answersArray = ["DO", "RE", "MI", "FA", "SOL", "LA", "SI"]

# in case of increasing difficulty
# the idea is to creat an array that will be used on the game,
# if we increase the difficulty we can concat these new arrays on it
#flatNotes = ["Bb" , "Eb", "Ab", "Db" , "Gb", "Cb" , "Fb"]
#sharpNotes = ["F#", "C#", "G#", "D#", "A#", "E#", "B#"]

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
    tela.blit(titleText, (416.5, 50))

    playingNoteText = feedbackProgressActionFont.render('Playing note: %d / 7'%noteIndex , False, (218, 196, 1))
    rightAnswerText = feedbackProgressActionFont.render('YOU GOT IT!', True, (1, 218, 49))
    wrongAnswerText = feedbackProgressActionFont.render('Wrong... But you can try again', True, (220, 49, 49))
    gameEndingText = feedbackProgressActionFont.render('Congratulations you won!', True, (1, 218, 49))
    
    if gameState == 1:
        tela.blit(playingNoteText, (385, 208))

    if gameState == 2:
        tela.blit(rightAnswerText, (440, 208))

    if gameState == 3:
        tela.blit(wrongAnswerText, (239, 208))

    if gameState == 4:
        tela.blit(gameEndingText, (315, 208))

    if gameState > 0:
        note1Text = feedbackProgressActionFont.render(answersArray[0], True, (255, 255, 255))
        note2Text = feedbackProgressActionFont.render(answersArray[1], True, (255, 255, 255))
        note3Text = feedbackProgressActionFont.render(answersArray[2], True, (255, 255, 255))
        note4Text = feedbackProgressActionFont.render(answersArray[3], True, (255, 255, 255))
        note5Text = feedbackProgressActionFont.render(answersArray[4], True, (255, 255, 255))
        note6Text = feedbackProgressActionFont.render(answersArray[5], True, (255, 255, 255))
        note7Text = feedbackProgressActionFont.render(answersArray[6], True, (255, 255, 255))
        tela.blit(note1Text, (87, 352))
        tela.blit(note2Text, (249.5, 352))
        tela.blit(note3Text, (403, 352))
        tela.blit(note4Text, (563.5, 352))
        tela.blit(note5Text, (703.5, 352))
        tela.blit(note6Text, (880.5, 352))
        tela.blit(note7Text, (1039.5, 352))

        key1Text = keyPressFont.render('Press "1"', True, (0, 240, 255))
        key2Text = keyPressFont.render('Press "2"', True, (0, 240, 255))
        key3Text = keyPressFont.render('Press "3"', True, (0, 240, 255))
        key4Text = keyPressFont.render('Press "4"', True, (0, 240, 255))
        key5Text = keyPressFont.render('Press "5"', True, (0, 240, 255))
        key6Text = keyPressFont.render('Press "6"', True, (0, 240, 255))
        key7Text = keyPressFont.render('Press "7"', True, (0, 240, 255))
        tela.blit(key1Text, (64, 422))
        tela.blit(key2Text, (217, 422))
        tela.blit(key3Text, (375, 422))
        tela.blit(key4Text, (533, 422))
        tela.blit(key5Text, (691, 422))
        tela.blit(key6Text, (849, 422))
        tela.blit(key7Text, (1007, 422))

    action1Text = feedbackProgressActionFont.render('START', True, (255, 255, 255))
    action2Text = feedbackProgressActionFont.render('SKIP', True, (255, 255, 255))
    tela.blit(action1Text, (253, 538))
    tela.blit(action2Text, (798.5, 538))

    keyEnterText = keyPressFont.render('Press "Enter"', True, (0, 240, 255))
    keySpaceText = keyPressFont.render('Press "Space"', True, (0, 240, 255))
    tela.blit(keyEnterText, (244, 608))
    tela.blit(keySpaceText, (761, 608))

# loop que ficara rodando enquanto o jogo estiver aberto
while running:

    pygame.time.delay(100)

    # funcao para poder clicar no x e fechar o jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # chamada da funcao render
    render()

    pygame.display.flip()

    if play:
        next_note(currentNote)
        play = False
    
    # funcao para receber input do teclado    
    keys = pygame.key.get_pressed()

    # aloca uma acao a cada input de teclado
    if keys[pygame.K_RETURN]:
        gameState = 1
        play = True
    if keys[pygame.K_SPACE]:
        currentNote += 1
        noteIndex += 1
        gameState = 1
        if currentNote < 7:
            play = True
    if keys[pygame.K_1]:
        if (answersArray[0] == noteDictionary[commonNotes[currentNote]]):
            gameState = 2
        else:
            gameState = 3
    if keys[pygame.K_2]:
        if (answersArray[1] == noteDictionary[commonNotes[currentNote]]):
            gameState = 2
        else:
            gameState = 3
    if keys[pygame.K_3]:
        if (answersArray[2] == noteDictionary[commonNotes[currentNote]]):
            gameState = 2
        else:
            gameState = 3
    if keys[pygame.K_4]:
        if (answersArray[3] == noteDictionary[commonNotes[currentNote]]):
            gameState = 2
        else:
            gameState = 3
    if keys[pygame.K_5]:
        if (answersArray[4] == noteDictionary[commonNotes[currentNote]]):
            gameState = 2
        else:
            gameState = 3
    if keys[pygame.K_6]:
        if (answersArray[5] == noteDictionary[commonNotes[currentNote]]):
            gameState = 2
        else:
            gameState = 3
    if keys[pygame.K_7]:
        if (answersArray[6] == noteDictionary[commonNotes[currentNote]]):
            gameState = 2
        else:
            gameState = 3

    if currentNote >= 7:
        gameState = 4
        pygame.display.flip()
        pygame.time.delay(4500)
        running = False


    # atualiza o display com a nova tela renderizada
    pygame.display.update()
