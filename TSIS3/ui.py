import pygame
import sys
from persistence import Persistence

class UI:
    def __init__(self, screen, clock, settings):
        self.screen = screen
        self.clock = clock
        self.settings = settings
        self.w, self.h = screen.get_size()
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        self.YELLOW = (255, 255, 0)
        
        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 60, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 48)
        self.medium_font = pygame.font.SysFont("Arial", 36)
        self.small_font = pygame.font.SysFont("Arial", 24)
        
        self.player_name = ""
    
    def draw_button(self, text, rect, color, text_color=None):
        if text_color is None:
            text_color = self.WHITE
        
        mouse_pos = pygame.mouse.get_pos()
        
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, self.WHITE, rect, 3, border_radius=10)
        else:
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            pygame.draw.rect(self.screen, self.WHITE, rect, 2, border_radius=10)
        
        text_surf = self.medium_font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
        
        return rect.collidepoint(mouse_pos)
    
    def main_menu(self):
        while True:
            self.screen.fill(self.BLACK)
            
            title = self.title_font.render("RACER GAME", True, self.RED)
            title_rect = title.get_rect(center=(self.w//2, 80))
            self.screen.blit(title, title_rect)
            
            subtitle = self.small_font.render("TSIS 3", True, self.WHITE)
            subtitle_rect = subtitle.get_rect(center=(self.w//2, 140))
            self.screen.blit(subtitle, subtitle_rect)
            
            button_width = 250
            button_height = 50
            button_x = self.w//2 - button_width//2
            
            play_btn = pygame.Rect(button_x, 220, button_width, button_height)
            leaderboard_btn = pygame.Rect(button_x, 290, button_width, button_height)
            settings_btn = pygame.Rect(button_x, 360, button_width, button_height)
            quit_btn = pygame.Rect(button_x, 430, button_width, button_height)
            
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
            
            if self.draw_button("PLAY", play_btn, self.GREEN):
                if mouse_clicked:
                    return self.get_username()
            
            if self.draw_button("LEADERBOARD", leaderboard_btn, self.BLUE):
                if mouse_clicked:
                    self.leaderboard_screen()
            
            if self.draw_button("SETTINGS", settings_btn, self.GRAY):
                if mouse_clicked:
                    self.settings_screen()
            
            if self.draw_button("QUIT", quit_btn, self.RED):
                if mouse_clicked:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def get_username(self):
        self.player_name = ""
        input_active = True
        
        while input_active:
            self.screen.fill(self.BLACK)
            
            title = self.large_font.render("Enter Your Name", True, self.WHITE)
            title_rect = title.get_rect(center=(self.w//2, 150))
            self.screen.blit(title, title_rect)
            
            input_rect = pygame.Rect(self.w//2 - 150, 250, 300, 50)
            pygame.draw.rect(self.screen, self.WHITE, input_rect, 2)
            
            name_surf = self.medium_font.render(self.player_name + "|", True, self.WHITE)
            name_rect = name_surf.get_rect(center=input_rect.center)
            self.screen.blit(name_surf, name_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.player_name.strip():
                            return self.player_name
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        if len(self.player_name) < 15:
                            self.player_name += event.unicode
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def settings_screen(self):
        car_colors = ["red", "green"]
        difficulties = ["easy", "normal", "hard"]
        current_color_idx = car_colors.index(self.settings.get("car_color", "red"))
        current_diff_idx = difficulties.index(self.settings.get("difficulty", "normal"))
        
        while True:
            self.screen.fill(self.BLACK)
            
            title = self.large_font.render("SETTINGS", True, self.WHITE)
            title_rect = title.get_rect(center=(self.w//2, 50))
            self.screen.blit(title, title_rect)
            
            sound_text = f"Sound: {'ON' if self.settings['sound'] else 'OFF'}"
            sound_btn = pygame.Rect(self.w//2 - 100, 120, 200, 50)
            
            if car_colors[current_color_idx] == "red":
                color_text = "Car Color: RED"
            else:
                color_text = "Car Color: GREEN"
            color_btn = pygame.Rect(self.w//2 - 100, 190, 200, 50)
            
            diff_text = f"Difficulty: {difficulties[current_diff_idx]}"
            diff_btn = pygame.Rect(self.w//2 - 100, 260, 200, 50)
            
            back_btn = pygame.Rect(self.w//2 - 100, 400, 200, 50)
            
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Persistence.save_settings(self.settings)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Persistence.save_settings(self.settings)
                        return
            
            if self.draw_button(sound_text, sound_btn, self.BLUE):
                if mouse_clicked:
                    self.settings['sound'] = not self.settings['sound']
                    pygame.time.wait(200)
            
            if self.draw_button(color_text, color_btn, self.GREEN):
                if mouse_clicked:
                    current_color_idx = (current_color_idx + 1) % len(car_colors)
                    self.settings['car_color'] = car_colors[current_color_idx]
                    pygame.time.wait(200)
            
            if self.draw_button(diff_text, diff_btn, (255, 165, 0)):
                if mouse_clicked:
                    current_diff_idx = (current_diff_idx + 1) % len(difficulties)
                    self.settings['difficulty'] = difficulties[current_diff_idx]
                    pygame.time.wait(200)
            
            if self.draw_button("BACK", back_btn, self.RED):
                if mouse_clicked:
                    Persistence.save_settings(self.settings)
                    return
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def leaderboard_screen(self):
        leaderboard = Persistence.load_leaderboard()
        
        while True:
            self.screen.fill(self.BLACK)
            
            title = self.large_font.render("TOP 10", True, self.YELLOW)
            title_rect = title.get_rect(center=(self.w//2, 40))
            self.screen.blit(title, title_rect)
            
            header_text = "RANK  NAME        SCORE  DIST  COINS"
            header = self.small_font.render(header_text, True, self.WHITE)
            self.screen.blit(header, (20, 90))
            
            if not leaderboard:
                no_data = self.medium_font.render("No scores yet!", True, self.GRAY)
                no_data_rect = no_data.get_rect(center=(self.w//2, 300))
                self.screen.blit(no_data, no_data_rect)
            else:
                for i, entry in enumerate(leaderboard[:10]):
                    y_pos = 130 + i * 35
                    
                    rank_text = self.small_font.render(f"{i+1:2d}.", True, self.WHITE)
                    self.screen.blit(rank_text, (20, y_pos))
                    
                    name_text = self.small_font.render(f"{entry['name'][:10]:10s}", True, self.WHITE)
                    self.screen.blit(name_text, (50, y_pos))
                    
                    score_text = self.small_font.render(f"{entry['score']:6d}", True, self.GREEN)
                    self.screen.blit(score_text, (170, y_pos))
                    
                    dist_text = self.small_font.render(f"{entry['distance']:5d}", True, self.BLUE)
                    self.screen.blit(dist_text, (240, y_pos))
                    
                    coins_text = self.small_font.render(f"{entry['coins']:5d}", True, self.YELLOW)
                    self.screen.blit(coins_text, (300, y_pos))
            
            back_btn = pygame.Rect(self.w//2 - 100, 500, 200, 50)
            
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            
            if self.draw_button("BACK", back_btn, self.RED):
                if mouse_clicked:
                    return
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def game_over_screen(self, score, distance, coins):
        while True:
            self.screen.fill(self.BLACK)
            
            over_text = self.title_font.render("GAME OVER", True, self.RED)
            over_rect = over_text.get_rect(center=(self.w//2, 80))
            self.screen.blit(over_text, over_rect)
            
            stats = [
                f"Score: {score}",
                f"Distance: {distance}m",
                f"Coins: {coins}"
            ]
            
            for i, stat in enumerate(stats):
                stat_surf = self.medium_font.render(stat, True, self.WHITE)
                stat_rect = stat_surf.get_rect(center=(self.w//2, 170 + i * 50))
                self.screen.blit(stat_surf, stat_rect)
            
            retry_btn = pygame.Rect(self.w//2 - 100, 360, 200, 50)
            menu_btn = pygame.Rect(self.w//2 - 100, 430, 200, 50)
            
            mouse_clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
            
            if self.draw_button("RETRY", retry_btn, self.GREEN):
                if mouse_clicked:
                    return "retry"
            
            if self.draw_button("MAIN MENU", menu_btn, self.BLUE):
                if mouse_clicked:
                    return "menu"
            
            pygame.display.flip()
            self.clock.tick(60)