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
    def __init__(self, pos, width, height, b_type, label):
        self.pos = pos
        self.width = width
        self.height = height
        self.b_type = b_type
        self.label = label


class SetupButtons(Button):
    Sbuttons = []
    def __init__(self, pos, width, height, b_type, label):
        super().__init__(pos, width, height, b_type, label)
        SetupButtons.Sbuttons.append([pygame.Rect(pos[0], pos[1], width, height), pos, b_type, label])

class GameButtons(Button):
    GButtons = []
    def __init__(self, pos, width, height, b_type, label):
        super().__init__(pos, width, height, b_type, label)
        GameButtons.GButtons.append([pygame.Rect(pos[0], pos[1], width, height), pos, b_type, label])

def init_sbuttons_labels():
    my_font = pygame.font.SysFont("monospace", 20)

    SetupButtons((525, 100), 40, 40, 'ac', my_font.render("AC", True, WHITE))
    SetupButtons((575, 100), 40, 40, 'bb', my_font.render("BB", True, WHITE))
    SetupButtons((525, 150), 40, 40, 'cc', my_font.render("CC", True, WHITE))
    SetupButtons((575, 150), 40, 40, 'dd', my_font.render("DD", True, WHITE))
    SetupButtons((550, 200), 40, 40, 'sb', my_font.render("SB", True, WHITE))

    SetupButtons((490, 270), 90, 40, 'rot', my_font.render("ROTATE", True, WHITE))
    SetupButtons((590, 270), 90, 40, 'place', my_font.render("PLACE", True, WHITE))
    SetupButtons((525, 340), 100, 40, 'done', my_font.render("DONE", True, WHITE))

def init_gbuttons_labels():
    my_font = pygame.font.SysFont("monospace", 20)

    GameButtons((530, 270), 90, 40, 'fire', my_font.render("FIRE", True, WHITE))

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
            sender.hit_grid[gr][st] = 'X'
        else:
            print('missed target')
            sender.hit_grid[gr][st] = 'O'
        return True
    else:
        print('you have already fired to this location')
        return False

def show_command(command):
    return my_font.render(f"Command: {command[0]} {command[1]} {command[2]} {command[3]}", True, BLACK)
