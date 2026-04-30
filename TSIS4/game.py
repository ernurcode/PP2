import pygame
import random

class SnakeGame:
    def __init__(self, app):
        self.app = app
        self.WIDTH = app.WIDTH
        self.HEIGHT = app.HEIGHT
        self.CELL = app.CELL
        self.screen = app.screen
        self.clock = app.clock
        self.settings = app.settings
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (200, 0, 0)
        self.DARK_RED = (100, 0, 0)
        self.GREEN = (0, 200, 0)
        self.BLUE = (0, 0, 200)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        self.CYAN = (0, 255, 255)
        self.ORANGE = (255, 165, 0)
        self.GRAY = (128, 128, 128)
        
        self.reset_game()
    
    def reset_game(self):
        # Snake
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (self.CELL, 0)
        
        # Obstacles
        self.obstacles = []
        
        # Poison food
        self.poison_food = None
        self.poison_time = 0
        
        # Power-ups
        self.powerup = None
        self.powerup_type = None
        self.powerup_time = 0
        self.powerup_active = False
        self.powerup_effect_end = 0
        
        # Shield
        self.shield_active = False
        
        # Food (MUST be after all other objects)
        self.food_value = random.randrange(10, 51, 5)
        self.food = self.random_food()
        self.food_time = pygame.time.get_ticks()
        
        # Stats
        self.score = 0
        self.level = 1
        self.money = 0
        self.speed = 7
        
        # Personal best
        self.personal_best = self.app.db.get_personal_best(self.app.username)
    
    def random_food(self):
        while True:
            pos = (random.randrange(0, self.WIDTH, self.CELL),
                   random.randrange(0, self.HEIGHT, self.CELL))
            if pos not in self.snake and pos not in self.obstacles:
                if self.poison_food is None or pos != self.poison_food:
                    if self.powerup is None or pos != self.powerup:
                        return pos
    
    def spawn_poison_food(self):
        if self.poison_food is None and random.random() < 0.3:
            while True:
                pos = (random.randrange(0, self.WIDTH, self.CELL),
                       random.randrange(0, self.HEIGHT, self.CELL))
                if pos != self.food and pos not in self.snake and pos not in self.obstacles:
                    if self.powerup is None or pos != self.powerup:
                        self.poison_food = pos
                        self.poison_time = pygame.time.get_ticks()
                        break
    
    def spawn_powerup(self):
        if self.powerup is None and not self.powerup_active and random.random() < 0.01:
            types = ['speed', 'slow', 'shield']
            self.powerup_type = random.choice(types)
            
            while True:
                pos = (random.randrange(0, self.WIDTH, self.CELL),
                       random.randrange(0, self.HEIGHT, self.CELL))
                if pos != self.food and pos not in self.snake and pos not in self.obstacles:
                    if self.poison_food is None or pos != self.poison_food:
                        self.powerup = pos
                        self.powerup_time = pygame.time.get_ticks()
                        break
    
    def spawn_obstacles(self):
        if self.level >= 3:
            num_obstacles = min(3 + self.level, 15)
            
            for _ in range(num_obstacles):
                attempts = 0
                while attempts < 50:
                    pos = (random.randrange(0, self.WIDTH, self.CELL),
                           random.randrange(0, self.HEIGHT, self.CELL))
                    
                    if pos not in self.snake and pos != self.food and pos not in self.obstacles:
                        if self.poison_food is None or pos != self.poison_food:
                            if self.powerup is None or pos != self.powerup:
                                head = self.snake[0]
                                safe_zone = [
                                    (head[0] + self.CELL, head[1]),
                                    (head[0] - self.CELL, head[1]),
                                    (head[0], head[1] + self.CELL),
                                    (head[0], head[1] - self.CELL)
                                ]
                                
                                if pos not in safe_zone:
                                    self.obstacles.append(pos)
                                    break
                    attempts += 1
    
    def update(self):
        # Spawn objects
        self.spawn_poison_food()
        self.spawn_powerup()
        
        # Move snake
        x, y = self.snake[0]
        head = (x + self.direction[0], y + self.direction[1])
        
        # Wall collision
        if head[0] < 0 or head[0] >= self.WIDTH or head[1] < 0 or head[1] >= self.HEIGHT:
            if self.shield_active:
                self.shield_active = False
                if head[0] < 0:
                    head = (self.WIDTH - self.CELL, head[1])
                elif head[0] >= self.WIDTH:
                    head = (0, head[1])
                elif head[1] < 0:
                    head = (head[0], self.HEIGHT - self.CELL)
                elif head[1] >= self.HEIGHT:
                    head = (head[0], 0)
            else:
                return False
        
        # Self collision
        if head in self.snake:
            if self.shield_active:
                self.shield_active = False
            else:
                return False
        
        # Obstacle collision
        if head in self.obstacles:
            if self.shield_active:
                self.shield_active = False
                self.obstacles.remove(head)
            else:
                return False
        
        self.snake.insert(0, head)
        
        # Food collision
        if head == self.food:
            self.money += self.food_value
            self.score += 1
            self.food_value = random.randrange(10, 51, 5)
            self.food = self.random_food()
            self.food_time = pygame.time.get_ticks()
            
            if self.score % 3 == 0:
                self.level += 1
                self.speed += 2
                self.obstacles = []
                self.spawn_obstacles()
        elif head == self.poison_food:
            self.snake.pop()
            if len(self.snake) > 1:
                self.snake.pop()
            self.poison_food = None
            
            if len(self.snake) <= 1:
                return False
        elif head == self.powerup:
            self.powerup_active = True
            self.powerup_effect_end = pygame.time.get_ticks() + 5000
            
            if self.powerup_type == 'speed':
                self.speed += 5
            elif self.powerup_type == 'slow':
                self.speed = max(3, self.speed - 3)
            elif self.powerup_type == 'shield':
                self.shield_active = True
            
            self.powerup = None
            self.powerup_type = None
        else:
            self.snake.pop()
        
        # Food timeout (5 seconds)
        if pygame.time.get_ticks() - self.food_time > 5000:
            self.food_value = random.randrange(10, 51, 5)
            self.food = self.random_food()
            self.food_time = pygame.time.get_ticks()
        
        # Poison food timeout (8 seconds)
        if self.poison_food and pygame.time.get_ticks() - self.poison_time > 8000:
            self.poison_food = None
        
        # Power-up timeout on field (8 seconds)
        if self.powerup and pygame.time.get_ticks() - self.powerup_time > 8000:
            self.powerup = None
            self.powerup_type = None
        
        # Power-up effect timeout (5 seconds)
        if self.powerup_active and pygame.time.get_ticks() >= self.powerup_effect_end:
            self.powerup_active = False
            if self.powerup_type == 'speed':
                self.speed = max(3, self.speed - 5)
            elif self.powerup_type == 'slow':
                self.speed += 3
        
        return True
    
    def draw_grid(self):
        if self.settings['grid_overlay']:
            for x in range(0, self.WIDTH, self.CELL):
                pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, self.HEIGHT))
            for y in range(0, self.HEIGHT, self.CELL):
                pygame.draw.line(self.screen, (30, 30, 30), (0, y), (self.WIDTH, y))
    
    def draw(self):
        self.screen.fill(self.BLACK)
        
        self.draw_grid()
        
        # Draw obstacles
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, self.GRAY, (*obs, self.CELL, self.CELL))
            pygame.draw.rect(self.screen, self.WHITE, (*obs, self.CELL, self.CELL), 1)
        
        # Draw food
        food_color = (min(255, self.food_value * 5), 0, 0)
        pygame.draw.rect(self.screen, food_color, (*self.food, self.CELL, self.CELL))
        
        # Draw poison food
        if self.poison_food:
            pygame.draw.rect(self.screen, self.DARK_RED, (*self.poison_food, self.CELL, self.CELL))
            pygame.draw.rect(self.screen, self.RED, (*self.poison_food, self.CELL, self.CELL), 2)
        
        # Draw power-up
        if self.powerup:
            if self.powerup_type == 'speed':
                color = self.YELLOW
            elif self.powerup_type == 'slow':
                color = self.BLUE
            else:
                color = self.CYAN
            
            pygame.draw.rect(self.screen, color, (*self.powerup, self.CELL, self.CELL))
            
            font = pygame.font.SysFont("Arial", 14, bold=True)
            if self.powerup_type == 'speed':
                text = font.render("S", True, self.BLACK)
            elif self.powerup_type == 'slow':
                text = font.render("W", True, self.BLACK)
            else:
                text = font.render("H", True, self.BLACK)
            
            text_rect = text.get_rect(center=(self.powerup[0] + self.CELL//2, 
                                              self.powerup[1] + self.CELL//2))
            self.screen.blit(text, text_rect)
        
        # Draw snake
        snake_color = tuple(self.settings['snake_color'])
        for i, segment in enumerate(self.snake):
            if self.shield_active:
                color = self.CYAN
            else:
                color = snake_color
            
            pygame.draw.rect(self.screen, color, (*segment, self.CELL, self.CELL))
            
            if i == 0:
                pygame.draw.rect(self.screen, self.WHITE, (*segment, self.CELL, self.CELL), 2)
            else:
                darker = (max(0, color[0]-50), max(0, color[1]-50), max(0, color[2]-50))
                pygame.draw.rect(self.screen, darker, (*segment, self.CELL, self.CELL), 1)
        
        # Draw UI
        font = pygame.font.SysFont("Arial", 18, bold=True)
        
        score_text = font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        level_text = font.render(f"Level: {self.level}", True, self.WHITE)
        self.screen.blit(level_text, (10, 35))
        
        money_text = font.render(f"Money: {self.money}", True, self.WHITE)
        self.screen.blit(money_text, (150, 10))
        
        pb_text = font.render(f"Best: {max(self.score, self.personal_best)}", True, self.YELLOW)
        self.screen.blit(pb_text, (150, 35))
        
        if self.powerup_active:
            remaining = (self.powerup_effect_end - pygame.time.get_ticks()) // 1000
            if remaining > 0:
                if self.powerup_type == 'speed':
                    pu_text = font.render(f"SPEED: {remaining}s", True, self.YELLOW)
                elif self.powerup_type == 'slow':
                    pu_text = font.render(f"SLOW: {remaining}s", True, self.BLUE)
                else:
                    pu_text = font.render(f"SHIELD", True, self.CYAN)
                self.screen.blit(pu_text, (300, 10))
        
        if self.shield_active:
            shield_text = font.render("SHIELD", True, self.CYAN)
            self.screen.blit(shield_text, (300, 35))
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP] and self.direction != (0, self.CELL):
            self.direction = (0, -self.CELL)
        elif keys[pygame.K_DOWN] and self.direction != (0, -self.CELL):
            self.direction = (0, self.CELL)
        elif keys[pygame.K_LEFT] and self.direction != (self.CELL, 0):
            self.direction = (-self.CELL, 0)
        elif keys[pygame.K_RIGHT] and self.direction != (-self.CELL, 0):
            self.direction = (self.CELL, 0)
    
    def run(self):
        running = True
        
        while running:
            self.clock.tick(self.speed)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.score, self.level
            
            self.handle_input()
            
            if not self.update():
                running = False
            
            self.draw()
            pygame.display.flip()
        
        return self.score, self.level