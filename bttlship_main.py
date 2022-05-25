# WORK IN PROGRESS
# This is a game remake of the popular game battleship
# Run this file to play battleship on your local machine
# Creator: The one and only potsephsboi
#
# TODO: add grey icon when ship is destroyed
#       add torpedo button
#       add double button

import time
from bttlship_setup import *
from bttlship_game import *


WIDTH = 700
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 32, 255)
PURPLE = (77, 26, 127)
GREEN = (124, 252, 0)
RED = (255, 0, 0)


FPS = 30
COLOR_LST = [BLACK, BLUE, PURPLE, RED, GREEN, BLACK, BLACK, BLACK]
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

my_font = pygame.font.SysFont("monospace", 20)

label_p1 = my_font.render("Player 1 setup", True, BLACK)
label_p2 = my_font.render("Player 2 setup", True, BLACK)
label_start = my_font.render("Welcome to battleship!", True, BLACK)
label_loading = my_font.render("Loading...", True, BLACK)
ship_img = pygame.image.load('bttlship.png')


init_sbuttons_labels()
init_gbuttons_labels()

def setup(player, command):
    WIN.fill(WHITE)
    WIN.blit(show_command(command), (WIDTH-225, 50))
    show_setup_ui(player)
    pygame.display.update()

def game(player):
    WIN.fill(WHITE)
    show_game_ui(player)
    pygame.display.update()

def start_screen(s_time, c_time):
    WIN.fill(WHITE)
    WIN.blit(label_start, (175, 25))
    WIN.blit(label_loading, (125, 400))
    WIN.blit(ship_img, (100, 75))
    pygame.display.update()
    return True if c_time - s_time < 1 else False

def main():
    run = True
    mode = 'start'
    clock = pygame.time.Clock()
    command = ['_', '_', '_', '_']
    command_len = 0

    while run:
        clock.tick(FPS)
        if mode == 'start':
            start_time = time.time()
            repeat = True
            while repeat:
                cur_time = time.time()
                repeat = start_screen(start_time, cur_time)
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        run = False
                        repeat = False
            mode = 'g1'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()

                if mode == 's1':
                    command_info = setup_command(mouse, command, command_len, player1, False)
                    if not command_info[2]:
                        command = command_info[0]
                        command_len = command_info[1]
                        
                    else:
                        mode = 's2'
                        
                elif mode == 's2':
                    command_info = setup_command(mouse, command, command_len, player2, False)
                    if not command_info[2]:
                        command = command_info[0]
                        command_len = command_info[1]
                        print(command)
                    else:
                        mode = 'g1'
                        command = ['_', '_']
                        command_len = 0

                elif mode == 'g1':
                    command_info = game_command(mouse, command, command_len, player1, player2, False)
                    if not command_info[2]:
                        command = command_info[0]
                        command_len = command_info[1]
                        print(command)
                    else:
                        mode = 'g2'

                elif mode == 'g2':
                    command_info = game_command(mouse, command, command_len, player2, player1, False)
                    if not command_info[2]:
                        command = command_info[0]
                        command_len = command_info[1]
                        print(command)
                    else:
                        mode = 'g1'
        if mode == 's1':
            setup(player1, command)
        elif mode == 's2':
            setup(player2, command)
        elif mode == 'g1':
            game(player1)
            game_info = win_check(player1, player2)
            print(game_info)
            if game_info[0]:
                print(f'game over, {game_info[1]}')
                run = False
        elif mode == 'g2':
            game(player2)
            game_info = win_check(player1, player2)
            if game_info[0]:
                print(f'game over, {game_info[1]}')
                run = False


    pygame.quit()


if __name__ == '__main__':
    main()



