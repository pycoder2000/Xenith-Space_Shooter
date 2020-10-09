# main.py
import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply

import webbrowser
import tkinter
import tkinter.messagebox
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Xenith - 1st Anniversary Edition")

background = pygame.image.load("images/Background2.gif").convert()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load Game Music
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.4)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(1.0)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.6)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.6)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target, inc):
    for each in target:
        each.speed += inc

def main():
    pygame.mixer.music.play(-1)

    # Generate our plane
    me = myplane.MyPlane(bg_size)

    enemies = pygame.sprite.Group()

    # Spawn small enemy aircraft
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # Spawn medium enemy aircraft
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    # Spawn large enemy aircraft
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # Generate ordinary bullets
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 200
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # Generate super bullets
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 200
    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx+30, me.rect.centery)))

    clock = pygame.time.Clock()

    # Shot Index
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # Statistical Score
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)

    # Flag whether to pause the game
    paused = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    # Set Difficulty Level
    level = 1

    # Full Screen Bomb
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    # Distribute a supply pack every 30 seconds
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

    # Super Bullet Timer
    DOUBLE_BULLET_TIME = USEREVENT + 1

    # Whether the logo uses super bullets
    is_double_bullet = False

    # Disable Invincibility Timer
    INVINCIBLE_TIME = USEREVENT + 2

    # Number of Lives
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # Prevent Repeated Opening of Log files
    recorded = False

    # Game Over Screen
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # Go to Page Button
    congratulation_image = pygame.image.load("images/Congratulations.png").convert_alpha()
    congratulation_rect = congratulation_image.get_rect()
    jump_image = pygame.image.load("images/jump.png").convert_alpha()
    jump_rect = jump_image.get_rect()

    # Used to Switch Pictures
    switch_image = True

    # For Delay
    delay = 100
    
    # Rate of Fire
    shoot_speed = 25

    # Target Score
    target_score = 20190719

    running = True

    while running:
        # Check if the target score is reached
        if score > target_score:
            paused = True
            pygame.time.set_timer(SUPPLY_TIME, 0)
            pygame.mixer.music.pause()
            pygame.mixer.pause()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        if score > target_score:
                            target_score = 9999999999999999
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                elif event.button == 1 and score > target_score and jump_rect.collidepoint(event.pos):
                    webbrowser.open("https://pycoder2000.github.io/reward/love.html")

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                       paused_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)
                         

        # Increase difficulty based on user score
        if level == 1 and score > 1000000:
            level = 2
            upgrade_sound.play()
            # Added 3 small enemy aircraft, 2 medium enemy aircraft and 1 large enemy aircraft
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            # Increase the speed of small enemy aircraft

            inc_speed(small_enemies, 1)
        elif level == 2 and score > 5000000:
            level = 3
            upgrade_sound.play()
            # Added 5 small enemy aircraft, 3 medium enemy aircraft and 2 large enemy aircraft
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # Increase the speed of small enemy aircraft

            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            # Increase the rate of fire
            shoot_speed = 20
        elif level == 3 and score > 10000000:
            level = 4
            upgrade_sound.play()
            # Added 5 small enemy aircraft, 3 medium enemy aircraft and 2 large enemy aircraft
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # Increase the speed of small enemy aircraft

            inc_speed(mid_enemies, 1)
            # Increase the rate of fire
            shoot_speed = 10
        elif level == 4 and score > 15000000:
            level = 5
            upgrade_sound.play()
            # Added 5 small enemy aircraft, 3 medium enemy aircraft and 2 large enemy aircraft
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # Increase the speed of small enemy aircraft

            # inc_speed(small_enemies, 1)
            # inc_speed(mid_enemies, 1)
            # Increase the rate of fire
            shoot_speed = 3
            
        screen.blit(background, (0, 0))
                
        if life_num and not paused:
            # Detect user's keyboard operation
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # Draw full-screen bomb supplies and check if they are obtained
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            # Draw super bullet supplies and check if they are obtained
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            # Fire a bullet
            if not(delay % shoot_speed):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-33, me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx+30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

                
            # Check if the bullet hits the enemy aircraft
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
            
            # Draw a large enemy plane
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # Draw blood tank
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    
                    # When the life is greater than 20%, it shows green, otherwise it shows red
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                        
                    # Will appear on the screen, playing sound effects
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:
                    # Destroy
                    if not(delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 400000
                            each.reset()

            # Draw medium enemy aircraft:
            for each in mid_enemies:
                if each.active:
                    each.move()

                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # Draw blood tank
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    
                    # When the life is greater than 20%, it shows green, otherwise it shows red
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                      each.rect.top - 5), 2)
                else:
                    # Destroy
                    if not(delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 160000
                            each.reset()

            # Draw a small enemy plane:
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # Destroy
                    if not(delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 30000
                            each.reset()

            # Check if our plane has been hit
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False
            
            # Draw our plane
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # destroy
                if not(delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # Draw the number of full-screen bombs
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # Plot the remaining lives
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, \
                                (width-10-(i+1)*life_rect.width, \
                                 height-10-life_rect.height))

        elif paused and score > target_score:
            congratulation_rect.left, congratulation_rect.top = (width - congratulation_rect.width) // 2, 150
            screen.blit(congratulation_image, congratulation_rect)

            jump_rect.left, jump_rect.top = (width - jump_rect.width) // 2, congratulation_rect.bottom + 10
            screen.blit(jump_image, jump_rect)

            '''# Detect user's mouse operation
            # If the user presses the left mouse button
            if pygame.mouse.get_pressed()[0]:
                # Get mouse coordinates
                pos = pygame.mouse.get_pos()
                # If the user clicks "jump to beautiful album"
                if jump_rect.left < pos[0] < jump_rect.right and \
                   jump_rect.top < pos[1] < jump_rect.bottom:
                    # 跳转网页
                    target_score = 9999999999999999
                    webbrowser.open("https://pycoder2000.github.io/reward/love.html")
                # If the user clicks the "Pause/Resume button"            
                elif paused_rect.left < pos[0] < paused_rect.right and \
                     paused_rect.top < pos[1] < paused_rect.bottom:
                    # Continue the game
                    paused = False
                    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                    pygame.mixer.music.unpause()
                    pygame.mixer.unpause()'''
        
        # Draw the game end screen
        elif life_num == 0:
            # Background music stopped
            pygame.mixer.music.stop()

            # Stop all sound effects
            pygame.mixer.stop()

            # Stop issuing supplies
            pygame.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:
                recorded = True
                # Read the highest score in history
                try:
                    with open("recor.txt", "r") as f:
                        print(type(f))
                        record_score = int(f.read())
                except:
                    record_score = 0

                # If the player score is higher than the highest score in history, save
                if score > record_score:
                    record_score = score
                    with open("record.txt", "w") as f:
                        f.write(str(record_score))

            # Draw the end screen
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (10, 100))
            
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                 (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                 (width - gameover_text2_rect.width) // 2, \
                                 gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # Detect user's mouse operation
            # If the user presses the left mouse button
            if pygame.mouse.get_pressed()[0]:
                # Get mouse coordinates
                pos = pygame.mouse.get_pos()
                # If the user clicks "restart"
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    # Call the main function to restart the game
                    main()
                # If the user clicks "End Game"            
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # Exit the game
                    pygame.quit()
                    sys.exit()      

        # Draw pause button
        screen.blit(paused_image, paused_rect)
        
        # Draw target score
        target_score_text = score_font.render("Target : %s" % str(target_score), True, WHITE)
        screen.blit(target_score_text, (10, 5))

        # Draw score
        score_text = score_font.render("Score : %s" % str(score), True, WHITE)
        screen.blit(score_text, (10, 50))

        # Switch picture
        if not(delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)
        
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
