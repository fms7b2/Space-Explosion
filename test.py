# Initialize
import math
import pygame
import random
import os
from pygame import font

from pygame.sprite import spritecollide

pygame.init()

screen = pygame.display.set_mode((1500,800))
pygame.display.update()
clock = pygame.time.Clock()

# Game Variables
SPACESHIP_SPEED = 0.5
SPACESHIP_SIZE = 150
GOODIE_SPEED = 3
ASTEROID_SPEED = 6
ASTEROID_INTERVAL = 50
GOODIE_INTERVAL = 900

screen_width = 1500
screen_length = 800

bg_surface = pygame.image.load('Assets/spacebackground.png').convert()
bg_surface = pygame.transform.scale(bg_surface,(screen_width,screen_length))
floor_x_pos = 0

spaceship_surface = pygame.image.load('Assets/spaceship2.png').convert_alpha()
spaceship_surface = pygame.transform.scale(spaceship_surface,(SPACESHIP_SIZE,SPACESHIP_SIZE))
spaceship_rect = spaceship_surface.get_rect()

explosion_surface = pygame.image.load('Assets/explosion.png').convert_alpha()
explosion_surface = pygame.transform.scale(explosion_surface,(400,400))
explosion_rect = explosion_surface.get_rect()

goodie_surface = pygame.image.load('Assets/astroboy.png').convert_alpha()
goodie_surface = pygame.transform.scale(goodie_surface,(70,70))
goodie_rect = goodie_surface.get_rect()

moon_surface = pygame.image.load('Assets/moon.png')
moon_surface = pygame.transform.scale(moon_surface,(400,400))
moon_x_pos = 0

HEART_SIZE = 80
heart1 = pygame.transform.scale(pygame.image.load('Assets/heart.png'),(HEART_SIZE,HEART_SIZE))
heart2 = pygame.transform.scale(pygame.image.load('Assets/heart.png'),(HEART_SIZE,HEART_SIZE))
heart3 = pygame.transform.scale(pygame.image.load('Assets/heart.png'),(HEART_SIZE,HEART_SIZE))

spaceship_x_pos = 0
spaceship_y_pos = 0

asteroid_surface = pygame.image.load('Assets/asteroid5.png').convert_alpha()
asteroid_surface = pygame.transform.scale(asteroid_surface,(90,90))

explosion_sound = pygame.mixer.Sound('Sound/explosionsound.mp3')
astronautsave_sound = pygame.mixer.Sound('Sound/woo.mp3')

asteroid_list = []
SPAWNASTEROID = pygame.USEREVENT
pygame.time.set_timer(SPAWNASTEROID,ASTEROID_INTERVAL)

goodie_list = []
SPAWNGOODIE = pygame.USEREVENT
pygame.time.set_timer(SPAWNGOODIE,GOODIE_INTERVAL)

game_active = True
game_font = pygame.font.Font('Assets/starfont.ttf',50)
transparent = (0, 0, 0, 0)
pygame.display.set_caption('Tiger Space')

# Functions
def update_hearts(player):
    if player.health == 3:
        # Do nothing
        screen.blit(heart1,(35,120))
        screen.blit(heart2,(55,120))
        screen.blit(heart3,(75,120))
    elif player.health == 2:
        screen.blit(heart2,(35,120))
        screen.blit(heart3,(55,120))
    elif player.health == 1:
        screen.blit(heart3,(35,120))

def show_text(msg,color):
    x = 550
    y = 100
    text = game_font.render(msg,True,color)
    screen.blit(text, (x,y))

def score_display(player):
    x = 500
    y = 100
    score_surface = game_font.render(str(player.score),True,(255,255,255))
    screen.blit(score_surface,(50,50))

def draw_floor():
    screen.blit(bg_surface,(floor_x_pos,0))
    screen.blit(bg_surface,(floor_x_pos+screen_width,0))
    
    screen.blit(moon_surface,(moon_x_pos,0))
    screen.blit(moon_surface,(moon_x_pos+screen_width,0))

# Goodie Functions

def check_goodiecollision(goodies,player):
    for index, goodie in enumerate(goodies):
        if player.imgcopyrect.colliderect(goodie):
            goodies.remove(goodie)
            player.score = player.score + 100
            astronautsave_sound.play()

