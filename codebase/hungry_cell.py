import scipy.ndimage as ndi, numpy as np, utility


class Cell:
    n_steps = 0
    depth = 0

    position = []
    state = [[]]
    directions = {}

    decisions = {}

    def __init__(self, N, depth, starting_position, initial_state):
        self.n_steps = N
        self.depth = depth
        self.position = starting_position
        self.state = initial_state
        self.directions = self.initialize_directions()

    def initialize_directions(self):
        return {1:[self.position[0]-1,self.position[1]-1],
                2:[self.position[0],self.position[1]-1],
                3:[self.position[0]+1,self.position[1]-1],
                4:[self.position[0]-1,self.position[1]],
                5:[self.position[0],self.position[1]],
                6:[self.position[0]+1,self.position[1]],
                7:[self.position[0]-1,self.position[1]+1],
                8:[self.position[0],self.position[1]+1],
                9:[self.position[0]+1,self.position[1]+1]}

    def generate_random_steps(self):
        c0 = [[1,1,1],[1,1,1],[1,1,1]]

        raw_steps = np.random.randint(1, 9, self.n_steps)
        random_walk = []
        state = np.array(self.state)
        for step in raw_steps:
            self.position = self.directions[step]
            if self.state[self.position] != 1:
                for x in range(state.shape[0]):
                    for y in range(state.shape[1]):
                        pov = self.state[x-2:x+2, y-2:y+2]
                        # Determine best step and record the directions
            # random_walk.append(self.position)
        return random_walk

w = 250
h = 250
state = np.zeros((w, h))


cell = Cell(10,3, utility.spawn_random_point(state), state)
random_walk = cell.generate_random_steps()