import pygame
import random
pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load("eisenfunk.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(loops=-1)

pygame.display.set_caption("PONG")

WIDTH = 600
HEIGHT = 400

SCORE_FONT = pygame.font.SysFont('DS-Digital',20)

WIN_FONT = pygame.font.SysFont('DS-Digital',40)

BLACK = (0,0,0)
MATRIX_GREEN = (57, 255, 20)
RED = (255,0,0)
BLUE = (0,0,255)

PADDLE_UNIT_WIDTH = 7
PADDLE_UNIT_HEIGHT = 35
PADDLE_VELOCITY = 15

PADDLE_MID_UNIT_HEIGHT = 5

PADDLE_1_START_X = 0
PADDLE_1_START_Y = (HEIGHT-(2*PADDLE_UNIT_HEIGHT)-(PADDLE_MID_UNIT_HEIGHT))//2

PADDLE_2_START_X = WIDTH - PADDLE_UNIT_WIDTH
PADDLE_2_START_Y = (HEIGHT-(2*PADDLE_UNIT_HEIGHT)-(PADDLE_MID_UNIT_HEIGHT))//2

BALL_WIDTH = 11
BALL_HEIGHT = 11
BALL_VELOCITY = 7

BORDER_THICKNESS = 20

DASH_HEIGHT = 14.4
DASH_THICKNESS = 5
NUMBER_DASHES = 13
DASH_CONSTANT_X = (WIDTH - DASH_THICKNESS)//2

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))

no_collision = True
score_player_1 = 0
score_player_2 = 0

COLLISION_BORDER = pygame.USEREVENT + 1

COLLISION_PADDLE_1_UPPER = pygame.USEREVENT + 2
COLLISION_PADDLE_1_MID = pygame.USEREVENT + 3
COLLISION_PADDLE_1_LOWER = pygame.USEREVENT + 4

COLLISION_PADDLE_2_UPPER = pygame.USEREVENT + 5
COLLISION_PADDLE_2_MID = pygame.USEREVENT + 6
COLLISION_PADDLE_2_LOWER = pygame.USEREVENT + 7

OUT_OF_BOUNDS_1 = pygame.USEREVENT + 8
OUT_OF_BOUNDS_2 = pygame.USEREVENT + 9

def game_over(score_player_1,score_player_2):
    if score_player_1 == 5:
        text_3 = 'PLAYER 2 WINS'
        draw_text_3 = WIN_FONT.render(text_3, 1, MATRIX_GREEN)
        WINDOW.blit(draw_text_3, (((WIDTH//2) - draw_text_3.get_width()) // 2+(WIDTH//2), (HEIGHT-(draw_text_3.get_height()))//2))
        pygame.display.update()
        pygame.time.delay(2000)
        exit()
        pygame.quit()
    elif score_player_2 == 5:
        text_3 = 'PLAYER 1 WINS'
        draw_text_4 = WIN_FONT.render(text_3, 1, MATRIX_GREEN)
        WINDOW.blit(draw_text_4, (((WIDTH//2) - draw_text_4.get_width()) // 2, (HEIGHT-(draw_text_4.get_height()))//2))
        pygame.display.update()
        pygame.time.delay(2000)
        exit()
        pygame.quit()

def handle_out_of_bounds(ball):
    if ball.x < 0:
        pygame.event.post(pygame.event.Event(OUT_OF_BOUNDS_1))
    if ball.x > WIDTH:
        pygame.event.post(pygame.event.Event(OUT_OF_BOUNDS_2))

def handle_ball_collision_with_borders(ball,lower_border,upper_border):
    if ball.colliderect(upper_border):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('wall_1.mp3'))
        pygame.mixer.Channel(1).set_volume(0.25)
        pygame.event.post(pygame.event.Event(COLLISION_BORDER))
    if ball.colliderect(lower_border):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('wall_1.mp3'))
        pygame.mixer.Channel(1).set_volume(0.25)
        pygame.event.post(pygame.event.Event(COLLISION_BORDER))

def handle_ball_collision_with_paddles(ball,paddle_1_upper,paddle_1_mid,paddle_1_lower,paddle_2_upper,paddle_2_mid,paddle_2_lower):

    if ball.colliderect(paddle_1_upper):
        pygame.event.post(pygame.event.Event(COLLISION_PADDLE_1_UPPER))
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('paddle_1.mp3'))
        pygame.mixer.Channel(0).set_volume(0.25)

    if ball.colliderect(paddle_1_mid):
        pygame.event.post(pygame.event.Event(COLLISION_PADDLE_1_MID))
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('paddle_1.mp3'))
        pygame.mixer.Channel(0).set_volume(0.25)

    if ball.colliderect(paddle_1_lower):
        pygame.event.post(pygame.event.Event(COLLISION_PADDLE_1_LOWER))
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('paddle_1.mp3'))
        pygame.mixer.Channel(0).set_volume(0.25)

    if ball.colliderect(paddle_2_upper):
        pygame.event.post(pygame.event.Event(COLLISION_PADDLE_2_UPPER))
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('paddle_1.mp3'))
        pygame.mixer.Channel(0).set_volume(0.25)

    if ball.colliderect(paddle_2_mid):
        pygame.event.post(pygame.event.Event(COLLISION_PADDLE_2_MID))
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('paddle_1.mp3'))
        pygame.mixer.Channel(0).set_volume(0.25)

    if ball.colliderect(paddle_2_lower):
        pygame.event.post(pygame.event.Event(COLLISION_PADDLE_2_LOWER))
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('paddle_1.mp3'))
        pygame.mixer.Channel(0).set_volume(0.25)


