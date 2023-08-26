from matplotlib.pyplot import angle_spectrum
from constants import *
from main import swords_disp
import pygame
import math

class Worker:
    def __init__(self, status, team):
        self.health = 100
        self.vel = WORKER_SPEED
        self.status = status
        self.team = team
        self.run_sprite = []
        self.frame = 0

        if self.team == 'blue':
            self.img = pygame.image.load('images/BLUE/worker/ready.png')
            self.x = BARRACKS_POS - self.img.get_width()/2
        elif self.team == 'red':
            self.img = pygame.image.load('images/RED/worker/ready.png')
            self.x = SCREEN_WIDTH - BARRACKS_POS - self.img.get_width()/2

        self.rect = self.img.get_rect()
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT

        for i in range(6):
            if self.team == 'blue':
                self.run_sprite.append(pygame.image.load(f'images/BLUE/worker/RUN/run-{i}.png'))
            else:
                self.run_sprite.append(pygame.image.load(f'images/RED/worker/RUN/run-{i}.png'))
                

    def update(self):

        if self.frame < 6:
            self.img = self.run_sprite[self.frame]
            self.frame += 1
        else:
            self.frame = 0

        if self.status == 'heading mining':
            if self.team == 'blue':
                if self.x > MINE_POS:
                    self.x -= self.vel
                else:
                    self.status = 'mining'

            else:
                if self.x < SCREEN_WIDTH - MINE_POS - self.img.get_width():
                    self.x += self.vel
                else:
                    self.status = 'mining'

        elif self.status == 'mining':
            # if self.team == 'blue':
            #     blue_player.resources += WORKER_PROD
            # else:
            #     red_player.resources += WORKER_PROD
            pass

        elif self.status == 'heading wall':

            if self.team == 'blue':
                self.run_sprite.clear()
                for i in range(6):
                    self.run_sprite.append(pygame.image.load(f'images/BLUE/worker/RUN/run-{i}.png'))

                if self.x < WALL_POS - self.img.get_width():
                    self.x += self.vel
                else:
                    self.status = 'wall'

            else:
                self.run_sprite.clear()
                for i in range(6):
                    self.run_sprite.append(pygame.image.load(f'images/RED/worker/RUN/run-{i}.png'))


                if self.x > SCREEN_WIDTH - WALL_POS:
                    self.x -= self.vel
                else:
                    self.status = 'wall'

        elif self.status == 'wall':
            pass
            # if self.team == 'blue' and blue_player.wall < WALL_HEALTH:
            #     blue_player.wall += WORKER_REPAIR
            # elif self.team == 'red' and red_player.wall < WALL_HEALTH:
            #     red_player.wall += WORKER_REPAIR

    def display(self, win):
        if self.status not in ['mining', 'barracks', 'wall']:
            win.blit(self.img, (self.x, SCREEN_HEIGHT - GROUND_HEIGHT - self.img.get_height()))

