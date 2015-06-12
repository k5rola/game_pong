# -*- coding: utf-8 -*-
#........................................................................................................................
# Name: mypong

# Purpose: Rebuild the classic Arcade game Pong

# Author: Karola Klatt

# Created: 2013

# Copyright: Karola Klatt, 2013

# Licence:

#.......................................................................................................................


# Implementation of classic arcade game Pong

# import modules
import pygame
import random

# pygame specific locals/constants
from pygame.locals import *

# some resource related warnings
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')


# pygame needs initialization
pygame.init()

# get Video info
videoinfo = pygame.display.Info()

# # initialize globals - pos and vel encode vertical info for paddles
WIDTH = videoinfo.current_w / 2
HEIGHT = videoinfo.current_h / 2
SIZE = (WIDTH, HEIGHT)
BALL_RADIUS = 20
PAD_WIDTH = 10
PAD_HEIGHT = 90
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [2, 1]
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
running = False

# title of screen
title = 'My Pong!'

# create a canvas
canvas = pygame.display.set_mode((SIZE))
pygame.display.set_caption(title)

# need to create fonts and colour objects in PyGame
fontObj1 = pygame.font.Font(pygame.font.match_font('krungthep'), 40)
fontObj2 = pygame.font.Font(pygame.font.match_font('krungthep'), 16)
fontObj3 = pygame.font.Font(pygame.font.match_font('krungthep'), 12)
ivory = pygame.Color("#eadebd")

# write instructions on canvas
def start_canvas(canvas):
    canvas.fill((0, 0, 0))
    text_headline = fontObj1.render("Pong", True, ivory)
    text_start = fontObj2.render("spacebar -- start game / reset game", True, ivory)
    text_quit = fontObj2.render("q -- quit game", True, ivory)
    text_escape = fontObj2.render("escape -- full screen", False, ivory)
    text_w = fontObj2.render("w -- move left paddle up", True, ivory)
    text_s = fontObj2.render("s -- move left paddle down", True, ivory)
    text_arrow_up = fontObj2.render("arrow up -- move right paddle up", True, ivory)
    text_arrow_down = fontObj2.render("arrow down -- move right paddle down", True, ivory)
    text_copyright = fontObj3.render("copyright Karola Klatt, 2015", True, ivory)

    canvas.blit(text_headline, (50, 10))
    canvas.blit(text_start, (50, 80))
    canvas.blit(text_quit, (50, 120))
    canvas.blit(text_escape, (50, 160))
    canvas.blit(text_w, (50, 200))
    canvas.blit(text_s, (50, 240))
    canvas.blit(text_arrow_up, (50, 280))
    canvas.blit(text_arrow_down, (50, 320))
    canvas.blit(text_copyright, (450, 370))
    pygame.display.update()

# initialize ball position and ball velocity for new ball in middle of canvas
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel  # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]

    # randomise velocity of ball when starting
    if direction == 'right':
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = - random.randrange(1, 3)
    else:
        ball_vel[0] = - random.randrange(2, 4)
        ball_vel[1] = - random.randrange(1, 3)

    return ball_pos, ball_vel

# initialize paddle position in middle of canvas
# initialize scores to 0
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global RIGHT, LEFT  # these are Booleans

    # reset score and paddle position
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    # randomise direction of ball when starting or resetting game
    RIGHT = random.choice([True, False])
    if RIGHT:
        direction = 'right'
    else:
        direction = 'left'
    spawn_ball(direction)


