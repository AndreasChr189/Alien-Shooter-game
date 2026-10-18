import pygame
import time
from random import randrange

pygame.font.init()

pygame.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooter")

# ------------------ ENEMY DATA ------------------
ENEMY_WIDTH, ENEMY_HEIGHT = 200, 200
enemy_x = 0
enemy_y = 0
enemy_type = None
ENEMY_COUNT = 195

# ------------------ SETUP ------------------
BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load("background2.jpg"), (WIDTH, HEIGHT))
BG3 = pygame.transform.scale(pygame.image.load("background3.jpg"), (WIDTH, HEIGHT))
GUN = pygame.image.load("gun.png")
GUN2 = pygame.transform.scale(pygame.image.load("gun2.png"), (WIDTH, HEIGHT))
ENEMY1 = pygame.transform.scale(pygame.image.load("enemy1.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
ENEMY2 = pygame.transform.scale(pygame.image.load("enemy2.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
ENEMY3 = pygame.transform.scale(pygame.image.load("enemy3.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
ENEMY4 = pygame.transform.scale(pygame.image.load("enemy4.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
ENEMY_2_1 = pygame.transform.scale(pygame.image.load("enemy2-1.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
ENEMY_2_2 = pygame.transform.scale(pygame.image.load("enemy2-2.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
ENEMY_2_3 = pygame.transform.scale(pygame.image.load("enemy2-3.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
ENEMY_2_4 = pygame.transform.scale(pygame.image.load("enemy2-4.png"), (ENEMY_WIDTH, ENEMY_HEIGHT))
DMGindicator = pygame.transform.scale(pygame.image.load("DamageIndicator.png"), (WIDTH, HEIGHT))
VICTORY = pygame.transform.scale(pygame.image.load("victory screen.png"), (WIDTH, HEIGHT))
GAME_OVER = pygame.transform.scale(pygame.image.load("gameOver.png"), (WIDTH, HEIGHT))

shoot_sfx = pygame.mixer.Sound("gunshot.mp3")
win_sfx = pygame.mixer.Sound("victory.mp3")
GameOver_sfx = pygame.mixer.Sound("gameOver.mp3")

PLAYER_WIDTH = 10
PLAYER_HEIGHT = 10
PLAYER_VEL = 10

FONT = pygame.font.SysFont("Arial", 30)

# ------------------ DRAW FUNCTION ------------------
def draw(player, enemy_hitbox, ENEMY_COUNT, HEALTH, DMGflash, cutscene, win, cutscene2):

    # Background
    if ENEMY_COUNT<=100:
        WIN.blit(BG, (0, 0))
    elif ENEMY_COUNT>100:
        WIN.blit(BG2, (0, 0))

    # Enemy
    if enemy_hitbox and ENEMY_COUNT<=100:
        if enemy_type == 0:
            WIN.blit(ENEMY1, (enemy_x, enemy_y))
        elif enemy_type == 1:
            WIN.blit(ENEMY2, (enemy_x, enemy_y))
        elif enemy_type == 2:
            WIN.blit(ENEMY3, (enemy_x, enemy_y))
        elif enemy_type == 3:
            WIN.blit(ENEMY4, (enemy_x, enemy_y))
    elif enemy_hitbox and ENEMY_COUNT>=100 and ENEMY_COUNT<200:
        if enemy_type == 0:
            WIN.blit(ENEMY_2_1, (enemy_x, enemy_y))
        elif enemy_type == 1:
            WIN.blit(ENEMY_2_2, (enemy_x, enemy_y))
        elif enemy_type == 2:
            WIN.blit(ENEMY_2_3, (enemy_x, enemy_y))
        elif enemy_type == 3:
            WIN.blit(ENEMY_2_4, (enemy_x, enemy_y))    

    # Player
    pygame.draw.rect(WIN, "red", player)

    # Gun
    gun_x = WIDTH // 2 - GUN.get_width() // 2
    gun_y = HEIGHT - GUN.get_height()
    if ENEMY_COUNT<=100:
        WIN.blit(GUN, (gun_x, gun_y))
    elif ENEMY_COUNT>100:
        WIN.blit(GUN2, (0,50))

    # Score
    score_text = FONT.render(f"SCORE : {ENEMY_COUNT}", 1 ,"white")
    WIN.blit(score_text, (20, 20))

    # Score
    health_text = FONT.render(f"HEALTH : {HEALTH}", 1 ,"white")
    WIN.blit(health_text, (20, HEIGHT-50))

    # Damage indicator
    if DMGflash:
        WIN.blit(DMGindicator, (0,0))

    # Victory screen
    if cutscene == True:
        WIN.blit(VICTORY, (0,0))

    # Game over screen
    if cutscene2 == True:
        WIN.blit(GAME_OVER, (0,0))
        
        

    pygame.display.update()

# ------------------ MAIN LOOP ------------------
def main():
    global enemy_type, ENEMY_COUNT, enemy_x, enemy_y

    HEALTH=3

    run = True

    win = False

    clock = pygame.time.Clock()

    player = pygame.Rect(500, 400, PLAYER_WIDTH, PLAYER_HEIGHT)

    enemy_hitbox = None

    last_spawn_time = time.time()

    damage_timer = time.time() 

    cooldown = 0.3

    last_shot_time = 0 

    DMGflash = None

    DMGflash_start = 0

    DMGflash_duration = 0.3

    cutscene = None

    cutscene_start = 0

    cutscene_duration = 0.5

    cutscene2 = None

    cutscene_start2 = 0

    cutscene_duration2 = 0.5

    while run and win == False:
        clock.tick(60)
        
        pygame.mouse.set_visible(False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Movement
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player.x = mouse_x - PLAYER_WIDTH // 2
        player.y = mouse_y - PLAYER_HEIGHT // 2
        if event.type == pygame.MOUSEBUTTONDOWN and time.time() - last_shot_time >= cooldown:
            shoot_sfx.play()
            last_shot_time = time.time()

        # Kill enemy
            if  enemy_hitbox and player.colliderect(enemy_hitbox):
                enemy_hitbox = None
                enemy_type = None
                ENEMY_COUNT += 1
                damage_timer = time.time()

        # Spawn enemy after 1 second
        if enemy_hitbox is None and time.time() - last_spawn_time >= 1:
            enemy_type = randrange(4)            

            enemy_x = randrange(0, WIDTH - ENEMY_WIDTH)
            enemy_y = randrange(50, HEIGHT - ENEMY_HEIGHT - 50)
            enemy_hitbox = pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)

            last_spawn_time = time.time()

        # take damage
        if time.time() - damage_timer > 2:
            HEALTH -= 1
            damage_timer = time.time()
            DMGflash = True
            DMGflash_start = time.time()        

        if DMGflash and time.time() - DMGflash_start > DMGflash_duration:
            DMGflash = False

        # Victory screen
        if ENEMY_COUNT >= 200 and not cutscene:
            cutscene = True
            cutscene_start = time.time() 
            win_sfx.play()
            if cutscene and time.time() - cutscene_start > cutscene_duration:
                cutscene = False
                win = True
            
        # Game over screen
        if HEALTH==0 and not cutscene2 and not cutscene:
            cutscene2 = True
            cutscene_start2 = time.time() 
            GameOver_sfx.play()
            if cutscene2 and time.time() - cutscene_start2 > cutscene_duration2:
                cutscene2 = False
                run = False


        draw(player, enemy_hitbox, ENEMY_COUNT, HEALTH, DMGflash, cutscene, win, cutscene2 )

    pygame.quit()

# ------------------ RUN ------------------
main()
