import pygame
import random
import math
from pygame import mixer

# Initialize the game
pygame.init()
clock = pygame.time.Clock()
# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('assets/images/background.png')

# Background Sound
mixer.music.load('assets/audios/background_music.mp3')
#mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('assets/images/ufo.png')
pygame.display.set_icon(icon)

# Enemy
enemyImg = []
enemyX = []
enemyY= []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

def generate_enemy():
    enemyImg.append(pygame.image.load('assets/images/enemy1.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

def generate_gameover_enemy(size):
    if size == 64:
        enemyImg.append(pygame.image.load('assets/images/enemy1.png'))
    elif size == 128:
        enemyImg.append(pygame.image.load('assets/images/enemy2.png'))
    elif size == 256:
        enemyImg.append(pygame.image.load('assets/images/enemy1.png'))
    elif size == 512:
        enemyImg.append(pygame.image.load('assets/images/enemy2.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 735))


for i in range(num_of_enemies):
    generate_enemy()

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Laser
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

laserImg = pygame.image.load('assets/images/bullet.png')
laserX = 0
laserY = 480
laserX_change = 3
laserY_change = 6
laser_state = "ready"


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX, 2)) + (math.pow(enemyY - laserY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Player
playerImg = pygame.image.load('assets/images/ufo.png')
playerX = 370
playerY = 480
playerX_change = 0

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Game Over sound
explosion_Played = False

# Game Over state
game_over = False

def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))
    if num_of_enemies >= 10:
        enemynum = font.render('# of Enemies : ' + str(num_of_enemies), True, (255,255,255))
        screen.blit(enemynum, (x, y + 25))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def game_over_show():
    mixer.music.stop()



def player(x, y):
    screen.blit(playerImg, (x, y))


# Game Loop
running = True
while running:

    # RGB Background
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check if left or right arrow
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if laser_state == 'ready' and game_over is False:
                    laserX = playerX
                    fire_laser(laserX, laserY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking for boundaries of spaceship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            # for j in range(num_of_enemies):
            #    enemyY[j] = 2000
            game_over_text()
            game_over = True
            if explosion_Played == False:
                game_over_show()
                explosion_Played = True

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 738:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            laserY = 480
            laser_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            num_of_enemies += 1
            generate_enemy()

        enemy(enemyX[i], enemyY[i], i)

    # Laser Movement
    if laserY <= 0:
        laserY = 480
        laser_state = 'ready'
    if laser_state == 'fire':
        fire_laser(laserX, laserY)
        laserY -= laserY_change



    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
