import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur 2D Platformer")

# Load game assets
dino_idle = pygame.image.load("dino_idle.png").convert_alpha()
dino_walking = pygame.image.load("dino_walking.png").convert_alpha()
dino_jumping = pygame.image.load("dino_jumping.png").convert_alpha()
dino_attack = pygame.image.load("dino_attack.png").convert_alpha()
background = pygame.image.load("background.png").convert_alpha()
standard_platform = pygame.image.load("standard_platform.png").convert_alpha()

# Scale images if necessary
dino_idle = pygame.transform.scale(dino_idle, (50, 50))
dino_walking = pygame.transform.scale(dino_walking, (50, 50))
dino_jumping = pygame.transform.scale(dino_jumping, (50, 50))
dino_attack = pygame.transform.scale(dino_attack, (50, 50))
standard_platform = pygame.transform.scale(standard_platform, (200, 50))
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Character settings
dino_rect = dino_idle.get_rect()
dino_rect.x = 100
dino_rect.y = SCREEN_HEIGHT - dino_rect.height

# Movement variables
dino_speed = 5
dino_jump_speed = -15
gravity = 1
jumping = False
y_velocity = 0

# Platforms
platforms = [
    pygame.Rect(100, 500, 200, 50),
    pygame.Rect(400, 400, 200, 50),
    pygame.Rect(200, 300, 200, 50),
]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dino_rect.x -= dino_speed
        current_dino_image = dino_walking
    if keys[pygame.K_RIGHT]:
        dino_rect.x += dino_speed
        current_dino_image = dino_walking
    if keys[pygame.K_SPACE] and not jumping:
        jumping = True
        y_velocity = dino_jump_speed
        current_dino_image = dino_jumping

    if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_SPACE]):
        current_dino_image = dino_idle

    # Apply gravity
    dino_rect.y += y_velocity
    y_velocity += gravity

    # Check collision with platforms
    on_platform = False
    for platform in platforms:
        if dino_rect.colliderect(platform) and y_velocity > 0:
            jumping = False
            y_velocity = 0
            dino_rect.y = platform.y - dino_rect.height
            on_platform = True
            break

    if not on_platform and not jumping:
        jumping = True
        y_velocity = gravity

    if dino_rect.y >= SCREEN_HEIGHT - dino_rect.height:
        dino_rect.y = SCREEN_HEIGHT - dino_rect.height
        jumping = False
        y_velocity = 0

    # Clear screen
    screen.blit(background, (0, 0))

    # Draw character
    screen.blit(current_dino_image, dino_rect)

    # Draw platforms
    for platform in platforms:
        screen.blit(standard_platform, platform)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()