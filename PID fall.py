import pygame as pg
from math import exp

pg.init()
win = pg.display.set_mode((300, 800))

dt = 1e-3
planet_mass = 7.36e22  # kg
planet_radius = 1737100  # m
G = 6.6759e-11


def load_sprites():
    sprites = []
    for thrust in range(0, 101, 25):
        sprites.append(pg.image.load(f'sprites/{thrust}.png'))
    return tuple(sprites)


class Ship:
    def __init__(self, K_p, K_i, K_d, x):
        self.mass = 1000  # kg
        self.max_trust = 2000  # N
        self.height = 10000  # m
        self.thrust = 0  # N
        self.V = 0  # m/s^2
        self.I = 0
        self.x = x
        self.name = 'Ship A'
        self.V_want = 60  # m/s
        self.prev_err = 0
        self.K_i = K_i
        self.K_p = K_p
        self.K_d = K_d
        self.sprites = load_sprites()

    def calculate_acceleration(self):
        g = G*planet_mass/(self.height+planet_radius) / \
            (self.height+planet_radius)
        a_E = self.thrust/self.mass
        return g-a_E

    def move(self):
        a = self.calculate_acceleration()
        if self.height > 100:
            self.V += a*dt
            self.height -= self.V*dt
        elif a < 0:
            self.V += 0 + a*dt
            if self.V < 0:
                self.height -= self.V*dt
        else:
            self.V = 0
        if self.mass > 300:
            self.thrust = self.PROP()+self.INT()+self.DIF()
        else:
            self.thrust = 0
            self.I = 0
        if self.thrust > 0 and self.mass > 300:
            self.mass -= self.thrust/2000000

        print(f'h = {f"{self.height:.2f}".zfill(9)}; V = {self.V:.2f}; F = {
              self.thrust:.2f}, m = {self.mass:.2f}', end='\t\t\t\r')

    def INT(self):
        self.I += (self.V-self.V_want)*dt*self.K_i * \
            (0 <= self.thrust <= self.max_trust)
        return self.I

    def PROP(self):
        self.P = (self.V-self.V_want)*self.K_p
        if self.P > 0:
            return self.P
        else:
            return 0

    def DIF(self):
        self.err = (self.V-self.V_want)
        self.D = (self.err-self.prev_err)/dt*self.K_d
        self.prev_err = self.err
        return self.D

    def render_ship(self):
        sprite_num = abs(round((self.thrust/self.max_trust)*4))
        try:
            sprite = self.sprites[sprite_num]
        except IndexError:
            sprite = self.sprites[0]
        win.blit(sprite, (self.x, 790-(self.height/10000*800)))
    
    def change_PID(self, K_p, K_i, K_d):
        self.K_p=K_p
        self.K_i=K_i
        self.K_d=K_d


ships = [Ship(200, 60, 2, 50), Ship(100, 30, 2, 100), Ship(50, 30, 2, 150)]
run = True
while run:
    win.fill((0, 0, 0))
    for ship in ships:
        ship.move()
        ship.render_ship()
    events = pg.event.get()
    ships[0].change_PID((10000-ships[0].height)/100, ships[0].K_i, ships[0].K_d)
    for i in events:
        if i.type == pg.QUIT:
            run = False
    pg.display.update()
