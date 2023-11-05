import pygame

WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
BALL_VEL = 5
PONG_VEL = 4

PONG_COLLISION = pygame.USEREVENT + 1
Y_BORDER_COLLISION = pygame.USEREVENT + 2
LEAVE_FIELD_LEFT = pygame.USEREVENT + 3
LEAVE_FIELD_RIGHT = pygame.USEREVENT + 4

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PypyPong")
BORDER = pygame.Rect(WIDTH / 2 - 4, 0, 8, HEIGHT)


def draw_game_window(left_pong, right_pong, ball):
    # Dessiner les objets statiques
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, BORDER)
    # Dessiner les objets dynamiques
    pygame.draw.rect(WIN, BLACK, left_pong)
    pygame.draw.rect(WIN, BLACK, right_pong)
    pygame.draw.rect(WIN, BLACK, ball)
    # Ne pas oublier de redessiner notre fenêtre
    pygame.display.update()


def handle_left_pong(left_pong, keys_pressed):
    if keys_pressed[pygame.K_z] and left_pong.y - PONG_VEL > 0:
        left_pong.y -= PONG_VEL
    if keys_pressed[pygame.K_s] and left_pong.y + 80 + PONG_VEL < HEIGHT:
        left_pong.y += PONG_VEL


def handle_right_pong(right_pong, keys_pressed):
    if keys_pressed[pygame.K_UP] and right_pong.y - PONG_VEL > 0:
        right_pong.y -= PONG_VEL
    if keys_pressed[pygame.K_DOWN] and right_pong.y + 80 + PONG_VEL < HEIGHT:
        right_pong.y += PONG_VEL


def handle_ball(left_pong, right_pong, ball, x_increment, y_increment):
    ball.x += x_increment
    ball.y += y_increment
    if left_pong.colliderect(ball) or right_pong.colliderect(ball):
        pygame.event.post(pygame.event.Event(PONG_COLLISION))
    elif ball.y == 0 or ball.y + 15 - HEIGHT > 0:
        pygame.event.post(pygame.event.Event(Y_BORDER_COLLISION))
    elif ball.x < 0:
        pygame.event.post(pygame.event.Event(LEAVE_FIELD_LEFT))
    elif ball.x > WIDTH:
        pygame.event.post(pygame.event.Event(LEAVE_FIELD_RIGHT))


def main():
    left_pong = pygame.Rect(30, HEIGHT / 2 - 40, 15, 80)
    right_pong = pygame.Rect(WIDTH - 30, HEIGHT / 2 - 40, 15, 80)
    ball = pygame.Rect(20, 90, 15, 15)
    score_right_player = 0
    score_left_player = 0
    x_increment = BALL_VEL
    y_increment = BALL_VEL

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == PONG_COLLISION:
                x_increment = -1 * x_increment
            if event.type == Y_BORDER_COLLISION:
                y_increment = -1 * y_increment
            if event.type == LEAVE_FIELD_LEFT:
                score_right_player += 1

            if event.type == LEAVE_FIELD_RIGHT:
                score_left_player += 1

        keys_pressed = pygame.key.get_pressed()

        handle_left_pong(left_pong, keys_pressed)
        handle_right_pong(right_pong, keys_pressed)
        handle_ball(left_pong, right_pong, ball, x_increment, y_increment)
        draw_game_window(left_pong, right_pong, ball)

    pygame.quit()


if __name__ == "__main__":
    main()
