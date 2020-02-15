import pygame
import random
pygame.init()

# Window Dimensions
win_height = 696
win_width = 696
win = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption("River Crossing [ALPHA]")

clock = pygame.time.Clock()

# Miscellaneous Global Variables
level = 1
player_speed = 5
# player_jump_speed = 4
run = True
whosplayin = 1

class entity(object):
    def __init__(self, x, y, dimens, sprite):
        self.x = x
        self.y = y
        self.width = dimens[0]
        self.height = dimens[1]
        self.speed = player_speed
        # self.jump_speed = player_jump_speed
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.is_dead = False
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

    def init_as_player(self, up, down):
        self.up = up
        self.down = down
        # self.is_jumping = 0

    def init_as_enemy(self, speed, direction):
        self.speed = speed
        self.direction = direction
        self.face_direction()

    def com(self):
        return (self.hitbox_static()[0] + (self.hitbox_static()[2] / 2), self.hitbox_static()[1] + (self.hitbox_static()[3] / 2))

    def draw(self):
        if self.up:
            win.blit(self.sprite[2], (self.x, self.y))
        elif self.down:
            win.blit(self.sprite[3], (self.x, self.y))
        elif self.left:
            win.blit(self.sprite[0], (self.x, self.y))
        elif self.right:
            win.blit(self.sprite[1], (self.x, self.y))

        # Visualize hitbox_statices [DEBUG]
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox_static(), 2)

# Sprite Dimensions
player_dimens = (28, 32)
orca_dimens = (95, 56)
turtle_dimens = (70, 40)
whale_dimens = (86, 70)
crab_dimens = (54, 30)
boat_dimens = (80, 90)

# Background
bg = pygame.image.load('res/main_bg.png').convert()

# Player 1 Sprites
blue_right = pygame.image.load('res/blue_right.png')
blue_right = pygame.transform.scale(blue_right, player_dimens)
blue_left = pygame.image.load('res/blue_left.png')
blue_left = pygame.transform.scale(blue_left, player_dimens)
blue_up = pygame.image.load('res/blue_up.png')
blue_up = pygame.transform.scale(blue_up, player_dimens)
blue_down = pygame.image.load('res/blue_down.png')
blue_down = pygame.transform.scale(blue_down, player_dimens)
blue_sprite = [blue_left, blue_right, blue_up, blue_down]

# Player 2 Sprites
purple_right = pygame.image.load('res/purple_right.png')
purple_right = pygame.transform.scale(purple_right, player_dimens)
purple_left = pygame.image.load('res/purple_left.png')
purple_left = pygame.transform.scale(purple_left, player_dimens)
purple_up = pygame.image.load('res/purple_up.png')
purple_up = pygame.transform.scale(purple_up, player_dimens)
purple_down = pygame.image.load('res/purple_down.png')
purple_down = pygame.transform.scale(purple_down, player_dimens)
purple_sprite = [purple_left, purple_right, purple_up, purple_down]

# Enemy Orca Sprites
orca_left =  pygame.image.load('res/orca_left.png')
orca_left = pygame.transform.scale(orca_left, orca_dimens)
orca_right =  pygame.image.load('res/orca_right.png')
orca_right = pygame.transform.scale(orca_right, orca_dimens)
orca_sprite = [orca_left, orca_right]

# Enemy Turtle Sprites
turtle_left =  pygame.image.load('res/turtle_left.png')
turtle_left = pygame.transform.scale(turtle_left, turtle_dimens)
turtle_right =  pygame.image.load('res/turtle_right.png')
turtle_right = pygame.transform.scale(turtle_right, turtle_dimens)
turtle_sprite = [turtle_left, turtle_right]

# Enemy Whale Sprites
whale_left =  pygame.image.load('res/whale_left.png')
whale_left = pygame.transform.scale(whale_left, whale_dimens)
whale_right =  pygame.image.load('res/whale_right.png')
whale_right = pygame.transform.scale(whale_right, whale_dimens)
whale_sprite = [whale_left, whale_right]

# Enemy Crab Sprites
crab_left =  pygame.image.load('res/crab_left.png')
crab_left = pygame.transform.scale(crab_left, crab_dimens)
crab_right =  pygame.image.load('res/crab_right.png')
crab_right = pygame.transform.scale(crab_right, crab_dimens)
crab_sprite = [crab_left, crab_right]

# Enemy Boat Sprites
boat_left =  pygame.image.load('res/boat_left.png')
boat_left = pygame.transform.scale(boat_left, boat_dimens)
boat_right =  pygame.image.load('res/boat_right.png')
boat_right = pygame.transform.scale(boat_right, boat_dimens)
boat_sprite = [boat_left, boat_right]

