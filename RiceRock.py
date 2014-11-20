# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
Missiles = set([])
Rocks = set([])
SmallRocks = set([])
shooting = False
count = 0
cycle = 10
started = False

def init():
    global score, lives, shooting, count, started
    for rock in Rocks:
        Rocks.remove(rock)
    for rock in SmallRocks:
        SmallRocks.remove(rock)
    for missile in Missiles:
        Missiles.remove(missile)
    count = 0
    score = 0
    lives = 3
    my_ship.fuel=100
    shooting = False
    started = False
    soundtrack.rewind()
    
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40, 1)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(.5)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.accelarate = 0.2
        self.fraction = 0.01
        self.missile_vel = 7
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.fuel = 100
        
    def draw(self,canvas):
        if self.thrust==False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            #ship_thrust_sound.rewind()
            ship_thrust_sound.pause()
        else:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.play()
            
    def update(self):
        global count, cycle, shooting, started
        if self.thrust==True:
            if(self.fuel>0):
                self.fuel -= 0.2
            else:
                self.thrust=False
            self.vel[0] += math.cos(self.angle)* self.accelarate
            self.vel[1] += math.sin(self.angle)* self.accelarate
        self.vel[0] = self.vel[0] * (1-self.fraction)
        self.vel[1] = self.vel[1] * (1-self.fraction)
        for index in range(2):
            self.pos[index] += self.vel[index]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.angle  += self.angle_vel
        if shooting==True:
            count += 1
            count = count%cycle
            if count==1:
                self.shoot()
        if started:
            self.collide()
       
    def shoot(self):
        vel = [self.vel[0] + math.cos(self.angle)* self.missile_vel, 
                       self.vel[1] + math.sin(self.angle)* self.missile_vel]
        pos = [self.pos[0] + math.cos(self.angle) * self.radius,
               self.pos[1] + math.sin(self.angle) * self.radius ]
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, False, missile_sound)
        Missiles.add(a_missile)
        
    def collide(self):
        global lives, started
        for rock in Rocks:
            if dist(rock.pos, self.pos)<rock.radius+self.radius:
                Rocks.remove(rock)
                lives -= 1
                if lives>0:
                        self.fuel = 100
                else:
                    init()
        for smallRock in SmallRocks:
            if dist(smallRock.pos, self.pos)<smallRock.radius/3+self.radius:
                SmallRocks.remove(smallRock)
                    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, small = False, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        if small:
            self.radius = self.radius * 0.5
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.small = small
        self.exploded = False
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if not self.exploded:
            if self.small:
                drawsize = [ self.image_size[0]*0.3, self.image_size[1]*0.3 ]
                canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, drawsize, self.angle)
            else:
                canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            size = explosion_info.get_size()
            center = explosion_info.get_center()
            life = explosion_info.get_lifespan()
            newCenter =[center[0]+ (life-self.lifespan)*size[0], center[1] ]
            canvas.draw_image(self.image, newCenter, size, self.pos,self.image_size, self.angle)
    
    def update(self):
        global score, lives
        
        if self not in Missiles:
            if self.exploded:
                self.lifespan -= 1
            else:
                for missile in Missiles:
                    distance = dist(self.pos, missile.pos)
                    if distance <= self.radius + missile.radius:
                        explosion_sound.rewind()
                        explosion_sound.play()
                        #generate new small rocks
                        if self not in SmallRocks:
                            score += 2
                            if len(SmallRocks)<10:
                                vel = [random.randrange(-50, 50)*0.01, random.randrange(-50, 50)*0.01]
                                angle_vel = random.randrange(-5, 5) * 0.01
                                SmallRocks.add(Sprite(self.pos, vel, 0, angle_vel, asteroid_image, asteroid_info, True))
                                SmallRocks.add(Sprite(self.pos, [-vel[0], -vel[1]], 0, angle_vel, asteroid_image, asteroid_info, True))
                        else:
                            score += 1
                        if score>50:
                            lives += 1
                            score -= 50
                        Missiles.remove(missile)
                        self.lifespan=24
                        self.exploded = True
                        self.image = explosion_image
            
        for index in range(2):
            self.pos[index] += self.vel[index]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.angle += self.angle_vel
        if self in Missiles and self.lifespan>0:
            self.lifespan -= 0.8

def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()

def draw(canvas):
    global time, life, started
    
    # animiate background
    time += 1
    wtime = (time / 5) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("RiceRocks by Ryan Yao", [630, 580], 15, "white")
    canvas.draw_text("Lives: "+str(lives), [550, 30], 25, "white")
    canvas.draw_text("Score: "+str(score), [650, 30], 25, "red")
    drawFuel(canvas, 80, 50)
    
    # draw ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    if started:
        for rock in SmallRocks:
            rock.update()
            if rock.lifespan<=0:
                  SmallRocks.remove(rock)
            else:
                rock.draw(canvas)  
        for rock in Rocks:
            rock.update()
            if rock.lifespan<=0:
                Rocks.remove(rock)
            else:
                rock.draw(canvas)
          
        for missile in Missiles:
            missile.update()
            if missile.lifespan>0:
                missile.draw(canvas)
            else:
                Missiles.remove(missile)
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())        

def drawFuel(canvas, x, y):
    color = "blue"
    percent = my_ship.fuel
    canvas.draw_text("Fuel", [x-40, y+10], 20, color)
    canvas.draw_polygon([[x, y],[x+percent, y], [x+percent, y+10], [x, y+10]],1, color, color)
    canvas.draw_polygon([[x+percent, y], [x+percent, y+10], [x+100, y+10], [x+100,y]],1, "white", "white")
            
# timer handler that spawns a rock    
def rock_spawner():
    if started and len(Rocks) < 5:
        pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        if dist(pos, my_ship.pos )>100:
            vel = [random.randrange(-200, 200)*0.01, random.randrange(-200, 200)*0.01]
            angle_vel = random.randrange(-10, 10) * 0.01
            Rocks.add(Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info))
        else:
            rock_spawner()
    
    
def keydown(key):
    global shooting, started
    if started:
        if key == simplegui.KEY_MAP['space']:
            shooting=True;
        if key == simplegui.KEY_MAP['up']:
            my_ship.thrust = True
        if key == simplegui.KEY_MAP['left']:
            my_ship.angle_vel = -0.1
        if key == simplegui.KEY_MAP['right']:
            my_ship.angle_vel = 0.1
        
def keyup(key):
    global shooting, count, started
    if key == simplegui.KEY_MAP['space']:
        shooting=False;
        count = 0
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0 

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0.1, 0.1], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()