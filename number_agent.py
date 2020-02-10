from random import randrange
import numpy as np
import time
import sys

class Agent:
    def __init__(self, value, position):
        self.value = value
        self.position = position

    def __str__(self):
        return 'Value: {} Pos: {}'.format(self.value, self.position)

    # neighbors[0] left neighbor
    # neighbor[1] right neighbor
    def update(self, neighbors):
        # Check left first, because we want
        # to sort in ascending order
        # -1 means there's no neighbor
        if neighbors[0] != None:
            if neighbors[0].value > self.value:
                # swap position
                neighbors[0].position, self.position = self.position, neighbors[0].position
        elif neighbors[1] != None:
            if neighbors[1].value < self.value:
                # swap position
                neighbors[1].position, self.position = self.position, neighbors[1].position


AGENT_NB = 30
TICKS_SEC = 10

def main():
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

    print_agents_values(agents)

    # Infinite loop
    try:
        while True:
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[F")
            print("###### TICK: {} ######".format(ticks))
            # Loop through agents to update
            for (i, agent) in enumerate(agents):
                # Check if lower-edge of the array
                if i == 0:
                    neigbors = [None, agents[i+1]]
                # Check if upper-edge of the array
                elif i == AGENT_NB - 1:
                    neigbors = [agents[i-1], None]
                else:
                    neigbors = [agents[i-1], agents[i+1]]

                agent.update(neigbors)

                # Reorganize agent in the array based
                # on their position 
                agents[agent.position] = agent
                if neigbors[0] != None:
                    agents[neigbors[0].position] = neigbors[0]
                elif neigbors[1] != None:
                    agents[neigbors[1].position] = neigbors[1]

            #print_agents(agents, False)

            print_agents_values(agents, False)

            # Check if values are correctly organized
            if np.array_equal([agent.value for agent in agents], wanted_result):
                print("\nORDER IS BACK!!")
                break
            ticks += 1

            # Sleep a bit
            time.sleep(1/TICKS_SEC)
    except KeyboardInterrupt:
        print('interrupted!')

def print_agents(agents, dynamically=False):
    if dynamically:
        print([str(agent) for agent in agents], end="\r")
    print([str(agent) for agent in agents])

def print_agents_values(agents, dynamically=False):
    if dynamically:
        print([agent.value for agent in agents], end="\r")
    print([agent.value for agent in agents])

def print_agents_positions(agents, dynamically=False):
    if dynamically:
        print([agent.position for agent in agents], end="\r")
    print([agent.position for agent in agents])

if __name__ == "__main__":
    main()