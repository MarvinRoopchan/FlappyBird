import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Game variables
GRAVITY = 0.25
BIRD_JUMP = -6.5
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds
PIPE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)

# Fonts
FONT = pygame.font.SysFont('Arial', 32)

# Bird class
def load_bird():
    surf = pygame.Surface((34, 24), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, (255, 255, 0), [0, 0, 34, 24])
    pygame.draw.circle(surf, (0, 0, 0), (26, 12), 4)
    return surf

class Bird:
    def __init__(self):
        self.image = load_bird()
        self.rect = self.image.get_rect(center=(80, HEIGHT // 2))
        self.movement = 0

    def update(self):
        self.movement += GRAVITY
        self.rect.y += int(self.movement)

    def jump(self):
        self.movement = BIRD_JUMP

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Pipe class
def create_pipe():
    height = random.randint(100, HEIGHT - 200)
    top = pygame.Rect(WIDTH, height - PIPE_GAP // 2 - 320, 52, 320)
    bottom = pygame.Rect(WIDTH, height + PIPE_GAP // 2, 52, 320)
    return {
        'top': top,
        'bottom': bottom,
        'scored': False
    }

def draw_pipe(surface, pipe_rect, flipped=False):
    color = GREEN
    if flipped:
        pipe_surf = pygame.transform.flip(pygame.Surface((52, 320)), False, True)
    else:
        pipe_surf = pygame.Surface((52, 320))
    pipe_surf.fill(color)
    surface.blit(pipe_surf, pipe_rect)

# Main game function
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    score = 0
    high_score = 0
    running = True
    game_active = True
    last_pipe = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird.jump()
                if event.key == pygame.K_SPACE and not game_active:
                    # Restart game
                    bird = Bird()
                    pipes.clear()
                    score = 0
                    game_active = True

        if game_active:
            # Bird
            bird.update()

            # Pipes
            now = pygame.time.get_ticks()
            if now - last_pipe > PIPE_FREQUENCY:
                pipes.append(create_pipe())
                last_pipe = now
            for pipe in pipes:
                pipe['top'].x -= PIPE_SPEED
                pipe['bottom'].x -= PIPE_SPEED
            # Remove off-screen pipes
            pipes = [p for p in pipes if p['top'].right > 0]

            # Collision
            for pipe in pipes:
                if bird.rect.colliderect(pipe['top']) or bird.rect.colliderect(pipe['bottom']):
                    game_active = False
            if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
                game_active = False

            # Score
            for pipe in pipes:
                if pipe['top'].right < bird.rect.left and not pipe['scored']:
                    score += 1
                    pipe['scored'] = True

        # Drawing
        SCREEN.fill(BLUE)
        for pipe in pipes:
            draw_pipe(SCREEN, pipe['top'], flipped=True)
            draw_pipe(SCREEN, pipe['bottom'])
        bird.draw(SCREEN)
        score_text = FONT.render(f'Score: {score}', True, WHITE)
        SCREEN.blit(score_text, (10, 10))
        if not game_active:
            high_score = max(high_score, score)
            over_text = FONT.render('Game Over! Press SPACE', True, WHITE)
            SCREEN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 40))
            hs_text = FONT.render(f'High Score: {high_score}', True, WHITE)
            SCREEN.blit(hs_text, (WIDTH // 2 - hs_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main() 