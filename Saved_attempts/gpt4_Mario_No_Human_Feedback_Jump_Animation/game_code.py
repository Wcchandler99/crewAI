import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load resources
dinosaur_image = pygame.image.load('dinosaur.png')
background_image = pygame.image.load('background.png')
platform_image = pygame.image.load('platform.png')
obstacle_image = pygame.image.load('obstacle.png')
dinosaur_movement_sound = pygame.mixer.Sound('dinosaur_movement.wav')
jump_sound = pygame.mixer.Sound('jump.wav')
landing_sound = pygame.mixer.Sound('landing.wav')
background_music = 'prehistoric_theme.mp3'

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dinosaur Platformer')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Dinosaur class
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dinosaur_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.jump_speed = -15
        self.gravity = 1
        self.change_y = 0
        self.direction = 'right'
        self.walk_frames = self.load_frames()
        self.jump_frames = self.load_frames(jump=True)
        self.walk_index = 0
        self.jump_index = 0
        self.is_jumping = False
        self.velocity = 0

    def load_frames(self, jump=False):
        frames = []
        frame_width = self.rect.width
        frame_height = self.rect.height
        y_offset = frame_height if jump else 0
        for i in range(4):
            frame = dinosaur_image.subsurface(pygame.Rect(i * frame_width, y_offset, frame_width, frame_height))
            frames.append(frame)
        return frames

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT:
            jump_sound.play()
            self.change_y = self.jump_speed
            self.is_jumping = True

        self.change_y += self.gravity
        self.rect.y += self.change_y

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.change_y = 0
            self.is_jumping = False

        if self.is_jumping:
            self.jump()
        else:
            self.walk()

    def jump(self):
        if self.jump_index >= len(self.jump_frames):
            self.jump_index = 0
        self.image = self.jump_frames[self.jump_index]
        self.jump_index += 1

    def walk(self):
        self.image = self.walk_frames[self.walk_index]
        self.walk_index = (self.walk_index + 1) % len(self.walk_frames)

    def move_left(self):
        self.rect.x -= 5
        dinosaur_movement_sound.play()
        self.direction = 'left'

    def move_right(self):
        self.rect.x += 5
        dinosaur_movement_sound.play()
        self.direction = 'right'

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

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Create the dinosaur
dinosaur = Dinosaur()
all_sprites.add(dinosaur)

# Create platforms
for i in range(5):
    platform = Platform(random.randint(0, SCREEN_WIDTH - 70), random.randint(100, SCREEN_HEIGHT - 50))
    platforms.add(platform)
    all_sprites.add(platform)

# Create obstacles
for i in range(5):
    obstacle = Obstacle(random.randint(0, SCREEN_WIDTH - 70), random.randint(100, SCREEN_HEIGHT - 50))
    obstacles.add(obstacle)
    all_sprites.add(obstacle)

# Function to play background music
def play_background_music():
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)  # Play indefinitely

# Main game loop
def main():
    play_background_music()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dinosaur.move_left()
                elif event.key == pygame.K_RIGHT:
                    dinosaur.move_right()
                elif event.key == pygame.K_SPACE:
                    dinosaur.jump()

        all_sprites.update()

        # Collision detection
        if pygame.sprite.spritecollideany(dinosaur, obstacles):
            landing_sound.play()
            running = False

        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
