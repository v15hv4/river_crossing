import pygame
import random
import configparser
pygame.init()

# Load configs
configparser = configparser.RawConfigParser()
configparser.read([
    'config/global.cfg',
    'config/player.cfg',
    'config/enemies.cfg',
    'config/map.cfg'
])

# Window dimensions
fps = configparser.getint('init', 'fps')
win_height = configparser.getint('init', 'win_height')
win_width = configparser.getint('init', 'win_width')
win = pygame.display.set_mode((win_width, win_height))

# Misc global variables
current_player = configparser.getint('init', 'current_player')
player_init_level = configparser.getint('player_general', 'init_level')
player_init_score = configparser.getint('player_general', 'init_score')
player_init_bonus = configparser.getint('player_general', 'init_bonus')
player_speed = configparser.getint('player_general', 'speed')
color_success = tuple(configparser.get('colors', 'color_success').split(','))
color_failure = tuple(configparser.get('colors', 'color_failure').split(','))
color_white = tuple(configparser.get('colors', 'color_white').split(','))
color_black = tuple(configparser.get('colors', 'color_black').split(','))
font_file = configparser.get('strings', 'font_file')

# Sprite dimensions
player_dimens = (
    configparser.getint('player_general', 'width'),
    configparser.getint('player_general', 'height')
)
orca_dimens = (
    configparser.getint('orca', 'width'),
    configparser.getint('orca', 'height')
)
turtle_dimens = (
    configparser.getint('turtle', 'width'),
    configparser.getint('turtle', 'height')
)
whale_dimens = (
    configparser.getint('whale', 'width'),
    configparser.getint('whale', 'height')
)
crab_dimens = (
    configparser.getint('crab', 'width'),
    configparser.getint('crab', 'height')
)
boat_dimens = (
    configparser.getint('boat', 'width'),
    configparser.getint('boat', 'height')
)

# Initial player positions
player1_x = configparser.getint('player1', 'x')
player1_y = configparser.getint('player1', 'y')
player2_x = configparser.getint('player2', 'x')
player2_y = configparser.getint('player2', 'y')

# Water Rows
water_r1 = configparser.getint('map', 'water_r1')
water_r2 = configparser.getint('map', 'water_r2')
water_r3 = configparser.getint('map', 'water_r3')
water_r4 = configparser.getint('map', 'water_r4')
water_r5 = configparser.getint('map', 'water_r5')
water_r6 = configparser.getint('map', 'water_r6')

# Land Rows
land_r1 = configparser.getint('map', 'land_r1')
land_r2 = configparser.getint('map', 'land_r2')
land_r3 = configparser.getint('map', 'land_r3')
land_r4 = configparser.getint('map', 'land_r4')
land_r5 = configparser.getint('map', 'land_r5')

# Enemies' Row Offsets
orca_offset = configparser.getint('orca', 'offset')
turtle_offset = configparser.getint('turtle', 'offset')
whale_offset = configparser.getint('whale', 'offset')
crab_offset = configparser.getint('crab', 'offset')
boat_offset = configparser.getint('boat', 'offset')

# Enemies' Base Speeds
orca_speed = configparser.getint('orca', 'speed')
turtle_speed = configparser.getint('turtle', 'speed')
whale_speed = configparser.getint('whale', 'speed')
crab_speed = configparser.getint('crab', 'speed')
boat_speed = configparser.getint('boat', 'speed')

# Game Strings
level_string = str(configparser.get('strings', 'level_string'))
score_string = str(configparser.get('strings', 'score_string'))
continue_string = str(configparser.get('strings', 'continue_string'))
time_string = str(configparser.get('strings', 'time_string'))
success_string = str(configparser.get('strings', 'success_string'))
failure_string = str(configparser.get('strings', 'failure_string'))
player1_win_string = str(configparser.get('strings', 'player1_win_string'))
player2_win_string = str(configparser.get('strings', 'player2_win_string'))
tie_string = str(configparser.get('strings', 'tie_string'))

pygame.display.set_caption("River Crossing [BETA]")

clock = pygame.time.Clock()


