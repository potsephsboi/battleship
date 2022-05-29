from bttlship_helper import *

WIDTH = 700
HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 32, 255)
PURPLE = (77, 26, 127)
GREEN = (124, 252, 0)
RED = (255, 0, 0)
COLOR_LST = [BLACK, BLUE, PURPLE, RED, GREEN, BLACK, BLACK, BLACK]

color_codes_setup = {
    'a': BLACK,
    'b': BLUE,
    'c': PURPLE,
    'd': RED,
    's': GREEN
}

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
my_font = pygame.font.SysFont("monospace", 20)

title_labels = [my_font.render("Player 1 setup", True, BLACK), my_font.render("Player 2 setup", True, BLACK)]


player1 = Player(1, [['_' for i in range(10)] for j in range(10)], [['_' for i in range(10)] for j in range(10)],
                 [Ship('a', 5), Ship('b', 4), Ship('c', 3), Ship('d', 2), Ship('s', 2)])

player2 = Player(2, [['_' for i in range(10)] for j in range(10)], [['_' for i in range(10)] for j in range(10)],
                 [Ship('a', 5), Ship('b', 4), Ship('c', 3), Ship('d', 2), Ship('s', 2)])



def show_setup_ui(player):
    WIN.blit(title_labels[player.identity-1], ((WIDTH / 2) - 140, 0))

    display_grid(WIN)
    for i, but in enumerate(SetupButtons.Sbuttons):
        pygame.draw.rect(WIN, COLOR_LST[i], but[0])
        WIN.blit(but[3], (but[1][0]+10, but[1][1]+10))
    for row in range(len(player.grid)):
        for col in range(len(player.grid)):
            if player.grid[row][col] != '_':
                name = player.grid[row][col]
                for b in SetupButtons.Sbuttons:
                    if b[2][0] == name:
                        SetupButtons((40*(col+1)+2, 40*(row+1)+2), 40, 40, f'{name}',
                                        my_font.render(f'{name}', True, WHITE), False, False)
                        pygame.draw.rect(WIN, color_codes_setup[f'{name}'], SetupButtons.Sbuttons[-1][0])
                        SetupButtons.Sbuttons.pop()


def find_valid_direction(start_points, ship, player):
    x = start_points[0] - 1
    y = start_points[1] - 1
    s_len = 0
    valid_dirs = []
    for s in player.ships:
        if s.s_type[0] == ship:
            s_len = s.hp
            break
    if y - s_len >= -1:
        valid_dirs.append('u')
    if y + s_len <= 9:
        valid_dirs.append('d')
    if x - s_len >= -1:
        valid_dirs.append('l')
    if x + s_len <= 9:
        valid_dirs.append('r')

    return valid_dirs


seen = []  # global var eww
def setup_command(mouse, command, command_len, player, done):
    global seen
    but_detect = detect_valid_bpress(mouse, 's')
    dirs = ['u', 'd', 'l', 'r']

    if but_detect:
        if type(but_detect) == list:
            if command[1] == '_' and command[2] == '_' and command[3] == '_':
                command_len += 3

            command[1] = but_detect[0] - 1
            command[2] = but_detect[1] - 1
        if but_detect in ['ac', 'bb', 'cc', 'dd', 'sb']:
            if command[0] == '_':
                command_len += 1
            command[3] = '_'
            command[0] = but_detect[0]

        if but_detect == 'rot':
            val_dirs = find_valid_direction([command[1], command[2]], command[0], player)
            if len(seen) == len(val_dirs):
                seen.clear()
            for d in dirs:
                if d in val_dirs and d not in seen:
                    command[3] = d
                    seen.append(d)
                    break
        if but_detect == 'place' and command_len == 4 and command[0] != '_':
            found = False
            for ship in player.ships:
                if ship.s_type[0] == command[0]:
                    found = True
                    if command[3] != '_':
                        grid_setup(command, player)
                    command[3] = '_'
                    break
            if not found:
                print('Ship already placed')
        if but_detect == 'done' and len(player.ships) == 0:
            print(f'Player {player.identity} setup completed')
            done = True
            return [command, command_len, done]

    return [command, command_len, done]


def grid_setup(command, player):

    ship_type = command[0]
    s_len = 0
    x = int(command[1])
    y = int(command[2])
    direction = command[3]
    place = True

    for ship in player.ships:
        if ship.s_type[0] == ship_type:
            s_len = ship.hp
            break

    if direction == 'u':
        for i in range(s_len):
            if player.grid[y-i][x] != '_':
                place = False
                break
        if place:
            for i in range(s_len):
                player.grid[y-i][x] = ship_type
    elif direction == 'd':
        for i in range(s_len):
            if player.grid[y+i][x] != '_':
                place = False
                break
        if place:
            for i in range(s_len):
                player.grid[y+i][x] = ship_type
    elif direction == 'l':
        for i in range(s_len):
            if player.grid[y][x-i] != '_':
                place = False
                break
        if place:
            for i in range(s_len):
                player.grid[y][x-i] = ship_type
    elif direction == 'r':
        for i in range(s_len):
            if player.grid[y][x+i] != '_':
                place = False
                break
        if place:
            for i in range(s_len):
                player.grid[y][x+i] = ship_type
    if not place:
        print('Cannot place ship due to collision with another ship.')
    else:
        for ship in player.ships:
            if ship.s_type == ship_type:
                player.ships.remove(ship)


