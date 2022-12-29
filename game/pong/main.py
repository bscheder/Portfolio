import pygame
from classes.screen import Screen

Screen_ = Screen()


def handle_screen():
    pygame.init()
    pygame.display.set_caption('Pong')

if __name__ == '__main__':
    Screen_.init_screen()

    while Screen_.game.running:
        Screen_.update_screen()
