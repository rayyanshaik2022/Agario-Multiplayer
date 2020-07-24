import pickle
import socket
import sys

import pygame

from _thread import *
from germ import Germ
from grid import Grid

server = "192.168.0.6"
port = 5555
grid_s = [2000,2000]
cells_s = 400

def prompt():
    ip = str(input("Ip Address [enter for local] : "))
    if ip == "":
        ip = ""
    elif "." not in ip:
        ip = "192.168.0.6"

    port = str(input("Ip Address [enter for port 5555] : "))
    if port == "":
        port = 5555
    else:
        port = int(port)

    grid_s = str(input("Grid Size as tuple (width,length) : "))

    try:
        grid_s = grid_s.split(",")
        print(grid_s)
        try:
            new_grid_s = [int(grid_s[0][1:]), int(grid_s[1][:-1])]
        except error as e:
            print(e)
        if new_grid_s[0] > 10000 or new_grid_s[0] < 5 or \
            new_grid_s[1] > 10000 or new_grid_s[1] < 5:
            grid_s = [2000,2000]
        else:
            grid_s = new_grid_s
    except:
        grid_s = [2000,2000]
    
    cells_s = int(input("Maximum food cells (n<400) : "))
    if cells_s > 400 or cells_s < 0:
        cells_s = 400

    return ip, port, grid_s, cells_s
server, port, grid_s, cells_s = prompt()

print(f"Attempting to start server on ({server},{port})")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(('', port))

except socket.error as e:
    print(str(e))
    print("Server will start on local address")


s.listen(2)
print("Waiting for a connection, Server Started")

class local:
    # Data is stored in a class to be easily accessed across threads
    # Grid setup occurs here
    grid = Grid(grid_s, cells_s)
    data = {}
    clock = pygame.time.Clock()
    once = 0


def threaded_client(conn):
    '''
    A threaded function that opens for each connected client.
    It receives input data and sends the current grid state
    '''

    conn.send(pickle.dumps("Connected"))
    last_addr = None
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            local.data[data[0]] = data[1:]
            last_addr = data[0]
            reply = local.grid

            if not data:
                print("Disconnected")
                break
            else:
                #print("Received input", data)
                #print("Sending grid state:",reply)
                pass
            
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    print("Removing cells from",last_addr)
    del local.grid.germs[last_addr]
    conn.close()

def update_grid():
    '''
    Function that manages the game/grid state.
    Using a clock, it updates 60 times a
    second (60 ticks)
    '''

    UPS = 60 # Updates per second
    while True:
        local.clock.tick(UPS)

        for id_ in local.grid.germs:
            for germ in local.grid.germs[id_]:
                try:
                    germ.update(local.data[id_][0])
                    germ.name = local.data[id_][2]

                    for event in local.data[id_][1]:
                        if event == 'space':
                            local.grid.cells.append(germ.eject())
                        elif event == 's':
                            splitter = germ.split()
                            if splitter:
                                local.grid.germs[id_].append(splitter)
                except:
                    pass

        local.grid.update_cells()
        local.grid.update_germ_pvp()

start_new_thread(update_grid, ())
while True:
    conn, addr = s.accept()
    print("Connection from:",addr)
    print("Added germ for", addr)

    germ = Germ(local.grid)
    germ.id = addr[1]
    local.grid.add_germ(germ, addr[1])
    local.once = addr[1]

    start_new_thread(threaded_client, (conn,))
