import pygame 
import json
import os
from utils.fileloader import load_asset

class Player:

    def __init__(self, screen: pygame.Surface, width: int, height: int, multiplier: float = 4):
        
        self.frames = self.load_frame_data("assets/sprites/player/hero.png")

        self.screen = screen
        self.multiplier = multiplier

        self.width = width
        self.height = height

        self.move_cooldown = 0.6
        self.move_timer = 0.0

        self.x = 0
        self.y = 0

        self.alternate = False

    def load_frame_data(self, sprite_path: str):

        json_path = os.path.join(os.path.dirname(__file__), 'Player.json')

        with open(json_path) as file:
            self.json = json.load(file)

        self.direction = self.json["move:right"]["frames"]

        return load_asset(sprite_path, 24, 32)

    def set_starting_position(self, x: int, y: int):
        self.x = x
        self.y = y

    def is_moving(self):
        keys = pygame.key.get_pressed()
        moving = keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]

        return moving
    
    def cooldown_done(self):
        return self.move_timer > 0
    
    def update_timer(self):
        self.move_timer = self.move_cooldown

    def actions(self, deltatime: float):

        self.move_timer -= deltatime

        if self.cooldown_done():
            return (False, False, False, False, False, False)
        
        keys = pygame.key.get_pressed()

        spacebar = keys[pygame.K_SPACE]
        interact = keys[pygame.K_e]

        up = keys[pygame.K_UP]
        down = keys[pygame.K_DOWN]
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]
        
        return (up, down, left, right, spacebar, interact)
    
    def update_sprite_frame(self, direction: str,):
        self.direction = self.json[F"move:{direction}"]["frames"]
        self.alternate = not self.alternate
        self.update_timer()

    def down(self, rows: int):
        self.update_sprite_frame("down")
        if self.y < (rows - 1):
            self.y += 1

    def left(self):
        self.update_sprite_frame("left")
        if self.x > 0:
            self.x -= 1
    
    def right(self, cols: int):
        self.update_sprite_frame("right")
        if self.x < (cols - 1):
            self.x += 1
        
    def up(self):
        self.update_sprite_frame("up")
        if(self.y > 0):
            self.y -= 1
        
    def spacebar(self):
        self.update_timer()
    
    def interact(self):
        self.update_timer()

    def get_position(self): 
        return (self.x, self.y)
    
    def draw(self):

        if self.is_moving() or self.cooldown_done():
            walk_frames = self.direction["walk"]

            if self.alternate: frame_index = walk_frames[1]
            else: frame_index = walk_frames[0]
                
        else:
            idle_frames = self.direction["idle"]
            frame_count = len(idle_frames)
            frame_index = (pygame.time.get_ticks() // 600) % frame_count
            frame_index = idle_frames[frame_index]

        size = int(self.width * 1.2 * self.multiplier), int(self.height * 1.3 * self.multiplier)
        sprite = pygame.transform.scale(self.frames[frame_index], size)
        
        if self.y == 0: offset = 0
        else: offset = 0.4

        px = self.x * self.width * self.multiplier + (self.width * self.multiplier) // 2 - sprite.get_width() // 2
        py = (self.y - offset) * self.height * self.multiplier + (self.height * self.multiplier) // 2 - sprite.get_height() // 2
        
        self.screen.blit(sprite, (int(round(px)), int(round(py))))
