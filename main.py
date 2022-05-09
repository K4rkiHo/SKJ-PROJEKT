from random import randint
from pygame.locals import *
import pygame
import random
import json

pygame.init()

GRAVITY = 0.75
FPS = 60
W = 1000
H = 500
TILE_SIZE = 20
start_game = False

BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
TRANSPARETN = (0,0,0,0)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Zombie shooter")

BG_image = pygame.image.load('BG2.jpg')
BG_image = pygame.transform.scale(BG_image,(W, H))

BG2_image = pygame.image.load('piva.png')
BG2_image = pygame.transform.scale(BG2_image,(W, H))

start_button_img = pygame.image.load('start.png').convert_alpha()
start_button_img = pygame.transform.scale(start_button_img,(200, 100))

exit_button_img = pygame.image.load('exit.png').convert_alpha()
exit_button_img = pygame.transform.scale(exit_button_img,(200, 100))

gameove_img = pygame.image.load('gameover.jpg').convert_alpha()
gameove_img = pygame.transform.scale(gameove_img,(200, 100))

title_img = pygame.image.load('TITLE.png').convert_alpha()
title_img = pygame.transform.scale(title_img,(300, 100))

bullet_img = pygame.image.load('bullet_img.png')
bullet_img = pygame.transform.scale(bullet_img,(20, 20))

heal_box_img = pygame.image.load('heal_box.png')
heal_box_img = pygame.transform.scale(heal_box_img,(50, 50))

ammo_box_img = pygame.image.load('ammo_box.png')
ammo_box_img = pygame.transform.scale(ammo_box_img,(50, 50))

platform_img = pygame.image.load('platform.png')
platform_img = pygame.transform.scale(platform_img,(300, 100))

option_easy_img = pygame.image.load('easy.png').convert_alpha()
option_easy_img = pygame.transform.scale(option_easy_img,(200, 200))

option_normal_img = pygame.image.load('normal.png').convert_alpha()
option_normal_img = pygame.transform.scale(option_normal_img,(200, 200))

option_hard_img = pygame.image.load('hard.png').convert_alpha()
option_hard_img = pygame.transform.scale(option_hard_img,(200, 200))

option_hardcore_img = pygame.image.load('hardcore.png').convert_alpha()
option_hardcore_img = pygame.transform.scale(option_hardcore_img,(200, 200))

item_boxes = {
    'Health'    : heal_box_img,
    'Ammo'      : ammo_box_img
}

move_left = False
move_right = False
shoot = False

font = pygame.font.SysFont('Futura', 30)

def draw_BG():
    screen.blit(BG_image, (0, 0))

def draw_BG2():
    screen.blit(BG2_image, (0, 0))

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

class player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.jump = False
        self.alive = True
        img = pygame.image.load(f'{self.char_type}.png')
        self.image = pygame.transform.scale(img,(img.get_width() * scale, img.get_height() * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.shoot_cooldown = 0
        self.ammo = ammo
        self.start_ammo = ammo
        self.healt = 100
        self.maxhealt = self.healt
        self.score = 0
        #AI
        self.move_counter = 0
        self.idling = False
        self.idle_counter = 0
        self.vision = pygame.Rect(0,0,300,20)

    def update(self):
        self.chech_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def move(self, move_left, move_right):
        dx = 0
        dy = 0
        if move_left:
            dx = -self.speed
            self.flip = False
            self.direction = -1
        if move_right:
            dx = self.speed
            self.flip = True
            self.direction = 1
        #jump
        if self.jump == True:
            self.vel_y = -11
            self.jump = False

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > W:
            dx = W - self.rect.right

        for x in platform_group:
            if x.rect.colliderect(self.rect.x, self.rect.y + dy, 48, 76):
                if self.rect.bottom < x.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = x.rect.top
                        dy = 0
        

        self.rect.x += dx
        self.rect.y += dy

    def attack(self):
        if pygame.sprite.spritecollide(pl, enemy_group, False):
            if select_dificulty_hardcore:
                pl.healt -= 5
            else:
                pl.healt -= 1
    
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 10
            bullet = Bullet(self.rect.centerx + (0.8 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
    
    def AI(self):
        if self.alive and pl.alive:
            if random.randint(1, 100) == 1:
                self.idling = True
                self.idle_counter = 50
            if self.vision.colliderect(pl.rect):
                if self.direction == 1:
                    self.move(False, True)
                    if self.rect.centerx == 0 or self.rect.centerx == W:
                        self.direction = -1
                        self.flip = True
                    self.attack()
                if self.direction == -1:
                    self.move(True, False)
                    if self.rect.centerx == 0 or self.rect.centerx == W:
                        self.direction = 1
                        self.flip = False
                    self.attack()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_move_r = True
                    else:
                        ai_move_r = False
                    ai_move_l = not ai_move_r
                    self.move(ai_move_l, ai_move_r)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 100 * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idling = False
            
    def chech_alive(self):
        if self.healt <= 0:
            self.healt = 0
            #self.speed = 0
            self.alive = False

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),self.rect)
        #border
        #pygame.draw.rect(screen, RED, self.rect, 1)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 25
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > W:
            self.kill()
        if pygame.sprite.spritecollide(pl, bullet_group, False): 
            if pl.alive:
                pl.healt -= 5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False): 
                if enemy.alive:
                    enemy.healt -= 20
                    print(enemy.healt)
                    self.kill()

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        if pygame.sprite.collide_rect(self, pl):
            if self.item_type == 'Health':
                pl.healt += 25
                if pl.healt > pl.maxhealt:
                    pl.healt = pl.maxhealt
            elif self.item_type == 'Ammo':
                pl.ammo += 15
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, maxhealth):
        self.x = x
        self.y = y
        self.health = health
        self.maxhealth = maxhealth

    def draw(self, health):
        self.health = health
        ratio = self.health / self.maxhealth
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_img, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Button():
    def __init__(self, x, y, image, scale):
        w = image.get_width()
        h = image.get_height()
        self.image = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.cliced = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.cliced == False:
                self.cliced = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.cliced = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

