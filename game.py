import pygame
import sys
import time

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game with Timer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player properties
player_width = 40
player_height = 60
player_speed = 5
player_jump = 20
player_gravity = 1

# Enemy properties
enemy_width = 40
enemy_height = 40
enemy_speed = 2

# Game objects
class Player(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, player_width, player_height)
        self.velocity = 0

    def move(self, dx):
        self.x += dx

    def jump(self):
        if self.velocity == 0:
            self.velocity = -player_jump

    def apply_gravity(self):
        self.velocity += player_gravity
        self.y += self.velocity

class Enemy(pygame.Rect):
    def __init__(self, x, y, direction):
        super().__init__(x, y, enemy_width, enemy_height)
        self.direction = direction

    def move(self):
        self.x += self.direction * enemy_speed

# Levels
levels = [
    # Level 1
    {
        "platforms": [
            pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
            pygame.Rect(300, 400, 200, 20),
            pygame.Rect(500, 300, 200, 20),
            pygame.Rect(100, 200, 200, 20),
        ],
        "enemies": [
            Enemy(400, 360, 1),
            Enemy(600, 260, -1),
        ],
        "player_start": (50, HEIGHT - 100),
        "goal": pygame.Rect(WIDTH - 70, 50, 50, 50)
    },
    # Level 2
    {
        "platforms": [
            pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
            pygame.Rect(100, 450, 150, 20),
            pygame.Rect(350, 350, 150, 20),
            pygame.Rect(600, 250, 150, 20),
            pygame.Rect(200, 150, 150, 20),
        ],
        "enemies": [
            Enemy(200, 410, 1),
            Enemy(450, 310, -1),
            Enemy(700, 210, 1),
        ],
        "player_start": (50, HEIGHT - 100),
        "goal": pygame.Rect(WIDTH - 70, 100, 50, 50)
    },
    # Level 3
    {
        "platforms": [
            pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
            pygame.Rect(150, 450, 100, 20),
            pygame.Rect(350, 400, 100, 20),
            pygame.Rect(550, 350, 100, 20),
            pygame.Rect(350, 250, 100, 20),
            pygame.Rect(150, 150, 100, 20),
        ],
        "enemies": [
            Enemy(200, 410, 1),
            Enemy(400, 360, -1),
            Enemy(600, 310, 1),
            Enemy(400, 210, -1),
        ],
        "player_start": (50, HEIGHT - 100),
        "goal": pygame.Rect(50, 100, 50, 50)
    },
    # Level 4
    {
        "platforms": [
            pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
            pygame.Rect(100, 450, 80, 20),
            pygame.Rect(300, 400, 80, 20),
            pygame.Rect(500, 350, 80, 20),
            pygame.Rect(700, 300, 80, 20),
            pygame.Rect(500, 200, 80, 20),
            pygame.Rect(300, 150, 80, 20),
            pygame.Rect(100, 100, 80, 20),
        ],
        "enemies": [
            Enemy(150, 410, 1),
            Enemy(350, 360, -1),
            Enemy(550, 310, 1),
            Enemy(750, 260, -1),
            Enemy(550, 160, 1),
            Enemy(350, 110, -1),
        ],
        "player_start": (50, HEIGHT - 100),
        "goal": pygame.Rect(50, 50, 50, 50)
    },
]

def show_end_screen(elapsed_time):
    screen.fill(WHITE)
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)

    congrats_text = font_large.render("Congratulations!", True, BLUE)
    time_text = font_small.render(f"Your Time: {elapsed_time:.2f} seconds", True, BLACK)
    by_leo_text = font_small.render("by Leo", True, BLACK)

    congrats_rect = congrats_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    by_leo_rect = by_leo_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(congrats_text, congrats_rect)
    screen.blit(time_text, time_rect)
    screen.blit(by_leo_text, by_leo_rect)

    pygame.display.flip()

    start_time = time.time()
    waiting = True
    while waiting:
        current_time = time.time()
        elapsed = current_time - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

        if elapsed >= 6:
            waiting = False

        pygame.time.Clock().tick(60)

def run_game():
    current_level = 0
    level = levels[current_level]
    player = Player(*level["player_start"])

    # Start the timer
    start_time = time.time()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player_speed)
        if keys[pygame.K_RIGHT]:
            player.move(player_speed)

        player.apply_gravity()

        for platform in level["platforms"]:
            if player.colliderect(platform):
                if player.velocity > 0:
                    player.bottom = platform.top
                    player.velocity = 0
                elif player.velocity < 0:
                    player.top = platform.bottom
                    player.velocity = 0

        for enemy in level["enemies"]:
            if player.colliderect(enemy):
                player.topleft = level["player_start"]
                player.velocity = 0

        for enemy in level["enemies"]:
            enemy.move()
            if enemy.left <= 0 or enemy.right >= WIDTH:
                enemy.direction *= -1

        if player.colliderect(level["goal"]):
            current_level += 1
            if current_level >= len(levels):
                elapsed_time = time.time() - start_time
                show_end_screen(elapsed_time)
                return
            level = levels[current_level]
            player.topleft = level["player_start"]
            player.velocity = 0

        screen.fill(WHITE)
        for platform in level["platforms"]:
            pygame.draw.rect(screen, GREEN, platform)
        for enemy in level["enemies"]:
            pygame.draw.rect(screen, RED, enemy)
        pygame.draw.rect(screen, BLUE, player)
        pygame.draw.rect(screen, YELLOW, level["goal"])

        # Display the timer
        elapsed_time = time.time() - start_time
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, BLACK)
        screen.blit(timer_text, (10, 40))

        level_text = font.render(f"Level: {current_level + 1}", True, BLACK)
        screen.blit(level_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run_game()
    pygame.quit()
    sys.exit()
