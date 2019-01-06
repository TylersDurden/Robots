import numpy as np, utility, sys


def create_start(padding, state, verbose):
    """
    Select random starting point within given
    2D state matrix.
    :param padding:
    :param state:
    :param verbose:
    :return:
    """
    rx = np.random.randint(0 + padding, state.shape[0] - padding, 1)[0]
    ry = np.random.randint(0 + padding, state.shape[1] - padding, 1)[0]
    start = [rx, ry]
    if verbose:
        print start
    return start


def manual_state_init():
    width = int(input('Enter Width: '))
    height = int(input('Enter Height: '))
    state = np.zeros((width, height))
    return state


class RandomWalker:
    random_walk = []
    pos = []
    N = 0

    def __init__(self, position, n_step):
        self.pos = position
        self.N = n_step
        self.random_walk = self.precompute_steps()

    def precompute_steps(self):
        random_steps = np.random.random_integers(1, 9, self.N)
        steps = []
        for step in random_steps:
            x = self.pos[0]
            y = self.pos[1]

            directions = {1: [x - 1, y - 1],
                          2: [x, y - 1],
                          3: [x + 1, y - 1],
                          4: [x - 1, y],
                          5: [x, y],
                          6: [x + 1, y],
                          7: [x - 1, y + 1],
                          8: [x, y + 1],
                          9: [x + 1, y + 1]}
            next_pos = directions[step]
            steps.append(next_pos)
            self.pos = [next_pos[0], next_pos[1]]
        return steps

    def run_synchronous_dla(self, point_cloud, initial_state):
        simulation = []
        for step in range(self.N):
            for pt in point_cloud.keys():
                try:
                    next_pos = point_cloud[pt].pop(step)
                    if initial_state[next_pos[0],next_pos[1]] != 1:
                        initial_state[next_pos[0],next_pos[1]] = 1
                    else:
                        next_pos = point_cloud[pt].pop(step-1)
                        initial_state[next_pos[0],next_pos[1]] = 1
                        break
                except IndexError:
                    break
            simulation.append(initial_state)
        print str(len(simulation)) + " Frames in simulation"
        return simulation


def main():

    default_dims = [250, 250]
    n_particles = 3500
    n_steps = 220
    verbose = False
    if '-v' in sys.argv:
        verbose = True
    if '-m' in sys.argv:
        state = manual_state_init()
    else:
        state = np.zeros(default_dims)
    if '-npt' in sys.argv:
        n_particles = int(input('Enter number of particles to use: '))
    if '-nstep' in sys.argv:
        n_steps = int(input('Enter number of steps to use: '))

    point_cloud = dict()

    # Try box in the center first
    center_x = state.shape[0]/2
    center_y = state.shape[1]/2
    boxsz = 20
    state[center_x-boxsz:center_x+boxsz,center_y-boxsz:center_y+boxsz] = 1

    for n_particles in range(n_particles+1):
        pt = RandomWalker(create_start(10, state, False), n_steps)
        point_cloud[n_particles] = pt.random_walk
    if verbose:
        print "Finished Pre computing "+str(n_steps)+" steps For all "+str(n_particles)+' Particles.'
        print str(len(pt.random_walk)*n_particles)+" Steps Total"

        simulation = pt.run_synchronous_dla(point_cloud, state)
        print "Simulation Complete. Beginning Rendering Process"
        utility.ImageProcessing.render(simulation, False, 2, False, '')

if __name__ == '__main__':
    main()