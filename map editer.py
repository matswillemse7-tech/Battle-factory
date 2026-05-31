import pygame
import random
import sys

pygame.init()

CELL_SIZE = 40
COLS = 1800 // CELL_SIZE  
ROWS = 800 // CELL_SIZE   

WIDTH = COLS * CELL_SIZE  
HEIGHT = ROWS * CELL_SIZE 

BACKGROUND = (20, 22, 26)  
GRID_LINE = (35, 40, 48)   
HIGHLIGHT = (55, 65, 80)   

COLOR_MAP = {
    0: (56, 55, 61),  # Background
    1: (24, 18, 30),     # Ground
    2: (24, 38, 30),     # Ground Alt (green)
    3: (92, 87, 88),  # Floor
    4: (37, 34, 45),     # Old buildings
    5: (20, 18, 25),     # Shadow background
    6: (37, 54, 45),    # Green background
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 20, bold=True)

matrix_data = [[0 for _ in range(COLS)] for _ in range(ROWS)]
current_brush = 1  

def print_matrix(data):
    print(data)

def print_nonzero_units(data):
    """Print each non-zero unit as ["number", column, row]"""
    for row in range(len(data)):
        for col in range(len(data[row])):
            val = data[row][col]
            if val != 0:
                print(f'[{val}, {col}, {row}]')

running = True
while running:
    pygame.display.set_caption(f"Map Editor | Active Brush: {current_brush} | Press 0-9 to change brush | SPACE to print array | K to print non-zero units")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                print_matrix(matrix_data)
            elif event.key == pygame.K_k:
                print_nonzero_units(matrix_data)
            elif pygame.K_0 <= event.key <= pygame.K_9:
                current_brush = event.key - pygame.K_0

    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked_col = mouse_x // CELL_SIZE
        clicked_row = mouse_y // CELL_SIZE
        
        if 0 <= clicked_row < ROWS and 0 <= clicked_col < COLS:
            matrix_data[clicked_row][clicked_col] = current_brush

    screen.fill(BACKGROUND)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover_col = mouse_x // CELL_SIZE
    hover_row = mouse_y // CELL_SIZE
    if 0 <= hover_row < ROWS and 0 <= hover_col < COLS:
        pygame.draw.rect(screen, HIGHLIGHT, (hover_col * CELL_SIZE, hover_row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            
            val = matrix_data[r][c]
            pygame.draw.rect(screen, COLOR_MAP[val], (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRID_LINE, (x, y, CELL_SIZE, CELL_SIZE), 1)
            
            text_surf = font.render(str(val), True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            screen.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()