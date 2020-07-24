from pygame.color import Color
import random
import math

class Cell:

    def __init__(self, position, radius, value):
        self.pos = [*position]
        self.rad = radius
        self.mass = value
        self.acc = [0,0]
        self.angle = 0
        self.color = self.generate_color()
    
    def update_position(self):
        '''
        To be run server-side. It adds velocity/acceleration
        to the cells current position
        '''

        FRICTION = 0.92
        vx = 0
        vy = 0
        
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
        

        self.pos[0] += int(vx)
        self.pos[1] += int(vy)
        
    
    def generate_color(self):
        '''
        Generates a color with a random hue
        '''
        
        color = Color(0,0,0)
        color.hsla = (random.randint(0,360), 100, 51, 1)

        return color[:-1]
