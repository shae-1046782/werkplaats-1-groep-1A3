from modules.Player import Player
from modules.Game import Game

def main() -> None:
    """
    Main entry point for the dungeon game.
    Initializes the game and player, then runs the main game loop.
    """
    
    WIDTH: int = 16  # width of a single grid cell
    HEIGHT: int = 16  # height of a single grid cell

    # Create the game instance with the specified grid size
    DUNGEON: Game = Game(WIDTH, HEIGHT)

    # Get the game screen and initial delta time
    SCREEN = DUNGEON.get_screen()
    deltatime: float = DUNGEON.get_deltatime()

    # Create the player and set their starting position
    PLAYER: Player = Player(SCREEN, WIDTH, HEIGHT)
    PLAYER.set_starting_position(1, 1)

    # Main game loop
    while True:

        # Exit loop if the game is inactive (e.g., window closed)
        if DUNGEON.inactive():
            break
        
        else:
            cols, rows = DUNGEON.get_grid_dimensions()
            
            DUNGEON.draw(cols, rows, WIDTH, HEIGHT)
            PLAYER.draw(cols)

            # Get player actions (input states)
            up, down, left, right, spacebar, interact = PLAYER.actions(deltatime)

            if up:
                PLAYER.up()

            if down:
                PLAYER.down(rows)

            if left:
                PLAYER.left()

            if right:
                PLAYER.right(cols)

            # Update delta time for the next frame
            deltatime = DUNGEON.update()

if __name__ == "__main__":
    main()
