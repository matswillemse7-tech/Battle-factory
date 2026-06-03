import pygame
import sys
import random
import math
import os
from collections import deque
from pygame._sdl2 import Window
from map_data_getter import map_data_get
from map_data_getter import enemy_spawn_get
import pymunk
import pymunk.pygame_util
from test_ragdol import add_ragdoll
from background import draw_battle_background

GAME_RES = (1920, 1009)


pygame.init()
pygame.display.set_caption("Evil Bitcoin Miner")
virtual_surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
Window.from_display_module().maximize()
screen = pygame.Surface(GAME_RES)
width = screen.get_width()
height = screen.get_height()
height2 = virtual_surface.get_height()

robot_IMG = pygame.image.load("graphics/temp_robot.png").convert_alpha()
head1_IMG = pygame.image.load("graphics/head1.png").convert_alpha()
leg1_IMG = pygame.image.load("graphics/leg1.png").convert_alpha()
body1_IMG = pygame.image.load("graphics/body1.png").convert_alpha()
arm1_IMG = pygame.image.load("graphics/arm1.png").convert_alpha()
swipe_IMG = pygame.image.load("graphics/swipe.png").convert_alpha()
basic_machine_head_IMG = pygame.image.load("graphics/basic_machine_head.png").convert_alpha()

space_ship_map_IMG = pygame.image.load("graphics/Space_ship_map.png").convert_alpha()

Massive_font = pygame.font.Font(None, 200)
title_font = pygame.font.Font(None, 74)
text_font = pygame.font.Font(None, 36)
bold_font = pygame.font.Font(None, 44)
clock = pygame.time.Clock()

map_data = map_data_get()
enemy_spawn = enemy_spawn_get()

x,y =0,0
gamemode = "factory"
messages = [];robots = [];items = []; area = ""; area_current = 0; enemies = [];attacks = []
def draw_image_fast(surface, x, y, angle):
    if angle != 0:
        rotated_surface = pygame.transform.rotate(surface, angle)
        rect = rotated_surface.get_rect(center=(x, y))
        screen.blit(rotated_surface, rect)
    else:
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)
def draw_image_standerd(image, x, y, angle, cell_size=80):
    image_rect = image.get_rect()
    scale_factor = min(cell_size / image_rect.width, cell_size / image_rect.height)
    new_size = (int(image_rect.width * scale_factor), int(image_rect.height * scale_factor))
    image = pygame.transform.scale(image, new_size)
    image = pygame.transform.rotate(image, angle)
    rect = image.get_rect(center=(x, y))
    screen.blit(image, rect)
def draw_text(text, font, color, x, y, center=True):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)
def screen_to_surface():
    mouse_pos()
    scaled_surface = pygame.transform.scale(screen, virtual_surface.get_size())
    virtual_surface.blit(scaled_surface, (0, 0))
    pygame.display.flip()
def mouse_pos():
    global mouse_x, mouse_y
    mouse_x, mouse_y = pygame.mouse.get_pos()
    width = screen.get_width()
    height = screen.get_height()
    width2 = virtual_surface.get_width()
    height2 = virtual_surface.get_height()
    mouse_x *=(width/width2)
    mouse_y *=(height/height2)
def get_colored_sprite(surface, color):

    colored_surface = surface.copy()
    tint = pygame.Surface(colored_surface.get_size(), pygame.SRCALPHA)
    tint.fill(color)
    colored_surface.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return colored_surface


def add_message(message, time = 180):
    global messages
    messages.append([message, time])
def load_message():
    global messages
    for i in range(len(messages) - 1, -1, -1):
        draw_text(messages[i][0], bold_font, (255,255,255), width/2, 150+i*50, center=True)
        messages[i][1]-=1
        if messages[i][1] <=0:
            messages.pop(i)
def draw_play_button():
    global gamemode, count
    pts = [(1600, 120), (1600, 240), (1700, 180)]
    pygame.draw.polygon(screen, (46, 204, 113), pts)
    pygame.draw.polygon(screen, (27, 102, 57), pts, 10)
    button_rect = pygame.Rect(1600, 120, 100, 120)
    if button_rect.collidepoint(mouse_x, mouse_y):
        if pygame.mouse.get_pressed()[0]:
            gamemode = "factory_go"
            count = 0
            items = []
            robots = []
