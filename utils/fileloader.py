import pygame

def load_asset(path: str, width: int, height: int):
    sheet = pygame.image.load(path).convert_alpha()

    sheet_width, sheet_height = sheet.get_size()

    frames = []
    for y in range(0, sheet_height, height):
        for x in range(0, sheet_width, width):
            rect = pygame.Rect(x, y, width, height)
            tile = sheet.subsurface(rect).copy() 
            frames.append(tile)
    
    return frames