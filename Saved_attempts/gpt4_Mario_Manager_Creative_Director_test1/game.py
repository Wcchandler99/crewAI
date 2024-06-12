import pygame
from pygame.locals import *
import os

#os.chdir("~/Research/crewai/Saved_attempts/gpt4_Mario_Manager_Creative_Director_test1")

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = 10
RUN_SPEED = 5
GROUND_LEVEL = SCREEN_HEIGHT - 70

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mario')

# Load images
mario_img = pygame.image.load('Mario_walking.png').convert_alpha()
bg_img = pygame.image.load('Grassland_Level.png').convert_alpha()

# Mario Class
class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mario_img
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = GROUND_LEVEL
        self.vel_y = 0
        self.jumping = False
        self.running = False
        self.crouching = False

    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Check for collision with ground
        if self.rect.bottom > GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.vel_y = 0
            self.jumping = False

        # Move left/right
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= RUN_SPEED
            self.running = True
        elif keys[K_RIGHT]:
            self.rect.x += RUN_SPEED
            self.running = True
        else:
            self.running = False

        # Jump
        if keys[K_SPACE] and not self.jumping:
            self.vel_y = -JUMP_STRENGTH
            self.jumping = True

        # Crouch
        if keys[K_DOWN]:
            self.crouching = True
        else:
            self.crouching = False

# Game logic
def game():
    clock = pygame.time.Clock()
    mario = Mario()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(mario)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Update
        all_sprites.update()

        # Draw
        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game()