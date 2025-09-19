import pygame

class Game:

    def __init__(self, width: int, height: int, screen: tuple = (1280, 720), multiplier: float = 4):
        
        pygame.init()
        
        self.deltatime = pygame.time.get_ticks() / 1000.0
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((screen[0], screen[1]))

        self.width = width
        self.height = height

        self.multiplier = multiplier

    def get_cols(self):
        return int(self.screen.get_width() // (self.width * self.multiplier))
    
    def get_rows(self):
        return int(self.screen.get_height() // (self.height * self.multiplier))

    def get_grid_dimensions(self):
        cols = self.get_cols()
        rows = self.get_rows()
        return cols, rows

    def get_screen(self):
        return self.screen
    
    def get_deltatime(self):
        return self.deltatime
    
    def get_clock(self):
        return self.clock

    def inactive(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False
    
    def update(self):
        pygame.display.flip()
        self.deltatime = self.clock.tick(60) / 1000.0

        return self.deltatime
    
    def draw(self, cols: int, rows: int, cell_width: int, cell_height: int):
        self.screen.fill((20, 20, 20))

        cell_width = int(cell_width * self.multiplier)
        cell_height = int(cell_height * self.multiplier)

        for col in range(cols):
            for row in range(rows):
                rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)
