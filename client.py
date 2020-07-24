import os
import pickle
import random
import sys

import numpy as np
import pygame
import pygame.gfxdraw

import germ
import grid
from network import Network


def generate_color():
        '''
        Generates two colors with a random hue
        '''

        color_a = pygame.Color(0,0,0)
        hue = random.randint(0,360)
        color_a.hsla = (hue, 100, 51, 1)

        color_b = pygame.Color(0,0,0)
        color_b.hsla = (hue, 100, 40, 1)

        return (color_a[:-1], color_b[:-1])

pygame.init()

WIDTH = 800
HEIGHT = 800
FPS = 60

button_color = generate_color()
button_state = 0
b_c = 0
text_string = ""
ip_string = ""

screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()

running = True
mode = "Start-Screen"
custom_font = '.\cfonts\Lato-Black.ttf'
dark_mode = False
selected_box = "name_box"

grid = None
inputs = []

while running:
    pygame.display.set_caption("Agario in Pygame | By Ray")
    if dark_mode:
        background_color = (25, 26, 31)
        boundary_color = (13, 13, 15)
        line_color = (66, 66, 66)
        text_color = (207, 207, 207)
    else:
        background_color = (245,245,245)
        boundary_color = (230,230,230)
        line_color = (200, 200, 205)
        text_color = (38, 38, 38)

    if mode == "Start-Screen":

        clock.tick(FPS)

        start_button = pygame.Rect(0,0,200,100)
        start_button.centerx = int(WIDTH/2)
        start_button.centery = int(HEIGHT*0.55)

        text_box = pygame.Rect(0,0,200,70)
        text_box.centerx = int(WIDTH/2)
        text_box.centery = int(HEIGHT*0.4)

        ip_box = pygame.Rect(0,0,400,60)
        ip_box.centerx = int(WIDTH/2)
        ip_box.centery = int(WIDTH-50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    b_c = 1
            else:
                b_c = 0
            
            if event.type == pygame.MOUSEBUTTONUP:
                m_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(m_pos):
                    mode = "Game"
                    inputs = [0,(0,0), [], text_string] # Mouse pos, keyboard inputs, name
                    n = Network(ip_string)
                    grid = n.send(inputs)
                    id_ = n.client.getsockname()[1]
                elif text_box.collidepoint(m_pos):
                    selected_box = "name_box"
                elif ip_box.collidepoint(m_pos):
                    selected_box = "ip_box"
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_BACKSPACE:
                    if selected_box == "name_box":
                            text_string = text_string[:-1]
                    elif selected_box == "ip_box":
                            ip_string = ip_string[:-1]
                    
                elif event.key == pygame.K_F1:
                    dark_mode = not dark_mode
                else:
                    if len(text_string) < 10:
                        if selected_box == "name_box":
                            text_string += event.unicode
                        elif selected_box == "ip_box":
                            ip_string += event.unicode

        #print(b_c)
        # Draw the background
        screen.fill((background_color))
        grid_w = 20
        for i in range(grid_w):
            pygame.gfxdraw.line(screen, 0, int(i*HEIGHT/grid_w), WIDTH, int(i*HEIGHT/grid_w), line_color)
            pygame.gfxdraw.line(screen, int(i*WIDTH/grid_w), 0, int(i*WIDTH/grid_w), HEIGHT, line_color)

        # Start button
        font = pygame.font.Font(custom_font,70)
        font2 = pygame.font.Font(custom_font,30)

        pygame.draw.rect(screen, button_color[b_c],start_button,2)
        pygame.draw.rect(screen, button_color[b_c], (start_button.x, start_button.y,200,100))

        pygame.draw.rect(screen, (0,0,0), text_box, 2)
        pygame.draw.rect(screen, (0,0,0), ip_box, 2)

        button_text = font.render("Join",True,text_color)
        screen.blit(button_text, (start_button.x+37,start_button.y+7))

        text_box_text = font2.render(text_string,True,text_color)
        screen.blit(text_box_text, (text_box.x+10, text_box.y+15) )

        ip_box_text = font2.render(ip_string, True, text_color)
        screen.blit(ip_box_text, (ip_box.x+10, ip_box.y+12))

        texts = [
            "Press 'f1' for dark mode"
        ]
 
        font3 = pygame.font.Font(custom_font, 20)
        for i, t in enumerate(texts):
            text = font3.render(t, True, text_color)
            screen.blit(text, (20,(25*i)+10))

        pygame.display.flip()

    if mode == "Game":
        clock.tick(FPS)

        grid = n.send([id_, pygame.mouse.get_pos(), inputs, text_string])
        inputs = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                if event.button == 4:
                    # mw up
                    player.scale += 0.01
                elif event.button == 5:
                    # mw down
                    player.scale -= 0.01

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    inputs.append('space')
                if event.key == pygame.K_s:
                    inputs.append('s')

        # Boundary color
        screen.fill(boundary_color)

        if len(grid.germs[id_]) < 1:
            mode = "Game-Over"
            continue
        else:
            player = grid.germs[id_][0]

        # Germ position difference
        dx = int(player.pos[0]*player.scale) - int(WIDTH/2)
        dy = int(player.pos[1]*player.scale) - int(WIDTH/2)

        # Draw background if existant
        pygame.draw.rect(screen, background_color, (0-dx, 0-dy, int(grid.size[0]*player.scale), int(grid.size[1])*player.scale))
        # Draw grid lines
        grid_w = int(grid.grid_w * player.scale)
        for i in range(1,int(grid.size[0]/grid_w)):
            i = i*player.scale
            pygame.gfxdraw.line(screen, int(i*grid_w)-dx, 0-dy, int(i*grid_w)-dx, int(grid.size[1]*player.scale)-dy, line_color)
            pygame.gfxdraw.line(screen, 0-dx, int(i*grid_w)-dy, int(grid.size[0]*player.scale)-dx, int(i*grid_w)-dy, line_color)

        # Draw each cell
        for cell in grid.cells:
            if not cell:
                continue
            if (cell.pos[0]*player.scale) - dx > 0 and (cell.pos[0]*player.scale) - dx < (WIDTH/player.scale) and \
                (cell.pos[1]*player.scale) - dy > 0 and (cell.pos[1]*player.scale) - dy < (HEIGHT/player.scale):

                pygame.gfxdraw.aacircle(screen, int(cell.pos[0]*player.scale)-dx, int(cell.pos[1]*player.scale)-dy, int(cell.rad*player.scale), cell.color)
                pygame.gfxdraw.filled_circle(screen, int(cell.pos[0]*player.scale)-dx, int(cell.pos[1]*player.scale)-dy, int(cell.rad*player.scale), cell.color)
            

        # Draw the player germ
        for germ_id in grid.germs:
            for germ in grid.germs[germ_id]:
                pygame.gfxdraw.aacircle(screen, int(germ.pos[0]*player.scale)-dx, int(germ.pos[1]*player.scale)-dy, int(germ.radius*player.scale), germ.color[1])
                pygame.gfxdraw.filled_circle(screen, int(germ.pos[0]*player.scale)-dx, int(germ.pos[1]*player.scale)-dy, int(germ.radius*player.scale) , germ.color[1])
                pygame.gfxdraw.aacircle(screen, int(germ.pos[0]*player.scale)-dx, int(germ.pos[1]*player.scale)-dy, int(germ.radius*0.85*player.scale) , germ.color[0])
                pygame.gfxdraw.filled_circle(screen, int(germ.pos[0]*player.scale)-dx, int(germ.pos[1]*player.scale)-dy, int(germ.radius*0.85*player.scale) , germ.color[0])

                germ.update(pygame.mouse.get_pos())

                if germ.name != None:
                    font2 = pygame.font.Font(custom_font,35)
                    name_text = font2.render(germ.name, True, text_color)
                    x1, y1 = name_text.get_size()
                    screen.blit(name_text, (int(germ.pos[0]*player.scale)-dx-int(x1/2),int(germ.pos[1]*player.scale)-dy-int(y1/2)))
              

        # Draw text
        total_mass = sum(x.mass for x in grid.germs[id_])
        texts = [
            f"Mass: {total_mass}",
            f"Germs: {len(grid.germs[id_])}",
            "",
            f"Ping: {n.ping}",
            f"FPS: {round(clock.get_fps(),2)}",
        ]
 
        font3 = pygame.font.Font(custom_font, 20)
        for i, t in enumerate(texts):
            text = font3.render(t, True, text_color)
            screen.blit(text, (20,(25*i)+10))
        #text = font3.render(f"Ping: {n.ping}",True,text_color)
        #screen.blit(text, (20,10))

        pygame.display.flip()

    if mode == "Game-Over":
        mode = "Start-Screen"

pygame.quit()
