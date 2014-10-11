# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel  = [0, 0]
ball_radius = 20
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
score1 = 0
score2 = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    velocity_h = random.randrange(120, 240)/60
    velocity_v = -random.randrange(60, 80)/60
    if direction:
        ball_vel = [velocity_h,velocity_v]
    else:
        ball_vel  = [-velocity_h,velocity_v]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    lr = random.randrange(0,2)
    if lr==0:
        spawn_ball(False)
    else:
        spawn_ball(True)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global HALF_PAD_HEIGHT
    global paddle1_vel, paddle2_vel
    global score
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    if ball_pos[1] <= ball_radius:
        ball_vel[1] *= -1
    if ball_pos[1] >= HEIGHT - ball_radius:
        ball_vel[1] *= -1
    
    if ball_pos[0] <= PAD_WIDTH + ball_radius:
        if ball_pos[1]>= paddle1_pos-HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos+HALF_PAD_HEIGHT:
            ball_vel[0] *= -1.1
        else:
            score2 += 1
            spawn_ball(True)
    if ball_pos[0] >= WIDTH - PAD_WIDTH - ball_radius:
        if ball_pos[1]>= paddle2_pos-HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos+HALF_PAD_HEIGHT:
            ball_vel[0] *= -1.1
        else:
            score1 += 1
            spawn_ball(False)
    # draw ball
    canvas.draw_circle(ball_pos, ball_radius,2, "white","white")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    if paddle1_pos >= HEIGHT-PAD_HEIGHT/2:
        paddle1_pos = HEIGHT-PAD_HEIGHT/2
        paddle1_vel = 0
    if paddle2_pos >= HEIGHT-PAD_HEIGHT/2:
        paddle2_pos = HEIGHT-PAD_HEIGHT/2
        paddle2_vel = 0
    if paddle1_pos <= PAD_HEIGHT/2:
        paddle1_pos = PAD_HEIGHT/2
        paddle1_vel = 0
    if paddle2_pos <= PAD_HEIGHT/2:
        paddle2_pos = PAD_HEIGHT/2
        paddle2_vel = 0
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos-HALF_PAD_HEIGHT], 
                         [0, paddle1_pos+HALF_PAD_HEIGHT],
                         [PAD_WIDTH, paddle1_pos+HALF_PAD_HEIGHT], 
                         [PAD_WIDTH, paddle1_pos-HALF_PAD_HEIGHT]],
                        1, 'white', "white")
    canvas.draw_polygon([[WIDTH-PAD_WIDTH, paddle2_pos-HALF_PAD_HEIGHT], 
                         [WIDTH-PAD_WIDTH, paddle2_pos+HALF_PAD_HEIGHT],
                         [WIDTH, paddle2_pos+HALF_PAD_HEIGHT], 
                         [WIDTH, paddle2_pos-HALF_PAD_HEIGHT]],
                        1, 'white', "white")
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/2-150, 100], 40, "yellow")
    canvas.draw_text(str(score2), [WIDTH/2+150, 100], 40, "yellow")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    speed = 1
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= speed
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += speed
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= speed
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel += speed
        
def keyup(key):
    global paddle1_vel, paddle2_vel

def restart():
    global score1, score2
    score1 = score2 = 0
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
restart = frame.add_button("restart", restart, 200)

# start frame
new_game()
frame.start()