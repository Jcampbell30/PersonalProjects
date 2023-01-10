 
from itertools import count
from tkinter import EventType

from turtle import update
import pygame
import os
from pygame import mixer


pygame.init()
mixer.init()
WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("DBZ 2D")

joysticks = {}
pygame.mixer.music.load('15 - The Monster Freeza Vs. The Legendary Super Saiyan.wav')
pygame.mixer.music.play()
if pygame.joystick.get_count() >= 1:
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()
if pygame.joystick.get_count() > 1:
    joy2 = pygame.joystick.Joystick(1)
    joy2.init()
else:
    pass

#colors
YELLOW = (243,235,35)
WHITE = (255,255,255)
BLUE = (25,55,255)
BLACK = (0,0,0)
LIMEGREEN = (50,205,50)
FPS = 60

vegeta = [0,10,20,30,40,50,60,70,80,90,100]
goku = [0,10,20,30,40,50,60,70,80,90,100]
countg = 10
countv = 10
c = 0
g = 0





PLAYER_WIDTH, PLAYER_HEIGHT = 75,100
sound = pygame.mixer.Sound("kiblast.wav")
vegetaHit = pygame.mixer.Sound('vegeta-pain.wav')
gokuHit = pygame.mixer.Sound('Goku Woah.wav')
YELLOW_SPACESHIP = pygame.image.load('Kakarot.png')
GOKU_FIRE = pygame.image.load('Kakarot.png')
KI_BLAST = pygame.image.load('KIB.png')
GOKU_WINS = pygame.image.load('GokuWins.png')
VEGETA_WINS = pygame.image.load('VegetaWins.png')
INSTRUCTIONS = pygame.image.load('Instructions.png')
KI = pygame.transform.scale(KI_BLAST,(PLAYER_WIDTH/2,PLAYER_HEIGHT/2))
KI.convert()
ki = KI.get_rect()
GOKU = pygame.transform.scale(GOKU_FIRE,(PLAYER_WIDTH,PLAYER_HEIGHT))
VEGETA_FIRE = pygame.image.load('vegetaL.png')
VEGETA = pygame.transform.scale(VEGETA_FIRE,(PLAYER_WIDTH,PLAYER_HEIGHT))
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 2, HEIGHT) 
BACKGROUND_NAMEK = pygame.image.load('namek.png')
NAMEK = pygame.transform.scale(BACKGROUND_NAMEK,(WIDTH,HEIGHT))
VEL = 10
BULLETS = 15000
BULLET_VEL = 10
PLAYER_TWO_HIT = pygame.USEREVENT + 1
PLAYER_ONE_HIT = pygame.USEREVENT + 2

def draw_window(player_one, player_two, player_one_bullets, player_two_bullets):
    global c
    global g
    x = countv - c
    y = countg - g
    WIN.fill(WHITE)
    WIN.blit(NAMEK,(0,0))
    #pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(GOKU,(player_one.x,player_one.y))
    WIN.blit(VEGETA,(player_two.x,player_two.y))
    #WIN.blit(KI,(323,324))
    
    for bullet in player_one_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
        if player_two.colliderect(bullet):
            if c == 10:
                pass
            else:
                vegetaHit.play()
                c += 1
                print(c)
                bullet.x = 0

    for bullet in player_two_bullets:
        pygame.draw.rect(WIN,BLUE,bullet)
        if player_one.colliderect(bullet):
            if g == 10:
                pass
            else:
                gokuHit.play()
                g += 1
                print(g)
                bullet.x =1501

    
    healthBox(vegeta[x],goku[y])
        
    pygame.display.update()
def vegeta_handle_movement(keys_pressed, player_two):
    if keys_pressed[pygame.K_a] and player_two.x  - VEL > 0: #Left
            player_two.x -= VEL
    if keys_pressed[pygame.K_d] and player_two.x + VEL + player_two.width < BORDER.x:#Right
            player_two.x += VEL
    if keys_pressed[pygame.K_w] and player_two.y  - VEL > 0: #Up
            player_two.y -= VEL
    if keys_pressed[pygame.K_s] and player_two.y + VEL + player_two.height < HEIGHT: #Down
           player_two.y += VEL