# Blueprint of every in-game entity
class Entity(object):
    def __init__(self, x, y, dimens, sprite):
        self.x = x
        self.y = y
        self.width = dimens[0]
        self.height = dimens[1]
        self.speed = player_speed
        self.score = player_init_score
        self.bonus = player_init_bonus
        self.level = player_init_level
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.is_dead = False
        self.has_played = False
        self.is_successful = False
        self.sprite = sprite

    def hitbox_static(self):
        return (self.x - 10, self.y + self.height / 1.8, self.width + 20, 45)

    def face_direction(self):
        if self.direction == -1:
            self.left = True
            self.right = False
        else:
            self.left = False
            self.right = True

    def init_as_player(self, up, down, move_up, move_down, move_left, move_right):
        self.up = up
        self.down = down
        self.move_up = move_up
        self.move_down = move_down
        self.move_left = move_left
        self.move_right = move_right

    def init_as_enemy(self, speed, direction):
        self.speed = speed
        self.direction = direction
        self.face_direction()

    def com(self):
        return (self.hitbox_static()[0] + (self.hitbox_static()[2] / 2),
                self.hitbox_static()[1] + (self.hitbox_static()[3] / 2))

    def draw(self):
        if self.up:
            win.blit(self.sprite[2], (self.x, self.y))
        elif self.down:
            win.blit(self.sprite[3], (self.x, self.y))
        elif self.left:
            win.blit(self.sprite[0], (self.x, self.y))
        elif self.right:
            win.blit(self.sprite[1], (self.x, self.y))

# Splash Screen
splash = [
    pygame.image.load('res/images/splash_screen_blank.png').convert(),
    pygame.image.load('res/images/splash_screen_text.png').convert()
]
for frame in range(0, 2):
    splash[frame] = pygame.transform.scale(splash[frame], (win_width, win_height))

# Tutorial Screen
tutorial = pygame.image.load('res/images/tutorial_screen.png')
tutorial = pygame.transform.scale(tutorial, (win_width, win_height))

# Background
bg = pygame.image.load('res/images/main_bg.png').convert()

# Default font
font = pygame.font.Font(font_file, 32)

# Player 1 Sprites
blue_right = pygame.image.load('res/sprites/blue_right.png')
blue_right = pygame.transform.scale(blue_right, player_dimens)
blue_left = pygame.image.load('res/sprites/blue_left.png')
blue_left = pygame.transform.scale(blue_left, player_dimens)
blue_up = pygame.image.load('res/sprites/blue_up.png')
blue_up = pygame.transform.scale(blue_up, player_dimens)
blue_down = pygame.image.load('res/sprites/blue_down.png')
blue_down = pygame.transform.scale(blue_down, player_dimens)
blue_sprite = [blue_left, blue_right, blue_up, blue_down]

# Player 2 Sprites
purple_right = pygame.image.load('res/sprites/purple_right.png')
purple_right = pygame.transform.scale(purple_right, player_dimens)
purple_left = pygame.image.load('res/sprites/purple_left.png')
purple_left = pygame.transform.scale(purple_left, player_dimens)
purple_up = pygame.image.load('res/sprites/purple_up.png')
purple_up = pygame.transform.scale(purple_up, player_dimens)
purple_down = pygame.image.load('res/sprites/purple_down.png')
purple_down = pygame.transform.scale(purple_down, player_dimens)
purple_sprite = [purple_left, purple_right, purple_up, purple_down]

# Enemy Orca Sprites
orca_left = pygame.image.load('res/sprites/orca_left.png')
orca_left = pygame.transform.scale(orca_left, orca_dimens)
orca_right = pygame.image.load('res/sprites/orca_right.png')
orca_right = pygame.transform.scale(orca_right, orca_dimens)
orca_sprite = [orca_left, orca_right]

# Enemy Turtle Sprites
turtle_left = pygame.image.load('res/sprites/turtle_left.png')
turtle_left = pygame.transform.scale(turtle_left, turtle_dimens)
turtle_right = pygame.image.load('res/sprites/turtle_right.png')
turtle_right = pygame.transform.scale(turtle_right, turtle_dimens)
turtle_sprite = [turtle_left, turtle_right]

