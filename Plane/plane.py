import pygame
import random
import math
from pygame import mixer

#initialize pygame
x=pygame.init()

#Game window
screen_width=800
screen_height=600
gamewindow=pygame.display.set_mode((screen_width,screen_height))

#Title and icon
pygame.display.set_caption("Space war")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Background
background=pygame.image.load('background.png')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Player
playerImg=pygame.image.load('player.png')
playerX = 350
playerY = 480
playerX_change = 0 

#Enemy 
enemyImg = []
enemyX= []
enemyY= []
enemyX_change = []
enemyY_change= []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(30)

#Bullet

#Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg=pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
bullet_state ="ready"

#Score
score=0
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

#GAme over text
over_font = pygame.font.Font('freesansbold.ttf', 80)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    gamewindow.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    gamewindow.blit(over_text, (200,250))
def player(x,y):
    gamewindow.blit(playerImg, (x,y))

def enemy(x,y,i):
    gamewindow.blit(enemyImg[i], (x,y))  

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    gamewindow.blit(bulletImg, (x+16, y+ 10))   

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
#Game Loop
running=True
while running:
    gamewindow.fill((0, 0, 0))
    #Background Image
    gamewindow.blit(background, (0, 0))
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        
        #if keystroke is pressed check wheter its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound=mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX=playerX
                    fire_bullet(playerX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    #Player Method
    playerX +=playerX_change

    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    player(playerX,playerY)

    #Enemy Movement
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] > 420:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] +=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=3
            enemyY[i] +=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-3 
            enemyY[i] +=enemyY_change[i]
        
        # Collision
        collision  = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_Sound=mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY= 480
            bullet_state = "ready"
            score_value +=10
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i], i)

    #Bullet Movement
    if bulletY <=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -=bulletY_change

   
       

    player(playerX,playerY)
    show_score(textX,textY)

    pygame.display.update()
