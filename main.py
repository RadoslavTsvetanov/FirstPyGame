# HI
# if you have not read the description this is my first game with pygame and most of the comments i have written are for education purposes so they are not recomended for reading by someone more experienced
# it is a two player pvp in space
import pygame
import os
import red_movement_handler
pygame.font.init()
pygame.mixer.init()
# everything to do with the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("my first pygame game")
background = (255, 255, 255)
# simple variables
FONT_COLOR = (255, 255, 255)
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 70)
BULLET = {"width": 10, "height": 5}
BULLET_VELOCITY = 10
MIDDLE = WINDOW_WIDTH // 2
MIDDLE_COLOR = (0, 0, 0)
RED_BULLET_COLOR = (255, 0, 0)
YELLOW_BULLET_COLOR = (255, 255, 0)
FPS = 60
VELOCITY = 3
BORDER = pygame.Rect(MIDDLE - 17 // 2, 0, 17, WINDOW_HEIGHT)
MAX_BULLETS = 5
# not simple variables
if(0 == 0):  # adding the if so that i can hide them
    SPACE_BACKGROUND = pygame.image.load(os.path.join("images", "space.png"))
    SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
    SPACESHIP_YELLOW = pygame.image.load(
        os.path.join('images', 'spaceship_yellow.png'))
    SPACESHIP_YELLOW = pygame.transform.rotate(pygame.transform.scale(
        SPACESHIP_YELLOW, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
    SPACESHIP_RED = pygame.image.load(
        os.path.join('images', 'spaceship_red.png'))
    SPACESHIP_RED = pygame.transform.rotate(pygame.transform.scale(
        SPACESHIP_RED, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 3 * 90)

YELLOW_HIT = pygame.USEREVENT + 1  # creating event
RED_HIT = pygame.USEREVENT + 2


def draw_window(redPlayer, yellow, red_bullets, yellow_bullets, red_life_points, yellow_life_points):
    WINDOW.blit((SPACE_BACKGROUND), (0, 0))
    pygame.draw.rect(WINDOW, MIDDLE_COLOR, BORDER)
    WINDOW.blit(SPACESHIP_YELLOW, (yellow.x, yellow.y))
    WINDOW.blit(SPACESHIP_RED, (redPlayer.x, redPlayer.y))
    red_health_text = HEALTH_FONT.render(
        "Health ->" + str(red_life_points), 1, FONT_COLOR)
    yellow_health_text = HEALTH_FONT.render(
        str(yellow_life_points) + "<- Health ", 1, FONT_COLOR)
    WINDOW.blit(red_health_text, (WINDOW_WIDTH - 200, 0))
    WINDOW.blit(yellow_health_text, (0, 0))
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED_BULLET_COLOR, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW_BULLET_COLOR, bullet)
        # order is important
        # updates/redraws the window, must stay at the end so that it will update after everything is redrawn
    pygame.display.update()


def yellow_movement_handler(yellow, keys_pressed):
    if(keys_pressed[pygame.K_a]):
        yellow.x -= VELOCITY
        if(yellow.x <= 0):
            yellow.x = 0
    if(keys_pressed[pygame.K_d]):
        yellow.x += VELOCITY
        if(yellow.x + SPACESHIP_WIDTH >= MIDDLE):
            yellow.x = MIDDLE - SPACESHIP_WIDTH
    if(keys_pressed[pygame.K_w]):
        yellow.y -= VELOCITY
        if(yellow.y <= 0):
            yellow.y = 0
    if(keys_pressed[pygame.K_s]):
        yellow.y += VELOCITY
        if(yellow.y + SPACESHIP_HEIGHT >= WINDOW_HEIGHT):
            yellow.y = WINDOW_HEIGHT


def red_movement_handler(red, keys_pressed):
    if(keys_pressed[pygame.K_j]):
        if(red.x <= MIDDLE + 17):
            red.x = MIDDLE + 17
        red.x -= VELOCITY
        if(red.x <= 0):
            red.x = 0
    if(keys_pressed[pygame.K_l]):
        red.x += VELOCITY
        if(red.x <= 0):
            red.x = 0
    if(keys_pressed[pygame.K_i]):
        red.y -= VELOCITY
        if(red.y <= 0):
            red.y = 0
    if(keys_pressed[pygame.K_k]):
        red.y += VELOCITY
        if(red.y + SPACESHIP_HEIGHT >= WINDOW_HEIGHT):
            red.y = WINDOW_HEIGHT


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, FONT_COLOR)
    WINDOW.blit(draw_text, (WINDOW_WIDTH/2 - draw_text.get_width() /
                            2, WINDOW_HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def bullets_handler(bullets_yellow, bullets_red, yellow, redPlayer):
    for bullet in bullets_yellow:
        bullet.x += BULLET_VELOCITY
        if(redPlayer.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(RED_HIT))
            bullets_yellow.remove(bullet)
        elif(bullet.x >= WINDOW_WIDTH):
            bullets_yellow.remove(bullet)
    for bullet in bullets_red:
        bullet.x -= BULLET_VELOCITY
        if(yellow.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            bullets_red.remove(bullet)
        elif(bullet.x <= 0):
            bullets_red.remove(bullet)


def main():
    redPlayer = pygame.Rect(500, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect((100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    clock = pygame.time.Clock()
    bullets_red = []
    bullets_yellow = []
    red_life_points = 5
    yellow_life_points = 5
    run = True
    while run:  # game loop
        clock.tick(FPS)
        for event in pygame.event.get():  # actual loop , which collects all the events that have happend for example RED_HIT and YELLOW_HIT
            if(event.type == pygame.QUIT):
                run = False
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_q) and len(bullets_yellow) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width + 5, yellow.y + yellow.height // 2, BULLET['width'], BULLET['height'])
                    bullets_yellow.append(bullet)
                if(event.key == pygame.K_o) and len(bullets_red) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        redPlayer.x - 5, redPlayer.y + redPlayer.height // 2, BULLET['width'], BULLET['height'])
                    bullets_red.append(bullet)
            if(event.type == RED_HIT):
                red_life_points -= 1
            if(event.type == YELLOW_HIT):
                yellow_life_points -= 1
        winner = ""
        if(red_life_points < 1):
            winner = "yellow"
        if(yellow_life_points < 1):
            winner = "red"
        if winner != "":
            draw_winner(winner)
            break
        keys_pressed = pygame.key.get_pressed()
        yellow_movement_handler(yellow, keys_pressed)
        red_movement_handler(redPlayer, keys_pressed)
        bullets_handler(bullets_yellow, bullets_red, yellow, redPlayer)
        draw_window(redPlayer, yellow, bullets_red, bullets_yellow,
                    red_life_points, yellow_life_points)
    pygame.quit()


# start game
if __name__ == '__main__':
    main()
