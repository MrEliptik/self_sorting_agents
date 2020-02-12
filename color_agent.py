import random
import itertools
import time
import sys
import pygame
import argparse
import numpy as np
from math import sqrt as sqrt


WHITE = 255, 255, 255
BLACK = 0, 0, 0
BLUE = 52, 116, 235
GREEN = 52, 235, 137
RED = 235, 52, 91
size = WIDTH, HEIGHT = 1024, 1024
ROWS = 20
COLS = 20
cell_width = (WIDTH/COLS)
cell_height = (HEIGHT/ROWS)
font_size = 60
COLORS = [BLUE, GREEN, RED]

AGENT_NB = ROWS*COLS
TICKS_SEC = 60

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()        
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result    
    return timed


class GUI():

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(WHITE)

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

    def drawRect(self, cell, color, refresh=False):
        pygame.draw.rect(self.screen, color, 
            pygame.Rect(
                int(cell_width*cell[1]), 
                int(cell_height*cell[0]), 
                int(cell_width), 
                int(cell_height)), 0)
        if refresh:
            self.refresh()

    def drawID(self, cell, id):
        myfont = pygame.font.SysFont("monospace", 20)

        # render text
        label = myfont.render(id, 50, (0,0,0))
        self.screen.blit(label, (cell_width*cell[1], cell_height*cell[0]))

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
    def __init__(self, color, position, id):
        self.color = color
        self.position = position
        self.id = id

    def __str__(self):
        return 'color: {} position: {}'.format(self.color, self.position)

    # neighbors[0] left neighbor
    # neighbor[1] top neighbor
    # neighbor[2] right neighbor
    # neighbor[3] down neighbor
    # In this method, we can define all sorts of rules to change
    # the behavior of the agents
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

        ###### agent need 2 same-color neighbor to not move #####
        '''
        same_color_neighbors_count = 0
        for neighbor in neighbors:
            # First check if we have a same-color neighbor
            if neighbor != None:
                if neighbor.color == self.color:
                    # same color as a neighbor cell, don't move
                    same_color_neighbors_count += 1
                    if same_color_neighbors_count >= 2: return 
        '''

        # If not the case, swap place with the first non-None neighbor
        for neighbor in neighbors:
            if neighbor != None:
                neighbor.position, self.position = self.position, neighbor.position
                return    

        ###### swap place with a random, different-color neighbor ######
        #random.choice([neighbor for neighbor in neighbors if neighbor != None])


def get_random_pairs(numbers):
    # Generate all possible non-repeating pairs
    pairs = list(itertools.permutations(numbers, 2))

    # Randomly shuffle these pairs
    random.shuffle(pairs)
    return pairs

def get_neighbors_position(agent):
    pos = agent.position

    # left neighbor
    if pos[1] != 0:
        left_pos = (pos[0], pos[1] - 1)
    else: left_pos = None

    # top neighbor
    if pos[0] != 0:
        top_pos = (pos[0] - 1, pos[1])
    else: top_pos = None

    # right neighbor
    if pos[1] != (COLS - 1):
        right_pos = (pos[0], pos[1] + 1)
    else: right_pos = None

    # bottom neighbor
    if pos[0] != (ROWS - 1):
        bottom_pos = (pos[0] + 1, pos[1])
    else: bottom_pos = None
    
    return [left_pos, top_pos, right_pos, bottom_pos]

def get_neighbors(agents, agent):
    positions = get_neighbors_position(agent)
    
    neighbors = []
    for pos in positions:
        if pos != None:
            neighbors.append(agents[pos[0]][pos[1]])
        else: neighbors.append(None)

    return neighbors

def print_agents(agents):
    for i in range(ROWS):
        for j in range(COLS):
            print(agents[i][j])

def arange(agents, agent, neighbors):
    tmp = agents.copy()

    tmp[agent.position[0]][agent.position[1]] = agent

    for neighbor in neighbors:
        if neighbor != None:
            tmp[neighbor.position[0]][neighbor.position[1]] = neighbor

    return tmp.copy()

#@timeit
def draw_agents(gui, to_draw):
    for a in to_draw:
        if a != None:
            gui.drawRect(a.position, a.color)
            gui.drawID(a.position, a.id)
    gui.update()

#@timeit
def draw_all_agents(gui, agents):
    for i in range(ROWS):
        for j in range(COLS):
            gui.drawRect(agents[i][j].position, agents[i][j].color)
            gui.drawID(agents[i][j].position, agents[i][j].id)
    gui.update()

def main():
    gui = GUI()

    ticks = 0

    print("###### INITIAL PLACEMENT ######")

    # Create X agents with ordonned values
    # and random position
    agents = [[None for i in range(ROWS)] for j in range(COLS)]

    for i in range(ROWS):
        for j in range(COLS):
            agents[i][j] = Agent(random.choice(COLORS), (i,j), str((ROWS*i)+j))

    draw_all_agents(gui, agents)
    print_agents(agents)

    # Click to start
    gui.playerInput()

    # Infinite loop
    try:
        while True:
            print("###### TICK: {} ######".format(ticks))

            # update agents
            for i in range(ROWS):
                for j in range(COLS):   
                    #print("         AGENT: {}".format((ROWS*i)+j))

                    neighbors = get_neighbors(agents, agents[i][j])

                    agents[i][j].update(neighbors)

                    # sort in place
                    agents = arange(agents, agents[i][j], neighbors)

                    #print_agents(agents)

                    # only re-draws current agent and its neighbors
                    # in case they've changed
                    # Note: drawing all agents cost ~200ms on i7 @3Ghz
                    # vs ~4ms with only current agent & neighbors
                    draw_agents(gui, neighbors + [agents[i][j]])

                    #gui.playerInput()
            #gui.playerInput()
            
            ticks += 1

            # Sleep a bit
            time.sleep(1/TICKS_SEC)
    except KeyboardInterrupt:
        print('interrupted!')

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", help="grid number of rows")
    parser.add_argument("--cols", help="grid number of columns")
    parser.add_argument("--width", help="window width")
    parser.add_argument("--height", help="window height")
    args = parser.parse_args()

    if args.rows != None: ROWS = args.rows
    if args.cols != None: COLS = args.cols
    if args.width != None: WIDTH = args.width
    if args.height != None: HEIGHT = args.height

    main()