from random import randrange
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
                self.screen, BLACK, [0, (height/ROWS)*i], [width, ((height/ROWS)*i)], ROWS)
        # Vertical lines
        for i in range(1, COLS):
            pygame.draw.line(
                self.screen, BLACK, [(width/COLS)*i, 0], [((width/COLS)*i), height], COLS)

    def drawRect(self, cell, color, refresh=False):
        pygame.draw.rect(self.screen, color, 
            pygame.Rect(
                cell_width*cell[0], 
                cell_width*cell[1], 
                cell_width, 
                cell_height), 0)
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
        return 'color: {} Pos: {}'.format(self.color, self.position)

    # neighbors[0] left neighbor
    # neighbor[1] top neighbor
    # neighbor[2] right neighbor
    # neighbor[3] down neighbor
    def update(self, neighbors):
        # Check left first, because we want
        # to sort in ascending order
        # -1 means there's no neighbor
        if neighbors[0] != None:
            if neighbors[0].color > self.color:
                # swap position
                neighbors[0].position, self.position = self.position, neighbors[0].position
        elif neighbors[1] != None:
            if neighbors[1].color < self.color:
                # swap position
                neighbors[1].position, self.position = self.position, neighbors[1].position
        elif neighbors[2] != None:
            if neighbors[2].color < self.color:
                # swap position
                neighbors[2].position, self.position = self.position, neighbors[1].position


AGENT_NB = 30
TICKS_SEC = 1

def main():
    gui = GUI()

    ticks = 0

    print("###### INITIAL PLACEMENT ######")

    # Create X agents with ordonned values
    # and random position
    positions = np.arange(AGENT_NB)
    np.random.shuffle(positions)

    agents = AGENT_NB*[None]
    wanted_result = AGENT_NB*[None]
    for i in range(AGENT_NB):
        agents[positions[i]] = Agent(i, positions[i])
        wanted_result[i] = i

    # Infinite loop
    try:
        while True:
            gui.clearScreen()
            gui.drawRect((ticks%3, 0), BLUE)
            gui.update()

            ticks += 1

            # Sleep a bit
            time.sleep(1/TICKS_SEC)
    except KeyboardInterrupt:
        print('interrupted!')

if __name__ == "__main__":
    main()