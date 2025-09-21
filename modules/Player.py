from utils.fileloader import load_json_file
from utils.fileloader import load_frames
import pygame

# Constants for player movement and animation
MOVE_COOLDOWN: float = 0.5
STATE_GENERAL: str = "general"

SCALE_ENLARGE_WIDTH: float = 1.2
SCALE_ENLARGE_HEIGHT: float = 1.3

OFFSET_Y_TOP: float = -0.1
OFFSET_Y_DEFAULT: float = 0.35
OFFSET_X_LEFT: float = 0

# Load frame animations from JSON
FRAME_ANIMATIONS = load_json_file('player.json')

class Player:
    """
    Player class for handling player state, movement, animation, and rendering.
    """

    def __init__(
            self,  screen: pygame.Surface, 
            width: int, height: int, multiplier: float = 4
        ):
        
        """
        Initialize the Player object.
        -    screen: The surface to draw the player on.
        -    width: Width of a single player frame.
        -    height: Height of a single player frame.
        -    multiplier: Scale multiplier for rendering.
        """

        super().__init__()

        # Load player frames
        self.FRAMES = load_frames([
            {
                "title": "general",
                "path": "assets/sprites/player/hero.png",
                "width": 24,
                "height": 32
            },
        ])

        self.state: str = STATE_GENERAL
        self.move_cooldown: float = MOVE_COOLDOWN
        self.frame_direction = FRAME_ANIMATIONS["action:right"]
        
        self.screen: pygame.Surface = screen
        self.multiplier: float = multiplier

        self.width: int = width
        self.height: int = height

        self.x: int = 0
        self.y: int = 0

        self.alternate: bool = False
        
        self.attack_animating: bool = False
        self.attack_frame_index: int = 0
        self.attack_anim_start_time: int = 0

        self.direction: str = "right"
        self.move_timer: float = 0.0

    ###########################################################################
    
    def set_starting_position(self, x: int, y: int) -> None:
        """
        Set the player's starting position.
        -    x (int): X position.
        -    y (int): Y position.
        """

        self.x = x
        self.y = y

    ###########################################################################
    
    def _is_moving(self) -> bool:
        """ Check if any movement key is pressed. """
        
        keys = pygame.key.get_pressed()
        moving = keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
        return moving
    
    def _cooldown_done(self) -> bool:
        """ Check if move cooldown is active. """

        return self.move_timer > 0
    
    ###########################################################################
    
    def get_position(self) -> tuple[int, int]:
        """ Get the current player position. """

        return (self.x, self.y)
    
    def _get_frame_animations(self, direction: str) -> dict:
        """
        Get frame animations for a given direction.
        -  direction: ("up", "down", "right", "left").
        """

        return FRAME_ANIMATIONS[f"action:{direction}"]
    
    ###########################################################################

    def _update_alternate(self) -> None:
        """ Toggle the alternate frame for walking animation. """

        self.alternate = not self.alternate

    def _update_timer(self) -> None:
        """ Reset the move timer to the cooldown value. """

        self.move_timer = self.move_cooldown

    def _update_state(self, state: str) -> None:
        """
        Update the player's state.
        -    state: ("general").
        """

        self.state = state

    def update_frame_direction(self, direction: str) -> None:
        """
        Update the frame direction for animation.
        -  direction: ("up", "down", "right", "left").
        """

        self.direction = direction
        self.frame_direction = self._get_frame_animations(direction)
    
    def update_sprite_frame(self, direction: str) -> None:
        """
        Update the sprite frame and direction for movement.
        -  direction: ("up", "down", "right", "left").
        """

        self.update_frame_direction(direction)
        self._update_alternate()
        self._update_timer()

    ###########################################################################
    
    def actions(self, deltatime: float) -> tuple[bool, bool, bool, bool, bool, bool]:
        """
        Handle player input and cooldowns.
        - deltatime: Time since last update.
        """

        self.move_timer -= deltatime

        if self._cooldown_done():
            return (False, False, False, False, False, False)
        
        keys = pygame.key.get_pressed()

        spacebar = keys[pygame.K_SPACE]
        interact = keys[pygame.K_e]

        up = keys[pygame.K_UP]
        down = keys[pygame.K_DOWN]
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]

        return (up, down, left, right, spacebar, interact)
    
    ###########################################################################

    def down(self, rows: int) -> None:
        """ Move the player down. """

        self.update_sprite_frame("down")
        if self.y < (rows - 1):
            self.y += 1

    def left(self) -> None:
        """ Move the player left."""

        self.update_sprite_frame("left")
        if self.x > 0:
            self.x -= 1
    
    def right(self, cols: int) -> None:
        """ Move the player right. """

        self.update_sprite_frame("right")
        if self.x < (cols - 1):
            self.x += 1
        
    def up(self) -> None:
        """ Move the player up. """

        self.update_sprite_frame("up")
        if self.y > 0:
            self.y -= 1

    def spacebar(self) -> None:
        """ Handle spacebar action (e.g., attack). """

        self._update_timer()

    def interact(self) -> None:
        """ Handle interact action (e.g., open door). """

        self._update_timer()
        
    ###########################################################################

    def _handle_animation(self, animation_type: str, speed: int = 600) -> tuple[list, int, int, int]:
        """
        Handle animation frame selection.
        - animation_type: ("idle", "walk").
        - speed: Animation speed in ms.
        """

        frames = self.frame_direction[self.state][animation_type]
        count = len(frames)
        index = (pygame.time.get_ticks() // speed) % count
        return frames, index, count, speed

    def _handle_idle(self) -> int:
        """ Get the idle frame index. """

        data = self._handle_animation("idle")
        frames = data[0]
        index = data[1]
        return frames[index]
        
    def _handle_movement(self) -> int:
        """ Get the movement frame index. """

        frames = self._handle_animation("walk")[0]
        return frames[1] if self.alternate else frames[0]

    ###########################################################################

    def draw(self, cols: int) -> None:
        """
        Draw the player sprite on the screen.
        -  cols (int): Number of columns in the grid.
        """

        x_player_offset = 0
        y_player_offset = 0

        width_enlarge = SCALE_ENLARGE_WIDTH
        height_enlarge = SCALE_ENLARGE_HEIGHT

        # Calculate y offset based on row
        if self.y == 0:
            y_offset = OFFSET_Y_TOP
        else:
            y_offset = OFFSET_Y_DEFAULT

        # Calculate x offset based on column
        if self.x == 0:
            x_offset = OFFSET_X_LEFT
        elif self.x == cols - 1:
            x_offset = -OFFSET_X_LEFT
        else:
            x_offset = 0

        # Select frame based on movement or idle state
        if self._is_moving() or self._cooldown_done(): 
            frame_index = self._handle_movement()
        else: 
            frame_index = self._handle_idle()
        
        # Calculate sprite size
        size = (
            int(self.width * width_enlarge * self.multiplier),
            int(self.height * height_enlarge * self.multiplier)
        )

        # Scale the sprite
        sprite = pygame.transform.scale(self.FRAMES[self.state][frame_index], size)

        # Calculate position to center the sprite
        x_pos = (self.x + x_offset) * self.width * self.multiplier + (self.width * self.multiplier) // 2 - sprite.get_width() // 2
        y_pos = (self.y - y_offset) * self.height * self.multiplier + (self.height * self.multiplier) // 2 - sprite.get_height() // 2

        # Draw the sprite on the screen
        self.screen.blit(sprite, (int(round(x_pos) - x_player_offset), int(round(y_pos) - y_player_offset)))