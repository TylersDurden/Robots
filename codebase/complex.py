import numpy as np, matplotlib.pyplot as plt, matplotlib.animation as animation
import sys, scipy.ndimage as ndi

class complex_movements:

    mix = [1, 1]    # Random walking/Automata
    state = [[]]
    size = 5
    width = 0
    height = 0
    length = 0

    position = []

    def __init__(self, dims, world, ratio, duration):
        self.state = world
        self.mix = ratio
        self.length = duration
        width = dims[0]
        height = dims[1]

        self.state = self.make_box(width, height)

        nrw, nau = self.initialize()
        self.simulate(n_random=nrw, n_auto=nau)

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

        print str(n_auto)+' Frames of Automata and ' +\
              str(n_random)+' Frames of Random Walking'

        return n_random, n_auto

    def simulate(self, n_random, n_auto):
        simulation = []
        visual = []
        f0 = [[1,1,1],[1,1,1],[1,1,1]] # Key #s: 9, 6, 3, 1
        f1 = [[1,2,1],[2,3,2],[1,2,1]] # Key #s: 15, 11, 8, 4
        f2 = [[1,1,1,1,1],[1,2,2,2,1],[1,2,0,2,1],[1,2,2,2,1],[1,1,1,1,1]] # Key #s: 23, 16, 11, 8

        automata_baselines = {'f0': [9, 6, 3, 1],
                              'f1': [15, 11, 8, 4],
                              'f2': [23, 16, 11, 8]}

        for frame in range(self.length):
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
            world = ndi.convolve(self.state, f0)
            simulation.append(world)
            visual.append([plt.imshow(world, 'gray_r')])
        a = animation.ArtistAnimation(plt.figure(), visual, interval=20,blit=True,repeat_delay=800)
        # plt.imshow(world)
        plt.show()
        return simulation


def main():
    # Global settings
    N = 250
    walk_ratio = 3
    auto_ratio = 2

    # User selection for canvas dimensions
    if '-dims' in sys.argv:
        N = int(input('Enter NxN Size: '))

    # User selection for entering RWalk/Automata Ratio
    if '-r' in sys.argv:
        walk_ratio = int(input('How Many Parts RandomWalk?: '))
        auto_ratio = int(input('How Many Parts Automata?: '))

    # Based on either defaults, or user defined params, create a
    # set of complex movements with a given mixture of random walk
    #  motion and automata movements.
    complex_movements([N, N], np.zeros((N, N)), [walk_ratio, auto_ratio], 100)


if __name__ == '__main__':
    main()
