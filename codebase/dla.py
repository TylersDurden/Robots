import matplotlib.pyplot as plt, matplotlib.animation as animation
import numpy as np
import utility

class walker:
    steps = []
    position = []
    state = [[]]
    depth = 0
    # Numbering scheme for direction keys
    # [[1,2,3],
    #  [4,5,6],
    #  [7,8,9]]
    directions = {1: 'u_left',
                  2: 'up',
                  3: 'u_right',
                  4: 'left',
                  5: 'self',
                  6: 'right',
                  7: 'd_left',
                  8: 'down',
                  9: 'd_right'}

    def __init__(self, startingPos, initial_state, steps):
        self.position = startingPos
        self.depth = steps
        self.state = initial_state
        self.random_walk(self.generate_random_steps())

    def generate_random_steps(self):
        rsteps = np.random.randint(1, 10, self.depth)
        steps = list()
        for step in rsteps:
            steps.append(self.directions[step])
        return steps

    def random_walk(self, step_keys):
        f = plt.figure()
        CenterBox = [int(self.state.shape[0]/2), int(self.state.shape[1]/2)]

        cardinal = {'u_left': [self.position[0] - 1, self.position[1] - 1],
                    'up': [self.position[0], self.position[1] - 1],
                    'u_right': [self.position[0] + 1, self.position[1] - 1],
                    'left': [self.position[0] - 1, self.position[1]],
                    'self': [self.position[0], self.position[1]],
                    'right': [self.position[0] + 1, self.position[1]],
                    'd_left': [self.position[0] - 1, self.position[1] + 1],
                    'down': [self.position[0], self.position[1] - 1],
                    'd_right': [self.position[0] + 1, self.position[1] + 1]}
        history = []
        visual = []
        for step in step_keys:
            self.state[self.position[0], self.position[1]] = 0
            card = cardinal[step]
            if abs(card[0]-self.position[0])<2 and abs(card[1]-self.position[1])<2:
                self.state[self.position] = 1
                print " ** Collision at " + str(self.position)+" **"
                break
            else:
                self.position = np.array([card[0], card[1]])
                history.append(self.position)
                self.state[card[0], card[1]] = 1
        return history


class randomlyDiffuse:
    # State variables
    state = [[]]
    dimensions = []
    # N Brownian Trees
    depth = 0
    # N Steps max per walk
    nsteps = 0

    def __init__(self, n_walkers, walk_length, window_size):
        self.nsteps = walk_length
        self.depth = n_walkers
        if len(window_size) == 2:
            self.dimensions = window_size
        self.initialize()

    def initialize(self):
        self.state = np.zeros(self.dimensions)
        # Create the center
        center_x = int(self.state.shape[0]/2)
        center_y = int(self.state.shape[1]/2)
        width = 3
        self.state[center_x-width:center_x+width,
                   center_y-width:center_y+width] = 1

        self.add_walker()

    def add_walker(self):
        start = np.array([np.random.randint(0, self.state.shape[0], 1),
                          np.random.randint(0, self.state.shape[1], 1)])
        print "starting at "+str(start)
        walker(start, self.state, self.nsteps)



def main():

    randomlyDiffuse(10, 50, [50, 50])


if __name__ == '__main__':
    main()