# Initial Positions
p1_x = (win_width / 2)
p1_y = 655
p2_x = (win_width / 2)
p2_y = 8

# Water Rows
water_r1 = 40
water_r2 = 148
water_r3 = 256
water_r4 = 364
water_r5 = 472
water_r6 = 580

# Land Rows
land_r1 = 118
land_r2 = 226
land_r3 = 334
land_r4 = 442
land_r5 = 550

# Enemies' Row Offsets
orca_offset = 0
turtle_offset = 20
whale_offset = -10
crab_offset = 0
boat_offset = -35

# Entity lists
orca = [
    orca_dimens, 
    orca_offset, 
    orca_sprite
]
turtle = [
    turtle_dimens, 
    turtle_offset, 
    turtle_sprite
]
whale = [
    whale_dimens, 
    whale_offset, 
    whale_sprite
]
boat = [
    boat_dimens, 
    boat_offset, 
    boat_sprite
]
crab = [
    crab_dimens, 
    crab_offset, 
    crab_sprite
]
entity_list = [
    orca, 
    turtle, 
    whale, 
    boat, 
    crab
]
entity_speeds = [3, 5, 7, 9, 11]

# Players
player1 = entity(p1_x, p1_y, player_dimens, blue_sprite)
player1.init_as_player(True, False)
player2 = entity(p2_x, p2_y, player_dimens, purple_sprite)
player2.init_as_player(False, True)

# Enemies
land_enemy = entity_list[4]

# Enemy at Land Row 1
crab1 = entity(
    random.randint(0, win_width - land_enemy[0][0]), 
    land_r1 + land_enemy[1], 
    land_enemy[0], 
    land_enemy[2]
)
crab1.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

# Enemy at Land Row 2
crab2 = entity(
    random.randint(0, win_width - land_enemy[0][0]), 
    land_r2 + land_enemy[1], 
    land_enemy[0], 
    land_enemy[2]
)
crab2.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

# Enemy at Land Row 3
crab3 = entity(
    random.randint(0, win_width - land_enemy[0][0]), 
    land_r3 + land_enemy[1], 
    land_enemy[0], 
    land_enemy[2]
)
crab3.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

# Enemy at Land Row 4
crab4 = entity(
    random.randint(0, win_width - land_enemy[0][0]), 
    land_r4 + land_enemy[1], 
    land_enemy[0], 
    land_enemy[2]
)
crab4.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

# Enemy at Land Row 5
crab5 = entity(
    random.randint(0, win_width - land_enemy[0][0]), 
    land_r5 + land_enemy[1], 
    land_enemy[0], 
    land_enemy[2]
)
crab5.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

# Enemy at Water Row 1
water_enemy_1 = entity_list[random.randint(0, 3)]
row1_enemy = entity(
    random.randint(0, win_width - water_enemy_1[0][0]),
    water_r1 + water_enemy_1[1],
    water_enemy_1[0],
    water_enemy_1[2]
)
row1_enemy.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

# Enemy at Water Row 2
water_enemy_2 = entity_list[random.randint(0, 3)]
row2_enemy = entity(
    random.randint(0, win_width - water_enemy_2[0][0]),
    water_r2 + water_enemy_2[1],
    water_enemy_2[0],
    water_enemy_2[2]
)
row2_enemy.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

# Enemy at Water Row 3
water_enemy_3 = entity_list[random.randint(0, 3)]
row3_enemy = entity(
    random.randint(0, win_width - water_enemy_3[0][0]),
    water_r3 + water_enemy_3[1],
    water_enemy_3[0],
    water_enemy_3[2]
)
row3_enemy.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

# Enemy at Water Row 4
water_enemy_4 = entity_list[random.randint(0, 3)]
row4_enemy = entity(
    random.randint(0, win_width - water_enemy_4[0][0]),
    water_r4 + water_enemy_4[1],
    water_enemy_4[0],
    water_enemy_4[2]
)
row4_enemy.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

# Enemy at Water Row 5
water_enemy_5 = entity_list[random.randint(0, 3)]
row5_enemy = entity(
    random.randint(0, win_width - water_enemy_5[0][0]),
    water_r5 + water_enemy_5[1],
    water_enemy_5[0],
    water_enemy_5[2]
)
row5_enemy.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