def create_goodie():
    random_goodie_pos = random.randint(0,screen_width)
    new_goodie = asteroid_surface.get_rect(midtop = (1600,random_goodie_pos))
    random_angle = random.randint(1,360)
    return new_goodie

def move_goodies(goodies):
    for goodie in goodies:
        goodie.centerx -= GOODIE_SPEED
    return goodies

def draw_goodies(goodies):
    for goodie in goodies:
        screen.blit(goodie_surface,goodie)

# Asteroid Functions
def check_asteroidcollision(asteroids,player):
    for index, asteroid in enumerate(asteroids):
        if player.imgcopyrect.colliderect(asteroid):
            player.health -= 1
            # asteroid.fill('Red')
            print(index)
            # explosion_sound.stop()
            explosion_sound.play()
            asteroids.remove(asteroid)
            
            screen.blit(explosion_surface,asteroid)

def create_asteroid():
    random_asteroid_pos = random.randint(0,screen_width)
    new_asteroid = asteroid_surface.get_rect(midtop = (1600,random_asteroid_pos))
    random_angle = random.randint(1,360)
    return new_asteroid

def move_asteroids(asteroids):
    for asteroid in asteroids:
        asteroid.centerx -= ASTEROID_SPEED
    return asteroids

def draw_asteroids(asteroids):
    for asteroid in asteroids:
        screen.blit(asteroid_surface,asteroid)

# Setup Player Class
class player():
    def __init__(self, x_position, y_position, length, height):
        self.x = x_position
        self.y = y_position
        self.l = length
        self.h = height
        self.image = spaceship_surface
        self.rect = spaceship_rect
        self.player_ship = pygame.transform.scale(spaceship_surface, (SPACESHIP_SIZE, SPACESHIP_SIZE))
        self.angle = 0
        self.health = 3
        self.score = 0
        self.img_copy = pygame.transform.rotate(self.player_ship, self.angle)
        self.imgcopyrect = self.img_copy.get_rect(center = (round(self.x), round(self.y)))
        
    def draw(self, win):
     
        cx, cy = pygame.mouse.get_pos()
        dx, dy = cx - self.x, cy - self.y
        if abs(dx) > 0 or abs(dy) > 0:
            self.angle = math.atan2(-dx, -dy)*57.2957795

        self.img_copy = pygame.transform.rotate(self.player_ship, self.angle)
        self.imgcopyrect = self.img_copy.get_rect(center = (round(self.x), round(self.y)))
        
        win.blit(self.img_copy, self.imgcopyrect)
    
    def move(self, speed):
        cx, cy = pygame.mouse.get_pos()
        dx, dy = cx - self.x, cy - self.y
        if abs(dx) > 0 or abs(dy) > 0:
            dist = math.hypot(dx, dy)
            self.x += min(dist, speed) * dx/dist
            self.y += min(dist, speed) * dy/dist

# Make player from the class ??
playa = player(0,0,100,100)
playa.draw(screen)

# Game Loop
open = True
while open:
    clock.tick(120)
    pygame.display.update()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            open = False
        if event.type == SPAWNASTEROID:
            asteroid_list.append(create_asteroid())
        if event.type == SPAWNGOODIE:
            goodie_list.append(create_goodie())
        
    # Moving background
    floor_x_pos -= 0.5
    moon_x_pos -= 0.15
    draw_floor()
    update_hearts(playa)

    if playa.health <= 0:
        # Player is dead
        game_active = False
        screen.blit(explosion_surface,playa.imgcopyrect)
        show_text("GAME OVER",(255,0,0))
        text = game_font.render(str(playa.score),True,(255,255,255))
        screen.blit(text, (700,200))

    # Handle Asteroids
    asteroid_list = move_asteroids(asteroid_list)
    draw_asteroids(asteroid_list)  

    # Handle Goodies
    goodie_list = move_goodies(goodie_list)
    draw_goodies(goodie_list)     

    if floor_x_pos <= -screen_width:
        floor_x_pos = 0
    if moon_x_pos <= -screen_width:
        moon_x_pos = 0

    if game_active:
        # Check collisions
        check_asteroidcollision(asteroid_list,playa)
        check_goodiecollision(goodie_list,playa)

        # Player
        playa.draw(screen)
        playa.move(4)
        score_display(playa)

# Quit Game
pygame.quit()
quit()