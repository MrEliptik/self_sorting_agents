from agent import Agent
from random import randrange
import numpy as np
import time

AGENT_NB = 50
TICKS_SEC = 60

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

    print_agents(agents)

    # Infinite loop
    try:
        while True:
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

            print_agents(agents)

            print_agents_values(agents)

            # Check if values are correctly organized
            if np.array_equal([agent.value for agent in agents], wanted_result):
                print("\nORDER IS BACK!!")
                break
            ticks += 1

            # Sleep a bit
            time.sleep(1/TICKS_SEC)
    except KeyboardInterrupt:
        print('interrupted!')

def print_agents(agents):
    print([str(agent) for agent in agents])

def print_agents_values(agents):
    print([agent.value for agent in agents])

def print_agents_positions(agents):
    print([agent.position for agent in agents])

if __name__ == "__main__":
    main()