def draw_rectangle(x, y, width, height, color1, color2, edge = 2, round=0):
    rect = pygame.Rect(x-edge, y-edge, width+edge*2, height+edge*2)
    pygame.draw.rect(screen, color2, rect, border_radius = round)
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color1, rect, border_radius = round)



def draw_grid():
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            color = (50, 50, 50) if grid[r][c] == 1 else (100, 100, 100)
            pygame.draw.rect(screen, color, (width/2-overlay_WIDTH/2+c*TILE_SIZE, 65+r*TILE_SIZE, TILE_SIZE-3, TILE_SIZE-3))

def draw_factory():
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            if grid[r][c] != -1:
                if grid_id[grid[r][c]][0] == "robot_spawner":
                    pygame.draw.rect(screen, (140, 255, 255), (width/2-overlay_WIDTH/2+c*TILE_SIZE, 65+r*TILE_SIZE, TILE_SIZE-3, TILE_SIZE-3))
                if grid_id[grid[r][c]][0] == "robot_exit":
                    pygame.draw.rect(screen, (255, 180, 0), (width/2-overlay_WIDTH/2+c*TILE_SIZE, 65+r*TILE_SIZE, TILE_SIZE-3, TILE_SIZE-3))
                if grid_id[grid[r][c]][0] == "item_giver":
                    pygame.draw.rect(screen, (190, 255, 255), (width/2-overlay_WIDTH/2+c*TILE_SIZE, 65+r*TILE_SIZE, TILE_SIZE-3, TILE_SIZE-3))    
                if grid_id[grid[r][c]][0] == "tree_harvester":
                    pygame.draw.rect(screen, (100, 180, 100), (width/2-overlay_WIDTH/2+c*TILE_SIZE, 65+r*TILE_SIZE, TILE_SIZE-3, TILE_SIZE-3))
                


                if grid_id[grid[r][c]][1] == 0:
                    pygame.draw.rect(screen, (0, 0, 0), (width/2-overlay_WIDTH/2+c*TILE_SIZE+18, 65+r*TILE_SIZE, 5, 20))
                if grid_id[grid[r][c]][1] == 2:
                    pygame.draw.rect(screen, (0, 0, 0), (width/2-overlay_WIDTH/2+c*TILE_SIZE+18, 65+r*TILE_SIZE+20, 5, 20))
                if grid_id[grid[r][c]][1] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (width/2-overlay_WIDTH/2+c*TILE_SIZE+20, 65+r*TILE_SIZE+18, 20, 5))
                if grid_id[grid[r][c]][1] == 3:
                    pygame.draw.rect(screen, (0, 0, 0), (width/2-overlay_WIDTH/2+c*TILE_SIZE, 65+r*TILE_SIZE+18, 20, 5))

def draw_inventory():
    pass
def manage_factory():
    pass
def move_items():
    global items, robots
    if count == 0:
        robots = []
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                if grid[r][c] != -1:
                    if grid_id[grid[r][c]][0] == "robot_spawner":
                        robots.append([width/2-overlay_WIDTH/2+c*TILE_SIZE+20, 65+r*TILE_SIZE+20, grid_id[grid[r][c]][1], [0,0,0,0,0,0,0]])#x0, y1, direction2, 3inventory(weapon0, ammo1, weapon2, ammo3, head4, body5, legs6)
    for robot in robots:
        row = int((robot[1]-65)/TILE_SIZE)
        col = int((robot[0]-(width/2-overlay_WIDTH/2))/TILE_SIZE)
        middle = False

        if (row >= 0 and row < GRID_HEIGHT) and (col >= 0 and col < GRID_WIDTH):
            center_x = width/2 - overlay_WIDTH/2 + col * TILE_SIZE + TILE_SIZE/2
            center_y = 65 + row * TILE_SIZE + TILE_SIZE/2
            if abs(robot[0] - center_x) <= 6 and abs(robot[1] - center_y) <= 6:
                middle = True


        if not (row >= 0 and row < GRID_HEIGHT and col >= 0 and col < GRID_WIDTH):
            add_message("Robot escaped the factory!")
            robot[2] = 6


        elif grid[row][col] != -1 and middle:
            if grid_id[grid[row][col]][0] == "robot_exit":
                robot[2] = 6; robot[0] = width/2-overlay_WIDTH/2+col*TILE_SIZE+20; robot[1] = 65+row*TILE_SIZE+20
            if grid_id[grid[row][col]][1] == "item_giver":
                robot[0] = width/2-overlay_WIDTH/2+col*TILE_SIZE+20; robot[1] = 65+row*TILE_SIZE+20
                if robot[3][0] == 0:
                    robot[3][0] = 1
        if robot[2] == 0:
            robot[1]-=0.3
        if robot[2] == 2:
            robot[1]+=0.3
        if robot[2] == 1:
            robot[0]+=0.3
        if robot[2] == 3:
            robot[0]-=0.3