class Swordsman:
    def __init__(self, team, x=None):
        self.health = 100
        self.vel = SWORD_SPEED
        self.status = ''
        self.team = team
        self.opponent_det = False
        self.rest = 0
        self.run_sprite = []
        self.frame = 0
        self.attack_sprite = []
        self.attack_frame = 0

        if self.team == 'blue':
            self.img = pygame.image.load('images/BLUE/sword/ready.png')
            self.x = BARRACKS_POS - self.img.get_width()/2
        elif self.team == 'red':
            self.img = pygame.image.load('images/RED/sword/ready.png')
            self.x = SCREEN_WIDTH - BARRACKS_POS - self.img.get_width()/2

        if x != None:
            self.x = x
        
        self.rect = self.img.get_rect()
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.img.get_height()

        for i in range(12):
            if self.team == 'red':
                self.run_sprite.append(pygame.image.load(f'images/RED/sword/RUN/run-{i}.png'))
            else:
                self.run_sprite.append(pygame.image.load(f'images/BLUE/sword/RUN/run-{i}.png'))


    def update(self):

        if self.rest > 0:
            self.rest -= 1
        self.opponent_det = False
        self.status = 'marching'
        self.rect.x = self.x

        if self.frame < 12:
            self.img = self.run_sprite[self.frame]
            self.frame += 1
        else:
            self.frame = 0

        # check for enemies
        for opp in swords_disp:
            if self.team == 'blue' and opp.team == 'red':
                if self.x + self.img.get_width() + SWORD_RANGE >= opp.x:
                    self.opponent_det = True
            elif self.team == 'red' and opp.team == 'blue':
                if self.x - SWORD_RANGE - self.img.get_width() <= opp.x:
                    self.opponent_det = True

        for opp in archers_disp:
            if self.team == 'blue' and opp.team == 'red':
                if self.x + self.img.get_width() + SWORD_RANGE >= opp.x:
                    self.opponent_det = True
            elif self.team == 'red' and opp.team == 'blue':
                if self.x - SWORD_RANGE - self.img.get_width() <= opp.x:
                    self.opponent_det = True
        

        # check for wall
        if self.team == 'blue':
            if self.x + self.img.get_width() + SWORD_RANGE >= SCREEN_WIDTH - WALL_POS:
                self.opponent_det = True
        elif self.team == 'red':
            if self.x - SWORD_RANGE <= WALL_POS:
                self.opponent_det = True


        if self.status == 'marching':
            if not self.opponent_det:
                if self.team == 'blue':
                    self.x += self.vel
                else:
                    self.x -= self.vel
            else:
                self.status = 'attacking'
                if self.team == 'blue':
                    self.img = pygame.image.load('images/BLUE/sword/ready.png')
                else:
                    self.img = pygame.image.load('images/RED/sword/ready.png')

        if self.status == 'attacking':

            # attack swordsman opponent
            for opp in swords_disp:
                if self.team == 'blue' and opp.team == 'red':
                    if self.x + self.img.get_width() + SWORD_RANGE >= opp.x:
                        if self.rest == 0:
                            opp.health -= SWORD_HIT
                            self.rest = SWORD_REST
                            self.img = pygame.image.load('images/BLUE/sword/ATTACK/attack-3.png')

                elif self.team == 'red' and opp.team == 'blue':
                    if self.x - SWORD_RANGE - self.img.get_width() <= opp.x:
                        if self.rest == 0:
                            opp.health -= SWORD_HIT
                            self.rest = SWORD_REST
                            self.img = pygame.image.load('images/RED/sword/ATTACK/attack-3.png')
            
            # attack archer opponent
            for opp in archers_disp:
                if self.team == 'blue' and opp.team == 'red':
                    if self.x + self.img.get_width() + SWORD_RANGE >= opp.x:
                        if self.rest == 0:
                            opp.health -= SWORD_HIT
                            self.rest = SWORD_REST
                            self.img = pygame.image.load('images/BLUE/sword/ATTACK/attack-3.png')
                elif self.team == 'red' and opp.team == 'blue':
                    if self.x - SWORD_RANGE - self.img.get_width() <= opp.x:
                        if self.rest == 0:
                            opp.health -= SWORD_HIT
                            self.rest = SWORD_REST
                            self.img = pygame.image.load('images/RED/sword/ATTACK/attack-3.png')


            if self.rest == 0:
                if self.team == 'blue':
                    if self.x + self.img.get_width() + SWORD_RANGE >= SCREEN_WIDTH - WALL_POS:
                        red_player.wall -= SWORD_HIT
                        self.rest = SWORD_REST
                        self.img = pygame.image.load('images/BLUE/sword/ATTACK/attack-3.png')
                else:
                    if self.x - SWORD_RANGE <= WALL_POS:
                        blue_player.wall -= SWORD_HIT
                        self.rest = SWORD_REST
                        self.img = pygame.image.load('images/RED/sword/ATTACK/attack-3.png')
                

    def display(self, win):
        win.blit(self.img, (self.x, SCREEN_HEIGHT - GROUND_HEIGHT - self.img.get_height()))

