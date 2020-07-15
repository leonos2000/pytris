import tetris
import simplegui
import os
from pynput import keyboard
import time

cetris = tetris.Tetris(mapType='color')
gui = simplegui.SimplestGui()



def on_press(key):
    if key == keyboard.Key.right:
        cetris.move('right')
    if key == keyboard.Key.left:
        cetris.move('left')
    if key == keyboard.Key.up:
        cetris.rotate('cw')
    if key == keyboard.Key.space:
        cetris.drop()
    if key  == keyboard.KeyCode(char = 'c'):
        cetris.hold()
           
    holdedBlock = tetris.Block(cetris.holdedBlock)
    gui.render(cetris.map, holdedBlock.coloredBlock())

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

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
        gui.render(cetris.map, holdedBlock.coloredBlock())
        print(lines)
        time.sleep(0.5)

if __name__ == "__main__":
    main()