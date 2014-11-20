# implementation of card game - Memory

import simplegui
import random

lst = []
exposed = []
clickNum = 0
LEN = 800
HEI = 100
totalPair = 0
# helper function to initialize globals
def new_game():
    global lst, totalPair, clickNum
    lst = range(0,8)
    lst2 = range(0,8)
    lst.extend(lst2)
    random.shuffle(lst)
    del exposed[:]
    totalPair = 0
    clickNum = 0
    label.set_text("Turns = 0")

     
# define event handlers
def mouseclick(pos):
    global LEN, lst, clickNum, totalPair
    index = pos[0]/(LEN/len(lst))
    if (index not in exposed):
        exposed.append(index)
        if clickNum==0:
            clickNum=1
        elif (clickNum==1):
            totalPair +=1
            label.set_text("Turns = "+str(totalPair))
            clickNum=2
        elif (clickNum==2):
            if(lst[exposed[-2]]!=lst[exposed[-3]]):
                exposed.pop(-2)
                exposed.pop(-2)
            clickNum=1
                         
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global lst
    for i in range(len(lst)):
        start=LEN/len(lst)*i;
        end = LEN/len(lst)*(i+1)
        if i not in exposed:
            canvas.draw_polygon([(start,0),(end,0),(end, HEI),(start,HEI)],1, "black","green")
        else:
            canvas.draw_text(str(lst[i]), [LEN/len(lst)*(i+0.2),HEI/2+15], 50, "white")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
