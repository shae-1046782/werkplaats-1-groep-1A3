
from modules.Player import Player
from modules.Game import Game

def main():

    WIDTH = 16
    HEIGHT = 16

    DUNGEON = Game(WIDTH, HEIGHT)

    SCREEN = DUNGEON.get_screen()
    deltatime = DUNGEON.get_deltatime()

    PLAYER = Player(SCREEN, WIDTH, HEIGHT)
    PLAYER.set_starting_position(1, 1)

    while True:

        if DUNGEON.inactive(): break
        
        else: 
            
            cols, rows = DUNGEON.get_grid_dimensions()
            DUNGEON.draw(cols, rows, WIDTH, HEIGHT)

            up, down, left, right, spacebar, interact = PLAYER.actions(deltatime)
            PLAYER.draw()
            
            if up: PLAYER.up()
            if down: PLAYER.down(rows)
            if left: PLAYER.left()
            if right: PLAYER.right(cols)

            if spacebar: PLAYER.spacebar()
            if interact: PLAYER.interact()

            deltatime = DUNGEON.update()
        
if __name__ == "__main__":
    main()
