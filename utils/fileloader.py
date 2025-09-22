import pygame
import json
import os

def load_json_file(file_name: str) -> dict:
    """ Loads a JSON file from the 'modules/structures' directory. """
    
    json_path = os.path.join(os.getcwd(), "modules", "structures", file_name)
    with open(json_path) as file:
        return json.load(file)

def load_frames(sprite_paths: list[dict[str, str | int]]) -> dict[str, list[pygame.Surface]]:
    """
    Loads multiple sprite sheets and returns a dictionary mapping sprite titles to lists of frames.
    sprite_paths:
        - path: Path to the sprite sheet image.
        - titl: Key for the returned dictionary.
        - width): Width of each frame.
        - height: Height of each frame.
    """

    frames: dict[str, list[pygame.Surface]] = {}
    for sprite in sprite_paths:

        # loop through each sprite definition and load its frames
        frames.update(load_asset(
            str(sprite["path"]), str(sprite["title"]),
            int(sprite["width"]), int(sprite["height"])
        ))

    return frames

def load_asset(path: str, title: str, width: int, height: int) -> dict[str, list[pygame.Surface]]:
    """
    Loads a sprite sheet and slices it into frames of the given width and height.
    - path: Path to the sprite sheet image.
    - title: Key for the returned dictionary.
    - width: Width of each frame.
    - height: Height of each frame.
    """

    sheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()

    frames: list[pygame.Surface] = []

    # Slice the sprite sheet into frames
    for y in range(0, sheet_height, height):
        for x in range(0, sheet_width, width):

            # Ensure we don't go out of bounds
            if x + width <= sheet_width and y + height <= sheet_height:
                frame = pygame.Rect(x, y, width, height)
                sprite = sheet.subsurface(frame).copy()
                frames.append(sprite)

    return {title: frames}