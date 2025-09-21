import pygame

class Game:
    """ A class to manage the main game window, grid, and timing using pygame. """

    def __init__(
        self, width: int, height: int,
        screen: tuple[int, int] = (1280, 720), multiplier: float = 4
        ):

        """
        Initialize the Game object.
        -    width: Width of a single grid cell (before scaling).
        -    height: Height of a single grid cell (before scaling).
        -    screen: Screen resolution (width, height). Defaults to (1280, 720).
        -    multiplier: Scale factor for grid cell size. Defaults to 4.
        """

        pygame.init()

        self.deltatime: float = pygame.time.get_ticks() / 1000.0  
        self.clock: pygame.time.Clock = pygame.time.Clock()     
        self.screen: pygame.Surface = pygame.display.set_mode((screen[0], screen[1])) 

        self.width: int = width
        self.height: int = height
        self.multiplier: float = multiplier

    def get_cols(self) -> int:
        """ Calculate the number of columns that fit on the screen. """

        return int(self.screen.get_width() // (self.width * self.multiplier))
    
    def get_rows(self) -> int:
        """ Calculate the number of rows that fit on the screen. """

        return int(self.screen.get_height() // (self.height * self.multiplier))

    def get_grid_dimensions(self) -> tuple[int, int]:
        """ Get the number of columns and rows that fit on the screen. """
        
        cols = self.get_cols()
        rows = self.get_rows()
        return cols, rows

    def get_screen(self) -> pygame.Surface:
        """ Get the games display surface. """

        return self.screen
    
    def get_deltatime(self) -> float:
        """ Get the time elapsed between frames. """

        return self.deltatime
    
    def get_clock(self) -> pygame.time.Clock:
        """ Get the game clock object. """

        return self.clock

    def inactive(self) -> bool:
        """ Handle game events and check if the window should close. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return True
                
        return False
    
    def update(self) -> float:
        """ Update the display and calculate delta time for the current frame. """
        
        pygame.display.flip()

        # Limit to 60 FPS
        self.deltatime = self.clock.tick(60) / 1000.0  
        return self.deltatime
    
    def draw(self, cols: int, rows: int, width: int, height: int) -> None:
        """
        Draw the grid on the screen.
        -  cols: Number of columns.
        -  rows: Number of rows.
        -  width: Width of each cell (before scaling).
        -  height: Height of each cell (before scaling).
        """
        
        # Fill background with dark gray
        self.screen.fill((20, 20, 20))  

        width = int(width * self.multiplier)
        height = int(height * self.multiplier)

        for col in range(cols):
            for row in range(rows):
                # Draw grid cell outline
                rect = pygame.Rect(col * width, row * height, width, height)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)  