def draw_items():
    for item in items:
        pygame.draw.circle(screen, (255, 255, 0), (int(item[0]), int(item[1])), 10)
    for item in robots:
        draw_image_standerd(head1_IMG, item[0]+3, item[1]-16, item[2]*90-90, 16)
        draw_image_standerd(body1_IMG, item[0], item[1]-4, 0, 16)
        draw_image_standerd(arm1_IMG, item[0]+12, item[1]-8-4*math.sin(count/10+3), 0+int(math.sin(count/10+3)*30), 12)
        draw_image_standerd(arm1_IMG, item[0]-12, item[1]-8+4*math.sin(count/10+3), 180+int(math.sin(count/10+3)*30), 12)
        draw_image_standerd(leg1_IMG, item[0]+4+4*math.sin(count/10+3), item[1]+8, int(math.sin(count/10+3)*30), 12)
        draw_image_standerd(leg1_IMG, item[0]-4+4*math.sin(count/10), item[1]+8, int(math.sin(count/10)*30), 12)



def draw_progress():
    global gamemode, first_time_load, count
    counter = 0
    for item in robots:
        if item[2] == 6:
            counter +=1
    draw_text(f"Robot progress {counter}/{len(robots)}", text_font, (255, 255, 255), width/2+700, height-50)
    if len(robots) > 0 and counter/len(robots) == 1:
        gamemode = "map"

def begin_space():
    global space
    space = pymunk.Space()
    space.gravity = (0.0, 900)


def draw_map():
    global gamemode, area, area_current, first_time_load, count
    screen.fill((0, 0, 30))
    draw_rectangle(width/2-200, height/2-100, 400, 200, (130, 130, 130), (100, 100, 100), edge=10)
    draw_text("Ruins", title_font, (50, 50, 50), width/2, height/2)
    rect = pygame.Rect(width/2-200, height/2-100, 400, 200)
    if rect.collidepoint(mouse_x, mouse_y):
        if pygame.mouse.get_pressed()[0]:
            add_message("Entering the ruins...")
            gamemode = "battle"
            area = 0 #"ruins"
            area_current= 0
            first_time_load = True
            count = 0

def check_bounds():
    global battle_robots, space, first_time_load, area_current, enemies, attacks
    for robot in battle_robots:
        if robot[0] > 1880:
            first_time_load = True
            area_current +=1
            for robot in battle_robots:
                robot[5] = "ragdolled"; robot[6] = 30
            begin_space()
            enemies = []
            attacks = []


def append_robots():
    global battle_robots
    battle_robots = []
    for robot in robots:
        battle_robots.append([200, 500, robot[3], 10, 10, "ragdolled", 180, 0])#x0, y1, inventory(weapon0, ammo1, weapon2, ammo3, head4, body5, legs6), hp3, maxhp4, status5, statusduration6, feet_touching_ground7
    
