import matplotlib.pyplot as plt, matplotlib.animation as animation
import numpy as np, utility, sys


class MapCreation:

    state = [[]]
    dims = []
    label = ''
    pre_loaded_maps = {'box': 1, 'lattice': 2}

    def __init__(self, width, height, type):
        self.dims = [width, height]
        self.label = type
        if type in self.pre_loaded_maps.keys():
            # Simple Box in the Center
            if self.pre_loaded_maps[type] == 1:
                self.state = self.make_box()
            # Create Square Lattice
            if self.pre_loaded_maps[type] == 2:
                self.state = MapCreation.draw_square_lattice(np.zeros((width,height)))

    def add_print(self, type):
        # Simple Box in the Center
        if self.pre_loaded_maps[type] == 1:
            state = self.make_box()
        # Create Square Lattice
        if self.pre_loaded_maps[type] == 2:
            state = MapCreation.draw_square_lattice(self.state)
        return state

    def make_box(self):
        self.state = np.zeros((self.dims[0], self.dims[1]))
        center_x = int(self.dims[0]/2)
        center_y = int(self.dims[1]/2)
        # Default box size is 10
        sz = 10
        self.state[center_x-sz:center_x+sz,center_y-sz:center_y+sz] = 1
        return self.state

    @staticmethod
    def draw_square_lattice(state):
        state[30:40, 110:120] = 1
        state[30:40, 130:140] = 1

        state[50:60, 90:100] = 1
        state[50:60, 110:120] = 1
        state[50:60, 130:140] = 1
        state[50:60, 150:160] = 1

        state[70:80, 70:80] = 1
        state[70:80, 90:100] = 1
        state[70:80, 110:120] = 1
        state[70:80, 130:140] = 1
        state[70:80, 150:160] = 1
        state[70:80, 170:180] = 1

        state[90:100, 50:60] = 1
        state[90:100, 70:80] = 1
        state[90:100, 90:100] = 1
        state[90:100, 110:120] = 1
        state[90:100, 130:140] = 1
        state[90:100, 150:160] = 1
        state[90:100, 170:180] = 1
        state[90:100, 190:200] = 1

        state[110:120, 30:40] = 1
        state[110:120, 50:60] = 1
        state[110:120, 70:80] = 1
        state[110:120, 90:100] = 1
        state[110:120, 110:120] = 1
        state[110:120, 130:140] = 1
        state[110:120, 150:160] = 1
        state[110:120, 170:180] = 1
        state[110:120, 190:200] = 1
        state[110:120, 210:220] = 1

        state[130:140, 30:40] = 1
        state[130:140, 50:60] = 1
        state[130:140, 70:80] = 1
        state[130:140, 90:100] = 1
        state[130:140, 110:120] = 1
        state[130:140, 130:140] = 1
        state[130:140, 150:160] = 1
        state[130:140, 170:180] = 1
        state[130:140, 190:200] = 1
        state[130:140, 210:220] = 1

        state[150:160, 50:60] = 1
        state[150:160, 70:80] = 1
        state[150:160, 90:100] = 1
        state[150:160, 110:120] = 1
        state[150:160, 130:140] = 1
        state[150:160, 150:160] = 1
        state[150:160, 170:180] = 1
        state[150:160, 190:200] = 1

        state[170:180, 70:80] = 1
        state[170:180, 90:100] = 1
        state[170:180, 110:120] = 1
        state[170:180, 130:140] = 1
        state[170:180, 150:160] = 1
        state[170:180, 170:180] = 1

        state[190:200, 90:100] = 1
        state[190:200, 110:120] = 1
        state[190:200, 130:140] = 1
        state[190:200, 150:160] = 1

        state[210:220, 110:120] = 1
        state[210:220, 130:140] = 1
        return state

    def show(self):
        plt.imshow(self.state, 'gray_r')
        plt.title(self.label)
        plt.show()


