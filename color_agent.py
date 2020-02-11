import random
import itertools
import numpy as np
import time
import sys
import pygame
from math import sqrt as sqrt

import time

WHITE = 255, 255, 255
BLACK = 0, 0, 0
BLUE = 0, 0, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
size = width, height = 640, 640
ROWS = 9
COLS = 9
cell_width = (width/COLS)
cell_height = (height/ROWS)
font_size = 60
COLORS = [BLUE, GREEN, RED]


class GUI():

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(WHITE)

        # Horizontal lines
        for i in range(1, ROWS):
            pygame.draw.line(self.screen, BLACK, [0, (height/ROWS)*i], [width, ((height/ROWS)*i)], ROWS)
        # Vertical lines
        for i in range(1, COLS):
            pygame.draw.line(self.screen, BLACK, [(width/COLS)*i, 0], [((width/COLS)*i), height], COLS)

    def clearScreen(self):
        self.screen.fill(WHITE)

        # Horizontal lines
        for i in range(1, ROWS):
            pygame.draw.line(
                self.screen, BLACK, [0, int((height/ROWS)*i)], [width, int((height/ROWS)*i)], ROWS)
        # Vertical lines
        for i in range(1, COLS):
            pygame.draw.line(
                self.screen, BLACK, [int((width/COLS)*i), 0], [int((width/COLS)*i), height], COLS)

    def drawRect(self, cell, color, refresh=False):
        pygame.draw.rect(self.screen, color, 
            pygame.Rect(
                int(cell_width*cell[0]), 
                int(cell_width*cell[1]), 
                int(cell_width), 
                int(cell_height)), 0)
        if refresh:
            self.refresh()

    def playerInput(self):
        running = True
        while running:
            for event in pygame.event.get():
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    cell = self.getCell(pos)
                    return cell[0], cell[1]
                if event.type == pygame.QUIT:
                    running = False
                self.refresh()
        pygame.quit()  # quits pygame
        sys.exit()

    def ask(self, question, line=2):
        running = True
        # "ask(screen, question) -> answer"
        pygame.font.init()
        self.writeScreen(question, line=line)
        center_yes_x = width/4
        center_yes_y = height/4
        center_no_x = (width/4)*2
        center_no_y = (height/4)
        while running:
            for event in pygame.event.get():
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                    return
                if event.type == pygame.QUIT:
                    running = False
                self.refresh()
        pygame.quit()
        sys.exit()

    def writeScreen(self, txt, line=1):
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        myfont = pygame.font.SysFont("monospace", font_size)

        # render text
        label = myfont.render(txt, 50, (0,200,0))
        screen.blit(label, ((width/2)-(font_size/3)*len(txt), (height/4)*line))
        self.refresh()

    def update(self):
        for event in pygame.event.get():
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                
            if event.type == pygame.QUIT:
                running = False

            self.refresh()

    def refresh(self):
        pygame.display.update()

class Agent:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def __str__(self):
        return 'color: {} position: {}'.format(self.color, self.position)

    # neighbors[0] left neighbor
    # neighbor[1] top neighbor
    # neighbor[2] right neighbor
    # neighbor[3] down neighbor
    def update(self, neighbors):
        # Check left first, because we want
        # to sort in ascending order
        # None means there's no neighbor
        for neighbor in neighbors:
            # First check if we have a same-color neighbor
            if neighbor != None:
                if neighbor.color == self.color:
                    # same color as a neighbor cell, don't move
                    return

        # If not the case, swap place with the first non-None neighbor
        for neighbor in neighbors:
            if neighbor != None:
                neighbor.position, self.position = self.position, neighbor.position
                return
        

def get_random_pairs(numbers):
    # Generate all possible non-repeating pairs
    pairs = list(itertools.permutations(numbers, 2))

    # Randomly shuffle these pairs
    random.shuffle(pairs)
    return pairs

def get_neighbors_position(agents, agent):
    pos = agent.position

    # left neighbor
    if pos[0] != 0:
        left_pos = (pos[0] - 1, pos[1])
    else: left_pos = None

    # top neighbor
    if pos[1] != 0:
        top_pos = (pos[0], pos[1] - 1)
    else: top_pos = None

    # right neighbor
    if pos[0] != (COLS - 1):
        right_pos = (pos[0] + 1, pos[1])
    else: right_pos = None

    # bottom neighbor
    if pos[0] != (ROWS + 1):
        bottom_pos = (pos[0], pos[1] + 1)
    else: bottom_pos = None
    
    return [left_pos, top_pos, right_pos, bottom_pos]

def get_neighbors(agents, agent):

    positions = get_neighbors_position(agents, agent)
    
    neighbors = []
    for pos in positions:
        if pos != None:
            neighbors.append(agents[((ROWS-1)*pos[0])+pos[1]])
        else: neighbors.append(None)

    return neighbors

def print_agents(agents):
    for agent in agents:
        print(agent)

AGENT_NB = ROWS*COLS
TICKS_SEC = 60

def main():
    gui = GUI()

    ticks = 0

    print("###### INITIAL PLACEMENT ######")

    # Create X agents with ordonned values
    # and random position
    agents = AGENT_NB*[None]

    for i in range(ROWS):
        for j in range(COLS):
            agents[(ROWS*i)+j] = Agent(random.choice(COLORS), (i,j))

    # sort in place
    #agents.sort(key=lambda x: x.position)

    print_agents(agents)

    # Infinite loop
    try:
        while True:
            # update agents
            for (i, agent) in enumerate(agents):
                # Check if lower-edge of the array
                neighbors = get_neighbors(agents, agent)

                agent.update(neighbors)

            # draw
            gui.clearScreen()
            for agent in agents:
                gui.drawRect(agent.position, agent.color)
            gui.update()
            
            ticks += 1

            # Sleep a bit
            time.sleep(1/TICKS_SEC)
    except KeyboardInterrupt:
        print('interrupted!')

if __name__ == "__main__":
    main()