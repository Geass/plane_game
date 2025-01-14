import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avoid Obstacles")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load assets
player_image = pygame.image.load("airplane.png")
player_image = pygame.transform.scale(player_image, (50, 50))
obstacle_image = pygame.image.load("cloud.png")
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))

# Player properties
player_width = 50
player_height = 50
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

# Obstacle properties
obstacle_width = 50
obstacle_height = 50

# Difficulty settings
difficulties = {
    "Easy": 3,
    "Medium": 5,
    "Hard": 8
}

def display_menu():
    menu_font = pygame.font.Font(None, 50)
    while True:
        screen.fill(WHITE)
        title_text = menu_font.render("Choose Difficulty", True, BLACK)
        easy_text = menu_font.render("1. Easy", True, BLACK)
        medium_text = menu_font.render("2. Medium", True, BLACK)
        hard_text = menu_font.render("3. Hard", True, BLACK)

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(easy_text, (SCREEN_WIDTH // 2 - easy_text.get_width() // 2, 200))
        screen.blit(medium_text, (SCREEN_WIDTH // 2 - medium_text.get_width() // 2, 300))
        screen.blit(hard_text, (SCREEN_WIDTH // 2 - hard_text.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return difficulties["Easy"]
                if event.key == pygame.K_2:
                    return difficulties["Medium"]
                if event.key == pygame.K_3:
                    return difficulties["Hard"]

def game_over_menu(score):
    menu_font = pygame.font.Font(None, 50)
    while True:
        screen.fill(WHITE)
        game_over_text = menu_font.render("Game Over", True, BLACK)
        score_text = menu_font.render(f"Score: {score}", True, BLACK)
        retry_text = menu_font.render("Press R to Retry", True, BLACK)
        quit_text = menu_font.render("Press Q to Quit", True, BLACK)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 100))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 300))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

# Select difficulty
obstacle_speed = display_menu()

# Score
score = 0

# Font
font = pygame.font.Font(None, 36)

# Obstacle list
obstacles = []

# Function to create a new obstacle
def create_obstacle():
    x = random.randint(0, SCREEN_WIDTH - obstacle_width)
    y = -obstacle_height
    return [x, y]

# Main game loop
while True:
    running = True
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - player_height - 10
    obstacles = []
    score = 0
    obstacle_spawn_chance = 30

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - player_height:
            player_y += player_speed

        # Update obstacles
        if random.randint(1, obstacle_spawn_chance) == 1:
            obstacles.append(create_obstacle())

        for obstacle in obstacles[:]:
            obstacle[1] += obstacle_speed
            if obstacle[1] > SCREEN_HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        # Gradually increase difficulty
        if score % 10 == 0 and score > 0:
            obstacle_speed += 0.1
            if obstacle_spawn_chance > 5:
                obstacle_spawn_chance -= 1

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
            if player_rect.colliderect(obstacle_rect):
                running = False

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        # Draw obstacles
        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)

    if not game_over_menu(score):
        break

# Quit Pygame
pygame.quit()
sys.exit()
