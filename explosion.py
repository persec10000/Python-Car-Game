#!/usr/bin/env python

from __future__ import division
import pygame
import random
from os import path

## assets folder
img_dir = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')

###############################
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
###############################

###############################
## to placed in "__init__.py" later
## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()     ## For syncing the FPS
background = pygame.image.load(path.join(img_dir, 'background - Copy.png'))
background = pygame.transform.scale(background, (WIDTH * 3, HEIGHT * 3))

background_rect = background.get_rect()
bg_x = -100 #-(int(kwargs['startX'])) #100 center
bg_y = -100 #-(int(kwargs['startY'])) #100 center
screen.blit(background, (bg_x,bg_y) )
###############################

font_name = pygame.font.match_font('arial')


def newmob(x,y):
    #print ("---newmob_x,y:(" + str(bg_x) + ":" + str(bg_y))
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## scale the player img down
        #self.image = pygame.transform.scale(player_img, (50, 38))
        self.image = pygame.transform.scale(player_img, (25, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT/2 - 10
        self.speedx = 0 
        self.speedy = 0 
        self.shield = 1 #100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        ## unhide 
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT / 2 - 10

        self.speedx = 0     ## makes the player static in the screen by default. 
        self.speedy = 0     ## makes the player static in the screen by default. 
        # then we have to check whether there is an event hanlding being done for the arrow keys being 
        ## pressed 

        ## will give back a list of the keys which happen to be pressed down at that moment
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -15
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 15

        if keystate[pygame.K_UP]:
            self.speedy = -15
        elif keystate[pygame.K_DOWN]:
            self.speedy = 15

        #Fire weapons by holding spacebar
        if keystate[pygame.K_SPACE]:
            if self.hidden == False:
                self.shoot()

        ## check for the borders at the left and right
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        #self.rect.x += self.speedx
        #self.rect.y += self.speedy

    def shoot(self):
        ## to tell the bullet where to spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shooting_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


# defines the enemies
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        #print ("---newmob_x,y:(" + str(bg_x) + ":" + str(bg_y))
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)

        if bg_x < -940:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width + (940+bg_x) )
            print ("===-940:"+ str(WIDTH - self.rect.width + (940+bg_x)))
        elif bg_x > 70:
            self.rect.x = random.randrange(0  + (220-bg_x), WIDTH - self.rect.width )
        else:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            print ("===norm:" + str(WIDTH - self.rect.width))
        #self.rect.x = random.randrange(0, WIDTH - self.rect.width) / 2
        self.rect.y = random.randrange(-150, -100) / 2

        print ("##Mob x:y:" + str(self.rect.x) + ":" + str(self.rect.y) + ":")
        self.speedy = random.randrange(1, 3)        ## for randomizing the speed of the Mob

        ## randomize the movements a little more 
        self.speedx = 0 #random.randrange(-3, 3)

        ## adding rotation to the mob element
        self.rotation = 0
        self.rotation_speed = random.randrange(-4, 4)
        self.last_update = pygame.time.get_ticks()  ## time when the rotation has to happen
        
    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # in milliseconds
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        print ("---newmob_x,y:(" + str(bg_x) + ":" + str(bg_y))
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        ## now what if the mob element goes out of the screen
# -1180,-1500
# 220,-1500
# 220,230
# -1180,230
        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            if bg_x < -940:
                self.rect.x = random.randrange(0, WIDTH - self.rect.width + (940+bg_x) )
                print ("===-940:"+ str(WIDTH - self.rect.width + (940+bg_x)))
            elif bg_x > 70:
                self.rect.x = random.randrange(0 , WIDTH - self.rect.width ) + WIDTH / 2 - (220-bg_x)
            else:
                self.rect.x = random.randrange(0, WIDTH - self.rect.width)
                print ("===norm:" + str(WIDTH - self.rect.width))

            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)        ## for randomizing the speed of the Mob

        

        keys = pygame.key.get_pressed() 
        vel = 10
        if keys[pygame.K_LEFT] :
            self.rect.x += vel      

        if keys[pygame.K_RIGHT]: 
            self.rect.x -= vel         

        if keys[pygame.K_UP]:
            self.rect.y += vel

        if keys[pygame.K_DOWN]:
            self.rect.y -= vel

        # if self.rect.right > WIDTH:
        #     self.rect.right = WIDTH
        # if self.rect.left < 0:
        #     self.rect.left = 0



## defines the sprite for bullets
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ## place the bullet according to the current position of the player
        self.rect.bottom = y 
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """should spawn right in front of the player"""
        self.rect.y += self.speedy
        ## kill the sprite after it moves over the top border
        if self.rect.bottom < 0:
            self.kill()

        ## now we need a way to shoot
        ## lets bind it to "spacebar".
        ## adding an event for it in Game loop