def update_window(paddle_1_upper,paddle_1_mid,paddle_1_lower,paddle_2_upper,paddle_2_mid,paddle_2_lower,ball,upper_border,lower_border,dash_array):

    WINDOW.fill((BLACK))

    #PADDLES
    pygame.draw.rect(WINDOW,MATRIX_GREEN,paddle_1_upper)
    pygame.draw.rect(WINDOW, MATRIX_GREEN, paddle_1_mid)
    pygame.draw.rect(WINDOW, MATRIX_GREEN, paddle_1_lower)

    pygame.draw.rect(WINDOW,MATRIX_GREEN,paddle_2_upper)
    pygame.draw.rect(WINDOW, MATRIX_GREEN, paddle_2_mid)
    pygame.draw.rect(WINDOW, MATRIX_GREEN, paddle_2_lower)

    #BALL
    pygame.draw.rect(WINDOW, MATRIX_GREEN, ball)

    #BORDERS
    pygame.draw.rect(WINDOW, MATRIX_GREEN, upper_border)
    pygame.draw.rect(WINDOW, MATRIX_GREEN, lower_border)

    #DASHES
    for element in dash_array:
        pygame.draw.rect(WINDOW,MATRIX_GREEN,element)

    #SCORES
    text_1 = "SCORE: "+ str(score_player_1)
    text_2 = "SCORE: " + str(score_player_2)
    draw_text_1 = SCORE_FONT.render(text_1, 1, MATRIX_GREEN)
    draw_text_2 = SCORE_FONT.render(text_2, 1, MATRIX_GREEN)
    WINDOW.blit(draw_text_1, (((WIDTH//2)-draw_text_1.get_width())//2, 60))
    WINDOW.blit(draw_text_2, ((((WIDTH//2)-draw_text_2.get_width())//2)+(WIDTH//2), 60))

    pygame.display.update()


def main():
    global no_collision
    global score_player_1
    global score_player_2

    ball_start_x = random.choice([0, WIDTH - BALL_WIDTH])
    ball_start_y = random.randint(BORDER_THICKNESS + 1, PADDLE_1_START_Y - 1)

    ball_x_velocity = 0
    ball_y_velocity = 0

    clock = pygame.time.Clock()

    run = True

    dash_array = []

    paddle_1_upper = pygame.Rect(PADDLE_1_START_X,PADDLE_1_START_Y,PADDLE_UNIT_WIDTH,PADDLE_UNIT_HEIGHT)
    paddle_1_mid = pygame.Rect(PADDLE_1_START_X,PADDLE_1_START_Y+PADDLE_UNIT_HEIGHT,PADDLE_UNIT_WIDTH,PADDLE_UNIT_HEIGHT)
    paddle_1_lower = pygame.Rect(PADDLE_1_START_X,PADDLE_1_START_Y+PADDLE_MID_UNIT_HEIGHT+PADDLE_UNIT_HEIGHT,PADDLE_UNIT_WIDTH,PADDLE_UNIT_HEIGHT)

    paddle_2_upper = pygame.Rect(PADDLE_2_START_X,PADDLE_2_START_Y,PADDLE_UNIT_WIDTH,PADDLE_UNIT_HEIGHT)
    paddle_2_mid = pygame.Rect(PADDLE_2_START_X,PADDLE_2_START_Y+PADDLE_UNIT_HEIGHT,PADDLE_UNIT_WIDTH,PADDLE_UNIT_HEIGHT)
    paddle_2_lower = pygame.Rect(PADDLE_2_START_X,PADDLE_2_START_Y+PADDLE_UNIT_HEIGHT+PADDLE_MID_UNIT_HEIGHT,PADDLE_UNIT_WIDTH,PADDLE_UNIT_HEIGHT)

    ball = pygame.Rect(ball_start_x,ball_start_y,BALL_WIDTH,BALL_HEIGHT)

    upper_border = pygame.Rect(0,0,WIDTH,BORDER_THICKNESS)

    lower_border = pygame.Rect(0,HEIGHT-BORDER_THICKNESS,WIDTH,BORDER_THICKNESS)

    for x in range(NUMBER_DASHES):
        y_increment = (x * 2 * DASH_HEIGHT)
        dash_x = DASH_CONSTANT_X
        dash_y = BORDER_THICKNESS + y_increment
        new_rect = pygame.Rect(dash_x,dash_y,DASH_THICKNESS,DASH_HEIGHT)
        dash_array.append(new_rect)

    while run:

        clock.tick(FPS)



        handle_out_of_bounds(ball)
        handle_ball_collision_with_borders(ball,lower_border,upper_border)
        handle_ball_collision_with_paddles(ball,paddle_1_upper,paddle_1_mid,paddle_1_lower,paddle_2_upper,paddle_2_mid,paddle_2_lower)


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == OUT_OF_BOUNDS_1:

                score_player_2 += 1
                pygame.time.delay(1000)
                no_collision = True
                main()

            if event.type == OUT_OF_BOUNDS_2:
                score_player_1 += 1
                pygame.time.delay(1000)
                no_collision = True
                main()

            if event.type == COLLISION_BORDER:
                no_collision = False
                ball_y_velocity = -ball_y_velocity

            if event.type == COLLISION_PADDLE_1_UPPER:
                print("UPPER_1")
                ball_x_velocity = BALL_VELOCITY
                if ball_y_velocity > 0:
                    ball_y_velocity = -BALL_VELOCITY
                elif ball_y_velocity == 0:
                    ball_y_velocity = -BALL_VELOCITY

            if event.type == COLLISION_PADDLE_1_MID:
                print("MID_1")
                ball_x_velocity = BALL_VELOCITY
                ball_y_velocity = 0

            if event.type == COLLISION_PADDLE_1_LOWER:
                print("LOW_1")
                ball_x_velocity = BALL_VELOCITY
                if ball_y_velocity < 0:
                    ball_y_velocity = BALL_VELOCITY
                elif ball_y_velocity == 0:
                    ball_y_velocity = BALL_VELOCITY

            if event.type == COLLISION_PADDLE_2_UPPER:
                print("UPPER_2")
                ball_x_velocity = -BALL_VELOCITY
                if ball_y_velocity > 0:
                    ball_y_velocity = -BALL_VELOCITY
                elif ball_y_velocity == 0:
                    ball_y_velocity = -BALL_VELOCITY

            if event.type == COLLISION_PADDLE_2_MID:
                print("MID_2")

                ball_x_velocity = -BALL_VELOCITY
                ball_y_velocity = 0

            if event.type == COLLISION_PADDLE_2_LOWER:
                print("LOW_2")
                ball_x_velocity = -BALL_VELOCITY
                if ball_y_velocity < 0:
                    ball_y_velocity = BALL_VELOCITY
                elif ball_y_velocity == 0:
                    ball_y_velocity = BALL_VELOCITY

        # INPUT BUTTON PRESSES

        keys_pressed = pygame.key.get_pressed()
        # userInput = pygame.mouse.get_pressed(num_buttons=3)

        if keys_pressed[pygame.K_w]:
            if paddle_1_upper.y > BORDER_THICKNESS:
                paddle_1_upper.y -= PADDLE_VELOCITY
                paddle_1_mid.y -= PADDLE_VELOCITY
                paddle_1_lower.y -= PADDLE_VELOCITY

        if keys_pressed[pygame.K_s]:
            if paddle_1_lower.y+PADDLE_UNIT_HEIGHT < HEIGHT-BORDER_THICKNESS:
                paddle_1_upper.y += PADDLE_VELOCITY
                paddle_1_mid.y += PADDLE_VELOCITY
                paddle_1_lower.y += PADDLE_VELOCITY

        # if userInput[0]:
        #     if paddle_2_upper.y > BORDER_THICKNESS:
        #         paddle_2_upper.y -= PADDLE_VELOCITY
        #         paddle_2_mid.y -= PADDLE_VELOCITY
        #         paddle_2_lower.y -= PADDLE_VELOCITY
        #
        # if userInput[2]:
        #     if paddle_2_lower.y + PADDLE_UNIT_HEIGHT < HEIGHT - BORDER_THICKNESS:
        #         paddle_2_upper.y += PADDLE_VELOCITY
        #         paddle_2_mid.y += PADDLE_VELOCITY
        #         paddle_2_lower.y += PADDLE_VELOCITY

        if keys_pressed[pygame.K_UP]:
            if paddle_2_upper.y > BORDER_THICKNESS:
                paddle_2_upper.y -= PADDLE_VELOCITY
                paddle_2_mid.y -= PADDLE_VELOCITY
                paddle_2_lower.y -= PADDLE_VELOCITY

        if keys_pressed[pygame.K_DOWN]:
            if paddle_2_lower.y+PADDLE_UNIT_HEIGHT < HEIGHT-BORDER_THICKNESS :
                paddle_2_upper.y += PADDLE_VELOCITY
                paddle_2_mid.y += PADDLE_VELOCITY
                paddle_2_lower.y += PADDLE_VELOCITY

        # movement at game start:

        if no_collision == True:

            ball_y_velocity = BALL_VELOCITY
            if ball_start_x == 0:
                ball_x_velocity = BALL_VELOCITY
            else:
                ball_x_velocity = -BALL_VELOCITY

        # update ball position

        ball.x += ball_x_velocity
        ball.y += ball_y_velocity

        update_window(paddle_1_upper,paddle_1_mid,paddle_1_lower,paddle_2_upper,paddle_2_mid,paddle_2_lower,ball,upper_border,lower_border,dash_array)
        game_over(score_player_2, score_player_1)

    exit()
    pygame.quit()

main()