def spawn_enemies():
    global enemies
    if enemy_spawn[area][area_current] != [0]:
        for i, spawner in enumerate(enemy_spawn[area][area_current]):
            enemies.append([spawner[0], spawner[1]*40+36, spawner[2]*40+20, 10, "inactive", 80, 0, 500, 100, 0])#type0, x1, y2, hp3, status4, statusduration5, target6, activation range7(not squared), weapon range8(not squared), attack cooldown9
            if spawner[0] == "basic_machine":
                head = pymunk.Body(10, 100)
                head.position = (enemies[i][1], enemies[i][2])
                head_shape = pymunk.Poly(head, [(12*math.cos(2*math.pi*i/8), 12*math.sin(2*math.pi*i/8)) for i in range(8)])
                head_shape.friction = 1
                head_shape.filter = pymunk.ShapeFilter(group=2)
                head_shape.part = 'basic_machine_head'
                head_shape.enemy = i
                head_shape.collision_type = 2
                head_shape.body.apply_force_at_world_point((-head_shape.body.mass * random.randint(-1000, 1000), 0), (head_shape.body.position.x, head_shape.body.position.y))
                space.add(head, head_shape)

    


def draw_battle_units():
    global battle_robots
    if first_time_load:
        if count == 0:
            for j, robot in enumerate(battle_robots):
                add_ragdoll(space,(300+random.randint(-100,100),300), j)
        else:
            for j, robot in enumerate(battle_robots):
                add_ragdoll(space,(300+random.randint(-100,100),600), j)

    for robot in battle_robots:
        robot[7] = 0


    for i, shape in enumerate(space.shapes):
        if hasattr(shape, 'part'):
            if shape.part == 'head':
                draw_image_standerd(head1_IMG, shape.body.position.x, shape.body.position.y, -math.degrees(shape.body.angle), 24)
                if battle_robots[shape.robot][5] != "ragdolled":  shape.body.apply_force_at_world_point((0, -shape.body.mass * 8000), (shape.body.position.x, shape.body.position.y))
                if battle_robots[shape.robot][5] == "getting_up": shape.body.apply_force_at_world_point((0, -shape.body.mass * 4000), (shape.body.position.x, shape.body.position.y))
                if battle_robots[shape.robot][5] == "moving left" or battle_robots[shape.robot][5] == "moving right": shape.body.apply_force_at_world_point((0, -shape.body.mass * 1500), (shape.body.position.x, shape.body.position.y))
            if shape.part == 'leg':
                draw_image_standerd(leg1_IMG, shape.body.position.x, shape.body.position.y, -math.degrees(shape.body.angle), 20)
                if any(shape.body.each_arbiter(lambda arb: True) or []): battle_robots[shape.robot][7] += 1
                for constraint in space.constraints:
                    if isinstance(constraint, pymunk.DampedRotarySpring) and (constraint.a == shape.body or constraint.b == shape.body):
                        if battle_robots[shape.robot][5] == "moving left": constraint.rest_angle = math.radians(int(math.sin(count/10+3-i*1.5)*45));shape.body.apply_force_at_world_point((0, +8000*math.radians(int(math.cos(count/10+3-i*1.5)*45))), (shape.body.position.x, shape.body.position.y))
                        if battle_robots[shape.robot][5] == "moving right": constraint.rest_angle = math.radians(int(math.sin(-count/10-3+i*1.5)*45));shape.body.apply_force_at_world_point((0, +8000*math.radians(int(math.cos(-count/10-3+i*1.5)*45))), (shape.body.position.x, shape.body.position.y))
                        if battle_robots[shape.robot][5] == "moving left" or battle_robots[shape.robot][5] == "moving right": constraint.stiffness = 200000
                        else: constraint.stiffness = 70000
            if shape.part == 'body':
                draw_image_standerd(body1_IMG, shape.body.position.x, shape.body.position.y, -math.degrees(shape.body.angle), 24)
                battle_robots[shape.robot][0] = shape.body.position.x
                battle_robots[shape.robot][1] = shape.body.position.y
                if battle_robots[shape.robot][5] == "turbo right": shape.body.apply_force_at_world_point((shape.body.mass * 8000, 0), (shape.body.position.x, shape.body.position.y))
                if battle_robots[shape.robot][5] == "jump": shape.body.apply_impulse_at_world_point((0,shape.body.mass * 4000), (shape.body.position.x, shape.body.position.y))
            if shape.part == 'arm':
                draw_image_standerd(arm1_IMG, shape.body.position.x, shape.body.position.y, -math.degrees(shape.body.angle)-90, 20)
            if shape.part == 'basic_machine_head':
                draw_image_standerd(basic_machine_head_IMG, shape.body.position.x, shape.body.position.y, -math.degrees(shape.body.angle), 24)
                enemies[shape.enemy][1] = shape.body.position.x
                enemies[shape.enemy][2] = shape.body.position.y