class Agent:
    """
    An Agent is tasked with navigating a provided map.

    The possible goal of an agent include:
        ** Longest Walk with NO Collisions!
        ** Cover the Most Area with NO Collision!

    Possible Milestones an agent can achieve:
        ** Pass through more than one,two or three quadrant(s)
        ** Travel through one or more quadrants and return to start (or near)
        ** Cross Map with ZERO Collisions
        ** Same agent succeeds across more than one level
    """
    position = []
    state = []
    N = 0

    def __init__(self, start, world, n_steps_minimum):
        self.state = world
        self.N = n_steps_minimum
        if len(start) == 2:
            self.position = [start[0], start[1]]
        else:
            self.position = self.spawn_random_point()

    def spawn_random_point(self):
        # Initialize a random position
        x = np.random.randint(0, self.state.shape[0], 1, dtype=int)
        y = np.random.randint(0, self.state.shape[1], 1, dtype=int)
        return [x, y]

    def train(self, show):
        if show:
            f = plt.figure()
        # Variables for recording the training
        simulation = []
        visual = []
        # Generate some random steps first
        raw_steps = np.random.randint(1, 9, self.N)
        locations = []
        # Training Info
        Notes = {'open': [],
                 'hit': []}
        # Generate the position list these steps would create
        for step in raw_steps:
            directions = {1: [self.position[0] - 1, self.position[1] - 1],
                          2: [self.position[0], self.position[1] - 1],
                          3: [self.position[0] + 1, self.position[1] - 1],
                          4: [self.position[0] - 1, self.position[1]],
                          5: [self.position[0], self.position[1]],
                          6: [self.position[0] + 1, self.position[1]],
                          7: [self.position[0] - 1, self.position[1] + 1],
                          8: [self.position[0], self.position[1] + 1],
                          9: [self.position[0] + 1, self.position[1] + 1]}
            try:
                if self.state[directions[step][0],directions[step][0]] == 0:
                    Notes['open'].append(directions[step])
                else:
                    Notes['hit'].append(directions[step])
                self.position = directions[step]
                locations.append(self.position)
                self.state[self.position[0], self.position[1]] += 1
                simulation.append(self.state)
                visual.append([plt.imshow(self.state, 'gray_r')])
            except IndexError:
                continue
        if show:
            a = animation.ArtistAnimation(f,visual,interval=20,blit=True,repeat_delay=900)
            plt.show()
        return Notes, simulation, locations


    def check_route(self, start, Notes, raw_steps):
        better_route = []
        for step in raw_steps:
            for s in Notes['hit']:
                if s!=step:
                    better_route.append(step)
        return better_route

    def retry_level(self, route, show):
        if show:
            f = plt.figure()
        visual = []
        simulate = []
        steps = []
        for step in route:
            directions = {1: [self.position[0] - 1, self.position[1] - 1],
                          2: [self.position[0], self.position[1] - 1],
                          3: [self.position[0] + 1, self.position[1] - 1],
                          4: [self.position[0] - 1, self.position[1]],
                          5: [self.position[0], self.position[1]],
                          6: [self.position[0] + 1, self.position[1]],
                          7: [self.position[0] - 1, self.position[1] + 1],
                          8: [self.position[0], self.position[1] + 1],
                          9: [self.position[0] + 1, self.position[1] + 1]}
            try:
                if self.state[step] == 0:
                    self.position = step
                    visual.append([plt.imshow(self.state, 'gray_r')])

            except IndexError:
                continue
            if show:
                a = animation.ArtistAnimation(f, visual, interval=20, blit=True, repeat_delay=900)
                plt.show()


def create_basic_levels(verbose):
    """
    Create some starting environments for the
    amoeba to try and navigate.
    :param verbose:
    :return:
    """
    level_1 = MapCreation(100, 100, 'box')
    level_2 = MapCreation(250, 250, 'lattice')
    level_3 = MapCreation(250, 250, 'box').add_print('lattice')
    LEVELS = {1: level_1,
              2: level_2,
              3: level_3}

    if verbose:
        f, ax = plt.subplots(1, 3)
        ax[0].imshow(level_1.state, 'gray_r')
        ax[0].set_title('Level 1')
        ax[1].imshow(level_2.state, 'gray_r')
        ax[1].set_title('Level 2')
        ax[2].imshow(level_3, 'gray_r')
        ax[2].set_title('Level 3')
        plt.show()
    return LEVELS


def main():
    verbose = False
    # Create the levels to test bots on
    if '-v' in sys.argv:
        verbose = True
        levels = create_basic_levels(True)
    else:
        levels = create_basic_levels(False)
    templates = create_basic_levels(False)
    # Start off with a bot on level 1
    bot_1 = Agent([], levels[1].state, 100)
    starting_point = bot_1.position
    training_notes, simulation, raw_steps = bot_1.train(verbose)
    # Look over the path taken and make it slightly better if possible
    lvl1_path = bot_1.check_route(starting_point, training_notes, raw_steps)

    print str(len(training_notes['hit'])) + " Collisions"
    print str(len(training_notes['open'])) + " Legal moves made"
    if len(training_notes['hit']) > 0:
        print 'collisions:'
        for point in training_notes['hit']:
            if point in raw_steps:
                print '['+str(point[0])+','+str(point[1])+']'

    # Reset the state and try again
    bot_1.position = starting_point
    bot_1.state = templates[1].state
    bot_1.retry_level(lvl1_path,True)

    # Create a level 2 bot
    # bot_2 = Agent([], levels[2])
    #
    # # Create a level 3 bot
    # bot_3 = Agent([], levels[3])


if __name__ == '__main__':
    main()