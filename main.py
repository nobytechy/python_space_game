import pygame
import time
import random
import sys

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game: Powered by Nobytechy")
crush_sound = pygame.mixer.Sound("crush.mp3")
BG = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 60  # Adjust player size
PLAYER_VEL = 5
STAR_VEL = 3
STAR_WIDTH, STAR_HEIGHT = 30, 30  # Adjust star size
FONT = pygame.font.SysFont("comicsans", 35)

# Load background music
background_music = pygame.mixer.music.load("background.mp3")


def wait_for_restart():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    main()


def draw(player, end, stars):
    WIN.blit(BG, (0, 0))

    # Draw player crocodile image
    WIN.blit(player_image, (player.x, player.y))

    time_text = FONT.render(f"Time: {round(end)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    for star in stars:
        # Draw rock image
        WIN.blit(rock_image, (star.x, star.y))

    pygame.display.update()


def main():
    pygame.mixer.music.play(-1)
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start = time.time()
    end = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        end = time.time() - start

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_HEIGHT, STAR_WIDTH)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            pygame.mixer.music.stop()
            crush_sound.play()
            lost_text = FONT.render("You lost!!! PRESS ENTER TO RESTART", 1, "white")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            wait_for_restart()

        draw(player, end, stars)
    pygame.quit()


# Load player image (crocodile)
player_image = pygame.transform.scale(pygame.image.load("user.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

# Load rock image
rock_image = pygame.transform.scale(pygame.image.load("chicken.png"), (STAR_WIDTH, STAR_HEIGHT))

if __name__ == '__main__':
    main()