# define event handlers
def draw_handler(canvas):

    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel, ivory

    # clear canvas -- fill canvas with uniform colour, then draw everything below.
    # this removes everything previously drawn and refreshes
    canvas.fill((0, 0, 0))

    # draw dashed mid line
    origin = 0
    dash_length = 10

    for index in range(0, HEIGHT / dash_length, 2):
        start = origin + (index * dash_length)
        end   = origin + ((index + 1) * dash_length)
        pygame.draw.line(canvas, ivory, [WIDTH / 2, start], [WIDTH / 2, end], 2)

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # collide and reflect off of top side
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        ball_vel[0] = ball_vel[0]

    # collide and reflect off of buttom side
    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        ball_vel[0] = ball_vel[0]

    # collide with right paddle causes reflection,
    # collide with right side causes new ball from the middle to upper-left and score increase left
    if (ball_pos[0] >= WIDTH - 1 - PAD_WIDTH - BALL_RADIUS):
        if (paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT):
            ball_vel[0] = -(ball_vel[0] + ball_vel[0] * 10 / 100)
            ball_vel[1] = (ball_vel[1] + ball_vel[1] * 10 / 100)
        else:
            score1 = str(int(score1) + 1)
            spawn_ball('left')

    # collide with left paddle causes reflection,
    # collide with left side causes new ball from the middle to upper-right and score increase left
    if (ball_pos[0] <= 0 + PAD_WIDTH + BALL_RADIUS):
        if (paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT):
            ball_vel[0] = -(ball_vel[0] + ball_vel[0] * 10 / 100)
            ball_vel[1] = (ball_vel[1] + ball_vel[1] * 10 / 100)
        else:
            score2 = str(int(score2) + 1)
            spawn_ball('right')

    # draw ball
    pygame.draw.circle(canvas, ivory, ball_pos, BALL_RADIUS)

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel

    if paddle1_pos + PAD_HEIGHT / 2 >= HEIGHT - 1:
        paddle1_vel = 0
    elif paddle1_pos - PAD_HEIGHT / 2 <= 0:
        paddle1_vel = 0

    paddle2_pos += paddle2_vel

    if paddle2_pos - PAD_HEIGHT / 2 <= 0:
        paddle2_vel = 0
    elif paddle2_pos + PAD_HEIGHT / 2 >= HEIGHT - 1:
        paddle2_vel = 0

    # draw paddles
    pygame.draw.line(canvas, ivory, [0, paddle1_pos + PAD_HEIGHT / 2], [0, paddle1_pos - PAD_HEIGHT / 2], PAD_WIDTH * 2)
    pygame.draw.line(canvas, ivory, [WIDTH, paddle2_pos + PAD_HEIGHT / 2], [WIDTH, paddle2_pos - PAD_HEIGHT / 2], PAD_WIDTH * 2)

    # draw scores
    score_draw = fontObj1.render(str(score1) + "     " + str(score2), True, ivory)
    score_pos = score_draw.get_rect(centerx=canvas.get_width()/2)
    canvas.blit(score_draw, score_pos)

    # update the display
    pygame.display.update()


def keydown_handler(key):
    global paddle1_vel, paddle2_vel, running
    # start and reset game, quit game, move paddles
    if key == pygame.K_SPACE:
        running = True
        new_game()
    elif key == pygame.K_q:
        pygame.quit()
    if key == pygame.K_w:
        paddle1_vel -= 4
    elif key == pygame.K_s:
        paddle1_vel += 4
    elif key == pygame.K_UP:
        paddle2_vel -= 4
    elif key == pygame.K_DOWN:
        paddle2_vel += 4
    elif key == pygame.K_ESCAPE:  # toggle fullscreen mode
        if canvas.get_flags() & FULLSCREEN:
            pygame.display.set_mode(SIZE)
        else:
            pygame.display.set_mode(SIZE, FULLSCREEN)


def keyup_handler(key):
    global paddle1_vel, paddle2_vel
    # stop paddle
    if key == pygame.K_w:
        paddle1_vel = 0
    elif key == pygame.K_s:
        paddle1_vel = 0
    elif key == pygame.K_UP:
        paddle2_vel = 0
    elif key == pygame.K_DOWN:
        paddle2_vel = 0


# call this function to start everything
def main():
    global running

    # create our FPS timer clock
    clock = pygame.time.Clock()


    while not running:
        # call instructions on canvas
        start_canvas(canvas)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keydown_handler(event.key)


# ------------------Frame is now Running-------------------------

    # doing the infinite loop until quit -- the game is running
    while running:

        # event queue iteration
        for event in pygame.event.get():

            # window GUI ('x' the window)
            if event.type == pygame.QUIT:
                running = False

            # input - key event handlers
            elif event.type == pygame.KEYDOWN:
                keydown_handler(event.key)

            elif event.type == pygame.KEYUP:
                keyup_handler(event.key)


        # the call to the draw handler
        draw_handler(canvas)

        # FPS limit to 60 -- essentially, setting the draw handler timing
        # it micro pauses so while loop only runs 60 times a second max.
        clock.tick(60)

# -----------------------------Frame Stops------------------------------------

    # quit game
    pygame.quit ()


# this calls the 'main' function when this script is executed
if __name__ == '__main__': main()