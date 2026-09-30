import pygame as pg
from math import exp

pg.init()
win = pg.display.set_mode((300, 800))

dt = 1e-3
planet_mass = 7.36e22 #kg
planet_radius = 1737100 #m
G = 6.6759e-11


class Ship:
    def __init__(self):
        self.mass = 1000 #kg
        self.max_trust = 10000 #N
        self.height = 100000 #m
        self.thrust = 0  #N
        self.V = 0 #m/s^2
        self.I = 0
        self.V_want = 60 #m/s
        self.prev_err=0
        self.K_i = 20
        self.K_p = 200
        self.K_d = 0.05

    def calculate_acceleration(self):
        g = G*planet_mass/(self.height+planet_radius)/(self.height+planet_radius)
        a_E = self.thrust/self.mass
        return g-a_E

    def move(self):
        a = self.calculate_acceleration()
        if self.height>0:
            self.V += a*dt
            self.height -= self.V*dt
        elif a < 0:
            self.V += 0 + a*dt
            if self.V < 0:
                self.height -= self.V*dt
        else:
            self.V = 0
        if  self.mass > 300:
            self.thrust = self.PROP()+self.INT()+self.DIF()
        else:
            self.thrust=0
            self.I = 0
        if self.thrust>0 and self.mass>300:self.mass-=self.thrust/20000000
        
        filea.write(str(self.thrust)+'\n')
        fileb.write(str(self.V)+'\n')
        filec.write(str(self.mass)+'\n')
        print(f'h = {f"{self.height:.2f}".zfill(9)}; V = {self.V:.2f}; F = {self.thrust:.2f}, m = {self.mass:.2f}', end = '\t\t\t\r')

    def INT(self):
        self.I+=(self.V-self.V_want)*dt*self.K_i*(0<=self.thrust<=10000)
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
a = Ship()
filea = open('a.txt', 'w')
fileb = open('b.txt', 'w')
filec = open('c.txt', 'w')
while True:
    a.move()
    win.fill((0,0,0))
    
    pg.draw.rect(win, (255, 255, 255), ((145, 790-(a.height/120000*800), 10, 10)))
    pg.display.update()
    if a.height<=0:
        filea.close()
        fileb.close()
        filec.close()
        break