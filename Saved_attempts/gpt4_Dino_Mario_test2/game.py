import pygame
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Platformer Game")

# Load images
dinosaur_idle = pygame.image.load("dinosaur_idle_pose.png")
dinosaur_run = pygame.image.load("dinosaur_running_animation.png")
dinosaur_jump = pygame.image.load("dinosaur_jumping_pose.png")
dinosaur_hurt = pygame.image.load("dinosaur_hurt_pose.png")
dinosaur_victory = pygame.image.load("dinosaur_victory_pose.png")

static_platform = pygame.image.load("static_platform.png")
moving_platform = pygame.image.load("moving_platform.png")
breakable_platform = pygame.image.load("breakable_platform.png")
spiked_platform = pygame.image.load("spiked_platform.png")

# Scale images
dinosaur_idle = pygame.transform.scale(dinosaur_idle, (50, 50))
dinosaur_run = pygame.transform.scale(dinosaur_run, (50, 50))
dinosaur_jump = pygame.transform.scale(dinosaur_jump, (50, 50))
dinosaur_hurt = pygame.transform.scale(dinosaur_hurt, (50, 50))
dinosaur_victory = pygame.transform.scale(dinosaur_victory, (50, 50))

static_platform = pygame.transform.scale(static_platform, (100, 20))
moving_platform = pygame.transform.scale(moving_platform, (100, 20))
breakable_platform = pygame.transform.scale(breakable_platform, (100, 20))
spiked_platform = pygame.transform.scale(spiked_platform, (100, 20))

# Game variables
dino_x = 100
dino_y = 500
dino_vel_x = 0
dino_vel_y = 0
gravity = 0.5
jump_strength = -15
on_ground = False

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()

    # Movement
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dino_vel_x = -5
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dino_vel_x = 5
    else:
        dino_vel_x = 0

    if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and on_ground:
        dino_vel_y = jump_strength
        on_ground = False

    # Apply gravity
    dino_vel_y += gravity

    # Update dinosaur position
    dino_x += dino_vel_x
    dino_y += dino_vel_y

    # Check for ground collision
    if dino_y >= 500:
        dino_y = 500
        on_ground = True
        dino_vel_y = 0

    # Clear screen
    screen.fill((135, 206, 235))  # Sky blue background

    # Draw dinosaur
    screen.blit(dinosaur_idle, (dino_x, dino_y))

    # Draw platforms
    screen.blit(static_platform, (300, 400))
    screen.blit(static_platform, (500, 300))
    screen.blit(static_platform, (100, 200))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()