###################################################
## Load all game images

## ^^ draw this rect first 

#player_img = pygame.image.load(path.join(img_dir, 'car.png')).convert()
#player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_img = pygame.image.load(path.join(img_dir, 'car3.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (20, 40))


player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'bullet.png')).convert()


meteor_images = []
meteor_list = [
    'Enemy/0.png',
    'Enemy/1.png', 
    'Enemy/2.png', 
    'Enemy/3.png',
    'Enemy/4.png',

]

for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, image)).convert())

## meteor explosion
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(10):
    filename = 'Blood/{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    ## resize the explosion
    img_lg = pygame.transform.scale(img, (25, 25))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
for i in range(14):
    ## player explosion
    if i < 9:
        filename = 'explosion/green_blob_explosion_01_00{}.png'.format(i+1)
    else:
        filename = 'explosion/green_blob_explosion_01_0{}.png'.format(i+1)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)



###################################################
### Load all game sounds
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))
## main background music
pygame.mixer.music.load(path.join(sound_folder, 'Background music.mp3'))
pygame.mixer.music.play(-1)     ## makes the gameplay sound in an endless loop
pygame.mixer.music.set_volume(1.0)      ## simmered the sound down a little

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))
###################################################

## TODO: make the game music loop over again and again. play(loops=-1) is not working
# Error : 
# TypeError: play() takes no keyword arguments
#pygame.mixer.music.play()

#############################
## Game loop
running = True
menu_display = True
while running:
    if menu_display:
        menu_display = False
        
        ## group all the sprites together for ease of update
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        ## spawn a group of mob
        mobs = pygame.sprite.Group()
        for i in range(8):      ## 8 mobs
            # mob_element = Mob()
            # all_sprites.add(mob_element)
            # mobs.add(mob_element)
            newmob(bg_x,bg_y)

        ## group for bullets
        bullets = pygame.sprite.Group()

    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False

        ## Press ESC to exit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #2 Update
    all_sprites.update()


    ## check if a bullet hit a mob
    ## now we have a group of bullets and a group of mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    ## now as we delete the mob element when we hit one with a bullet, we need to respawn them again
    ## as there will be no mob_elements left out 
    for hit in hits:
        random.choice(expl_sounds).play()
        # m = Mob()
        # all_sprites.add(m)
        # mobs.add(m)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)

        newmob(bg_x,bg_y)        ## spawn a new mob

    ## ^^ the above loop will create the amount of mob objects which were killed spawn again
    #########################

    ## check if the player collides with the mob
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)        ## gives back a list, True makes the mob element disappear
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob(bg_x,bg_y)
        if player.shield <= 0: 
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.shield = 1

    keys = pygame.key.get_pressed() 
    vel = 10
    if keys[pygame.K_LEFT] :
        if bg_x < WIDTH / 2 - 25:
            bg_x += vel      
        else:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.shield = 1
        print ("bg_x,y:(" + str(bg_x) + ":" + str(bg_y))

    if keys[pygame.K_RIGHT]:
        if bg_x > -WIDTH * 2 - WIDTH / 2 + 25: 
            bg_x -= vel         
        else :
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.shield = 1

        print ("bg_x,y:(" + str(bg_x) + ":" + str(bg_y))

    if keys[pygame.K_UP] : 
        if bg_y < HEIGHT / 2 - 75:
            bg_y += vel
        else:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.shield = 1
        print ("bg_x,y:(" + str(bg_x) + ":" + str(bg_y))

    if keys[pygame.K_DOWN] : 
        if bg_y > -HEIGHT * 2 - HEIGHT / 2 + 5:
            bg_y -= vel
        else:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.shield = 1
        print ("bg_x,y:(" + str(bg_x) + ":" + str(bg_y))

    screen.fill((0,0,0))
    screen.blit(background, (bg_x,bg_y))
    
    
    # screen.blit(car, (int(kwargs['width']) / 2 - 25, int(kwargs['height']) / 2 - 15))
    # pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height)) 
    # pygame.display.flip()


    #3 Draw/render
    # screen.fill(BLACK)
    # screen.blit(background, background_rect)
    # screen.blit(background, ( player.rect.x,player.rect.y ))
    #print ("player_x,y:(" + str(player.rect.x) + ":" + str(player.rect.y))
    # screen.blit(car, (int(kwargs['width']) / 2 - 25, int(kwargs['height']) / 2 - 15))
    all_sprites.draw(screen)

    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.quit()
