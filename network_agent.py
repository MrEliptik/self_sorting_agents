from random import randrange
from random import choices
import itertools
import time
import sys
import pygame
import argparse
import numpy as np
from math import sqrt as sqrt

class GUI():

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(BLACK)

        '''
        # Horizontal lines
        for i in range(1, ROWS):
            pygame.draw.line(self.screen, BLACK, [0, int((HEIGHT/ROWS)*i)], [WIDTH, int((HEIGHT/ROWS)*i)], ROWS)
        # Vertical lines
        for i in range(1, COLS):
            pygame.draw.line(self.screen, BLACK, [int((WIDTH/COLS)*i), 0], [int((WIDTH/COLS)*i), HEIGHT], COLS)
        '''

    def clearScreen(self):
        self.screen.fill(WHITE)

        # Horizontal lines
        for i in range(1, ROWS):
            pygame.draw.line(
                self.screen, BLACK, [0, int((HEIGHT/ROWS)*i)], [WIDTH, int((HEIGHT/ROWS)*i)], ROWS)
        # Vertical lines
        for i in range(1, COLS):
            pygame.draw.line(
                self.screen, BLACK, [int((WIDTH/COLS)*i), 0], [int((WIDTH/COLS)*i), HEIGHT], COLS)

    def drawCircle(self, pos, radius, color):
        x = int(WIDTH/COLS*pos[0] + CELL_WIDTH/2)
        y = int(HEIGHT/COLS*pos[1] + CELL_HEIGHT/2)
        pygame.draw.circle(self.screen, color, (x, y), int(CELL_WIDTH/2), 1)

    def playerInput(self):
        running = True
        while running:
            for event in pygame.event.get():
                # handle MOUSEBUTTONUP
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    return
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
        center_yes_x = WIDTH/4
        center_yes_y = HEIGHT/4
        center_no_x = (WIDTH/4)*2
        center_no_y = (HEIGHT/4)
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
        screen.blit(label, ((WIDTH/2)-(font_size/3)*len(txt), (HEIGHT/4)*line))
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
    def __init__(self, position):
        self.position = position
        self.connections = []

    def __str__(self):
        return 'position: {}    connections: {}'.format(self.position, self.connections)


    # In this method, we can define all sorts of rules to change
    # the behavior of the agents
    def update(self, neighborhood):
        impossible = True
        while impossible:
            dir = choices(DIRECTIONS, CHANCES)
            if dir[0] == "forward":
                if neighborhood[self.position[0]][self.position[1]-1] == None:
                    self.position = (self.position[0], self.positiob[1]-1)
                    impossible = False
            elif dir[0] == "left":
                if neighborhood[self.position[0]-1][self.position[1]] == None:
                    self.position = (self.position[0]-1, self.positiob[1])
                    impossible = False
            elif dir[0] == "right":
                if neighborhood[self.position[0]+1][self.position[1]] == None:
                    self.position = (self.position[0]+1, self.positiob[1])
                    impossible = False
            elif dir[0] == "backwards":
                if neighborhood[self.position[0]][self.position[1]+1] == None:
                    self.position = (self.position[0], self.positiob[1]+1)
                    impossible = False

        for i in range(len(neighborhood[0])):
            for j in range(len(neighborhood[1])):
                pass

def draw_all_agents(gui, agents):
    for i in range(ROWS):
        for j in range(COLS):
            if agents[i][j] != None:
                gui.drawCircle(agents[i][j].position, RADIUS, (255, 0, 0))

def main():
    gui = GUI()

    ticks = 0

    print("###### INITIAL PLACEMENT ######")

    # Create X agents with ordonned values
    # and random position
    agents = [[None for i in range(ROWS)] for j in range(COLS)]

    for x in range(AGENT_NB):
        i, j = randrange(ROWS), randrange(COLS)
        agents[i][j] = Agent((randrange(ROWS), randrange(COLS)))

    draw_all_agents(gui, agents)

    # Click to start
    gui.playerInput()

    # Infinite loop
    try:
        while True:
            print("###### TICK: {} ######".format(ticks))

            for i in range(ROWS):
                for j in range(COLS):
                    if agents[i][j] != None:

                        neighborhood = agents[i-NEIGHBORHOOD_SIZE:i+NEIGHBORHOOD_SIZE][j-NEIGHBORHOOD_SIZE:j+NEIGHBORHOOD_SIZE]

                        agents[i][j].update(neighborhood)

            draw_all_agents(gui, agents)

            ticks += 1

            # Sleep a bit
            time.sleep(1/TICKS_SEC)
    except KeyboardInterrupt:
        print('interrupted!')

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, help="grid number of rows")
    parser.add_argument("--cols", type=int, help="grid number of columns")
    parser.add_argument("--width", type=int, help="window width")
    parser.add_argument("--height", type=int, help="window height")
    args = parser.parse_args()

    if args.rows != None: ROWS = args.rows
    if args.cols != None: COLS = args.cols
    if args.width != None: WIDTH = args.width
    if args.height != None: HEIGHT = args.height

    print(args)

    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    BLUE = 52, 116, 235
    GREEN = 52, 235, 137
    RED = 235, 52, 91
    YELLOW = 252, 194, 3
    size = WIDTH, HEIGHT = 1024, 1024
    font_size = 60
    COLORS = [RED, YELLOW, BLUE]

    ROWS = COLS = 30
    CELL_WIDTH = WIDTH/COLS
    CELL_HEIGHT = HEIGHT/ROWS
    AGENT_NB = int(ROWS*COLS/4)
    TICKS_SEC = 60
    RADIUS = 20
    NEIGHBORHOOD_SIZE = 5 # square of SIZE*SIZE around the agent

    DIRECTIONS = ["forward", "left", "right", "backwards"]
    CHANCES = [0.5, 0.2, 0.2, 0.1]

    main()