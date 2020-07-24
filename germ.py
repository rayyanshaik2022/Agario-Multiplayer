import math
import random

from pygame.color import Color

from cell import Cell
from constants import *


class Germ:
    def __init__(self, grid):
        self.grid = grid
        self.mass = 10
        self.angle = 2 * math.pi
        self.acc = [10,10]
        self.pos = [ random.randint(0, grid.size[0]), random.randint(0, grid.size[1]) ]
        self.speed = 3
        self.radius = max(int(self.mass ** (1/3)), 30)
        self.scale = 1

        self.color = self.generate_color()
        self.id = None
        self.name = None

    def eject(self):
        '''
        Subtracts mass from the user germ
        and spawns a new cell with acceleration
        (effectively shooting it)
        '''

        if self.mass > 50:
            self.mass -= 35
            px = int(math.cos(self.angle) * self.radius * 1.2) 
            py = int(math.sin(self.angle) * self.radius * 1.2)

            new_cell = Cell([self.pos[0]+px, self.pos[1]+py], 15, 35)

            new_cell.color = self.color[0]
            new_cell.angle = self.angle
            new_cell.acc = [20, 20]

            return new_cell

    def split(self):
        '''
        Splits the germ if its mass is large enough.
        The newly created germ will be given accelerated
        and effectively "shot out" from the current germ.
        The new germ will be controllable via mouse input
        and will act exactly as its parent germ
        '''

        if self.mass > 650:
            main = self.mass - int(self.mass*0.4)
            new = self.mass - int(self.mass*0.6)
            self.mass = main

            px = int(math.cos(self.angle) * self.radius * 1.2) 
            py = int(math.sin(self.angle) * self.radius * 1.2)

            new_germ = Germ(self.grid)
            new_germ.mass = new
            new_germ.pos = [self.pos[0]+px,self.pos[1]+py]
            new_germ.angle = self.angle
            new_germ.acc = [30,30]
            new_germ.color = self.color
            new_germ.id = self.id

            return new_germ
        return

    def update(self, m_pos):
        '''
        Based on the mouse position, an angle is calculated.
        Using the angle and current mass, a direction and
        magnitude will be generated to move an individual
        germ at the calculated rate
        '''

        FRICTION = 0.92
        
        o, a = m_pos[0]-int(WIDTH/2), m_pos[1]-int(HEIGHT/2)
        self.angle = math.atan2(a,o)
        vx = math.cos(self.angle) * self.speed
        vy = math.sin(self.angle) * self.speed

        # Add acceleration to vx, vy
        if self.acc[0] > 0.2:
            vx = math.cos(self.angle) * self.acc[0]
            self.acc[0] *= FRICTION
        else:
            self.acc[0] = 0
        
        if self.acc[1] > 0.2:
            vy = math.sin(self.angle) * self.acc[1]
            self.acc[1] *= FRICTION
        else:
            self.acc[1] = 0

        # move & check if out of bounds
        self.pos[0] += int(vx)
        self.pos[1] += int(vy)

        if self.pos[0] > self.grid.size[0]:
            self.pos[0] = self.grid.size[0]
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[1] > self.grid.size[1]:
            self.pos[1] = self.grid.size[1]
        if self.pos[1] < 0:
            self.pos[1] = 0


        # update radius by size (max size)
        if self.mass > 3500:
            self.mass = 3500
        
        # update scale by size
        self.scale = (-7/69980)*sum(x.mass for x in self.grid.germs[self.id]) + 1
    
        self.radius = max(int(self.mass ** (0.65)), 30)
        self.speed = max(5 * (self.mass**-0.2)+2.5, 3)

    def generate_color(self):
        '''
        Generates colors with the same
        random hue
        '''

        hue = random.randint(0,360)

        color_a = Color(0,0,0)
        color_a.hsla = (hue, 100, 51, 1)

        color_b = Color(0,0,0)
        color_b.hsla = (hue, 100, 40, 1)

        return (color_a[:-1], color_b[:-1])
