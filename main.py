import tetris
import simplegui
import os
import keyboard
import time



def rotate(direction, gui, tetris):
    tetris.rotate(direction)
    gui.render(tetris.map)

def move(direction, gui, tetris):
    tetris.move(direction)
    gui.render(tetris.map)

def drop(gui, tetris):
    tetris.drop()
    gui.render(tetris.map)


def main():
    cetris = tetris.Tetris()
    gui = simplegui.SimplestGui()
    gui.render(cetris.map)

    keyboard.add_hotkey('right', lambda: move('right', gui, cetris))
    keyboard.add_hotkey('left', lambda: move('left', gui, cetris))
    keyboard.add_hotkey('up', lambda: rotate('cw', gui, cetris))
    keyboard.add_hotkey('space', lambda: drop(gui, cetris))

    while True:
        pass
        gameOver, score = cetris.tetris()
        if gameOver:
            print('GAME OVER!')
            break
        gui.render(cetris.map)
        print(score)
        if keyboard.is_pressed('down'):
            time.sleep(0.05)
        else:
            time.sleep(0.4)

if __name__ == "__main__":
    main()