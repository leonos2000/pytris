import os
import random
import time


class Tetris:

    def __init__(self, height=20, width=10):
        self.mapWidth = width
        self.mapHeight = height
        self.map = []

        for i in range(height):
            self.map.append(list([False for j in range(width)]))

        random.seed()

        self.score = 0
        self.blocksCounter = 0

        self.newBlock()
        self.putBlockOnMap()


    def tetris(self):
        if self.isLaying():
            self.newBlock()
        else:
            self.wipeBlockFromMap()
            self.currentBlock.y -= 1

        self.putBlockOnMap()


    def isLaying(self):
        if self.currentBlock.y == 0:
            return True
        else:
            i = 0
            for skirtLine in self.currentBlock.skirt():
                if self.map[self.currentBlock.y - 1 + skirtLine][self.currentBlock.x + i]:
                    return True
                i += 1
        return False


    def newBlock(self):
        self.currentBlock = Block(random.randrange(6))
        self.currentBlock.x = int((self.mapWidth - self.currentBlock.w) / 2)
        self.currentBlock.y = self.mapHeight - self.currentBlock.h

        self.blocksCounter += 1

    def putBlockOnMap(self, delBlock=False):
        for i in range(self.currentBlock.h):
            for j in range(self.currentBlock.w):
                if delBlock:
                    self.map[self.currentBlock.y + i][self.currentBlock.x + j] = False
                elif self.map[self.currentBlock.y + i][self.currentBlock.x + j] ^ self.currentBlock.block[i][j]:
                    self.map[self.currentBlock.y + i][self.currentBlock.x + j] = True

    def wipeBlockFromMap(self):
        self.putBlockOnMap(True)


class Block:

    def __init__(self, blockType, x=0, y=0, blockPreset=None):
        """
        Blocks in default preset:
            0 - long skinny one
            1 - L
            2 - L mirrored
            3 - S
            4 - S mirrored
            5 - square
            6 - pyramid
        """
        if not blockPreset:
            blockPreset = [
                [[True, True, True, True]],
                [[True, True], [True, False], [True, False]],
                [[True, True], [False, True], [False, True]],
                [[True, True, False], [False, True, True]],
                [[False, True, True], [True, True, False]],
                [[True, True], [True, True]],
                [[True, True, True], [False, True, False]]
            ]
        
        self.block = blockPreset[blockType]

        self.x = x
        self.y = y
        self.w = len(self.block[0])
        self.h = len(self.block)


    def rotate(self, direction='cw'):
        tmpBlock = self.block
        self.block = []

        if direction == 'cw':
            start1 = len(tmpBlock[0]) - 1
            start2 = len(tmpBlock) - 1
            end1 = end2 = step = -1
        elif direction == 'ccw':
            start1 = start2 = 0
            end1 = len(tmpBlock[0])
            end2 = len(tmpBlock)
            step = 1
        else:
            raise ValueError(f'invalid direction type (expected \'cw\' or \'ccw\', got: {direction})')    


        for i in range(start1, end1, step):
            line = []
            for j in range(start2, end2, step):
                line.append(tmpBlock[j][i])
            self.block.append(line)

        self.w = len(self.block[0])
        self.h = len(self.block)


    def skirt(self):
        skirt = []
        
        for i in range(len(self.block[0])):
            for j in range(len(self.block)):
                if self.block[j][i]:
                    skirt.append(j)
                    break

        return skirt

    
class SimplestGui:

    def __init__(self):
        pass
        self._clean()

    def _clean(self):
        if 'nt' in os.name:
            os.system('cls')
        else:
            os.system('clear')

    def render(self, data):

        buffer = ''

        for i in data:
            for j in i:
                buffer += 'O' if j else ' '
            buffer += '\r\n'
        
        self._clean()
        print(buffer[::-1])



def main():
    tetris = Tetris()
    gui = SimplestGui()
    gui.render(tetris.map)

    while True:
        tetris.tetris()
        gui.render(tetris.map)
        print(tetris.currentBlock.skirt())
        time.sleep(0.2)


if __name__ == "__main__":
    main()