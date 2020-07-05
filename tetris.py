import random

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
            self.checkAndDestroyLine()
            self.newBlock()
        else:
            self.wipeBlockFromMap()
            self.currentBlock.y -= 1

        self.putBlockOnMap()


    def rotate(self, direction):
        self.wipeBlockFromMap()
        self.currentBlock.rotate(direction)

        if self.currentBlock.x < 0:
            self.currentBlock.x = 0
        elif self.currentBlock.x + self.currentBlock.w > self.mapWidth:
            self.currentBlock.x = self.mapWidth - self.currentBlock.w

        self.putBlockOnMap()


    def move(self, direction):
        self.wipeBlockFromMap()

        if direction == 'right':
            if self.currentBlock.x < self.mapWidth - self.currentBlock.w:
                self.currentBlock.x += 1
        elif direction == 'left':
            if self.currentBlock.x > 0:
                self.currentBlock.x -= 1
        else:
            raise ValueError(f'invalid direction type (expected \'right\' or \'left\', got: {direction})')

        self.putBlockOnMap()


    def drop(self):
        while not self.isLaying():
            self.tetris()
        self.tetris()


    def checkAndDestroyLine(self):
        for i in range(self.currentBlock.h):
            for j in self.map[self.currentBlock.y + i]:
                if not j:
                    break
            else:
                for j in range(self.currentBlock.y + i, self.mapHeight):
                    try:
                        self.map[j] = self.map[j + 1]
                    except:
                        pass


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
        self.currentBlock = Block(random.randrange(7))
        self.currentBlock.x = int((self.mapWidth - self.currentBlock.w) / 2)
        self.currentBlock.y = self.mapHeight - self.currentBlock.h

        self.blocksCounter += 1


    def putBlockOnMap(self, delBlock=False):
        for i in range(self.currentBlock.h):
            for j in range(self.currentBlock.w):
                if delBlock and self.currentBlock.block[i][j]:
                    self.map[self.currentBlock.y + i][self.currentBlock.x + j] = False
                elif self.map[self.currentBlock.y + i][self.currentBlock.x + j] or self.currentBlock.block[i][j]:
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
            for i in range(len(tmpBlock[0]) - 1, -1, -1):
                self.block.append([x[i] for x in tmpBlock])
            self.x += int((self.w - len(self.block[0])) / 2)
        elif direction == 'ccw':
            pass
        else:
            raise ValueError(f'invalid direction type (expected \'cw\' or \'ccw\', got: {direction})')    

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


def main():
    pass

if __name__ == "__main__":
    main()