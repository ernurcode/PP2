import pygame
import sys
import json
from game import SnakeGame
from db import Database

class GameApp:
    def __init__(self):
        pygame.init()
        
        self.WIDTH, self.HEIGHT = 600, 400
        self.CELL = 20
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Snake Game - TSIS 4")
        self.clock = pygame.time.Clock()
        
        # Load settings
        self.settings = self.load_settings()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (200, 0, 0)
        self.GREEN = (0, 200, 0)
        self.BLUE = (0, 0, 200)
        self.GRAY = (128, 128, 128)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 165, 0)
        self.PURPLE = (128, 0, 128)
        
        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 36)
        self.medium_font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)
        
        # Database
        self.db = Database()
        
        # Username
        self.username = ""
    
    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except:
            return {
                "snake_color": [0, 200, 0],
                "grid_overlay": True,
                "sound": False
            }
    
    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f, indent=4)
    
    def draw_button(self, text, rect, color, hover_color, text_color=None):
        if text_color is None:
            text_color = self.WHITE
        
        mouse_pos = pygame.mouse.get_pos()
        
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_color, rect, border_radius=8)
            pygame.draw.rect(self.screen, self.WHITE, rect, 2, border_radius=8)
        else:
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
        
        text_surf = self.medium_font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        
        return rect.collidepoint(mouse_pos)
    
    def main_menu(self):
        input_active = True
        username = ""
        
        while True:
            self.screen.fill(self.BLACK)
            
            title = self.title_font.render("SNAKE GAME", True, self.GREEN)
            title_rect = title.get_rect(center=(self.WIDTH//2, 60))
            self.screen.blit(title, title_rect)
            
            # Username input
            input_text = self.small_font.render("Enter username:", True, self.WHITE)
            self.screen.blit(input_text, (self.WIDTH//2 - 60, 110))
            
            input_rect = pygame.Rect(self.WIDTH//2 - 100, 140, 200, 35)
            pygame.draw.rect(self.screen, self.WHITE, input_rect, 2)
            
            name_surf = self.small_font.render(username + ("|" if input_active else ""), True, self.WHITE)
            self.screen.blit(name_surf, (input_rect.x + 5, input_rect.y + 5))
            
            # Buttons
            button_width = 200
            button_height = 40
            button_x = self.WIDTH//2 - button_width//2
            
            play_btn = pygame.Rect(button_x, 200, button_width, button_height)
            leaderboard_btn = pygame.Rect(button_x, 255, button_width, button_height)
            settings_btn = pygame.Rect(button_x, 310, button_width, button_height)
            quit_btn = pygame.Rect(button_x, 365, button_width, button_height)
            
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if username.strip():
                            self.username = username
                            return "play"
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 15:
                            username += event.unicode
            
            if self.draw_button("PLAY", play_btn, self.GREEN, (0, 150, 0)):
                if mouse_clicked and username.strip():
                    self.username = username
                    return "play"
            
            if self.draw_button("LEADERBOARD", leaderboard_btn, self.BLUE, (0, 0, 150)):
                if mouse_clicked:
                    return "leaderboard"
            
            if self.draw_button("SETTINGS", settings_btn, self.GRAY, (100, 100, 100)):
                if mouse_clicked:
                    return "settings"
            
            if self.draw_button("QUIT", quit_btn, self.RED, (150, 0, 0)):
                if mouse_clicked:
                    self.db.close()
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def leaderboard_screen(self):
        scores = self.db.get_top_scores()
        
        while True:
            self.screen.fill(self.BLACK)
            
            title = self.large_font.render("TOP 10 LEADERBOARD", True, self.YELLOW)
            title_rect = title.get_rect(center=(self.WIDTH//2, 30))
            self.screen.blit(title, title_rect)
            
            headers = ["RANK", "NAME", "SCORE", "LEVEL", "DATE"]
            header_x = [50, 120, 250, 350, 430]
            
            for i, header in enumerate(headers):
                surf = self.small_font.render(header, True, self.WHITE)
                self.screen.blit(surf, (header_x[i], 70))
            
            if not scores:
                no_data = self.medium_font.render("No scores yet!", True, self.GRAY)
                self.screen.blit(no_data, (self.WIDTH//2 - 80, 200))
            else:
                for i, entry in enumerate(scores[:10]):
                    y = 100 + i * 30
                    
                    rank_surf = self.small_font.render(f"{i+1}.", True, self.WHITE)
                    self.screen.blit(rank_surf, (header_x[0], y))
                    
                    name_surf = self.small_font.render(entry['username'][:10], True, self.WHITE)
                    self.screen.blit(name_surf, (header_x[1], y))
                    
                    score_surf = self.small_font.render(str(entry['score']), True, self.GREEN)
                    self.screen.blit(score_surf, (header_x[2], y))
                    
                    level_surf = self.small_font.render(str(entry['level']), True, self.BLUE)
                    self.screen.blit(level_surf, (header_x[3], y))
                    
                    date_surf = self.small_font.render(entry['date'], True, self.GRAY)
                    self.screen.blit(date_surf, (header_x[4], y))
            
            back_btn = pygame.Rect(self.WIDTH//2 - 100, 350, 200, 40)
            
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            
            if self.draw_button("BACK", back_btn, self.RED, (150, 0, 0)):
                if mouse_clicked:
                    return
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def settings_screen(self):
        snake_colors = [
            ("Green", [0, 200, 0]),
            ("Red", [200, 0, 0]),
            ("Blue", [0, 0, 200]),
            ("Yellow", [255, 255, 0]),
            ("Purple", [128, 0, 128])
        ]
        
        current_color_idx = 0
        for i, (_, color) in enumerate(snake_colors):
            if color == self.settings["snake_color"]:
                current_color_idx = i
                break
        
        while True:
            self.screen.fill(self.BLACK)
            
            title = self.large_font.render("SETTINGS", True, self.WHITE)
            title_rect = title.get_rect(center=(self.WIDTH//2, 30))
            self.screen.blit(title, title_rect)
            
            # Grid toggle
            grid_text = f"Grid: {'ON' if self.settings['grid_overlay'] else 'OFF'}"
            grid_btn = pygame.Rect(self.WIDTH//2 - 100, 80, 200, 40)
            
            # Sound toggle
            sound_text = f"Sound: {'ON' if self.settings['sound'] else 'OFF'}"
            sound_btn = pygame.Rect(self.WIDTH//2 - 100, 135, 200, 40)
            
            # Snake color
            color_text = f"Snake: {snake_colors[current_color_idx][0]}"
            color_btn = pygame.Rect(self.WIDTH//2 - 100, 190, 200, 40)
            
            # Color preview
            preview_rect = pygame.Rect(self.WIDTH//2 - 25, 245, 50, 50)
            pygame.draw.rect(self.screen, snake_colors[current_color_idx][1], preview_rect)
            pygame.draw.rect(self.screen, self.WHITE, preview_rect, 2)
            
            # Save button
            save_btn = pygame.Rect(self.WIDTH//2 - 100, 330, 200, 40)
            
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_settings()
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.save_settings()
                        return
            
            if self.draw_button(grid_text, grid_btn, self.BLUE, (0, 0, 150)):
                if mouse_clicked:
                    self.settings['grid_overlay'] = not self.settings['grid_overlay']
                    pygame.time.wait(200)
            
            if self.draw_button(sound_text, sound_btn, self.BLUE, (0, 0, 150)):
                if mouse_clicked:
                    self.settings['sound'] = not self.settings['sound']
                    pygame.time.wait(200)
            
            if self.draw_button(color_text, color_btn, self.GREEN, (0, 150, 0)):
                if mouse_clicked:
                    current_color_idx = (current_color_idx + 1) % len(snake_colors)
                    self.settings['snake_color'] = snake_colors[current_color_idx][1]
                    pygame.time.wait(200)
            
            if self.draw_button("SAVE & BACK", save_btn, self.RED, (150, 0, 0)):
                if mouse_clicked:
                    self.save_settings()
                    return
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def game_over_screen(self, score, level):
        personal_best = self.db.get_personal_best(self.username)
        
        while True:
            self.screen.fill(self.BLACK)
            
            over_text = self.title_font.render("GAME OVER", True, self.RED)
            over_rect = over_text.get_rect(center=(self.WIDTH//2, 50))
            self.screen.blit(over_text, over_rect)
            
            stats = [
                f"Score: {score}",
                f"Level: {level}",
                f"Personal Best: {max(score, personal_best)}"
            ]
            
            for i, stat in enumerate(stats):
                surf = self.large_font.render(stat, True, self.WHITE)
                rect = surf.get_rect(center=(self.WIDTH//2, 130 + i * 50))
                self.screen.blit(surf, rect)
            
            retry_btn = pygame.Rect(self.WIDTH//2 - 100, 290, 200, 40)
            menu_btn = pygame.Rect(self.WIDTH//2 - 100, 345, 200, 40)
            
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "retry"
            
            if self.draw_button("RETRY", retry_btn, self.GREEN, (0, 150, 0)):
                if mouse_clicked:
                    return "retry"
            
            if self.draw_button("MAIN MENU", menu_btn, self.BLUE, (0, 0, 150)):
                if mouse_clicked:
                    return "menu"
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def run(self):
        while True:
            action = self.main_menu()
            
            if action == "play":
                game = SnakeGame(self)
                score, level = game.run()
                
                # Save score to database
                self.db.save_score(self.username, score, level)
                
                # Game over screen
                action = self.game_over_screen(score, level)
                
                if action == "menu":
                    continue
                else:
                    continue
            elif action == "leaderboard":
                self.leaderboard_screen()
            elif action == "settings":
                self.settings_screen()

if __name__ == "__main__":
    app = GameApp()
    app.run()