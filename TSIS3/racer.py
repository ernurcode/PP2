import pygame
import random
import os

class RacerGame:
    def __init__(self, screen, clock, settings, player_name):
        self.screen = screen
        self.clock = clock
        self.settings = settings
        self.player_name = player_name
        self.w, self.h = screen.get_size()
        
        # Load all images
        self.load_images()
        
        # Load sounds
        self.load_sounds()
        
        # Initialize game
        self.reset_game()
        
        # Set difficulty
        self.set_difficulty()
    
    def load_images(self):
        """Load all game images from assets folder"""
        try:
            # Background road
            self.bg_img = pygame.image.load("assets/road.png")
            self.bg_img = pygame.transform.scale(self.bg_img, (self.w, self.h))
            
            # Player car - choose based on settings
            car_color = self.settings.get('car_color', 'red')
            if car_color == 'green':
                self.player_img = pygame.image.load("assets/carpg.png")
            else:
                self.player_img = pygame.image.load("assets/carpr.png")
            self.player_img = pygame.transform.scale(self.player_img, (50, 80))
            
            # Enemy car
            self.enemy_img = pygame.image.load("assets/care.png")
            self.enemy_img = pygame.transform.scale(self.enemy_img, (55, 80))
            
            # Coin
            self.coin_orig_img = pygame.image.load("assets/imas.png")
            
            # Obstacles
            self.barrier_img = pygame.image.load("assets/barrier.png")
            self.barrier_img = pygame.transform.scale(self.barrier_img, (50, 40))
            
            self.oil_img = pygame.image.load("assets/oil.png")
            self.oil_img = pygame.transform.scale(self.oil_img, (50, 40))
            
            self.pothole_img = pygame.image.load("assets/pothole.png")
            self.pothole_img = pygame.transform.scale(self.pothole_img, (50, 40))
            
            # Powerups
            self.nitro_img = pygame.image.load("assets/nitro.png")
            self.nitro_img = pygame.transform.scale(self.nitro_img, (30, 30))
            
            self.shield_img = pygame.image.load("assets/shield.png")
            self.shield_img = pygame.transform.scale(self.shield_img, (30, 30))
            
            print(f"All images loaded! Car color: {car_color}")
            
        except Exception as e:
            print(f"Error loading images: {e}")
            print("Check if all files are in assets folder:")
            print("road.png, carpr.png, carpg.png, care.png, imas.png")
            print("barrier.png, oil.png, pothole.png")
            print("nitro.png, shield.png")
            raise SystemExit(1)
    
    def load_sounds(self):
        """Load sound effects"""
        self.bell_sound = None
        self.crash_sound = None
        
        try:
            if self.settings.get('sound', True):
                pygame.mixer.music.load("assets/background.wav")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                
                self.bell_sound = pygame.mixer.Sound("assets/bell.wav")
                self.bell_sound.set_volume(0.5)
                
                self.crash_sound = pygame.mixer.Sound("assets/crash.wav")
                self.crash_sound.set_volume(0.7)
                
                print("Sounds loaded!")
        except Exception as e:
            print(f"Warning: {e}")
            print("Game will run without sound")
    
    def reset_game(self):
        """Reset all game variables"""
        # Player
        self.player_rect = self.player_img.get_rect(center=(self.w//2, 540))
        self.player_speed = 6
        
        # Active powerup
        self.active_powerup = None
        self.active_powerup_timer = 0
        self.player_shield = False
        
        # Game objects lists
        self.enemies = []
        self.coins = []
        self.obstacles = []
        self.powerups = []
        
        # Stats
        self.coins_collected = 0
        self.money = 0
        self.distance = 0
        self.score = 0
        
        # Background animation
        self.bg_y = 0
        
        # Lane positions
        self.lanes = [60, 175, 290]  # Left, Center, Right
        
        # Spawn timers
        self.spawn_timer = 0
        self.obstacle_timer = 0
        self.spawn_powerup_timer = 0
        
        # Game state
        self.gameover = False
    
    def set_difficulty(self):
        """Set game parameters based on difficulty"""
        difficulty = self.settings.get('difficulty', 'normal')
        
        if difficulty == 'easy':
            self.spawn_delay = 90
            self.obstacle_delay = 120
            self.powerup_delay = 240
            self.base_speed = 3
        elif difficulty == 'normal':
            self.spawn_delay = 60
            self.obstacle_delay = 90
            self.powerup_delay = 180
            self.base_speed = 5
        else:  # hard
            self.spawn_delay = 40
            self.obstacle_delay = 60
            self.powerup_delay = 150
            self.base_speed = 7
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
            
            if not self.gameover:
                self.handle_input()
                self.update()
                self.draw()
            else:
                # Save score
                from persistence import Persistence
                Persistence.add_score(
                    self.player_name,
                    self.score,
                    self.distance,
                    self.coins_collected
                )
                return "gameover"
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return "quit"
    
    def handle_input(self):
        """Handle player input"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.player_rect.left > 0:
            self.player_rect.x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_rect.right < self.w:
            self.player_rect.x += self.player_speed
        if keys[pygame.K_UP] and self.player_rect.top > 400:
            self.player_rect.y -= self.player_speed
        if keys[pygame.K_DOWN] and self.player_rect.bottom < self.h:
            self.player_rect.y += self.player_speed
    
    def update(self):
        """Update game logic"""
        # Background animation
        self.bg_y = (self.bg_y + 5) % self.h
        
        # Increase distance
        self.distance += 1
        
        # Update timers
        self.spawn_timer += 1
        self.obstacle_timer += 1
        self.spawn_powerup_timer += 1
        
        # Difficulty scaling
        current_spawn_delay = max(20, self.spawn_delay - self.coins_collected // 2)
        current_obstacle_delay = max(30, self.obstacle_delay - self.coins_collected // 3)
        
        # Spawn enemies
        if self.spawn_timer >= current_spawn_delay:
            self.spawn_enemy()
            self.spawn_timer = 0
        
        # Spawn obstacles
        if self.obstacle_timer >= current_obstacle_delay:
            if random.random() < 0.6:
                self.spawn_obstacle()
            self.obstacle_timer = 0
        
        # Spawn powerups
        if self.spawn_powerup_timer >= self.powerup_delay:
            self.spawn_powerup()
            self.spawn_powerup_timer = 0
        
        # Spawn coins (random)
        if random.random() < 0.02:
            self.spawn_coin()
        
        # Update enemies positions
        for enemy in self.enemies[:]:
            enemy['rect'].y += enemy['speed']
            if enemy['rect'].top > self.h:
                self.enemies.remove(enemy)
        
        # Update obstacles positions
        for obstacle in self.obstacles[:]:
            obstacle['rect'].y += self.base_speed
            if obstacle['rect'].top > self.h:
                self.obstacles.remove(obstacle)
        
        # Update powerups positions
        for powerup in self.powerups[:]:
            powerup['rect'].y += self.base_speed
            powerup['timer'] -= 1
            if powerup['timer'] <= 0 or powerup['rect'].top > self.h:
                self.powerups.remove(powerup)
        
        # Update coins positions
        for coin in self.coins[:]:
            coin['rect'].y += self.base_speed
            if coin['rect'].top > self.h:
                self.coins.remove(coin)
        
        # Active powerup timer
        if self.active_powerup_timer > 0:
            self.active_powerup_timer -= 1
            if self.active_powerup_timer == 0:
                self.deactivate_powerup()
        
        # Check collisions
        self.check_collisions()
        
        # Update score
        self.score = self.money + (self.distance // 10) + (self.coins_collected * 5)
    
    def spawn_enemy(self):
        """Create an enemy car"""
        lane_x = random.choice(self.lanes)
        enemy_rect = self.enemy_img.get_rect()
        enemy_rect.centerx = lane_x + 25
        enemy_rect.top = -80
        
        if not self.is_safe_spawn(enemy_rect):
            return
        
        for coin in self.coins:
            if enemy_rect.colliderect(coin['rect']):
                return
        
        speed = self.base_speed + random.randint(0, 3)
        self.enemies.append({
            'rect': enemy_rect,
            'speed': speed
        })
    
    def spawn_obstacle(self):
        """Create an obstacle"""
        lane_x = random.choice(self.lanes)
        obs_type = random.choice(['barrier', 'oil', 'pothole'])
        
        if obs_type == 'barrier':
            img = self.barrier_img
        elif obs_type == 'oil':
            img = self.oil_img
        else:
            img = self.pothole_img
        
        obstacle_rect = img.get_rect()
        obstacle_rect.centerx = lane_x + 25
        obstacle_rect.top = -40
        
        if self.is_safe_spawn(obstacle_rect):
            self.obstacles.append({
                'rect': obstacle_rect,
                'type': obs_type,
                'image': img
            })
    
    def spawn_powerup(self):
        """Create a powerup"""
        lane_x = random.choice(self.lanes)
        power_type = random.choice(['nitro', 'shield'])
        
        if power_type == 'nitro':
            img = self.nitro_img
        else:
            img = self.shield_img
        
        powerup_rect = img.get_rect()
        powerup_rect.centerx = lane_x + 25
        powerup_rect.top = -30
        
        self.powerups.append({
            'rect': powerup_rect,
            'type': power_type,
            'image': img,
            'timer': 300
        })
    
    def spawn_coin(self):
        """Create a coin with random size"""
        lane_x = random.choice(self.lanes)
        size = random.randrange(20, 41, 5)
        coin_img = pygame.transform.scale(self.coin_orig_img, (size, size))
        
        coin_rect = coin_img.get_rect()
        coin_rect.centerx = lane_x + 25
        coin_rect.top = -size
        
        for enemy in self.enemies:
            if coin_rect.colliderect(enemy['rect']):
                return
        
        for obstacle in self.obstacles:
            if coin_rect.colliderect(obstacle['rect']):
                return
        
        if not self.is_safe_spawn(coin_rect):
            return
        
        self.coins.append({
            'rect': coin_rect,
            'image': coin_img,
            'value': size
        })
    
    def is_safe_spawn(self, new_rect):
        """Check safe distance from player"""
        safe_zone = self.player_rect.inflate(150, 150)
        return not new_rect.colliderect(safe_zone)
    
    def activate_powerup(self, power_type):
        """Activate collected powerup"""
        if power_type == 'nitro':
            self.active_powerup = 'nitro'
            self.active_powerup_timer = 300
            self.player_speed = 10
        elif power_type == 'shield':
            self.active_powerup = 'shield'
            self.player_shield = True
    
    def deactivate_powerup(self):
        """Deactivate current powerup"""
        if self.active_powerup == 'nitro':
            self.player_speed = 6
        elif self.active_powerup == 'shield':
            self.player_shield = False
        
        self.active_powerup = None
        self.active_powerup_timer = 0
    
    def check_collisions(self):
        """Check all collisions"""
        for enemy in self.enemies[:]:
            if self.player_rect.colliderect(enemy['rect']):
                if self.player_shield:
                    self.deactivate_powerup()
                    self.enemies.remove(enemy)
                    if self.bell_sound:
                        self.bell_sound.play()
                else:
                    self.gameover = True
                    if self.crash_sound:
                        self.crash_sound.play()
                    return
        
        for obstacle in self.obstacles[:]:
            if self.player_rect.colliderect(obstacle['rect']):
                if self.player_shield:
                    self.deactivate_powerup()
                    self.obstacles.remove(obstacle)
                    if self.bell_sound:
                        self.bell_sound.play()
                elif obstacle['type'] == 'oil':
                    self.player_speed = max(2, self.player_speed - 3)
                    self.obstacles.remove(obstacle)
                else:
                    self.gameover = True
                    if self.crash_sound:
                        self.crash_sound.play()
                    return
        
        for coin in self.coins[:]:
            if self.player_rect.colliderect(coin['rect']):
                self.money += coin['value']
                self.coins_collected += 1
                self.coins.remove(coin)
                if self.bell_sound:
                    self.bell_sound.play()
        
        for powerup in self.powerups[:]:
            if self.player_rect.colliderect(powerup['rect']):
                self.activate_powerup(powerup['type'])
                self.powerups.remove(powerup)
    
    def draw(self):
        """Draw all game objects"""
        self.screen.blit(self.bg_img, (0, self.bg_y - self.h))
        self.screen.blit(self.bg_img, (0, self.bg_y))
        
        for obstacle in self.obstacles:
            self.screen.blit(obstacle['image'], obstacle['rect'])
        
        for coin in self.coins:
            self.screen.blit(coin['image'], coin['rect'])
        
        for powerup in self.powerups:
            self.screen.blit(powerup['image'], powerup['rect'])
        
        for enemy in self.enemies:
            self.screen.blit(self.enemy_img, enemy['rect'])
        
        self.screen.blit(self.player_img, self.player_rect)
        
        if self.player_shield:
            shield_rect = self.player_rect.inflate(20, 20)
            pygame.draw.ellipse(self.screen, (0, 255, 255), shield_rect, 3)
        
        self.draw_ui()
    
    def draw_ui(self):
        """Draw UI elements"""
        font = pygame.font.SysFont("Arial", 22, bold=True)
        
        coins_text = font.render(f"Coins: {self.coins_collected}", True, (255, 255, 255))
        self.screen.blit(coins_text, (self.w - 140, 10))
        
        money_text = font.render(f"Money: {self.money}", True, (255, 255, 255))
        self.screen.blit(money_text, (self.w - 265, 10))
        
        dist_text = font.render(f"Dist: {self.distance}m", True, (255, 255, 255))
        self.screen.blit(dist_text, (10, 10))
        
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 40))
        
        if self.active_powerup:
            power_text = font.render(f"{self.active_powerup.upper()}", True, (255, 255, 0))
            self.screen.blit(power_text, (10, 70))
            
            if self.active_powerup_timer > 0:
                sec = self.active_powerup_timer // 60
                timer_text = font.render(f"{sec}s", True, (255, 255, 0))
                self.screen.blit(timer_text, (10, 95))