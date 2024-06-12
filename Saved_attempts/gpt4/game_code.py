import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game settings
FPS = 60
GRAVITY = 0.5

# Load assets
mario_image = pygame.image.load('mario.png')
enemy_image = pygame.image.load('enemy.png')
bg_image = pygame.image.load('background.jpg')

# Mario class
class Mario(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mario_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x

        # Check for horizontal collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        # Check for vertical collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
            self.on_ground = True

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.change_y = 0
            self.on_ground = True

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        if self.on_ground:
            self.change_y = -10
            self.on_ground = False

    def move_left(self):
        self.change_x = -5

    def move_right(self):
        self.change_x = 5

    def stop(self):
        self.change_x = 0

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 1000)
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.change_x = -3

    def update(self):
        self.rect.x += self.change_x
        if self.rect.x < -self.rect.width:
            self.rect.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 1000)

# Level class
class Level:
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        screen.blit(bg_image, (0, 0))
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

# Main game function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mario Game")

    mario = Mario()

    level_list = []
    level_list.append(Level(mario))

    current_level_no = 0
    current_level = level_list[current_level_no]

    mario.level = current_level

    all_sprites = pygame.sprite.Group()
    all_sprites.add(mario)

    for _ in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        current_level.enemy_list.add(enemy)

    platform1 = Platform(200, 20, 200, 400)
    platform2 = Platform(200, 20, 500, 300)
    current_level.platform_list.add(platform1)
    current_level.platform_list.add(platform2)

    clock = pygame.time.Clock()
    running = True
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mario.move_left()
                elif event.key == pygame.K_RIGHT:
                    mario.move_right()
                elif event.key == pygame.K_UP:
                    mario.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and mario.change_x < 0:
                    mario.stop()
                elif event.key == pygame.K_RIGHT and mario.change_x > 0:
                    mario.stop()

        all_sprites.update()

        current_level.update()

        screen.fill(WHITE)
        current_level.draw(screen)
        all_sprites.draw(screen)

        # Check for collisions
        if pygame.sprite.spritecollideany(mario, current_level.enemy_list):
            running = False

        # Update score
        score += 1
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()