# Enemy at Water Row 6
water_enemy_6 = entity_list[random.randint(0, 3)]
row6_enemy = entity(
    random.randint(0, win_width - water_enemy_6[0][0]),
    water_r6 + water_enemy_6[1],
    water_enemy_6[0],
    water_enemy_6[2]
)
row6_enemy.init_as_enemy(entity_speeds[level - 1], random.choice([-1, 1]))

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

# Restrict player from accessing certain regions of the map
def restrict_player():
    #if not player.is_jumping:
    if player.y < 0:
        player.y = 0
    if player.y > (win_height - player_dimens[1] - 2):
        player.y = (win_height - player_dimens[1] - 2)
        '''
        if player.y > 558 and player.y < 640:
            if player.up:
                player.y = 642
            elif player.down:
                player.y = 556
        if player.y > 450 and player.y < 532:
            if player.up:
                player.y = 534
            elif player.down:
                player.y = 448
        if player.y > 342 and player.y < 424:
            if player.up:
                player.y = 426
            elif player.down:
                player.y = 340
        if player.y > 234 and player.y < 316:
            if player.up:
                player.y = 318
            elif player.down:
                player.y = 232
        if player.y > 126 and player.y < 208:
            if player.up:
                player.y = 210
            elif player.down:
                player.y = 124
        if player.y > 18 and player.y < 100:
            if player.up:
                player.y = 102
            elif player.down:
                player.y = 16
        '''

# Redraw surface
def redraw():
    if not player.is_dead:
        win.blit(bg, (0, 0))
        crab1.draw()
        crab2.draw()
        crab3.draw()
        crab4.draw()
        crab5.draw()
        '''
        if not player.is_jumping:
            player.draw()
        '''
        row1_enemy.draw()
        row2_enemy.draw()
        row3_enemy.draw()
        row4_enemy.draw()
        row5_enemy.draw()
        row6_enemy.draw()
        #if player.is_jumping:
        player.draw()
    else:
        win.fill((0, 0, 0))
        player.draw()
    pygame.display.update()

# Main Loop
while(run):
    clock.tick(60)

    if whosplayin == 1:
        player = player1
    else:
        player = player2

    # Single keypress actions
    for event in pygame.event.get():

        # Quit Game
        if event.type == pygame.QUIT:
            run = False

        '''
        # Jump Trigger
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not player.right and not player.left:
                    if player.up and player.y > 50:
                        player.is_jumping = 1
                    elif player.down and player.y < (win_height - 50):
                        player.is_jumping = 2
        '''

        # Switch Player [DEBUG]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                if whosplayin == 1:
                    whosplayin = 2
                else:
                    whosplayin = 1

    if not player.is_dead:

        '''
        # Jump
        delta = clock.tick(60)
        if player.is_jumping == 1:
            if player.jump_speed > -2:
                player.y -= player.jump_speed * delta
                player.jump_speed -= 2
            else:
                player.is_jumping = False
                player.jump_speed = player_jump_speed
        elif player.is_jumping == 2:
            if player.jump_speed > -2:
                player.y += player.jump_speed * delta
                player.jump_speed -= 2
            else:
                player.is_jumping = False
                player.jump_speed = player_jump_speed
        '''

        # Restrict motion of player
        restrict_player()

        # Enemy motion
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
            if player.com()[0] > enemy_i.hitbox_static()[0] and player.com()[0] < enemy_i.hitbox_static()[0] + enemy_i.hitbox_static()[2]:
                if player.com()[1] > enemy_i.hitbox_static()[1] and player.com()[1] < enemy_i.hitbox_static()[1] + enemy_i.hitbox_static()[3]:
                    # if player.is_jumping:
                    player.is_dead = True

        for enemy_i in static_entity_list:
            if player.com()[0] > enemy_i.hitbox_static()[0] and player.com()[0] < enemy_i.hitbox_static()[0] + enemy_i.hitbox_static()[2]:
                if player.com()[1] > enemy_i.hitbox_static()[1] and player.com()[1] < enemy_i.hitbox_static()[1] + enemy_i.hitbox_static()[3]:
                    player.is_dead = True

        # Sustained keypress actions
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            sprite_direction('left')
            if player.x > 2:
                player.x -= player.speed
        elif keys[pygame.K_RIGHT]:
            sprite_direction('right')
            if player.x < (win_width - player_dimens[0] - 2):
                player.x += player.speed
        elif keys[pygame.K_UP]:
            sprite_direction('up')
            if player.y > 2:
                player.y -= player.speed
        elif keys[pygame.K_DOWN]:
            sprite_direction('down')
            if player.y < (win_height - player_dimens[1] - 2):
                player.y += player.speed

    redraw()
pygame.quit()