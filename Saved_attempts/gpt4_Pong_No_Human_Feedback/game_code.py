import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

# Ball dimensions
BALL_SIZE = 20

# Load the beach background image
background = pygame.image.load('beach_scene.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong with Beach Background')

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, y):
        self.rect.y += y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def reset(self):
        self.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.speed_x *= -1

# Main function
def main():
    clock = pygame.time.Clock()

    player = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    opponent = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)

    player_speed = 0
    opponent_speed = 7

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_speed = -7
                if event.key == pygame.K_s:
                    player_speed = 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player_speed = 0

        player.move(player_speed)
        ball.move()

        # Improved paddle collision detection
        if ball.rect.colliderect(player.rect):
            if ball.speed_x < 0:
                ball.rect.left = player.rect.right
            ball.speed_x *= -1
        if ball.rect.colliderect(opponent.rect):
            if ball.speed_x > 0:
                ball.rect.right = opponent.rect.left
            ball.speed_x *= -1

        if ball.rect.left <= 0 or ball.rect.right >= SCREEN_WIDTH:
            ball.reset()

        opponent.rect.y += opponent_speed if ball.rect.centery > opponent.rect.centery else -opponent_speed
        if opponent.rect.top < 0:
            opponent.rect.top = 0
        if opponent.rect.bottom > SCREEN_HEIGHT:
            opponent.rect.bottom = SCREEN_HEIGHT

        screen.blit(background, (0, 0))
        player.draw(screen)
        opponent.draw(screen)
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