# Enemy Whale Sprites
whale_left = pygame.image.load('res/sprites/whale_left.png')
whale_left = pygame.transform.scale(whale_left, whale_dimens)
whale_right = pygame.image.load('res/sprites/whale_right.png')
whale_right = pygame.transform.scale(whale_right, whale_dimens)
whale_sprite = [whale_left, whale_right]

# Enemy Crab Sprites
crab_left = pygame.image.load('res/sprites/crab_left.png')
crab_left = pygame.transform.scale(crab_left, crab_dimens)
crab_right = pygame.image.load('res/sprites/crab_right.png')
crab_right = pygame.transform.scale(crab_right, crab_dimens)
crab_sprite = [crab_left, crab_right]

# Enemy Boat Sprites
boat_left = pygame.image.load('res/sprites/boat_left.png')
boat_left = pygame.transform.scale(boat_left, boat_dimens)
boat_right = pygame.image.load('res/sprites/boat_right.png')
boat_right = pygame.transform.scale(boat_right, boat_dimens)
boat_sprite = [boat_left, boat_right]

# Entity lists
orca = [orca_dimens, orca_offset, orca_sprite, orca_speed]
turtle = [turtle_dimens, turtle_offset, turtle_sprite, turtle_speed]
whale = [whale_dimens, whale_offset, whale_sprite, whale_speed]
boat = [boat_dimens, boat_offset, boat_sprite, boat_speed]
crab = [crab_dimens, crab_offset, crab_sprite, crab_speed]
entity_list = [orca, turtle, whale, boat, crab]
entity_speeds = [3, 5, 7, 9, 11, 13, 15, 17, 19, 100]

