import pygame
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer Game")

# Load images
dinosaur_standing = pygame.image.load('dinosaur_standing.png')
dinosaur_running_frame1 = pygame.image.load('dinosaur_running_frame1.png')
dinosaur_running_frame2 = pygame.image.load('dinosaur_running_frame2.png')
dinosaur_jumping = pygame.image.load('dinosaur_jumping.png')
static_platform = pygame.image.load('static_platform.png')
moving_platform = pygame.image.load('moving_platform.png')

# Scale images
dinosaur_standing = pygame.transform.scale(dinosaur_standing, (50, 50))
dinosaur_running_frame1 = pygame.transform.scale(dinosaur_running_frame1, (50, 50))
dinosaur_running_frame2 = pygame.transform.scale(dinosaur_running_frame2, (50, 50))
dinosaur_jumping = pygame.transform.scale(dinosaur_jumping, (50, 50))
static_platform = pygame.transform.scale(static_platform, (100, 20))
moving_platform = pygame.transform.scale(moving_platform, (100, 20))

# Game variables
clock = pygame.time.Clock()
running = True

# Platform Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create platforms
platforms = pygame.sprite.Group()
platforms.add(Platform(300, 400, static_platform))
platforms.add(Platform(500, 300, moving_platform))

# Dinosaur Class
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = {
            'standing': dinosaur_standing,
            'running1': dinosaur_running_frame1,
            'running2': dinosaur_running_frame2,
            'jumping': dinosaur_jumping
        }
        self.image = self.images['standing']
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500
        self.vel_y = 0
        self.jumping = False
        self.running = False
        self.running_frame = 0

    def update(self, keys_pressed):
        self.move(keys_pressed)
    
    def move(self, keys_pressed):
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.rect.x -= 5
            self.running = True
        elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.rect.x += 5
            self.running = True
        else:
            self.running = False
        
        if keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_w]:
            if not self.jumping:
                self.vel_y = -15
                self.jumping = True
        
        self.vel_y += 1  # gravity
        self.rect.y += self.vel_y
        
        # Check for collision with platforms
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for platform in platform_hit_list:
            if self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.jumping = False
                self.vel_y = 0
        
        # Update image
        if self.jumping:
            self.image = self.images['jumping']
        elif self.running:
            self.running_frame = (self.running_frame + 1) % 2
            if self.running_frame == 0:
                self.image = self.images['running1']
            else:
                self.image = self.images['running2']
        else:
            self.image = self.images['standing']

# Create dinosaur instance
dinosaur = Dinosaur()
all_sprites = pygame.sprite.Group()
all_sprites.add(dinosaur)

# Main game loop
while running:
    keys_pressed = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update sprites
    all_sprites.update(keys_pressed)
    
    # Clear screen
    screen.fill((135, 206, 250))  # Sky blue background
    
    # Draw platforms
    platforms.draw(screen)
    
    # Draw sprites
    all_sprites.draw(screen)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()