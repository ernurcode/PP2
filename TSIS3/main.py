import pygame
import sys
from ui import UI
from racer import RacerGame
from persistence import Persistence

def main():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Create window
    w, h = 400, 600
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Racer Game - TSIS 3")
    clock = pygame.time.Clock()
    
    # Load settings
    settings = Persistence.load_settings()
    print(f"Settings loaded: {settings}")
    
    # Create UI
    ui = UI(screen, clock, settings)
    
    print("\n" + "="*50)
    print("GAME READY!")
    print("="*50 + "\n")
    
    # Main loop
    while True:
        # Show main menu
        player_name = ui.main_menu()
        print(f"\nPlayer: {player_name}")
        print("Starting game...\n")
        
        # Start game
        game = RacerGame(screen, clock, settings, player_name)
        result = game.run()
        
        if result == "quit":
            break
        elif result == "gameover":
            print("\nGame Over!")
            
            # Save score
            Persistence.add_score(
                player_name,
                game.score,
                game.distance,
                game.coins_collected
            )
            
            # Show game over screen
            action = ui.game_over_screen(
                game.score,
                game.distance,
                game.coins_collected
            )
            
            if action == "retry":
                continue
            elif action == "menu":
                continue
            else:
                break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()