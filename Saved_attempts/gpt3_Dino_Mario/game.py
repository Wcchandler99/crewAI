# Python code for a 2D platformer game

# Import necessary libraries
import pygame
import os

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2D Platformer Game")

# Colors
WHITE = (255, 255, 255)

# Load images
background = pygame.image.load(os.path.join("images", "background.png")).convert()
player_img = pygame.image.load(os.path.join("images", "dinosaur.png")).convert()
platform_img = pygame.image.load(os.path.join("images", "platform.png")).convert()
enemy_img = pygame.image.load(os.path.join("images", "enemy.png")).convert()
powerup_img = pygame.image.load(os.path.join("images", "powerup.png")).convert()

# Scale images
player_img = pygame.transform.scale(player_img, (50, 50))
platform_img = pygame.transform.scale(platform_img, (100, 20))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
powerup_img = pygame.transform.scale(powerup_img, (30, 30))

# Player variables
player_x = 50
player_y = 450
player_dx = 0
player_dy = 0
player_speed = 5
is_jumping = False
jump_count = 10

# Platform variables
platforms = [(300, 400), (500, 300), (200, 200)]

# Game loop
running = True
while running:
    screen.fill(WHITE)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_dx = -player_speed
    if keys[pygame.K_RIGHT]:
        player_dx = player_speed
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True

    player_x += player_dx
    player_y += player_dy

    if is_jumping:
        player_y -= jump_count
        jump_count -= 1
        if jump_count < -10:
            is_jumping = False
            jump_count = 10

    player_rect = pygame.Rect(player_x, player_y, player_img.get_width(), player_img.get_height())

    for platform in platforms:
        platform_rect = pygame.Rect(platform[0], platform[1], platform_img.get_width(), platform_img.get_height())
        if player_rect.colliderect(platform_rect):
            player_dy = 0
            player_y = platform[1] - player_img.get_height()

        pygame.draw.rect(screen, (0, 0, 0), platform_rect)

    screen.blit(player_img, (player_x, player_y))

    pygame.display.flip()

pygame.quit()