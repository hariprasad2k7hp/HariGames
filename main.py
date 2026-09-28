import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Custom Dino Game")

# Load background image
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Ground/platform alignment
ground_y = 260   # adjust until Dino feet align with grass

# Load Dino frames
dino_run1 = pygame.image.load("dino_run1.png").convert_alpha()
dino_run2 = pygame.image.load("dino_run2.png").convert_alpha()
dino_run3 = pygame.image.load("dino_run3.png").convert_alpha()

dino_run1 = pygame.transform.scale(dino_run1, (80, 80))
dino_run2 = pygame.transform.scale(dino_run2, (80, 80))
dino_run3 = pygame.transform.scale(dino_run3, (80, 80))

dino_frames = [dino_run1, dino_run2, dino_run3]
dino_jump = pygame.image.load("dino_jump.png").convert_alpha()
dino_jump = pygame.transform.scale(dino_jump, (80, 80))

# Load cactus image
cactus_img = pygame.image.load("cactus.png").convert_alpha()
cactus_img = pygame.transform.scale(cactus_img, (35, 55))

# Sounds
jump_sound = pygame.mixer.Sound("jump.wav")
pygame.mixer.music.load("background_music.ogg")
pygame.mixer.music.play(-1)

# Font
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

def game_loop():
    dino_rect = dino_run1.get_rect(midbottom=(100, ground_y))
    gravity = 0
    jump_strength = -20
    frame_index = 0
    score = 0
    running = True

    # Background scroll setup
    bg_x1 = 0
    bg_x2 = WIDTH

    # Create multiple cactus obstacles spaced far apart
    cacti = []
    for i in range(3):
        x_pos = WIDTH + (i * 400) + random.randint(200, 400)
        rect = cactus_img.get_rect(midbottom=(x_pos, ground_y))
        cacti.append(rect)

    cactus_speed = 7  # starting speed

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dino_rect.bottom >= ground_y:
                    gravity = jump_strength
                    jump_sound.play()

        # Gravity
        gravity += 1
        dino_rect.y += gravity
        if dino_rect.bottom >= ground_y:
            dino_rect.bottom = ground_y

        # Animation
        if dino_rect.bottom < ground_y:
            current_dino = dino_jump
        else:
            frame_index += 0.2
            if frame_index >= len(dino_frames):
                frame_index = 0
            current_dino = dino_frames[int(frame_index)]

        # Increase cactus speed as score rises
        cactus_speed = 7 + score // 5

        # Background scroll
        bg_x1 -= cactus_speed
        bg_x2 -= cactus_speed
        if bg_x1 <= -WIDTH:
            bg_x1 = WIDTH
        if bg_x2 <= -WIDTH:
            bg_x2 = WIDTH

        # Move cacti
        for rect in cacti:
            rect.x -= cactus_speed
            if rect.right < 0:
                rect.left = WIDTH + random.randint(500, 900)
                score += 1

            # Collision check
            if dino_rect.colliderect(rect):
                return score

        # Draw scrolling background
        screen.blit(background, (bg_x1, 0))
        screen.blit(background, (bg_x2, 0))

        # Draw Dino and cacti
        screen.blit(current_dino, dino_rect)
        for rect in cacti:
            screen.blit(cactus_img, rect)

        # Score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(30)

def game_over_screen(score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return  # restart game

        screen.blit(background, (0, 0))
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
        restart_text = font.render("Press SPACE to Restart", True, (0, 0, 0))

        screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2 - 40))
        screen.blit(score_text, (WIDTH//2 - 100, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - 150, HEIGHT//2 + 40))

        pygame.display.update()
        clock.tick(30)

# Main loop
while True:
    final_score = game_loop()
    game_over_screen(final_score)
