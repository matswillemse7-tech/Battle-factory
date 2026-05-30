import pygame
import sys
import random
import math
import os
from collections import deque
from pygame._sdl2 import Window

GAME_RES = (1920, 1009)


pygame.init()
virtual_surface = pygame.display.set_mode((10, 10), pygame.RESIZABLE)
Window.from_display_module().maximize()
screen = pygame.Surface(GAME_RES)
width = screen.get_width()
height = screen.get_height()
height2 = virtual_surface.get_height()
print(height, height2, height2-height)

robot_IMG = pygame.image.load("graphics/temp_robot.png").convert_alpha()

Massive_font = pygame.font.Font(None, 200)
title_font = pygame.font.Font(None, 74)
text_font = pygame.font.Font(None, 36)
bold_font = pygame.font.Font(None, 44)
clock = pygame.time.Clock()

x,y =0,0

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
        draw_text(messages[i][0], bold_font, (0,0,0), width/2, 150+i*50, center=True)
        messages[i][1]-=1
        if messages[i][1] <=0:
            messages.pop(i)


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


grid[10][0] = 0
grid[10][20] = 1
grid_id = []
grid_id.append(["robot_spawner", 1])#name0, rotation1(0 = up, 1 = right, 2 = down, 3 = left),
grid_id.append(["robot_exit", 1])#name0, rotation1(0 = up, 1 = right, 2 = down, 3 = left),
running = 1
while running:
    screen.fill((0, 0, 10))
    draw_grid()
    draw_factory()

    draw_inventory()



    screen_to_surface()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False