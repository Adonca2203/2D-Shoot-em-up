#Importing libraries
import pygame
import random
import sys
import time
from os import path
import datetime
import math

# Select path for external files (IMG & Sound)
img_dir = path.join(path.dirname(__file__), "images")

#Variables for screen
WIDTH = 480
HEIGHT = 600
FPS = 60

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#Pygame Initializations
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adonis' Shoot 'em Up")
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("Comic-Sans", 75)
sfont = pygame.font.SysFont("Comic-Sans", 30)

#Draw the player lives within the given parameters
def draw_lives(surf, x, y, lives, img):

    for i in range(lives):

        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

#Draw Boss' HP within the given parameters
#(I will give surface, location on x and y, the current health, and original health num)
def draw_health(surf, x, y, pct, o_life):

    #In case their health reaches a number lower than 0 for whatever reason
    if pct < 0:

        pct = 0

    BAR_LENGTH = o_life
    BAR_HEIGHT = 10

    color = []
    color.append(GREEN) # 0
    color.append(YELLOW) # 1
    color.append(RED) # 2


    fill = (pct / o_life) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)

    if fill <= o_life:

        c = 0
        pygame.draw.rect(surf, color[c], fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    if fill <= o_life / 2:

        c = 1
        pygame.draw.rect(surf, color[c], fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    if fill <= o_life * (1/4):

        c = 2
        pygame.draw.rect(surf, color[c], fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    if fill == 0:

        pygame.draw.rect(surf, BLACK, fill_rect)
        pygame.draw.rect(surf, BLACK, outline_rect, 2)

#The Player class and attributes
class Player(pygame.sprite.Sprite):

    def __init__(self):

        #Set the image to be used and original position for the Player class
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pimg, (47, 60))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        
    def update(self):

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        #Sets the speed of the Player class
        self.speedx = 0
        #self.speedy = 0

        #Takes key presses as inputs to alter player speed/movements
        keystate = pygame.key.get_pressed()

        #if keystate[pygame.K_UP] or keystate[pygame.K_w]:

        #    self.speedy = 5

        #if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:

        #    self.speedy = -5

        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:

            self.speedx = 5

        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:

            self.speedx = -5

        self.rect.x -= self.speedx

        #Keeps Player class from going off the screen
        if self.rect.right > WIDTH:

            if not self.hidden:

                self.rect.right = WIDTH

        if self.rect.left < 0:

            if not self.hidden:

                self.rect.left = 0

    #The shoot function for the Player class
    def shoot(self):

        #Use instance of the Bullet class and add it onto the screen
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def hide(self):

        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH + 700, HEIGHT + 700)

#Enemies class for enemy Mobs
class Mob(pygame.sprite.Sprite):

    def __init__(self):

        #Starting position of mobs chosen at random
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mimg, (30, 40))
        self.img_copy = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 10)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    #def rotate(self):

    #    now = pygame.time.get_ticks()

     #   if now - self.last_update > 50:

      #      self.last_update = now
      #      self.rot = (self.rot + self.rot_speed) % 360

       #     new_image = pygame.transform.rotate(self.image, self.rot)
        #    old_center = self.rect.center
        #    self.image = new_image
       #     self.rect = self.image.get_rect()
         #   self.rect.center = old_center

    def update(self):

        #self.rotate()
        #Move the Mobs class along the x and y plane using their randomly generated speeds
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        #If they go off screen respawn them at the top
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:

            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)