# Players
player1 = Entity(player1_x, player1_y, player_dimens, blue_sprite)
player1.init_as_player(True, False, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
player2 = Entity(player2_x, player2_y, player_dimens, purple_sprite)
player2.init_as_player(False, True, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)

# Enemies
land_enemy = entity_list[4]

# Enemy at Land Row 1
crab1 = Entity(
    random.randint(0, win_width - land_enemy[0][0]),
    land_r1 + land_enemy[1],
    land_enemy[0],
    land_enemy[2]
)
crab1.init_as_enemy(crab_speed, random.choice([-1, 1]))

# Enemy at Land Row 2
crab2 = Entity(
    random.randint(0, win_width - land_enemy[0][0]),
    land_r2 + land_enemy[1],
    land_enemy[0],
    land_enemy[2]
)
crab2.init_as_enemy(crab_speed, random.choice([-1, 1]))

# Enemy at Land Row 3
crab3 = Entity(
    random.randint(0, win_width - land_enemy[0][0]),
    land_r3 + land_enemy[1],
    land_enemy[0],
    land_enemy[2]
)
crab3.init_as_enemy(crab_speed, random.choice([-1, 1]))

# Enemy at Land Row 4
crab4 = Entity(
    random.randint(0, win_width - land_enemy[0][0]),
    land_r4 + land_enemy[1],
    land_enemy[0],
    land_enemy[2]
)
crab4.init_as_enemy(crab_speed, random.choice([-1, 1]))

# Enemy at Land Row 5
crab5 = Entity(
    random.randint(0, win_width - land_enemy[0][0]),
    land_r5 + land_enemy[1],
    land_enemy[0],
    land_enemy[2]
)
crab5.init_as_enemy(crab_speed, random.choice([-1, 1]))

# Enemy at Water Row 1
water_enemy_1 = entity_list[random.randint(0, 3)]
row1_enemy = Entity(
    random.randint(0, win_width - water_enemy_1[0][0]),
    water_r1 + water_enemy_1[1],
    water_enemy_1[0],
    water_enemy_1[2]
)
row1_enemy.init_as_enemy(water_enemy_1[3] + entity_speeds[0], random.choice([-1, 1]))

# Enemy at Water Row 2
water_enemy_2 = entity_list[random.randint(0, 3)]
row2_enemy = Entity(
    random.randint(0, win_width - water_enemy_2[0][0]),
    water_r2 + water_enemy_2[1],
    water_enemy_2[0],
    water_enemy_2[2]
)
row2_enemy.init_as_enemy(water_enemy_2[3] + entity_speeds[0], random.choice([-1, 1]))

# Enemy at Water Row 3
water_enemy_3 = entity_list[random.randint(0, 3)]
row3_enemy = Entity(
    random.randint(0, win_width - water_enemy_3[0][0]),
    water_r3 + water_enemy_3[1],
    water_enemy_3[0],
    water_enemy_3[2]
)
row3_enemy.init_as_enemy(water_enemy_3[3] + entity_speeds[0], random.choice([-1, 1]))

# Enemy at Water Row 4
water_enemy_4 = entity_list[random.randint(0, 3)]
row4_enemy = Entity(
    random.randint(0, win_width - water_enemy_4[0][0]),
    water_r4 + water_enemy_4[1],
    water_enemy_4[0],
    water_enemy_4[2]
)
row4_enemy.init_as_enemy(water_enemy_4[3] + entity_speeds[0], random.choice([-1, 1]))

# Enemy at Water Row 5
water_enemy_5 = entity_list[random.randint(0, 3)]
row5_enemy = Entity(
    random.randint(0, win_width - water_enemy_5[0][0]),
    water_r5 + water_enemy_5[1],
    water_enemy_5[0],
    water_enemy_5[2]
)
row5_enemy.init_as_enemy(water_enemy_5[3] + entity_speeds[0], random.choice([-1, 1]))

# Enemy at Water Row 6
water_enemy_6 = entity_list[random.randint(0, 3)]
row6_enemy = Entity(
    random.randint(0, win_width - water_enemy_6[0][0]),
    water_r6 + water_enemy_6[1],
    water_enemy_6[0],
    water_enemy_6[2]
)
row6_enemy.init_as_enemy(water_enemy_6[3] + entity_speeds[0], random.choice([-1, 1]))

# Enemy Lists
static_entity_list = [
    crab1,
    crab2,
    crab3,
    crab4,
    crab5
]
moving_entity_list = [
    row1_enemy,
    row2_enemy,
    row3_enemy,
    row4_enemy,
    row5_enemy,
    row6_enemy
]


# Change sprite variant based on direction
def sprite_direction(new_direction):
    player.up = False
    player.down = False
    player.right = False
    player.left = False
    if new_direction == 'left':
        player.left = True
    elif new_direction == 'right':
        player.right = True
    elif new_direction == 'up':
        player.up = True
    elif new_direction == 'down':
        player.down = True


# Update speeds of moving enemies
def update_speeds():
    for entity in moving_entity_list:
        try:
            entity.speed = entity_speeds[player.level - 1]
        except:
            entity.speed = entity_speeds[len(entity_speeds) - 1]
    row1_enemy.speed += water_enemy_1[3]
    row2_enemy.speed += water_enemy_2[3]
    row3_enemy.speed += water_enemy_3[3]
    row4_enemy.speed += water_enemy_4[3]
    row5_enemy.speed += water_enemy_5[3]
    row6_enemy.speed += water_enemy_6[3]


# Calculate score based on player's position
def update_score():
    if player == player1:
        if player.y < 580 and player.y > 550:
            player.score = 10
        elif player.y < 550 and player.y > 472:
            player.score = 15
        elif player.y < 472 and player.y > 442:
            player.score = 25
        elif player.y < 442 and player.y > 364:
            player.score = 30
        elif player.y < 364 and player.y > 334:
            player.score = 40
        elif player.y < 334 and player.y > 256:
            player.score = 45
        elif player.y < 256 and player.y > 226:
            player.score = 55
        elif player.y < 226 and player.y > 148:
            player.score = 60
        elif player.y < 148 and player.y > 118:
            player.score = 70
        elif player.y < 118 and player.y > 40:
            player.score = 75
        elif player.y < 40:
            player.score = 80
            player.is_successful = True
            player.is_dead = True
    else:
        if player.y > 630:
            player.score = 80
            player.is_successful = True
            player.is_dead = True
        elif player.y < 580 and player.y > 550:
            player.score = 75
        elif player.y < 550 and player.y > 472:
            player.score = 65
        elif player.y < 472 and player.y > 442:
            player.score = 60
        elif player.y < 442 and player.y > 364:
            player.score = 55
        elif player.y < 364 and player.y > 334:
            player.score = 45
        elif player.y < 334 and player.y > 256:
            player.score = 40
        elif player.y < 256 and player.y > 226:
            player.score = 30
        elif player.y < 226 and player.y > 148:
            player.score = 25
        elif player.y < 148 and player.y > 118:
            player.score = 15
        elif player.y < 118 and player.y > 40:
            player.score = 10
        elif player.y < 40:
            player.score = 0


# Reinitialize player values for the next round
def next_round():
    player1.is_dead = False
    player1.is_successful = False
    player1.has_played = False
    player1.score = 0
    player1.bonus = 0
    player1.x = player1_x
    player1.y = player1_y
    player2.is_dead = False
    player2.is_successful = False
    player2.has_played = False
    player2.score = 0
    player2.bonus = 0
    player2.x = player2_x
    player2.y = player2_y

    # Randomize crab positions in each round
    for crab in static_entity_list:
        crab.x = random.randint(0, win_width - land_enemy[0][0])


# Switch player when one's turn is done
def switch_player():
    global current_player
    if player1.is_dead and player2.is_dead:
        next_round()
        current_player = 1
    if player.is_dead:
        if current_player == 1:
            current_player = 2
        else:
            current_player = 1


# Restrict player from accessing certain regions of the map
def restrict_player():
    if player.y < 0:
        player.y = 0
    if player.y > (win_height - player_dimens[1] - 2):
        player.y = (win_height - player_dimens[1] - 2)

splash_frame = 0


# Redraw surface
def redraw(result_text):
    global splash_frame
    if splash_screen:
        win.blit(
            splash[splash_frame],
            (0, 0)
        )
        splash_frame = (splash_frame + 1) % 2
        pygame.time.delay(200)
    elif tutorial_screen:
        win.blit(
            tutorial,
            (0, 0)
        )
    else:
        round_text = font.render(
            level_string + ' ' + str(player.level),
            1, (255, 255, 255)
        )
        score_text = font.render(
            score_string + ' ' + str(player.score),
            1, (255, 255, 255)
        )
        time_text = font.render(
            '[ ' + time_string + ' +' + str(player.bonus) + ' ]',
            1, (255, 255, 255)
        )
        continue_text = font.render(
            continue_string,
            1, (255, 255, 255)
        )
        if not player.is_dead:
            win.blit(
                bg,
                (0, 0)
            )
            win.blit(
                score_text,
                (5, 0)
            )
            win.blit(
                round_text,
                (win_width - 87, 0)
                )
            for entity in static_entity_list:
                entity.draw()
            for entity in moving_entity_list:
                entity.draw()
            player.draw()
        else:
            win.fill((0, 0, 0))
            player.draw()
            if player.is_successful:
                end_text = font.render(
                    success_string,
                    1, (0, 255, 0)
                )
            else:
                end_text = font.render(
                    failure_string,
                    1, (255, 0, 0)
                )
            win.blit(
                end_text,
                (((win_width - end_text.get_width() / 2) / 2) - 5, (win_height / 2) - 60)
            )
            win.blit(
                score_text,
                (((win_width - score_text.get_width() / 2) / 2) - 10, win_height / 2)
            )
            if player.bonus > 0:
                win.blit(
                    time_text,
                    (((win_width - time_text.get_width() / 2) / 2) - 40, (win_height / 2) + 50)
                )
            if player1.is_dead and player2.is_dead:
                win.blit(
                    result_text,
                    (((win_width - result_text.get_width() / 2) / 2) - 60, (win_height / 2) + 100)
                )
            win.blit(
                continue_text,
                (((win_width - continue_text.get_width() / 2) / 2) - 60, (win_height / 2) + 150)
            )
    pygame.display.update()

# Main loop
run = True
splash_screen = True
tutorial_screen = False
start_time = 0
end_time = 0
time_bonus = 0
while(run):
    clock.tick(fps)

    if start_time == 0:
        start_time = pygame.time.get_ticks()

    # Check for player change
    if current_player == 1:
        player = player1
        player1.has_played = True
    else:
        player = player2
        player2.has_played = True

    # Splash and Tutorial screens
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT or
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if splash_screen:
                    splash_screen = False
                    tutorial_screen = True
                elif tutorial_screen:
                    tutorial_screen = False

    # Update enemy speeds according to player's level
    update_speeds()

    # Single keypress actions
    for event in pygame.event.get():

        # Quit Game
        if (
            event.type == pygame.QUIT or
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            run = False

    if not player.is_dead:

        # Restrict motion of player
        restrict_player()

        # Enemy movement
        for enemy_i in moving_entity_list:
            if enemy_i.x < win_width and enemy_i.direction == 1:
                enemy_i.x += enemy_i.speed
            if enemy_i.x >= win_width:
                enemy_i.direction = -1
                enemy_i.face_direction()
            if enemy_i.x > -enemy_i.width and enemy_i.direction == -1:
                enemy_i.x -= enemy_i.speed
            if enemy_i.x <= 0:
                enemy_i.direction = 1
                enemy_i.face_direction()

        # Death
        for enemy_i in moving_entity_list:
            if (
                player.com()[0] > enemy_i.hitbox_static()[0] and
                player.com()[0] < enemy_i.hitbox_static()[0] + enemy_i.hitbox_static()[2]
            ):
                if (
                    player.com()[1] > enemy_i.hitbox_static()[1] and
                    player.com()[1] < enemy_i.hitbox_static()[1] + enemy_i.hitbox_static()[3]
                ):
                    end_time = pygame.time.get_ticks()
                    player.is_dead = True
        for enemy_i in static_entity_list:
            if (
                player.com()[0] > enemy_i.hitbox_static()[0] and
                player.com()[0] < enemy_i.hitbox_static()[0] + enemy_i.hitbox_static()[2]
            ):
                if (
                    player.com()[1] > enemy_i.hitbox_static()[1] and
                    player.com()[1] < enemy_i.hitbox_static()[1] + enemy_i.hitbox_static()[3]
                ):
                    end_time = pygame.time.get_ticks()
                    player.is_dead = True

        # Sustained keypress actions
        keys = pygame.key.get_pressed()
        if keys[player.move_left]:
            sprite_direction('left')
            if player.x > 2:
                player.x -= player.speed
        elif keys[player.move_right]:
            sprite_direction('right')
            if player.x < (win_width - player_dimens[0] - 2):
                player.x += player.speed
        elif keys[player.move_up]:
            sprite_direction('up')
            if player.y > 2:
                player.y -= player.speed
        elif keys[player.move_down]:
            sprite_direction('down')
            if player.y < (win_height - player_dimens[1] - 2):
                player.y += player.speed
        result_text = font.render('', 1, (255, 255, 255))

        # Update score based on player's position
        update_score()

        # Add time bonus to total score if successfully reached
        if player.is_successful:
            end_time = pygame.time.get_ticks()
            time_bonus = (100 - ((end_time - start_time) // 1000)) // 2
            if time_bonus < 0:
                time_bonus = 0
            player.bonus = time_bonus
            player.score += time_bonus
            start_time = 0
            end_time = 0
            time_bonus = 0

        # Decide winner of the round
        if player1.is_dead and player2.is_dead:
            if (
                player1.is_successful and not player2.is_successful or
                player1.score > player2.score
            ):
                result_text = font.render(player1_win_string, 1, (255, 255, 255))
                player1.level += 1
            elif (
                not player1.is_successful and player2.is_successful or
                player1.score < player2.score
            ):
                result_text = font.render(player2_win_string, 1, (255, 255, 255))
                player2.level += 1
            else:
                result_text = font.render(tie_string, 1, (255, 255, 255))
                player1.level += 1
                player2.level += 1

    else:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                switch_player()
                start_time = 0
                end_time = 0
                time_bonus = 0

    redraw(result_text)
pygame.quit()

# TODO: Sounds (?)
