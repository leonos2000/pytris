import pygame
from pytris import Tetris
        

def colorRGB(color='white'):
    if color == 'white':
        return (255, 255, 255)
    elif color == 'black':
        return (0, 0, 0)
    elif color == 'cyan':
        return (0, 255, 255)
    elif color == 'blue':
        return (0, 0, 255)
    elif color == 'red':
        return (255, 0, 0)
    elif color == 'yellow':
        return (255, 255, 0)
    elif color == 'orange':
        return (255, 165, 0)
    elif color == 'green':
        return (0, 255, 0)
    elif color == 'magenta':
        return (255, 0, 255)


def displayBlock(x, y, blockCode):
    gameDisplay.blit(pygame.image.load(f'blockImages/block{blockCode}.png'), (x, y))

def displayMainFrame(x, y, tetrisData):
    for line in tetrisData:
        x = 100
        for block in line:
            if block != tetris.emptyMapVal:
                displayBlock(x, y, block)
            x += 40
        y -= 40


tetris = Tetris()

pygame.init()

displayWidth = 800
displayHeight = 1000

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Pytris with pygame frontend')

clock = pygame.time.Clock()

tetrisSpeed = 60
speedCounter = 0
crashed = False
while not crashed:
    gameDisplay.fill(colorRGB('white'))
    pygame.draw.rect(gameDisplay, colorRGB('black'), (100, 140, 400, 800))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tetris.move('left')
            elif event.key == pygame.K_RIGHT:
                tetris.move('right')
            elif event.key == pygame.K_UP:
                tetris.rotate('cw')
            elif event.key == pygame.K_SPACE:
                tetris.drop()

        displayMainFrame(100, 900, tetris.map)
        pygame.display.update()

        print(event)

    
    if speedCounter % tetrisSpeed == 0:
        tetris.tetris()

    displayMainFrame(100, 900, tetris.map)

    pygame.display.update()
    clock.tick(60)
    speedCounter += 1

pygame.quit()
quit()