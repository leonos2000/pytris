import tetris
import simplegui
import os
from pynput import keyboard
import time

cetris = tetris.Tetris()
gui = simplegui.TerminalGui()
speed = 0.5


def on_press(key):
    global speed
    if key == keyboard.Key.right:
        cetris.move('right')
    if key == keyboard.Key.left:
        cetris.move('left')
    if key == keyboard.Key.up:
        cetris.rotate('cw')
    if key == keyboard.Key.down:
        speed = 0.05
    if key == keyboard.Key.space:
        cetris.drop()
    if key  == keyboard.KeyCode(char = 'c'):
        cetris.hold()
           
    holdedBlock = tetris.Block(cetris.holdedBlock)
    gui.render(cetris.map, holdedBlock.block)

def on_release(key):
    global speed
    if key == keyboard.Key.down:
        speed = 0.5

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()


def main():

    while True:
        gameOver, score, lines = cetris.tetris()
        if gameOver:
            print('GAME OVER!')
            break
        holdedBlock = tetris.Block(cetris.holdedBlock)
        gui.render(cetris.map, holdedBlock.block)
        print(lines)
        time.sleep(speed)

if __name__ == "__main__":
    main()