def manage_enemies():
    global enemies
    remove_enemies = []
    if enemies != []:
        for i, enemy in enumerate(enemies):
            
            if enemy[9] > 0:
                enemy[9]-=1
            if enemy[3] <= 0:
                remove_enemies.append(i)
                continue


            if enemy[4] == "inactive" and enemy[5]> 0:
                enemy[5] -=1
            elif enemy[4] == "inactive":

                distance_closest = 10000000; closest_robot = 0
                for j, robot in enumerate(battle_robots):
                    dx = robot[0] - enemy[1]
                    dy = robot[1] - enemy[2]
                    if dx**2+dy**2 <distance_closest:
                        distance_closest =dx**2+dy**2
                        closest_robot = j
                if distance_closest<enemy[7]**2:
                    enemy[4] = "active"; enemy[5] = 120; enemy[6]=closest_robot; enemy[9] = 30
            




            if enemy[4] == "active":
                if enemy[5] > 0:
                    enemy[5]-1
                robot = battle_robots[enemy[6]]
                dx = robot[0] - enemy[1]
                dy = robot[1] - enemy[2]

                distance_closest =dx**2+dy**2

                if enemy[9] == 0:
                    if enemy[8]**2 > distance_closest:
                        enemy_attack(enemy, robot, i)

                if distance_closest>enemy[7]**2:
                    enemy[4] = "inactive"; enemy[5] = 60
def enemy_attack(enemy, robot, i):
    global attacks, enemies
    if enemy[0] == "basic_machine":
        dx = robot[0] - enemy[1]
        dy = robot[1] - enemy[2]
        tangent = math.atan2(dy, dx)
        attacks.append([enemy[1], enemy[2], tangent, 1, "swipe", 30, "enemy"])#x0, y1, direction2, speed3, type4, duration5, team6,
        enemies[i][9] = 60

def manage_attacks():
    global attacks, battle_robots, enemies
    remove_attacks = []

    for i, attack in enumerate(attacks):

        if attack[4] == "swipe":
                attack[0] += (math.cos(attack[2]) * (5-(7-attack[5]*0.25)))*0.5
                attack[1] += (math.sin(attack[2]) * (5-(7-attack[5]*0.25)))*0.5
                if attack[6] == "enemy":
                    for j, robot in enumerate(battle_robots):
                        dx = robot[0] - attack[0]
                        dy = robot[1] - attack[1]
                        if dx**2 + dy**2 < 20**2:
                            battle_robots[j][3]-=attack[3]
                            remove_attacks.append(i)
                            messages.append(["Robot hit!", 60])
                            break
                if attack[6] == "player":
                    for j, enemy in enumerate(enemies):
                        dx = enemy[1] - attack[0]
                        dy = enemy[2] - attack[1]
                        if dx**2 + dy**2 < 20**2:
                            enemies[j][3]-=attack[3]
                            remove_attacks.append(i)
                            break
        attack[5]-=1
        if attack[5] <=0: remove_attacks.append(i)
        for i in sorted(remove_attacks, reverse=True):
            attacks.pop(i)

def draw_attacks():
    global attacks
    for attack in attacks:
        if attack[4] == "swipe":
            draw_image_standerd(swipe_IMG, attack[0], attack[1], -math.degrees(attack[2])+180, 32)


