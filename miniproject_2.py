# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math

secret_number = 0
high_range = 100
chances = 0
# helper function to start and restart the game
def new_game():
    global secret_number, high_range, chances
    secret_number = random.randrange(0,high_range)
    chances = int ( math.ceil( math.log(high_range, 2) ) )
    print ''
    print 'New Game'
    print 'The current range is [ 0 -', high_range,')'
    print 'Chances left is ', chances
    
# define event handlers for control panel
def range100():
    global high_range, chances
    high_range = 100
    new_game()
    
def range1000():
    global high_range, chances
    high_range = 1000
    new_game()
    
def input_guess(guess):
    global secret_number, chances
    guess_num = int (guess)
    print 'Guess was',guess_num
    if guess_num == secret_number:
        print "Correct!!"
        new_game()
    else:
        if guess_num > secret_number:
            print "Lower"
        else:
            print 'Higher'
        chances = chances - 1
        if chances == 0:
            print 'Ooops, you used up your chances, you failed to guess the correct number'
            new_game()
        else:
            print 'Chances left is ', chances
            print ''

    
# create frame
frame = simplegui.create_frame('guess game',200,200)

# register event handlers for control elements and start frame
range100 = frame.add_button('Start new game [0,100)', range100, 200)
range1000 = frame.add_button('Start new game [0,1000)', range1000, 200)
guess_number = frame.add_input('guess a number:',input_guess,200)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
frame.start()