def draw_line():
    pygame.draw.line(screen, RED, (0,400), (W, 400))

def writeToJSONFile(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

start_button = Button(W // 2 - 100, H // 2  , start_button_img, 1)
exit_button = Button(W // 2 - 100, H // 2 - 50 + 150 , exit_button_img, 1)
title = Button(W // 2 - 250, H // 2 - 50 - 150 , title_img, 2)

title_end= Button(W // 2 - 200, H // 2 - 50 - 150 , gameove_img, 2)

option_easy = Button(W // 2 - 500, H // 2 - 50 - 150 , option_easy_img, 1)
option_medium = Button(W // 2 - 250, H // 2 - 50 - 150 , option_normal_img, 1)
option_hard = Button(W // 2 + 50, H // 2 - 50 - 150 , option_hard_img, 1)
option_hardcore = Button(W // 2 + 300, H // 2 - 50 - 150 , option_hardcore_img, 1)

pl = player('player', 500, 100, 0.2, 3, 20)
health_bar = HealthBar(15, 15, pl.healt, pl.maxhealt)

enemy_group = pygame.sprite.Group()

bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()

platform1 = Platform(100, 200, 300)
platform_group.add(platform1)

platform2 = Platform(600, 200, 300)
platform_group.add(platform2)

"""
enemy1 = player('Zombie1', 800, 400, 0.05, 2, 8)
enemy2 = player('Zombie2', 200, 400, 0.1, 2, 8)
enemy3 = player('Zombie3', 900, 400, 0.05, 2, 8)
enemy4 = player('Zombie4', 100, 400, 0.05, 2, 8)

enemy_group = pygame.sprite.Group()
enemy_group.add(enemy1)
enemy_group.add(enemy2)
enemy_group.add(enemy3)
enemy_group.add(enemy4)
"""


def spawn_enemy():
    if select_dificulty_easy:
        x1 = randint(0,200)
        x2 = randint(800,1000)
        enemy1 = player('Zombie1', x2, 400, 0.05, 1, 8)
        enemy2 = player('Zombie2', x1, 400, 0.1, 1, 8)

        enemy_group.add(enemy1)
        enemy_group.add(enemy2)
        run_once = 0
        return run_once
    if select_dificulty_medium:
        x1 = randint(0,300)
        x2 = randint(700,1000)
        enemy1 = player('Zombie1', x2, 400, 0.05, 2, 8)
        enemy2 = player('Zombie2', x1, 400, 0.1, 2, 8)
        enemy3 = player('Zombie3', x2, 400, 0.05, 2, 8)
        enemy4 = player('Zombie4', x1, 400, 0.05, 2, 8)

        enemy_group.add(enemy1)
        enemy_group.add(enemy2)
        enemy_group.add(enemy3)
        enemy_group.add(enemy4)
        run_once = 0
        return run_once

    if select_dificulty_hard:
        x1 = randint(0,400)
        x2 = randint(0,400)
        x3 = randint(0,400)
        x4 = randint(600,1000)
        x5 = randint(600,1000)
        x6 = randint(600,1000)
        enemy1 = player('Zombie1', x5, 400, 0.05, 3, 8)
        enemy2 = player('Zombie2', x1, 400, 0.1, 3, 8)
        enemy3 = player('Zombie3', x2, 400, 0.05, 3, 8)
        enemy4 = player('Zombie4', x3, 400, 0.05, 3, 8)
        enemy5 = player('Zombie1', x4, 400, 0.05, 3, 8)
        enemy6 = player('Zombie3', x6, 400, 0.05, 3, 8)

        enemy_group.add(enemy1)
        enemy_group.add(enemy2)
        enemy_group.add(enemy3)
        enemy_group.add(enemy4)
        enemy_group.add(enemy5)
        enemy_group.add(enemy6)
        run_once = 0
        return run_once
    if select_dificulty_hardcore:
        x = randint(0, 1000)
        enemy1 = player('Zombie1', x, 400, 0.05 , 6, 8)
        enemy1.healt = 1000
        enemy_group.add(enemy1)

def spawn_heal():
    item_box = ItemBox('Health', 220, 180)
    item_box_group.add(item_box)

def spawn_ammo():
    item_box = ItemBox('Ammo', 730, 180)
    item_box_group.add(item_box)

enemy_count = 0
for enemy in enemy_group:
    enemy_count += 1

run = True
i = 0

run_once = 0
run_once2 = 0
run_once3 = 0
end_game = False

game_idle = False

select_dificulty_easy = False
select_dificulty_medium = False
select_dificulty_hard = False
select_dificulty_hardcore = False

while run:
    clock.tick(FPS)

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    if game_idle == False:
        screen.fill(ORANGE)
        title.draw()

        if start_button.draw():
            game_idle = True
        if exit_button.draw():
            run = False
    if game_idle == True:
        screen.fill(WHITE)
        draw_text(f'MEDIUM', font, BLACK, W // 2 - 200, H // 2 + 100)
        draw_text(f'EASY', font, BLACK, W // 2 - 425, H // 2 + 100)
        draw_text(f'HARD', font, BLACK, W // 2 + 125, H // 2 + 100)
        draw_text(f'HARDCORE', font, BLACK, W // 2 + 350, H // 2 + 100)
        if option_easy.draw(): 
            spawn_enemy()
            start_game = True
            select_dificulty_easy = True
        if option_medium.draw():
            spawn_enemy()
            start_game = True
            select_dificulty_medium = True
        if option_hard.draw():
            spawn_enemy()
            start_game = True
            select_dificulty_hard = True
        if option_hardcore.draw():
            spawn_enemy()
            start_game = True
            select_dificulty_hardcore = True
    if start_game == True:
        draw_BG()
            #health
        health_bar.draw(pl.healt)
            #ammo
        draw_text(f'AMMO: {pl.ammo}', font, WHITE, 10,50)
        for x in range(pl.ammo):
            screen.blit(bullet_img, (125 + (x * 10), 45))
            #score
        draw_text(f'SCORE: {pl.score}', font, WHITE, 450, 10)

        draw_text(f'Zombies Left: {enemy_count}', font, WHITE, 450, 50)

        bullet_group.update()
        bullet_group.draw(screen)

        platform_group.draw(screen)
        pl.draw()
        pl.update()
        pl.move(move_left, move_right)

        for enemy in enemy_group:
            enemy.AI()
            enemy.update()
            enemy.draw()
            if enemy.alive == False:
                enemy.image.fill(TRANSPARETN)
                enemy.kill()
                if select_dificulty_hardcore:
                    pl.score += 1250
                else:
                    pl.score += 50
                enemy_count -= 1
            if select_dificulty_hardcore:
                draw_text(f'Hardcore Zombies healt: {enemy.healt}', font, RED, 700, 10)

        if pl.healt == 20:
            heal_count = 0

        if enemy_count == 0:
            if run_once == 0:
                spawn_enemy()
                if select_dificulty_easy:
                    enemy_count = 2
                if select_dificulty_medium:
                    enemy_count = 4
                if select_dificulty_hard:
                    enemy_count = 6
                if select_dificulty_hardcore:
                    enemy_count = 1
        
        x = randint(1, 300)
        a = 4
        if pl.ammo < 5 and a == x:
            run_once3 = 0
        if pl.healt < 20 and a == x:
            run_once2 = 0

        if run_once3 == 0:
            spawn_ammo()
            run_once3 = 1

        if run_once2 == 0:
            spawn_heal()
            run_once2 = 1

        item_box_group.update()
        item_box_group.draw(screen)

        if shoot:
            pl.shoot()
        if pl.alive == False:
            screen.fill(BLACK)
            title_end.draw()
            draw_text(f'SCORE: {pl.score}', font, WHITE, W // 2 - 50, H // 2)
            if exit_button.draw():

                user_data = {
                    "name" : "test",
                    "score" : pl.score
                }
                with open('data.json') as json_file:
                    data = json.load(json_file)
                    temp = data["game_score"]
                    temp.append(user_data)

                writeToJSONFile(data, 'data.json')
                run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_w:
                pl.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()
pygame.quit()