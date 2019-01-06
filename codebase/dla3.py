import matplotlib.pyplot as plt, matplotlib.animation as animation
import numpy as np, time, sys


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

    def run_synchronous_dla(self, point_cloud, initial_state, show):
        simulation = []
        visual = []
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
            visual.append([plt.imshow(initial_state, 'gray_r')])

        print str(len(simulation)) + " Frames in simulation"
        if show:
            f = plt.figure(figsize=(8,8))
            a = animation.ArtistAnimation(f,visual,interval=10,blit=True,repeat_delay=800)
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

    default_dims = [250, 250]
    n_particles = 12000
    n_steps = 260
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
    start = time.time()
    point_cloud = dict()

    # Try box in the center first
    center_x = state.shape[0]/2
    center_y = state.shape[1]/2
    boxsz = 10
    state[center_x-boxsz:center_x+boxsz,center_y-boxsz:center_y+boxsz] = 1

    # And add lattice of boxes
    state = draw_square_lattice(state)

    for n_particles in range(n_particles+1):
        pt = RandomWalker(create_start(0, state, False), n_steps)
        point_cloud[n_particles] = pt.random_walk

    if verbose:
        print "Finished Pre computing "+str(n_steps)+" steps For all "+str(n_particles)+' Particles.'
        print str(len(pt.random_walk)*n_particles)+" Steps Total"
        t1 = time.time()-start
        print '[Computation Time: '+str(t1)+' s]\n'

    simulation = pt.run_synchronous_dla(point_cloud, state, verbose)
    t2 = (time.time() - start) - t1

    if verbose:
        print "Simulation Complete. Beginning Rendering Process"
        print '[Simulation Time: ' + str(t2) + ' s]'
    else:
        plt.imshow(simulation.pop(), 'gray_r')
        plt.title(str(n_particles) + ' Particle DLA [Final State]')
        plt.show()


if __name__ == '__main__':
    main()