def manage_robot_status():
    global battle_robots
    for robot in battle_robots:
        if robot[5] == "ragdolled":
            robot[6]-=1
            if robot[6] <=0:
                robot[5] = "getting_up"
                robot[6] = 30  
        if robot[5] == "getting_up":
            robot[6]-=1
            if robot[6] <=0:
                robot[5] = "standing"
                robot[6] = 10  
        if robot[5] == "moving left" or robot[5] == "moving right":
            robot[6]-=1
            if robot[6] <=0:
                robot[5] = "standing"
                robot[6] = 10
            


def temp_wasd_robot():
    global battle_robots
    if len(battle_robots) > 0:
        for robot in battle_robots:
            if robot[5] != "ragdolled":
                if pygame.key.get_pressed()[pygame.K_a]:
                    robot[5] = "moving left"
                    robot[6] = 10
                if pygame.key.get_pressed()[pygame.K_d]:
                    robot[5] = "moving right"
                    robot[6] = 10 
                if pygame.key.get_pressed()[pygame.K_k]:
                    robot[5] = "turbo right"
                    robot[6] = 10  
                if pygame.key.get_pressed()[pygame.K_w]:
                    print(robot[7])
                    if robot[7] > 0:
                        robot[5] = "jump"
                        robot[6] = 10 
        




    

GRID_WIDTH = 21
GRID_HEIGHT = 21
TILE_SIZE = 42
overlay_WIDTH = GRID_WIDTH * TILE_SIZE
overlay_HEIGHT = GRID_HEIGHT * TILE_SIZE
overlay = pygame.Surface((overlay_WIDTH, overlay_HEIGHT), pygame.SRCALPHA)
grid = [[-1 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
running = True
count = 0


while running:
    count +=1
    screen.fill((30, 30, 30))
    draw_text(f"Battle Factory!", title_font, (255, 255, 200), width // 2, height //2 )
    draw_text(f"Click to continue", bold_font, (255, 255, 255), width // 2, height - height/4)

    clock.tick(60)

    screen_to_surface()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                running = False


grid[10][18] = 0
grid[10][19] = 2
grid[10][20] = 1
grid[10][17] = 3




grid_id = []
grid_id.append(["robot_spawner", 1])#name0, rotation1(0 = up, 1 = right, 2 = down, 3 = left),
grid_id.append(["robot_exit", 1])#name0, rotation1(0 = up, 1 = right, 2 = down, 3 = left),
grid_id.append(["item_giver", 1])#name0, rotation1(0 = up, 1 = right, 2 = down, 3 = left),
grid_id.append(["tree_harvester", 1, "gatherer", 15, 300, "wood", 1])#name0, rotation1(0 = up, 1 = right, 2 = down, 3 = left), type2, cooldown3, gatherrate4, gather_what5, gather_amount6
running = 1

begin_space()
draw_options = pymunk.pygame_util.DrawOptions(screen)
debug_physics = False

while running:
    count +=1

    first_time_load = False
    screen.fill((0, 0, 10))

    if gamemode == "factory": draw_play_button()


    if gamemode == "factory" or gamemode == "factory_go" :draw_grid()
    if gamemode == "factory" or gamemode == "factory_go" :draw_factory()

    if gamemode == "factory": draw_inventory()
    if gamemode == "factory_go": manage_factory()
    if gamemode == "factory_go": move_items()
    if gamemode == "factory_go": draw_items()
    if gamemode == "factory_go": draw_progress()
    if gamemode == "map": draw_map()

    if gamemode == "battle" and not first_time_load: check_bounds()
    if gamemode == "battle" and first_time_load and count == 0: append_robots(); print("Appended robots")
    if gamemode == "battle" and first_time_load: spawn_enemies()
    if gamemode == "battle": draw_battle_background(screen, space, map_data, area, area_current)
    if gamemode == "battle" and debug_physics: space.debug_draw(draw_options)
    if gamemode == "battle": draw_battle_units()
    if gamemode == "battle": manage_robot_status()
    if gamemode == "battle": temp_wasd_robot()
    if gamemode == "battle": manage_enemies()
    if gamemode == "battle": manage_attacks()
    if gamemode == "battle": draw_attacks()
   


    space.step(1/60)
    load_message()
    draw_text(f"FPS: {int(clock.get_fps())}", text_font, (255, 255, 255), 20, 20, center=False)
    screen_to_surface()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False