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

        self._deltatime: float = pygame.time.get_ticks() / 1000.0  
        self._clock: pygame.time.Clock = pygame.time.Clock()     
        self._screen: pygame.Surface = pygame.display.set_mode((screen[0], screen[1])) 

        self._width: int = width
        self._height: int = height
        self._multiplier: float = multiplier

    ###########################################################################
    
    def _get_cols(self) -> int:
        """ Calculate the number of columns that fit on the screen. """

        return int(self._screen.get_width() // (self._width * self._multiplier))
    
    def _get_rows(self) -> int:
        """ Calculate the number of rows that fit on the screen. """

        return int(self._screen.get_height() // (self._height * self._multiplier))
    
    def get_grid_dimensions(self) -> tuple[int, int]:
        """ Get the number of columns and rows that fit on the screen. """
        
        cols = self._get_cols()
        rows = self._get_rows()
        return cols, rows

    @property
    def get_screen(self) -> pygame.Surface:
        """ Get the games display surface. """

        return self._screen
    
    @property
    def get_deltatime(self) -> float:
        """ Get the time elapsed between frames. """

        return self._deltatime
    
    @property
    def get_clock(self) -> pygame.time.Clock:
        """ Get the game clock object. """

        return self._clock
    
    ###########################################################################
    
    @property
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
    
    ###########################################################################
    
    def update(self) -> float:
        """ Update the display and calculate delta time for the current frame. """
        
        pygame.display.flip()

        # Limit to 60 FPS
        self._deltatime = self._clock.tick(60) / 1000.0  
        return self.get_deltatime
    
    ###########################################################################
    
    def draw(self, cols: int, rows: int, width: int, height: int) -> None:
        """
        Draw the grid on the screen.
        -  cols: Number of columns.
        -  rows: Number of rows.
        -  width: Width of each cell (before scaling).
        -  height: Height of each cell (before scaling).
        """
        
        # Fill background with dark gray
        self._screen.fill((20, 20, 20))  

        width = int(width * self._multiplier)
        height = int(height * self._multiplier)

        for col in range(cols):
            for row in range(rows):
                # Draw grid cell outline
                rect = pygame.Rect(col * width, row * height, width, height)
                pygame.draw.rect(self._screen, (50, 50, 50), rect, 1)  
