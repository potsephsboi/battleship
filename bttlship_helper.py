import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 32, 255)

pygame.init()
my_font = pygame.font.SysFont("monospace", 20)

class Player:
    def __init__(self, identity, grid, hit_grid, ships):
        self.identity = identity
        self.hit_grid = hit_grid
        self.grid = grid
        self.ships = ships

    def __repr__(self):
        return f"Player id: {self.identity} || Ships available: {len(self.ships)}."

class Ship:
    def __init__(self, s_type, hp):
        self.s_type = s_type
        self.hp = hp

    def __repr__(self):
        return f"Ship type: {self.s_type} || HP: {self.hp}"


class Button:
    def __init__(self, pos, width, height, b_type, label, pressed1, pressed2):
        self.pos = pos
        self.width = width
        self.height = height
        self.b_type = b_type
        self.label = label
        self.pressed1 = pressed1
        self.pressed2 = pressed2

class SetupButtons(Button):
    Sbuttons = []
    def __init__(self, pos, width, height, b_type, label, pressed1, pressed2):
        super().__init__(pos, width, height, b_type, label, pressed1, pressed2)
        SetupButtons.Sbuttons.append([pygame.Rect(pos[0], pos[1], width, height), pos, b_type, label, pressed1, pressed2])

class GameButtons(Button):
    GButtons = []
    def __init__(self, pos, width, height, b_type, label, pressed1, pressed2):
        super().__init__(pos, width, height, b_type, label, pressed1, pressed2)
        GameButtons.GButtons.append([pygame.Rect(pos[0], pos[1], width, height), pos, b_type, label, pressed1, pressed2])


def init_sbuttons_labels():
    my_font = pygame.font.SysFont("monospace", 20)

    SetupButtons((525, 100), 40, 40, 'ac', my_font.render("AC", True, WHITE), False, False)
    SetupButtons((575, 100), 40, 40, 'bb', my_font.render("BB", True, WHITE), False, False)
    SetupButtons((525, 150), 40, 40, 'cc', my_font.render("CC", True, WHITE), False, False)
    SetupButtons((575, 150), 40, 40, 'dd', my_font.render("DD", True, WHITE), False, False)
    SetupButtons((550, 200), 40, 40, 'sb', my_font.render("SB", True, WHITE), False, False)

    SetupButtons((490, 270), 90, 40, 'rot', my_font.render("ROTATE", True, WHITE), False, False)
    SetupButtons((590, 270), 90, 40, 'place', my_font.render("PLACE", True, WHITE), False, False)
    SetupButtons((525, 340), 100, 40, 'done', my_font.render("DONE", True, WHITE), False, False)

def init_gbuttons_labels():
    my_font = pygame.font.SysFont("monospace", 20)

    GameButtons((530, 270), 90, 40, 'fire', my_font.render("FIRE", True, WHITE), False, False)
    GameButtons((480, 120), 90, 40, 'radar', my_font.render("RADAR", True, WHITE), False, False)
    GameButtons((530, 170), 100, 40, 'torp', my_font.render("TORPEDO", True, WHITE), False, False)
    GameButtons((580, 120), 90, 40, 'double', my_font.render("DOUBLE", True, WHITE), False, False)

def display_grid(surface):
    x_lines = []
    y_lines = []
    for i in range(11):
        x_line = pygame.Rect(42, 40 * (i + 1), 400, 5)
        x_lines.append(x_line)
    for k in range(11):
        y_line = pygame.Rect(40 * (k + 1), 42, 5, 400)
        y_lines.append(y_line)
    for xl in x_lines:
        pygame.draw.rect(surface, BLACK, xl)
    for yl in y_lines:
        pygame.draw.rect(surface, BLACK, yl)


