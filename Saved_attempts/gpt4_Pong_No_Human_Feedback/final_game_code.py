```python
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Beach Background")

# Colors
WHITE = (255, 255, 255)

# Load background image
background = pygame.image.load('beach_background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Ball settings
BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Define the paddles and ball
paddle1 = pygame.Rect(30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Score
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys
    keys = pygame.key.get_pressed()
    
    # Player 1 controls
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += PADDLE_SPEED
    
    # Player 2 controls
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
        paddle2.y += PADDLE_SPEED

    # Move the ball
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y = -BALL_SPEED_Y

    # Ball collision with paddles
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        BALL_SPEED_X = -BALL_SPEED_X

    # Ball goes out of bounds
    if ball.left <= 0:
        score2 += 1
        ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
        BALL_SPEED_X = -BALL_SPEED_X
    if ball.right >= WIDTH:
        score1 += 1
        ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
        BALL_SPEED_X = -BALL_SPEED_X

    # Draw background
    screen.blit(background, (0, 0))

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    
    # Draw the net
    for i in range(0, HEIGHT, 15):
        pygame.draw.line(screen, WHITE, (WIDTH // 2, i), (WIDTH // 2, i + 10))

    # Draw scores
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
```