import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5

# Colors
WHITE = (255, 255, 255)

# Load images
def load_image(file_name):
    return pygame.image.load(os.path.join('assets', file_name))

dinosaur_idle = load_image('dinosaur_idle.png')
dinosaur_running = load_image('dinosaur_running.png')
dinosaur_jumping = load_image('dinosaur_jumping.png')
dinosaur_falling = load_image('dinosaur_falling.png')
dinosaur_special_action = load_image('dinosaur_special_action.png')

static_platform_img = load_image('static_platform.png')
moving_platform_img = load_image('moving_platform.png')
interactive_platform_img = load_image('interactive_platform.png')
background_elements_img = load_image('background_elements.png')
collectibles_img = load_image('collectibles.png')
enemies_img = load_image('enemies.png')
obstacles_img = load_image('obstacles.png')

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2D Platformer')

# Scale images
dinosaur_idle = pygame.transform.scale(dinosaur_idle, (50, 50))
dinosaur_running = pygame.transform.scale(dinosaur_running, (50, 50))
dinosaur_jumping = pygame.transform.scale(dinosaur_jumping, (50, 50))
dinosaur_falling = pygame.transform.scale(dinosaur_falling, (50, 50))
dinosaur_special_action = pygame.transform.scale(dinosaur_special_action, (50, 50))

static_platform_img = pygame.transform.scale(static_platform_img, (100, 20))
moving_platform_img = pygame.transform.scale(moving_platform_img, (100, 20))
interactive_platform_img = pygame.transform.scale(interactive_platform_img, (100, 20))

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dinosaur_idle
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel_y = 0
        self.jumping = False
        self.running = False
        self.falling = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
            self.image = dinosaur_running
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            self.image = dinosaur_running
        if keys[pygame.K_UP] and not self.jumping:
            self.vel_y = -15
            self.jumping = True
            self.image = dinosaur_jumping
        if self.jumping:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y
            if self.vel_y > 0:
                self.image = dinosaur_falling
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.jumping = False
            self.image = dinosaur_idle

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

platforms = pygame.sprite.Group()

# Create platforms
platform_data = [
    (200, 500, static_platform_img),
    (400, 400, moving_platform_img),
    (600, 300, interactive_platform_img),
]

for plat in platform_data:
    p = Platform(*plat)
    platforms.add(p)
    all_sprites.add(p)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()