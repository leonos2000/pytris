import pygame
import pytris
        

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

def displayBlocks(x, y, tetrisData):
    tmpX = x
    for line in tetrisData:
        x = tmpX
        for block in line:
            if block != tetris.emptyMapVal:
                displayBlock(x, y, block)
            x += 40
        y -= 40


def renderBlocks():
    displayBlocks(100, 860, tetris.map)
    holdedBlock = pytris.Block(tetris.holdedBlock)
    displayBlocks(540, 220, holdedBlock.block)
    nextBlock = pytris.Block(tetris.queue[0])
    displayBlocks(540, 440, nextBlock.block)

    nextX = 540
    nextY = 440

    for block in holdedBlocks():
        displayBlocks(nextX, nextY, block)
        nextY += 160


def renderText(x, y, text):
    infoText = pygame.font.Font('freesansbold.ttf', 40)
    textSurface = infoText.render(text, True, colorRGB('black'))
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    gameDisplay.blit(textSurface, textRect)


def holdedBlocks():
    for block in tetris.queue:
        nextBlock = pytris.Block(block)
        yield nextBlock.block


tetris = pytris.Tetris()

pygame.init()

displayWidth = 800
displayHeight = 1000

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Pytris with pygame frontend')

clock = pygame.time.Clock()

speedCounter = 0
crashed = False
while not crashed:
    gameDisplay.fill(colorRGB('white'))
    pygame.draw.rect(gameDisplay, colorRGB('black'), (100, 100, 400, 800))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tetris.move('left')
            elif event.key == pygame.K_RIGHT:
                tetris.move('right')
            elif event.key == pygame.K_UP:
                tetris.rotate('cw')
            elif event.key == pygame.K_SPACE:
                tetris.hardDrop()
            elif event.key == pygame.K_DOWN:
                tetris.softDrop()
            elif event.key == pygame.K_c:
                tetris.hold()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                tetris.endSoftDrop()

        print(event)

    
    if speedCounter / 60 > tetris.delay / 1000:
        if not tetris.tetris():
            crashed = True
        speedCounter = 0
    else:
        speedCounter += 1

    renderBlocks()
    renderText(620, 80, 'HOLD')
    renderText(620, 280, 'NEXT')
    renderText(320, 40, f'SCORE: {tetris.score} LEVEL: {tetris.level} LINES: {tetris.destroyedLines}')
    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()