#Bullet class for the Player class to use
class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):

        #Starting position of the bullet
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(missileimg, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -5

    def update(self):

        #Travel along the y axis from whatever x you were shot from
        self.rect.y += self.speedy

        #If you leave the screen kill the sprite
        if self.rect.bottom < 0:

            self.kill()


#The class for the first boss (Boss1) and its attributes
class Boss1(pygame.sprite.Sprite):

    def __init__(self):

        #Set intial position of the boss (outside the screen)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss1img, (130, 150))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.x = WIDTH/3
        self.rect.y = -200
        self.speedy = 1
        self.speedx = 5
        self.health = 25
        self.o_life = 25

    def update(self):
        
        #Move along the y axis (Traverse into the screen)
        self.rect.y += self.speedy

        #Once you reach 1/4th of the screen stop moving along the y axis
        if self.rect.bottom >= HEIGHT * (1/4):

            self.speedy = 0
            self.rect.bottom = HEIGHT * (1/4)

            #Traverse the x axis at a speed of speedx attributes
            self.rect.x += self.speedx

            #Boss attack the player while he is within 30 pixels of the player's current location
            if player.rect.x - 15 <= self.rect.x <= player.rect.x + 15:

                self.shoot()

            #If you reach the edge of the screen move the other way
            if self.rect.right == WIDTH:
                self.speedx = -5

            if self.rect.left == 0:
                self.speedx = 5
            
            #Stay withing the bounds of the screen (extra measure)
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH

            if self.rect.left < 0:
                self.rect.left = 0

    #First boss' attack function
    def shoot(self):

        #Invoke the attack class and add it onto the screen
        b1attack = B1Attack(self.rect.centerx, self.rect.bottom)
        all_sprites.add(player)
        eattack.add(b1attack)
        all_sprites.add(b1attack)

#The class for the second boss and its attributes
class Boss2(pygame.sprite.Sprite):

    def __init__(self):

        #Aspects for the boss and his image
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss2img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.x = WIDTH + 200
        self.rect.y = 10
        self.speedy = 1
        self.speedx = -5
        self.health = 50
        self.o_life = 50

    def update(self):

        #The boss' movements
        self.rect.x += self.speedx

        if self.rect.left == 0:

            self.speedx = 10

        if self.rect.right == WIDTH:

            self.speedx = -10

        if player.rect.x - 15 <= self.rect.x <= player.rect.x + 15:

            self.shoot()

    #The boss' attack
    def shoot(self):

        b2attack = B2Attack(self.rect.centerx, self.rect.bottom)
        all_sprites.add(player)
        eattack.add(b2attack)
        all_sprites.add(b2attack)

#The class for the third boss and its attributes
class Boss3(pygame.sprite.Sprite):

    def __init__(self):

        #Aspects of the boss and its appearance
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss3img, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.x = 0
        self.rect.y = -300
        self.speedx = 10
        self.speedy = 10
        self.health = 75
        self.o_life = 75

    def update(self):

        #The boss' movements
        self.rect.y += self.speedy

        if self.rect.y >= HEIGHT * (1/10):

            self.rect.y = HEIGHT * (1/10)

            self.rect.x += self.speedx

            if self.rect.right >= WIDTH:

                self.speedx = (self.speedx * -1)

            if self.rect.left <= 0:

                self.speedx = (self.speedx * -1)

#First boss' attack class
class B1Attack(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = pygame.transform.scale(b1aimg[self.index], (30, 40))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
        self.imgflip = 0

    def update(self):

        #Move the attack down the y axis at a speed of 10
        self.rect.y += self.speedy
        self.index += self.imgflip

        #Kill the sprite if it goes out of screen
        if self.rect.bottom > HEIGHT:

            self.kill()


#The second boss' attack class
class B2Attack(pygame.sprite.Sprite):

    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(b2aimg, (30, 40))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):

        #Move the attack down the y axis at a speed of 10
        self.rect.y += self.speedy

        #Kill the sprite if it goes out of screen
        if self.rect.bottom > HEIGHT:

            self.kill()

#Attaching images to keywords to use for sprites
pimg = pygame.image.load(path.join(img_dir, "Main_Char8-bit.png"))
mini_pimg = pygame.transform.scale(pimg, (25, 20))
missileimg = pygame.image.load(path.join(img_dir, "missile8-bit.png"))
boss1img = pygame.image.load(path.join(img_dir, "Boss1-8Bit.png"))
boss2img = pygame.image.load(path.join(img_dir, "b2-8bit.png"))
boss3img = pygame.image.load(path.join(img_dir, "boss3-8bit.png"))

#Creating arrays to use for animated images
b1aimg = []
b1aimg.append(pygame.image.load(path.join(img_dir, "egg-8bit.png")))
b1aimg.append(pygame.image.load(path.join(img_dir, "CrackedEgg-8Bit.png")))
b2aimg = pygame.image.load(path.join(img_dir, "glove-8bit.png"))

mimg = (pygame.image.load(path.join(img_dir, "asteroid.png")))

#Create groups of sprites for later use
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
boss1s = pygame.sprite.Group()
boss2s = pygame.sprite.Group()
boss3s = pygame.sprite.Group()
eattack = pygame.sprite.Group()

#Create instances of the classes
player = Player()
boss1 = Boss1()
boss2 = Boss2()
boss3 = Boss3()

#Add the classes into the sprites groups
all_sprites.add(player)
boss1s.add(boss1)
boss2s.add(boss2)
boss3s.add(boss3)

#Add 8 mob sprites
for i in range(8):

    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#Setting variables to use with the program
running = True
score = 0

#Main program / Game loop
while running:

    #Set the refresh rate [Frames Per Second (FPS)]
    clock.tick(FPS)

    #Events for the computer to detect and how to handle them
    for event in pygame.event.get():

        #If the player quits the screen close the window and leave the main game loop
        if event.type == pygame.QUIT:

            running = False

        #Key events to expect
        elif event.type == pygame.KEYDOWN:

            #If the player hits the space bar, invoke the shoot funtion inside the player
            if event.key == pygame.K_SPACE:

                player.shoot()

    #Invoke the update function within the all_sprites sprite group
    all_sprites.update()

    #Variable to hold the number of collisions between the bullets sprite group
    #And the mobs sprite group
    mhits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for hit in mhits:

        #Increase the score by 1 per kill and re-add a mob onto the screen per 
        #Mob killed
        score += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    #Create a variable to hold the number of collisions between the bosses and 
    #Bullets group
    b1hits = pygame.sprite.groupcollide(boss1s, bullets, False, True)

    #For every hit a boss receives (Collision between bullet and boss)
    #Reduce health attribute of boss by 1
    for hits in b1hits:

        boss1.health -= 1

        if boss1.health == 0:

            score += 20

            boss1.kill()
            b1dead = pygame.time.get_ticks()

    b2hits = pygame.sprite.groupcollide(boss2s, bullets, False, True)

    for hits in b2hits:

        boss2.health -= 1

        if boss2.health == 0:

            score += 30
            boss2.kill()
            b2dead = pygame.time.get_ticks()

    b3hits = pygame.sprite.groupcollide(boss3s, bullets, False, True)

    for hits in b3hits:

        boss3.health -= 1

        if boss3.health == 0:

            score += 40
            boss3.kill()
            b3dead = pygame.time.get_ticks()

    #if 5 seconds pass, add the first boss onto the screen
    if pygame.time.get_ticks() >= 5000 and boss1.health > 0:

        all_sprites.add(boss1)

    #If the first boss is dead and it has been more than 5 seconds have passed,
    #add the second boss onto the screen, etc...
    if boss1.health == 0 and pygame.time.get_ticks() - b1dead >= 5000 and boss2.health > 0:

        all_sprites.add(boss2)

    if boss2.health == 0 and pygame.time.get_ticks() - b2dead >= 5000 and boss2.health > 0:

        all_sprites.add(boss3)

    #Variables holding the times the player gets hit
    hits = pygame.sprite.spritecollide(player, mobs, False)
    phit = pygame.sprite.spritecollide(player, eattack, False)

    #If the player is hit, drop their health by 1
    if hits or phit:

        player.lives -= 1

        if player.lives > 0:

            player.hide()

        if player.lives == 0:

            red_over = myfont.render("GAME OVER!", 1, RED)
            black_over = myfont.render("GAMER OVER!", 1, BLACK)

            for i in range(3):
            
                screen.fill(RED)
                screen.blit(black_over, ((WIDTH/6), (HEIGHT/2)))
                pygame.display.flip()
                time.sleep(.100)
                screen.fill(BLACK)
                screen.blit(red_over, ((WIDTH/6), (HEIGHT/2)))
                pygame.display.flip()
                time.sleep(.100)

            running = False

    #Fill the background of the screen
    screen.fill(BLACK)
    points = sfont.render("Score: " + str(score), 1, WHITE)

    screen.blit(points, (10, 7))

    #Draw boss health
    draw_health(screen, boss1.rect.centerx - 5, boss1.rect.bottom, boss1.health, boss1.o_life)
    draw_health(screen, boss2.rect.left + 25, boss2.rect.bottom, boss2.health, boss2.o_life)
    draw_health(screen, boss3.rect.left + 40, boss3.rect.bottom, boss3.health, boss3.o_life)

    #Draw the player lives
    draw_lives(screen, (WIDTH - 100), 5,player.lives,mini_pimg)

    #Draw all sprites onto the screen
    all_sprites.draw(screen)
    pygame.display.flip()

#When the main game loop stops running, exit the program
sys.exit()
