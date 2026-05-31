import pygame
import pymunk


def _merge_tile_rectangles(grid, solid_values):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    active = []
    rects = []

    for r in range(rows):
        current_spans = []
        c = 0
        while c < cols:
            if grid[r][c] in solid_values:
                start = c
                while c < cols and grid[r][c] in solid_values:
                    c += 1
                current_spans.append((start, c))
            else:
                c += 1

        new_active = []
        for span in current_spans:
            matched = None
            for rect in active:
                if rect['start'] == span[0] and rect['end'] == span[1] and rect['row'] + rect['height'] == r:
                    rect['height'] += 1
                    new_active.append(rect)
                    matched = rect
                    break
            if matched is None:
                new_active.append({'start': span[0], 'end': span[1], 'row': r, 'height': 1})

        for rect in active:
            if rect not in new_active:
                rects.append(rect)
        active = new_active

    rects.extend(active)
    return rects


def draw_battle_background(screen, space, map_data, area, area_current):
    tilesize = 42
    tile_color_map = {
        0: (56, 65, 75),  # Background
        1: (24, 18, 30),  # Ground
        2: (24, 38, 30),  # Ground Alt (green)
        3: (92, 87, 88),  # Floor
        4: (34, 34, 40),  # Old buildings
        5: (20, 18, 25),  # Shadow background
        6: (37, 54, 45),  # Green background
    }

    current_grid = map_data[area][area_current]
    current_area_key = (area, area_current)
    if getattr(space, 'battle_tile_area', None) != current_area_key:
        if hasattr(space, 'battle_tile_shapes'):
            for shape in space.battle_tile_shapes:
                if shape in space.shapes:
                    space.remove(shape, shape.body)
        space.battle_tile_shapes = []
        space.battle_tile_area = current_area_key

        rects = _merge_tile_rectangles(current_grid, {1, 2, 3})
        for rect in rects:
            tile_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            tile_body.position = (
                (rect['start'] + rect['end']) * tilesize / 2 + 16,
                (rect['row'] + rect['height'] / 2) * tilesize,
            )
            tile_shape = pymunk.Poly.create_box(
                tile_body,
                ((rect['end'] - rect['start']) * tilesize, rect['height'] * tilesize),
            )
            tile_shape.friction = 1
            space.add(tile_body, tile_shape)
            space.battle_tile_shapes.append(tile_shape)

    for r, row in enumerate(current_grid):
        for c, tile_id in enumerate(row):
            if tile_id in tile_color_map:
                color = tile_color_map[tile_id]
                pygame.draw.rect(screen, color, (c * tilesize + 16, r * tilesize, tilesize, tilesize))
