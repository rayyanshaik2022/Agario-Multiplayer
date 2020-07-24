import math
import random

import pygame

from cell import Cell
from constants import *


class Grid:

    def __init__(self, size, cell_max):
        self.size = size
        self.grid_w = 40
        self.cells = []
        self.total_cells = cell_max
        self.cells_alive = 0
        self.address_book = {}
        self.germs = {}

        self.spawn_cells(cell_max)

    def clean_germs(self):
        '''
        Delete dictionary entries for germs/connections
        which have been eliminated or are now nonexistant
        '''

        for key in self.germs:
            if self.germs[key] == []:
                del self.germs[key]

    def add_germ(self, germ, id_):
        '''
        Adds germs by their connection id
        '''

        if id_ in self.germs:
            self.germs[id_].append(germ)
        else:
            self.germs[id_] = [germ]

    def spawn_cells(self, n):
        '''
        Spawns 'n' cells randomly across
        the grid's area
        '''

        for i in range(n):
            loc = ( random.randint(0, self.size[0]), random.randint(0, self.size[1]) )
            rad = 7
            val = random.randint(1,3)

            self.cells.append(Cell(position=loc, radius=rad, value=val))
            self.cells_alive += n

    def update_cells(self):
        '''
        Adds cells if they were eaten, 
        detects & modifies cells if they are eaten by
        a player germ
        '''

        # Respawn cells immediately after being eaten
        if len(self.cells) < self.total_cells:
            self.spawn_cells(self.total_cells - len(self.cells))
        
        for germ_id in self.germs:
            for germ in self.germs[germ_id]:
                dx = germ.pos[0] - int(WIDTH/2)
                dy = germ.pos[1] - int(HEIGHT/2)

                for cell in self.cells:
                    if not cell:
                        continue

                    cell.update_position()

                    if cell.pos[0] > self.size[0]:
                        cell.pos[0] = self.size[0]
                    if cell.pos[0] < 0:
                        cell.pos[0] = 0
                    if cell.pos[1] > self.size[1]:
                        cell.pos[1] = self.size[1]
                    if cell.pos[1] < 0:
                        cell.pos[1] = 0

                    # Check if should be eaten by germ
                    dist = int(((germ.pos[0]-cell.pos[0])**2 + (germ.pos[1]-cell.pos[1])**2 ) ** 0.5)
                    if dist < germ.radius:
                        if sum(x.mass for x in self.germs[germ.id]) < 3500:
                            germ.mass += cell.mass
                        self.cells.remove(cell)
                        #print("mass:",germ.mass, "radius:",germ.radius, "speed:",germ.speed, "id",germ.id)

    def update_germ_pvp(self):
        '''
        Checks whether player germs are/should be interacting,
        and the protocol if one is eaten.
        '''

        for germ_id in self.germs:
            for current_germ in self.germs[germ_id]:
                    
                for germ_id_ in self.germs:
                    for germ in self.germs[germ_id_]:
                        if current_germ is germ:
                            continue
                        
                        dist = int(((germ.pos[0]-current_germ.pos[0])**2 + (germ.pos[1]-current_germ.pos[1])**2 ) ** 0.5)
                        if dist < current_germ.radius and \
                            current_germ.mass > germ.mass: 
                                
                            h_id = germ.id
                            # If in the same group
                            if h_id == current_germ.id:
                                if self.germs[h_id][0] == current_germ:
                                    current_germ.mass += germ.mass
                                    self.germs[h_id].remove(germ)
                                elif self.germs[h_id][0] == germ:
                                    germ.mass += current_germ.mass
                                    self.germs[h_id].remove(current_germ)
                                else:
                                    current_germ.mass += germ.mass
                                    self.germs[h_id].remove(germ)
                            else:
                                s = sum(x.mass for x in self.germs[current_germ.id])
                                if s + germ.mass > 3500:
                                    current_germ.mass += max(0, 3500-s)
                                else:
                                    current_germ.mass += germ.mass
                                self.germs[h_id].remove(germ)