def detect_valid_bpress(pos, game_phase):
    if game_phase == 's':
        for but_cls in SetupButtons.Sbuttons:
            but = but_cls[0]
            if but.w + but.x > pos[0] > but.x and but.h + but.y > pos[1] > but.y:
                return but_cls[2]

        if 440 > pos[0] > 40 and 440 > pos[1] > 40:
            return [pos[0] // 40, pos[1] // 40]
    elif game_phase == 'g':
        for but_cls in GameButtons.GButtons:
            but = but_cls[0]
            if but.w + but.x > pos[0] > but.x and but.h + but.y > pos[1] > but.y:
                return but_cls[2]

        if 440 > pos[0] > 40 and 440 > pos[1] > 40:
            return [pos[0] // 40, pos[1] // 40]

def fire_check(pos, sender, receiver):
    st, gr = int(pos[0]), int(pos[1])
    if sender.hit_grid[gr][st] != 'X' and sender.hit_grid[gr][st] != 'O':
        if receiver.grid[gr][st] != '_':
            print('hit target')
            ship = find_ship(receiver, [st, gr])[0]
            ship.hp -= 1
            sender.hit_grid[gr][st] = 'X'
            if ship.hp == 0:
                destroy_ship(sender, receiver, ship)
                
            
        else:
            print('missed target')
            sender.hit_grid[gr][st] = 'O'
        return True
    else:
        print('you have already fired to this location')
        return False

def torpedo(pos, sender, receiver, dir):
    st, gr = int(pos[0]), int(pos[1])
    if dir  == 'u' and gr >= 4:
        for i in range(5):
            if receiver.grid[gr-i][st] != '_':
                sender.hit_grid[gr-i][st] = 'X'
                ship = find_ship(receiver, [st, gr-i])[0]
                ship.hp -= 1
                if ship.hp == 0:
                    destroy_ship(sender, receiver, ship)
            else:
                sender.hit_grid[gr-i][st] = 'O'
        return True
    elif dir  == 'd' and gr <= 5:
        for i in range(5):
            if receiver.grid[gr+i][st] != '_':
                sender.hit_grid[gr+i][st] = 'X'
                ship = find_ship(receiver, [st, gr+i])[0]
                ship.hp -= 1
                if ship.hp == 0:
                    destroy_ship(sender, receiver, ship)
            else:
                sender.hit_grid[gr+i][st] = 'O'
        return True
    elif dir == 'l' and st >= 4:
        for i in range(5):
            if receiver.grid[gr][st-i] != '_':
                sender.hit_grid[gr][st-i] = 'X'
                ship = find_ship(receiver, [st-i, gr])[0]
                ship.hp -= 1
                if ship.hp == 0:
                    destroy_ship(sender, receiver, ship)
            else:
                sender.hit_grid[gr][st-i] = 'O'
        return True
    elif dir == 'r' and st <= 5:
        for i in range(5):
            if receiver.grid[gr][st+i] != '_':
                sender.hit_grid[gr][st+i] = 'X'
                ship = find_ship(receiver, [st+i, gr])[0]
                ship.hp -= 1
                if ship.hp == 0:
                    destroy_ship(sender, receiver, ship)
            else:
                sender.hit_grid[gr][st+i] = 'O'
        return True
    else:
        return False


def radar(pos, sender, receiver):
    st, gr = int(pos[0]), int(pos[1])
    if 9 > gr > 0 and 9 > st > 0:
        if receiver.grid[gr][st] != '_':
            sender.hit_grid[gr][st] = 'XO'
        else:
            sender.hit_grid[gr][st] = 'O'

        if receiver.grid[gr-1][st] != '_':
            sender.hit_grid[gr-1][st] = 'XO'
        else:
            sender.hit_grid[gr-1][st] = 'O'

        if receiver.grid[gr+1][st] != '_':
            sender.hit_grid[gr+1][st] = 'XO'
        else:
            sender.hit_grid[gr+1][st] = 'O'

        if receiver.grid[gr][st-1] != '_':
            sender.hit_grid[gr][st-1] = 'XO'
        else:
            sender.hit_grid[gr][st-1] = 'O'

        if receiver.grid[gr][st+1] != '_':
            sender.hit_grid[gr][st+1] = 'XO'
        else:
            sender.hit_grid[gr][st+1] = 'O'
        return True
    else:
        return False


def show_command(command, mode):
    if mode == 's':
        return my_font.render(f"Command: {command[0]} {command[1]} {command[2]} {command[3]}", True, BLACK)
    elif mode =='g':
        return my_font.render(f"Command: {command[0]} {command[1]}", True, BLACK)

def win_check(player1, player2):
    if not player1.ships:
        return [True, 'p2']
    elif not player2.ships:
        return [True, 'p1']
    else:
        return [False]

def find_ship(player, pos):
    st, gr = int(pos[0]), int(pos[1])
    ship_name = player.grid[gr][st]
    for ship in player.ships:
        if ship_name == ship.s_type[0]:
            return [ship, True]
    return [False]

def destroy_ship(sender, receiver, ship):
    for gr in range(len(receiver.grid)):
        for st in range((len(receiver.grid))):
            if receiver.grid[gr][st] == ship.s_type:
                sender.hit_grid[gr][st] = 'XX'
    receiver.ships.remove(ship)


