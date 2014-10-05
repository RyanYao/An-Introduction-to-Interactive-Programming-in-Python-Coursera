import simplegui

# define global variables
count = 0
success = 0
attempts = 0
running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    #time in the format of a:bc.d
    d = t%10
    c = (t/10)%10
    b = (t/100)%6
    a = t/600
    return str(a)+":"+str(b)+str(c)+"."+str(d)

def success_rate():
    global success
    global attempts
    return str(success)+"/"+str(attempts)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    global running
    timer.start()
    running = True
  
def stop_timer():
    timer.stop()
    global count, success, attempts, running
    if running:
        timer.stop()
        attempts += 1
        if count%10==0:
            success += 1
    running = False
    
def reset_timer():
    global count, success, attempts, running
    timer.stop()
    count = success = attempts = 0
    running = False

# define event handler for timer with 0.1 sec interval
def increase_count():
    global count
    count += 1

# define draw handler
def draw_time(canvas):
    global count
    canvas.draw_text(format(count), (80, 100), 24, "white")
    canvas.draw_text(success_rate(),(150,30), 24, "yellow")
    
# create frame
frame = simplegui.create_frame("stop watch", 200, 200)

# register event handlers
frame.set_draw_handler(draw_time)
timer = simplegui.create_timer(100,increase_count)
start = frame.add_button("start",start_timer, 100)
stop = frame.add_button("stop", stop_timer, 100)
reset = frame.add_button("reset", reset_timer, 100)
# start frame
frame.start()

# Please remember to review the grading rubric
