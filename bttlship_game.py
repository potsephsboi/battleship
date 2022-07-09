from bttlship_helper import *

WIDTH = 700
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 32, 255)
RED = (255, 0, 0)
PURPLE = (77, 26, 127)
GREY = (99, 102, 106)

color_codes_game = {
    'X': RED,
    'O': BLUE,
    'XO': PURPLE,
    'XX': GREY
}

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
my_font = pygame.font.SysFont("monospace", 20)

title_labels = [my_font.render("Player 1's turn", True, BLACK), my_font.render("Player 2's turn", True, BLACK)]


def show_game_ui(player):
    WIN.blit(title_labels[player.identity - 1], ((WIDTH / 2) - 140, 0))
    display_grid(WIN)
    for but in GameButtons.GButtons:
        pygame.draw.rect(WIN, RED, but[0])
        WIN.blit(but[3], (but[1][0] + 10, but[1][1] + 10))
    for row in range(len(player.hit_grid)):
        for col in range(len(player.hit_grid)):
            if player.hit_grid[row][col] != '_':
                val = player.hit_grid[row][col]
                GameButtons((40 * (col + 1) + 2, 40 * (row + 1) + 2), 40, 40, f'{val}',
                                my_font.render(f'{val}', True, WHITE), False, False)
                pygame.draw.rect(WIN, color_codes_game[f'{val}'], GameButtons.GButtons[-1][0])
                GameButtons.GButtons.pop()


def game_command(mouse, command, command_len, sender, receiver, done):
    b_detect = detect_valid_bpress(mouse, 'g') # should return button object
    b_obj = 0

    for but in GameButtons.GButtons:
        if but[2] == b_detect:
            b_obj = but
            break

    if type(b_detect) == list:
        if command[0] == '_' and command[1] == '_':
            command_len += 2
        command[0], command[1] = f'{b_detect[0] - 1}', f'{b_detect[1] - 1}'

    if (b_detect == 'fire' or b_detect == 'dfire') and command_len == 2:
        done = fire_check(command, sender, receiver)
        if sender.identity == 1:
            if b_detect == 'dfire' and GameButtons.GButtons[-1][-2] is True:
                done = False
                b_obj[2] = 'fire'
        else:
            if b_detect == 'dfire' and GameButtons.GButtons[-1][-1] is True:
                done = False
                b_obj[2] = 'fire'

    if (b_detect =='radar' or b_detect =='dradar') and command_len == 2:
        done = radar(command, sender, receiver)
        if sender.identity == 1:
            if b_detect == 'dradar' and GameButtons.GButtons[-1][-2] is True:
                done = False
                b_obj[2] = 'radar'
        else:
            if b_detect == 'dradar' and GameButtons.GButtons[-1][-1] is True:
                done = False
                b_obj[2] = 'radar'

    if b_detect == 'torp' and command_len == 2 and b_obj[-receiver.identity] is False:
        if sender.identity == 1:
            b_obj[-2] = True    
        else:
            b_obj[-1] = True           
        print('Used game boost. You can fire a torpedo. ')
        dir = input('Enter torpedo direction (u, d, l, r): ')
        done = torpedo(command, sender, receiver, dir)
    elif b_detect == 'torp' and command_len == 0:
        print('Select location')
    elif b_detect == 'torp':
        print('Already used torpedo boost.')

    if b_detect == 'double' and b_obj[-receiver.identity] is False:
        if sender.identity == 1:
            b_obj[-2] = True    
        else:
            b_obj[-1] = True                
        for b in GameButtons.GButtons:
            if b[2] == 'fire':
                b[2] = 'dfire'
            if b[2] == 'radar':
                b[2] = 'dradar'

        print('Used game boost. You can radar or fire twice for one round.')
    elif b_detect == 'double':
        print('Alredy used double boost')

    return [command, command_len, done]
