import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)

# Load assets
dinosaur_walking = pygame.image.load('dinosaur_walking.png')
dinosaur_jumping = pygame.image.load('dinosaur_jumping.png')
background_image = pygame.image.load('prehistoric_jungle_background.png')
platform_image = pygame.image.load('stone_platform.png')
obstacle_image = pygame.image.load('prehistoric_obstacle.png')

# Dinosaur class
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walking_frames = [dinosaur_walking]
        self.jumping_frame = dinosaur_jumping
        self.image = self.walking_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.is_jumping = False
        self.jump_speed = 15
        self.gravity = 1
        self.velocity_y = 0

    def update(self):
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
                self.rect.y = SCREEN_HEIGHT - self.rect.height
                self.is_jumping = False
                self.velocity_y = 0
            self.image = self.jumping_frame
        else:
            self.image = self.walking_frames[0]

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_speed

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = platform_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dinosaur Adventure")
        self.clock = pygame.time.Clock()
        self.dinosaur = Dinosaur()
        self.platforms = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.dinosaur)
        self.create_level()

    def create_level(self):
        # Create platforms
        platform1 = Platform(200, 500)
        platform2 = Platform(400, 400)
        platform3 = Platform(600, 300)
        self.platforms.add(platform1, platform2, platform3)
        self.all_sprites.add(platform1, platform2, platform3)

        # Create obstacles
        obstacle1 = Obstacle(300, 550)
        obstacle2 = Obstacle(500, 450)
        obstacle3 = Obstacle(700, 350)
        self.obstacles.add(obstacle1, obstacle2, obstacle3)
        self.all_sprites.add(obstacle1, obstacle2, obstacle3)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.dinosaur.jump()

            self.all_sprites.update()

            # Collision detection
            self.handle_collisions()

            # Draw everything
            self.screen.blit(background_image, (0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_collisions(self):
        # Dinosaur-platform collision
        platform_collision = pygame.sprite.spritecollide(self.dinosaur, self.platforms, False)
        if platform_collision and self.dinosaur.velocity_y >= 0:
            self.dinosaur.rect.y = platform_collision[0].rect.top - self.dinosaur.rect.height
            self.dinosaur.is_jumping = False
            self.dinosaur.velocity_y = 0

        # Dinosaur-obstacle collision
        # if pygame.sprite.spritecollide(self.dinosaur, self.obstacles, False):
        #     print("Game Over")
        #     pygame.quit()
        #     sys.exit()

# Main execution
if __name__ == "__main__":
    game = Game()
    game.run()
