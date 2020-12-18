import pygame
import sys
import random


# stops the floor from running out for continuous movement
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        #flip the pipe if it's a top pipe
        if pipe.bottom >= 1024: #bottom pipe
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) #top pipe
            screen.blit(flip_pipe, pipe)

def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False;
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 2, 1)
    return new_bird

# puts a new rectangle around the bird
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    # text rendering and store on surface and put in rect
    if game_state == 'main_game':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# SOUND
#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 1024)

# GAME
pygame.init()
screen = pygame.display.set_mode((576, 1024))
# clock to control frame rate
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# GAME VARIABLES
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# BACKGROUND
# .convert() helps pygame run the image faster in-game
bg_surface = pygame.image.load('assets/background-day.png').convert()
# scales the background to fit the screen size
bg_surface = pygame.transform.scale2x(bg_surface)

# FLOOR
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# BIRD
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png')).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png')).convert_alpha()
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png')).convert_alpha()
# this is a list containing the different bird surfaces
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))
# we need to cycle through the list at a certain speed
BIRDFLAP = pygame.USEREVENT + 1 # plus 1 to make a diff user event
pygame.time.set_timer(BIRDFLAP, 200)

# PIPES
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# timer
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
#randomized pipe height
pipe_height = [400, 600, 800]

# GAME OVER SCREEN
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288, 512))

# GAME SOUND
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

# GAME LOOP
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # check for player input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 11
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True # game restart
                # empty pipe list when game over
                pipe_list.clear()
                # reset the location of the bird
                bird_rect.center = (100, 512)
                # clear bird movement
                bird_movement = 0
                # reset score
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    # adds background to screen
    screen.blit(bg_surface, (0, 0))

    if game_active:
        # bird movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collisions(pipe_list)

        # pipe movement
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #draw/update score
        score += 0.01
        high_score = update_score(score, high_score)
        score_display('main_game')
        score_sound_countdown -= 1
        if (score_sound_countdown <= 0):
            score_sound.play()
            score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # floor movement
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    # limit frame rate:
    clock.tick(120)
