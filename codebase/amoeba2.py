import matplotlib.pyplot as plt, matplotlib.animation as animation
import numpy as np, utility, scipy.ndimage as ndi


class Maps:
    N = 0
    Debug = False
    box_size = 0

    levels = {}
    labels = {}

    def __init__(self, n, box_sz, verbose):
        self.N = n
        self.box_size = box_sz
        self.Debug = verbose
        # Create the first two levels
        box = Maps.centered_box(box_sz * 10, [n, n], verbose)
        lattice = Maps.create_square_lattice(box_sz * 2, [n, n], [7, 7], verbose)
        # Index them for external access
        self.levels[1] = box
        self.levels[2] = lattice
        self.labels = {1: 'box', 2: 'lattice'}

    @staticmethod
    def create_square_lattice(box_sz, dims, layout, show):
        """
        Create a grid of square boxes with the given layout
        I.E [4x4] yields a grid of 4 boxes by 4 boxes.
        :param box_sz:
        :param dims:
        :param layout:
        :param show:
        :return state:
        """
        state = np.zeros(dims)
        nr = state.shape[0] / layout[0]
        nc = state.shape[1] / layout[1]

        row_size = np.arange(2 * box_sz, state.shape[0] + 2 * box_sz, nr)
        col_size = np.arange(2 * box_sz, state.shape[1] + 2 * box_sz, nc)

        for i in row_size:
            for j in col_size:
                state[i - box_sz:i + box_sz, j - box_sz:j + box_sz] = 1
        if show:
            plt.imshow(state, 'gray_r')
            plt.show()
        return state

    @staticmethod
    def centered_box(box_sz, dims, show):
        state = np.zeros(dims)
        cx = int(state.shape[0] / 2)
        cy = int(state.shape[1] / 2)
        state[cx - box_sz:cx + box_sz, cy - box_sz:cy + box_sz] = 1

        if show:
            plt.imshow(state, 'gray_r')
            plt.show()
        return state


class Agent:
    position = []
    state = [[]]
    debug = False

    def __init__(self, pos, lvl):
        self.position = pos
        self.state = lvl
        floating = True
        if self.state[pos[0], pos[1]] ==0:
            self.state[pos[0], pos[1]] = 1
            floating = False
        else:
            while floating:
                pos = utility.spawn_random_point(lvl)
                if self.state[pos[0], pos[1]] == 0:
                    self.state[pos[0], pos[1]] = 1
                    floating = False
        if floating:
            print "Bad Starting Point!!"
            exit(0)

    def set_debug(self, new_setting):
        self.debug = new_setting

    def view(self, state):
        II = 0
        view = {'left': [[1, 1, 1], [0, 0, 0], [0, 0, 0]],
                'right': [[0, 0, 0], [0, 0, 0], [1, 1, 1]],
                'down': [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
                'up': [[0, 0, 1], [0, 0, 1], [0, 0, 1]]}
        n = len(view.keys())
        f, ax = plt.subplots(1, n,figsize=(3*n, n), sharex=True, sharey=True)
        for label in view.keys():
            ax[II].imshow(ndi.convolve(state, np.array(view[label])), 'gray_r')
            ax[II].set_title(label)
            II += 1
        plt.show()

    def generate_random_steps(self, n_steps, injector):
        pos = self.position
        raw_steps = np.random.randint(1, 9, n_steps)
        valid = list()
        path = []
        for step in raw_steps:
            directions = {1: [pos[0] - 1, pos[1] - 1],
                          2: [pos[0], pos[1] - 1],
                          3: [pos[0] + 1, pos[0] - 1],
                          4: [pos[0] - 1, pos[1]],
                          5: pos,
                          6: [pos[0] + 1, pos[1]],
                          7: [pos[0] - 1, pos[1] + 1],
                          8: [pos[0], pos[1] + 1],
                          9: [pos[0] + 1, pos[1] + 1]}
            dx = directions[step][0]
            dy = directions[step][1]
            try:
                if self.state[dx, dy] == 0:
                    pos = [dx,dy]
                    valid.append(True)
                    path.append([dx, dy])
                else:
                    pos = [dx, dy]
                    valid.append(False)
            except IndexError:
                pass
        if self.debug:
            print utility.Console.BLD + str(len(path)) + " Legal Steps [" + utility.Console.GRN + \
                  str(100 * float(len(path)) / n_steps) + "%" + utility.Console.END + \
                  utility.Console.BLD + "]" + utility.Console.END
        return valid, path

    def test_path(self, truth, steps):
        if self.debug:
            f = plt.figure()
            film = []
        ii = 0
        for step in steps:
            self.position = step
            if self.state[step[0],step[1]] == 1:
                self.state[step[0], step[1]] -= 1
            else:
                self.state[step[0], step[1]] += 1
            film.append([plt.imshow(self.state, 'gray_r')])
            try:
                if truth.pop(ii):
                    self.state[self.position[0], self.position[1]] *= self.state[self.position[0], self.position[1]]
            except IndexError:
                pass
            # self.state[self.position[0], self.position[1]] = 0
            ii += 1
        if self.debug:
            a = animation.ArtistAnimation(f,film,interval=2,blit=True,repeat_delay=900)
            plt.show()


def find_most_legal_sequence(legality, locations, verbose):
    positions = []
    n_steps = {}
    max_steps = 0
    n = 0
    path_num = 0
    ii = 0
    for step in legality:
        try:
            if step:
                positions.append(locations.pop(ii))
            else:
                n_steps[path_num] = positions
                positions = []
                path_num += 1
            if len(positions) > n:
                n = len(positions)
                max_steps = path_num
        except IndexError:
            break
        ii += 1
    if verbose:
        print str(len(n_steps)) + " Pathways"
        print 'Best Path found: Path ' + str(max_steps)
        print "Path " + str(max_steps) + ' is ' + str(len(n_steps[max_steps])) + ' steps'
    return n_steps, max_steps


def main():
    N = 250
    DEBUG = False
    box_size = 5

    environments = Maps(N, box_size, DEBUG)

    start_pt = utility.spawn_random_point(environments.levels[2])
    bot = Agent(start_pt, environments.levels[2])
    bot.set_debug(True)
    DEBUG = True
    if DEBUG:
        print "Starting @ "+str(start_pt[0])+','+str(start_pt[1])
        # bot.view(bot.state)

    good, level1 = bot.generate_random_steps(N*10, [])
    find_most_legal_sequence(good, level1)
    bot.test_path(good, level1)


if __name__ == '__main__':
    main()