def goku_handle_movement(keys_pressed, player_one):
    if pygame.joystick.get_count() > 0:
        if my_joystick.get_button(13)and player_one.x  - VEL > BORDER.x + BORDER.width: #Left
                player_one.x -= VEL
        if my_joystick.get_button(14)and player_one.x + VEL + player_one.width < WIDTH: #Right
                player_one.x += VEL
        if my_joystick.get_button(11)and player_one.y  - VEL > 0: #Up
                player_one.y -= VEL
        if my_joystick.get_button(12)and player_one.y + VEL + player_one.height < HEIGHT: #Down
                player_one.y += VEL
    else:
        if keys_pressed[pygame.K_LEFT]and player_one.x  - VEL > BORDER.x + BORDER.width: #Left
                player_one.x -= VEL
        if keys_pressed[pygame.K_RIGHT]and player_one.x + VEL + player_one.width < WIDTH: #Right
                player_one.x += VEL
        if keys_pressed[pygame.K_UP]and player_one.y  - VEL > 0: #Up
                player_one.y -= VEL
        if keys_pressed[pygame.K_DOWN]and player_one.y + VEL + player_one.height < HEIGHT: #Down
                player_one.y += VEL
    
def handle_bullets(player_two_bullets, player_one_bullets, player_two,player_one):
   
    for bullet in player_two_bullets :
        bullet.x -= BULLET_VEL
        if player_one.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_ONE_HIT))
            pygame.display.update()


    for bullet in player_one_bullets:
        bullet.x += BULLET_VEL
        if player_two.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_TWO_HIT))
            pygame.display.update()


def healthBox(healthV,healthG):
   
    HB_1Border = pygame.Rect(2,2,110,20)
    HB_2Border = pygame.Rect(1390,2,110,20)
    HEALTHBAR_1 = pygame.Rect(5,5,healthV,10)
    HEALTHBAR_2 = pygame.Rect(1395,5,healthG,10)
    pygame.draw.rect(WIN,WHITE,HB_1Border)
    pygame.draw.rect(WIN, WHITE, HB_2Border)
    pygame.draw.rect(WIN,LIMEGREEN,HEALTHBAR_1)
    pygame.draw.rect(WIN,LIMEGREEN,HEALTHBAR_2)
def getWinner():
    if c >= 9:
        WIN.blit(GOKU_WINS,(500,150))
        WIN.blit(INSTRUCTIONS,(500,300))
        pygame.display.update()
    if g >= 9:
        WIN.blit(VEGETA_WINS,(500,150))
        WIN.blit(INSTRUCTIONS,(500,300))
        pygame.display.update()
def paused():
    global c
    global g
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()    
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                    c = 0
                    g = 0
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        WIN.fill(WHITE)
        WIN.blit(NAMEK,(0,0))
        getWinner()
        pygame.display.update()
        


def main():

    player_one = pygame.Rect(1300,600,PLAYER_WIDTH, PLAYER_HEIGHT)
    player_two = pygame.Rect(100,600,PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    player_one_bullets = []
    player_two_bullets = []

    
    
    Running = True
    while Running:

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False


            if pygame.joystick.get_count() > 0:
                if my_joystick.get_button(0):
                        sound.play()
                        bullet = pygame.Rect((player_one.x-20) + player_one.width, (player_one.y -20) + player_one.height // 2 - 2,10, 5)
                        player_one_bullets.append(bullet)
                
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if len(player_two_bullets) == BULLETS:
                        pass
                    else:
                        sound.play()
                        bullet = pygame.Rect((player_two.x-20) + player_two.width, (player_two.y -20) + player_two.height // 2 - 2,10, 5)
                        player_two_bullets.append(bullet)
 
                if event.key == pygame.K_RCTRL:
                    if len(player_one_bullets) == BULLETS:
                        pass
                    else:
                        sound.play()
                        bullet = pygame.Rect((player_one.x-50) + player_one.width, (player_one.y-30) + player_one.height // 2 - 2,10, 5)
                        player_one_bullets.append(bullet)
        
        
        keys_pressed = pygame.key.get_pressed()
        vegeta_handle_movement(keys_pressed, player_two)
        goku_handle_movement(keys_pressed, player_one)
        handle_bullets(player_one_bullets,player_two_bullets,player_one,player_two)
        draw_window(player_one,player_two, player_one_bullets, player_two_bullets)
        if c >= 10:
            paused()
        if g >= 10:
            paused()
        

    pygame.quit()
if __name__ == "__main__":
    main()
