import numpy as np, matplotlib.pyplot as plt, matplotlib.animation as animation
import sys, scipy.ndimage as ndi, utility, time


class complex_movements:

    mix = [1, 1]    # Random walking/Automata
    state = [[]]
    size = 5
    width = 0
    height = 0
    length = 0

    position = []

    def __init__(self, dims, world, ratio, duration,opts):
        self.state = world
        self.mix = ratio
        self.length = duration
        self.width = dims[0]
        self.height = dims[1]

        self.state = self.make_box(dims[0], dims[1])
        self.state = draw_square_lattice(self.state)
        nrw, nau = self.initialize()
        self.simulate(n_random=nrw, n_auto=nau)
        if 'swarm' in opts:
            self.simulate_swarm(15, nrw)

    def make_box(self, width,height):
        center_x = width / 2
        center_y = height / 2

        self.position = [center_x, center_y]

        box = np.zeros((width, height))
        box[center_x - self.size:center_x + self.size,
            center_y - self.size:center_y + self.size] = 1
        return box

    def initialize(self):
        denom = self.mix[0]+self.mix[1]
        n_random = int(float(self.mix[0])/denom*self.length)
        n_auto = int(float(self.mix[1])/denom*self.length)

        print str(n_auto)+'% Frames of Automata and ' +\
              str(n_random)+'% Frames of Random Walking'

        return n_random, n_auto

    def simulate_swarm(self, n_particles, n_random):
        simulation = []
        visual = []
        f0 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]  # Key #s: 9, 6, 3, 1
        f1 = [[1, 2, 1], [2, 3, 2], [1, 2, 1]]  # Key #s: 15, 11, 8, 4
        f2 = [[1, 1, 1, 1, 1], [1, 2, 2, 2, 1], [1, 2, 0, 2, 1], [1, 2, 2, 2, 1],
              [1, 1, 1, 1, 1]]  # Key #s: 23, 16, 11, 8

        automata_baselines = {'f0': [9, 6, 3, 1],
                              'f1': [15, 11, 8, 4],
                              'f2': [23, 16, 11, 8]}
        t0 = time.time()
        for frame in range(self.length):
            for pt in range(n_particles):
                # Initialize a random position
                x = np.random.randint(0,self.width,1,dtype=int)
                y = np.random.randint(0,self.height,1,dtype=int)
                self.position = [x, y]
                random_steps = np.random.random_integers(1, 9, n_random)
                # Add random steps to simulation matrix
                for step in random_steps:
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
                        self.position = directions[step]
                        self.state[self.position[0], self.position[1]] += 1
                        simulation.append(self.state)
                        visual.append([plt.imshow(self.state, 'gray_r')])
                    except IndexError:
                        continue
                # Add conv/automata to simulation matrix
                world = ndi.convolve(self.state, f1)
                flat_state = self.state.flatten()
                II = 0
                for cell in world.flatten():
                    for keynum in automata_baselines['f1']:
                        if cell == keynum:
                            flat_state[II] -= 1
                        if cell >= keynum:
                            flat_state[II] -= 2
                    II += 1
                self.state = flat_state.reshape(self.width, self.height)
                simulation.append(world)
                visual.append([plt.imshow(self.state, 'gray_r')])
        print "Finished Simulation [" + str(II) + " Frames in " + str(time.time() - t0) + 's'
        a = animation.ArtistAnimation(plt.figure(), visual, interval=1, blit=True, repeat_delay=800)
        # plt.imshow(world)
        plt.show()
        return simulation

    def simulate(self, n_random, n_auto):
        simulation = []
        visual = []
        f0 = [[1,1,1],[1,1,1],[1,1,1]] # Key #s: 9, 6, 3, 1
        f1 = [[1,2,1],[2,3,2],[1,2,1]] # Key #s: 15, 11, 8, 4
        f2 = [[1,1,1,1,1],[1,2,2,2,1],[1,2,0,2,1],[1,2,2,2,1],[1,1,1,1,1]] # Key #s: 23, 16, 11, 8

        automata_baselines = {'f0': [9, 6, 3, 1],
                              'f1': [15, 11, 8, 4],
                              'f2': [23, 16, 11, 8]}
        t0 = time.time()
        for frame in range(self.length):
            # Initialize a random position

            random_steps = np.random.random_integers(1,9,n_random)
            # Add random steps to simulation matrix
            for step in random_steps:
                directions = {1:[self.position[0]-1, self.position[1]-1],
                              2:[self.position[0],self.position[1]-1],
                              3:[self.position[0]+1,self.position[1]-1],
                              4:[self.position[0]-1,self.position[1]],
                              5:[self.position[0],self.position[1]],
                              6:[self.position[0]+1,self.position[1]],
                              7:[self.position[0]-1,self.position[1]+1],
                              8:[self.position[0], self.position[1]+1],
                              9:[self.position[0]+1, self.position[1]+1]}
                try:
                    self.position = directions[step]
                    self.state[self.position[0], self.position[1]] += 1
                    simulation.append(self.state)
                    visual.append([plt.imshow(self.state, 'gray_r')])
                except IndexError:
                    continue
            # Add conv/automata to simulation matrix
            world = ndi.convolve(self.state, f1)
            flat_state = self.state.flatten()
            II = 0
            for cell in world.flatten():
                for keynum in automata_baselines['f1']:
                    if cell == keynum:
                        flat_state[II] -= 1
                    if cell >= keynum:
                        flat_state[II] -= 2
                II += 1
            self.state = flat_state.reshape(self.width, self.height)
            simulation.append(world)
            visual.append([plt.imshow(self.state, 'gray_r')])
        print "Finished Simulation ["+str(II)+" Frames in "+str(time.time() - t0)+'s'
        a = animation.ArtistAnimation(plt.figure(), visual, interval=1, blit=True, repeat_delay=800)
        # plt.imshow(world)
        plt.show()
        return simulation


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


def main():
    # Global settings
    N = 250
    walk_ratio = 2
    auto_ratio = 4

    # User selection for canvas dimensions
    if '-dims' in sys.argv:
        N = int(input('Enter NxN Size: '))

    # User selection for entering RWalk/Automata Ratio
    if '-r' in sys.argv:
        walk_ratio = int(input('How Many Parts RandomWalk?: '))
        auto_ratio = int(input('How Many Parts Automata?: '))

    if 'swarm' in sys.argv:
        complex_movements([N,N], np.zeros((N,N)), [walk_ratio, auto_ratio], 100,['swarm'])
    else:
        # Based on either defaults, or user defined params, create a
        # set of complex movements with a given mixture of random walk
        #  motion and automata movements.
        complex_movements([N, N], np.zeros((N, N)), [walk_ratio, auto_ratio], 100,[''])


if __name__ == '__main__':
    main()
