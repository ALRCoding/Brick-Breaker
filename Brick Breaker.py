import pygame
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
PADDLE_SPEED = 7.6
BALL_SPEED_X, BALL_SPEED_Y = 5, -5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Fonts
font = pygame.font.Font(None, 36)

# Function to draw a paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to draw a ball
def draw_ball(x, y):
    pygame.draw.circle(screen, RED, (x, y), BALL_RADIUS)

# Function to draw a brick
def draw_brick(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, BRICK_WIDTH, BRICK_HEIGHT))

# Function to display game over screen
def game_over(score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Draw game over text and score
        screen.fill(WHITE)
        game_over_text = font.render("Game Over", True, RED)
        score_text = font.render("Bricks Broken: " + str(score), True, RED)
        restart_text = font.render("Press R to Restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            main()

# Function to display "You Won" screen
def you_won():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Draw "You Won" text and restart button
        screen.fill(WHITE)
        you_won_text = font.render("You Won!", True, GREEN)
        restart_text = font.render("Press R to Restart", True, GREEN)
        screen.blit(you_won_text, (SCREEN_WIDTH // 2 - you_won_text.get_width() // 2, 200))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 300))

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            main()

# Main function to run the Brick Breaker game
def main():
    # Initialize the paddle and ball position
    paddle_x, paddle_y = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 2 * PADDLE_HEIGHT
    ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    ball_speed_x, ball_speed_y = BALL_SPEED_X, BALL_SPEED_Y

    # Create a list of bricks
    bricks = []
    for i in range(5):
        for j in range(9):  # Reduce the number of bricks to 45
            bricks.append((j * (BRICK_WIDTH + 5) + 30, i * (BRICK_HEIGHT + 5) + 30))

    # Initialize the score
    score = 0

    # Main game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move the paddle left or right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_x = max(paddle_x - PADDLE_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            paddle_x = min(paddle_x + PADDLE_SPEED, SCREEN_WIDTH - PADDLE_WIDTH)

        # Move the ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Check for collisions with the window boundaries
        if ball_x <= BALL_RADIUS or ball_x >= SCREEN_WIDTH - BALL_RADIUS:
            ball_speed_x *= -1
        if ball_y <= BALL_RADIUS:
            ball_speed_y *= -1

        # Check for collisions with the paddle
        if paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH and paddle_y <= ball_y + BALL_RADIUS:
            ball_speed_y *= -1

        # Check for collisions with the bricks
        for brick in bricks:
            brick_x, brick_y = brick
            if brick_x <= ball_x <= brick_x + BRICK_WIDTH and brick_y <= ball_y + BALL_RADIUS <= brick_y + BRICK_HEIGHT:
                ball_speed_y *= -1
                bricks.remove(brick)
                score += 1
                if len(bricks) == 0:
                    you_won()

        # Check for game over
        if ball_y >= SCREEN_HEIGHT:
            game_over(score)

        # Clear the screen
        screen.fill(WHITE)

        # Draw the paddle, ball, and bricks
        draw_paddle(paddle_x, paddle_y)
        draw_ball(ball_x, ball_y)
        for brick in bricks:
            draw_brick(brick[0], brick[1])

        # Update the display
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
