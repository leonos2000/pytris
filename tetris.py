import random
from functools import wraps
import os
import copy

class Tetris:

    def __init__(self, height=20, width=10):
        self.mapWidth = width
        self.mapHeight = height

        self.map = []
        self.emptyMapVal = -1
        self.score = 0
        self.blocksCounter = 0
        self.destroyedLines = 0
        self.holdedBlock = 7
        self.lastHoldedBlockNumber = 0
        
        for i in range(height):
            self.map.append(list([self.emptyMapVal for j in range(width)]))

        random.seed()

        self.newBlock()
        self.putBlockOnMap()


    def tetris(self):
        if self.isLaying():
            self.checkAndDestroyLine()
            if not self.newBlock():
                return (True, self.blocksCounter, self.destroyedLines)
            self.blocksCounter += 1
        else:
            self.wipeBlockFromMap()
            self.currentBlock.y -= 1

        self.putBlockOnMap()

        return (False, self.blocksCounter, self.destroyedLines)


    def put_block_on_map(func):
        @wraps(func)
        def wrapper(self, direction):
            func(self, direction)
            self.putBlockOnMap()
        return wrapper


    @put_block_on_map
    def rotate(self, direction):
        self.wipeBlockFromMap()

        blockBackup = copy.copy(self.currentBlock)

        self.currentBlock.rotate(direction)
        if not self.isColliding():
            return

        self.currentBlock.x += 1
        if not self.isColliding():
            return

        self.currentBlock.x -= 2
        if not self.isColliding():
            return

        self.currentBlock = copy.copy(blockBackup)


    def move(self, direction):
        self.wipeBlockFromMap()

        if direction == 'right':
            if self.currentBlock.x < self.mapWidth - self.currentBlock.w:
                self.currentBlock.x += 1
                if self.isColliding():
                    self.currentBlock.x -= 1
        elif direction == 'left':
            if self.currentBlock.x > 0:
                self.currentBlock.x -= 1
                if self.isColliding():
                    self.currentBlock.x += 1
        else:
            raise ValueError(f'invalid direction type (expected \'right\' or \'left\', got: {direction})')

        self.putBlockOnMap()


    def drop(self):
        while not self.isLaying():
            self.tetris()
        self.tetris()

    
    def hold(self):
        if self.lastHoldedBlockNumber == self.blocksCounter:
            return

        self.lastHoldedBlockNumber = self.blocksCounter
        newHoldedBlock = self.currentBlock.blockType

        self.wipeBlockFromMap()
        self.newBlock(self.holdedBlock if self.holdedBlock < 6 else -1)
        self.putBlockOnMap()

        self.holdedBlock = newHoldedBlock


    def checkAndDestroyLine(self):
        for i in range(self.currentBlock.h - 1, -1, -1):
            for j in self.map[self.currentBlock.y + i]:
                if j == self.emptyMapVal:
                    break
            else:
                for j in range(self.currentBlock.y + i, self.mapHeight):
                    if j == self.mapHeight - 1:
                        self.map[j] = [self.emptyMapVal for x in self.map[j]]
                    else:
                        self.map[j] = self.map[j + 1]

                self.destroyedLines += 1
        

    def isLaying(self):
        if self.currentBlock.y == 0:
            return True
        else:
            i = 0
            for skirtLine in self.currentBlock.skirt():
                if self.map[self.currentBlock.y - 1 + skirtLine][self.currentBlock.x + i] != self.emptyMapVal:
                    return True
                i += 1
        return False
    

    def isColliding(self):
        for i in range(self.currentBlock.h):
            for j in range(self.currentBlock.w):
                if (0 < (self.currentBlock.y + i) < len(self.map)) and (0 <= (self.currentBlock.x + j) < (len(self.map[0]))):
                    if self.map[self.currentBlock.y + i][self.currentBlock.x + j] != self.emptyMapVal and self.currentBlock.block[i][j] != self.emptyMapVal:
                        return True
                else:
                    return True
        return False


    def newBlock(self, blockType=-1):
        self.currentBlock = Block(random.randrange(7) if blockType == -1 else blockType)
        self.currentBlock.x = int((self.mapWidth - self.currentBlock.w) / 2)
        self.currentBlock.y = self.mapHeight - self.currentBlock.h
        
        if self.isColliding():
            return False

        return True


    def putBlockOnMap(self, delBlock=False):
        for i in range(self.currentBlock.h):
            for j in range(self.currentBlock.w):
                try:
                    if delBlock and (self.currentBlock.block[i][j] != self.emptyMapVal):
                        self.map[self.currentBlock.y + i][self.currentBlock.x + j] = self.emptyMapVal
                    elif self.currentBlock.block[i][j] != self.emptyMapVal:
                        self.map[self.currentBlock.y + i][self.currentBlock.x + j] = self.currentBlock.blockType
                except:
                    pass


    def wipeBlockFromMap(self):
        self.putBlockOnMap(True)


class Block:
    blockPreset = [
                [[0, 0, 0, 0]],
                [[1, 1], [1, -1], [1, -1]],
                [[2, 2], [-1, 2], [-1, 2]],
                [[3, 3, -1], [-1, 3, 3]],
                [[-1, 4, 4], [4, 4, -1]],
                [[5, 5], [5, 5]],
                [[6, 6, 6], [-1, 6, -1]],
                [[-1]]
            ]

    def __init__(self, blockType, x=0, y=0):
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
        self.blockType = blockType
            
        if not -1 < blockType < len(self.blockPreset):
            blockType = -1

        self.block = self.blockPreset[blockType]

        self.x = x
        self.y = y
        self.w = len(self.block[0])
        self.h = len(self.block)


    def rotate(self, direction='cw'):
        tmpBlock = self.block
        self.block = []

        if direction == 'cw':
            for i in range(len(tmpBlock[0]) -1, -1, -1):
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
                if self.block[j][i] != -1:
                    skirt.append(j)
                    break

        return skirt

    @classmethod
    def defBlocks(self):
        for i in self.blockPreset:
            yield i


def main():
    for block in Block.defBlocks():
        print(block)

if __name__ == "__main__":
    main()