class Archer:
    def __init__(self, team, x=None):
        self.health = 100
        self.vel = ARCHER_SPEED
        self.status = ''
        self.team = team
        self.opponent_det = False
        self.rest = 0
        self.arrows = []
        self.run_sprite = []
        self.frame = 0

        if self.team == 'blue':
            self.img = pygame.image.load('images/BLUE/archer/ready.png')
            self.x = BARRACKS_POS - self.img.get_width()/2
        elif self.team == 'red':
            self.img = pygame.image.load('images/RED/archer/ready.png')
            self.x = SCREEN_WIDTH - BARRACKS_POS - self.img.get_width()/2

        if x != None:
            self.x = x
        
        self.rect = self.img.get_rect()
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.img.get_height()

        for i in range(12):
            if self.team == 'red':
                self.run_sprite.append(pygame.image.load(f'images/RED/archer/RUN/run-{i}.png'))
            else:
                self.run_sprite.append(pygame.image.load(f'images/BLUE/archer/RUN/run-{i}.png'))



    def update(self):

        
        if self.rest > 0:
            self.rest -= 1
        self.opponent_det = False
        self.status = 'marching'
        self.rect = self.img.get_rect()
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.img.get_height()
        self.rect.x = self.x

        if self.frame < 12:
            self.img = self.run_sprite[self.frame]
            self.frame += 1
        else:
            self.frame = 0

        # check for enemies
        for opp in swords_disp:
            if self.team == 'blue' and opp.team == 'red':
                if self.x + self.img.get_width() + ARCHER_RANGE >= opp.x:
                    self.opponent_det = True
            elif self.team == 'red' and opp.team == 'blue':
                if self.x - ARCHER_RANGE - self.img.get_width() <= opp.x:
                    self.opponent_det = True
        
        for opp in archers_disp:
            if self.team == 'blue' and opp.team == 'red':
                if self.x + self.img.get_width() + ARCHER_RANGE >= opp.x:
                    self.opponent_det = True
            elif self.team == 'red' and opp.team == 'blue':
                if self.x - ARCHER_RANGE - self.img.get_width() <= opp.x:
                    self.opponent_det = True

        if self.team == 'blue':
            if self.x + self.img.get_width() + ARCHER_RANGE >= SCREEN_WIDTH - WALL_POS:
                self.opponent_det = True
        elif self.team == 'red':
            if self.x - ARCHER_RANGE <= WALL_POS:
                self.opponent_det = True


        if self.status == 'marching':
            if not self.opponent_det:
                if self.team == 'blue':
                    self.x += self.vel
                else:
                    self.x -= self.vel
            else:
                self.status = 'attacking'
                if self.team == 'blue':
                    self.img = pygame.image.load('images/BLUE/archer/ready.png')
                else:
                    self.img = pygame.image.load('images/RED/archer/ready.png')


        if self.status == 'attacking':

            # attack swordsman opponent
            for opp in swords_disp:
                if self.team == 'blue' and opp.team == 'red':
                    if self.x + self.img.get_width() + ARCHER_RANGE >= opp.x:
                        if self.rest == 0:
                            self.shoot()
                elif self.team == 'red' and opp.team == 'blue':
                    if self.x - ARCHER_RANGE - self.img.get_width() <= opp.x:
                        if self.rest == 0:
                            self.shoot()
            
            # attack archer opponent
            for opp in archers_disp:
                if self.team == 'blue' and opp.team == 'red':
                    if self.x + self.img.get_width() + ARCHER_RANGE >= opp.x:
                        if self.rest == 0:
                            self.shoot()
                elif self.team == 'red' and opp.team == 'blue':
                    if self.x - ARCHER_RANGE - self.img.get_width() <= opp.x:
                        if self.rest == 0:
                            self.shoot()

            # attack wall
            if self.team == 'blue':
                if self.x + self.img.get_width() + ARCHER_RANGE >= SCREEN_WIDTH - WALL_POS:
                    self.shoot()
            else:
                if self.x - ARCHER_RANGE <= WALL_POS:
                    self.shoot()


    def shoot(self):
        if self.rest == 0:
            if self.team == 'blue':
                self.img = pygame.image.load('images/BLUE/archer/shoot-1.png')
            else:
                
                self.img = pygame.image.load('images/RED/archer/shoot-1.png')
            self.arrows.append(Arrow(self.x + self.rect.width, self.team))
            self.rest = ARCHER_REST

            

    def display(self, win):
        win.blit(self.img, (self.x, SCREEN_HEIGHT - GROUND_HEIGHT - self.img.get_height()))

class Arrow:
    def __init__(self, x, team):
        self.x = x
        self.team = team

        if self.team == 'red':
            self.img = pygame.image.load('images/arrow.png')
        else:
            self.img = pygame.transform.flip(pygame.image.load('images/arrow.png'), 1, 0)
        self.rect = self.img.get_rect()
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 15

    def update(self):

        self.rect.x = self.x

        # move the arrow
        if self.team == 'blue':
            self.x += ARROW_SPEED
        else:
            self.x -= ARROW_SPEED


    def display(self, win):
        win.blit(self.img, (self.x, SCREEN_HEIGHT - GROUND_HEIGHT - 15))

class Projectile:
    def __init__(self, team, stopx, stopy):
        self.team = team
        self.y = TOWER_HEIGHT - 10
        self.img = pygame.image.load('images/projectile.png')
        self.rect = self.img.get_rect()
        self.stopx = stopx
        self.stopy = stopy-2

        if self.team == 'blue':
            self.x = WALL_POS
        else:
            self.x = SCREEN_WIDTH - WALL_POS

    def update(self):

        self.rect.x, self.rect.y = self.x, self.y

        dx = self.stopx - self.x
        dy = self.stopy - self.y

        angle = math.atan2(dx, dy)
        mvx = math.sin(angle)
        mvy = math.cos(angle)

        self.x += mvx * TOWER_SPEED
        self.y += mvy * TOWER_SPEED

    def display(self, win):
        win.blit(self.img, (self.x, self.y))