from random import randint
from pygame.locals import *
import pygame
import random

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

home_img = pygame.image.load('home.png').convert_alpha()
home_img = pygame.transform.scale(home_img,(100, 100))

title_img = pygame.image.load('TITLE.png').convert_alpha()
title_img = pygame.transform.scale(title_img,(300, 100))

bullet_img = pygame.image.load('bullet_img.png')
bullet_img = pygame.transform.scale(bullet_img,(20, 20))

heal_box_img = pygame.image.load('heal_box.png')
heal_box_img = pygame.transform.scale(heal_box_img,(50, 50))

ammo_box_img = pygame.image.load('ammo_box.png')
ammo_box_img = pygame.transform.scale(ammo_box_img,(50, 50))

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
            self.flip = True
            self.direction = -1
        if move_right:
            dx = self.speed
            self.flip = False
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
        
        self.rect.x += dx
        self.rect.y += dy

    def attack(self):
        if pygame.sprite.spritecollide(pl, enemy_group, False):
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
                    #pygame.draw.rect(screen, RED, self.vision)

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

class Playtform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y

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

start_button = Button(W // 2 - 100, H // 2 - 50  , start_button_img, 1)
exit_button = Button(W // 2 - 100, H // 2 - 50 + 150 , exit_button_img, 1)
title = Button(W // 2 - 250, H // 2 - 50 - 150 , title_img, 2)

title_end= Button(W // 2 - 200, H // 2 - 50 - 150 , gameove_img, 2)
home_btn =Button(W // 2 - 50, H // 2 - 50  , home_img, 1)

pl = player('player', 500, 100, 0.2, 3, 20)
health_bar = HealthBar(15, 15, pl.healt, pl.maxhealt)

enemy_group = pygame.sprite.Group()

bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

item_box = ItemBox('Health', 100, 380)
item_box_group.add(item_box)

item_box = ItemBox('Ammo', 900, 380)
item_box_group.add(item_box)

enemy1 = player('Zombie1', 800, 400, 0.05, 2, 8)
enemy2 = player('Zombie2', 200, 400, 0.1, 2, 8)
enemy3 = player('Zombie3', 900, 400, 0.05, 2, 8)
enemy4 = player('Zombie4', 100, 400, 0.05, 2, 8)

enemy_group = pygame.sprite.Group()
enemy_group.add(enemy1)
enemy_group.add(enemy2)
enemy_group.add(enemy3)
enemy_group.add(enemy4)

def spawn_enemy():
    enemy1 = player('Zombie1', 800, 400, 0.05, 2, 8)
    enemy2 = player('Zombie2', 200, 400, 0.1, 2, 8)
    enemy3 = player('Zombie3', 900, 400, 0.05, 2, 8)
    enemy4 = player('Zombie4', 100, 400, 0.05, 2, 8)

    enemy_group.add(enemy1)
    enemy_group.add(enemy2)
    enemy_group.add(enemy3)
    enemy_group.add(enemy4)
    run_once = 0
    return run_once

def spawn_heal():
    item_box = ItemBox('Health', 100, 380)
    item_box_group.add(item_box)

def spawn_ammo():
    item_box = ItemBox('Ammo', 900, 380)
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

while run:
    clock.tick(FPS)

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    if start_game == False:
        screen.fill(ORANGE)
        title.draw()

        if start_button.draw():
            start_game = True
            pl.alive = True
            pl.healt = 100
            pl.ammo = 20

        if exit_button.draw():
            run = False
    elif start_game == True:
        draw_BG2()
            #health
        health_bar.draw(pl.healt)
            #ammo
        draw_text(f'AMMO: {pl.ammo}', font, WHITE, 10,50)
        for x in range(pl.ammo):
            screen.blit(bullet_img, (125 + (x * 10), 45))
            #score
        draw_text(f'SCORE: {pl.score}', font, WHITE, 450, 10)

        draw_text(f'Zombies Left: {enemy_count}', font, WHITE, 450, 50)

        if enemy_count == 0:
            draw_text(f'YOU WIN!', font, RED, 450, 450)

        bullet_group.update()
        bullet_group.draw(screen)

        draw_line()
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
                pl.score += 50
                enemy_count -= 1

        if pl.healt == 20:
            heal_count = 0

        if enemy_count == 0:
            if run_once == 0:
                spawn_enemy()
                enemy_count = 4
        
        x = randint(1, 500)
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
            if home_btn.draw():
                start_game = False
            if exit_button.draw():
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