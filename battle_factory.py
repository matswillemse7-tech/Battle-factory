import pygame
import sys
import random
import math
import os
from collections import deque
from pygame._sdl2 import Window
from map_data_getter import map_data_get

GAME_RES = (1920, 1009)


pygame.init()
virtual_surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
Window.from_display_module().maximize()
screen = pygame.Surface(GAME_RES)
width = screen.get_width()
height = screen.get_height()
height2 = virtual_surface.get_height()
print(height, height2, height2-height)

robot_IMG = pygame.image.load("graphics/temp_robot.png").convert_alpha()
head1_IMG = pygame.image.load("graphics/head1.png").convert_alpha()
leg1_IMG = pygame.image.load("graphics/leg1.png").convert_alpha()
body1_IMG = pygame.image.load("graphics/body1.png").convert_alpha()
arm1_IMG = pygame.image.load("graphics/arm1.png").convert_alpha()

space_ship_map_IMG = pygame.image.load("graphics/Space_ship_map.png").convert_alpha()

Massive_font = pygame.font.Font(None, 200)
title_font = pygame.font.Font(None, 74)
text_font = pygame.font.Font(None, 36)
bold_font = pygame.font.Font(None, 44)
clock = pygame.time.Clock()

map_data = map_data_get()
x,y =0,0
gamemode = "factory"
messages = [];robots = [];items = []; area = ""; area_current = 0
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

def move_items():
    global items, robots
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            if grid[r][c] != -1:
                if grid_id[grid[r][c]][0] == "robot_spawner":
                    if count == 0:
                        robots.append([width/2-overlay_WIDTH/2+c*TILE_SIZE+20, 65+r*TILE_SIZE+20, grid_id[grid[r][c]][1], [0,0,0,0,0,0,0]])#x, y, direction, inventory(weapon0, ammo1, weapon2, ammo3, head4, body5, legs6)
    for item in robots:
        row = int((item[1]-65)/TILE_SIZE)
        col = int((item[0]-(width/2-overlay_WIDTH/2))/TILE_SIZE)
        if not (row >= 0 and row < GRID_HEIGHT and col >= 0 and col < GRID_WIDTH):
            add_message("Robot escaped the factory!")
            robots.remove(item)
        elif grid[row][col] != -1:
            if grid_id[grid[row][col]][0] == "robot_exit":
                item[2] = 6; item[0] = width/2-overlay_WIDTH/2+col*TILE_SIZE+20; item[1] = 65+row*TILE_SIZE+20
        
        if item[2] == 0:
            item[1]-=0.3
        if item[2] == 2:
            item[1]+=0.3
        if item[2] == 1:
            item[0]+=0.3
        if item[2] == 3:
            item[0]-=0.3

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
    global gamemode
    counter = 0
    for item in robots:
        if item[2] == 6:
            counter +=1
    draw_text(f"Robot progress {counter}/{len(robots)}", text_font, (255, 255, 255), width/2+700, height-50)
    if len(robots) > 0 and counter/len(robots) == 1:
        gamemode = "map"

def draw_map():
    global gamemode, area, area_current
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



def draw_battle_background():
    tilesize = 42
    
    # ruins color map
    tile_color_map = {
    0: (56, 65, 75),  # Background
    1: (24, 18, 30),     # Ground
    2: (24, 38, 30),     # Ground Alt (green)
    3: (92, 87, 88),  # Floor
    4: (34, 34, 40),     # Old buildings
    5: (20, 18, 25),     # Shadow background
    6: (37, 54, 45),    # Green background
    }
    current_grid = map_data[area][area_current]
    for r in range(len(current_grid)):
        for c in range(len(current_grid[0])):
            tile_id = current_grid[r][c]

            if tile_id in tile_color_map:
                color = tile_color_map[tile_id]
                pygame.draw.rect(screen, color, (c * tilesize+16, r * tilesize, tilesize, tilesize))




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
                print("Game starting...")
                running = False


grid[10][18] = 0
grid[10][20] = 1
grid_id = []
grid_id.append(["robot_spawner", 1])#name0, rotation1(0 = up, 1 = right, 2 = down, 3 = left),
grid_id.append(["robot_exit", 1])#name0, rotation1(0 = up, 1 = right, 2 = down, 3 = left),
running = 1

while running:
    count +=1
    print(gamemode)


    screen.fill((0, 0, 10))

    if gamemode == "factory": draw_play_button()


    if gamemode == "factory" or gamemode == "factory_go" :draw_grid()
    if gamemode == "factory" or gamemode == "factory_go" :draw_factory()

    if gamemode == "factory": draw_inventory()
    if gamemode == "factory_go": move_items()
    if gamemode == "factory_go": draw_items()
    if gamemode == "factory_go": draw_progress()
    

    if gamemode == "map": draw_map()
    if gamemode == "battle": draw_battle_background()



    load_message()
    screen_to_surface()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False