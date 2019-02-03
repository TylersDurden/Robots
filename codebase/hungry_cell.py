import scipy.ndimage as ndi, numpy as np, utility
import matplotlib.pyplot as plt, matplotlib.animation as animation

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

    def generate_random_steps(self, animate):
        c0 = [[1,1,1],[1,1,1],[1,1,1]]
        raw_steps = np.random.randint(1, 9, self.n_steps)
        random_walk = []
        state = np.array(self.state)

        if animate:
            reel = []
            f = plt.figure()
        for step in raw_steps:
            self.position = self.directions[step]
            if self.state[self.position] != 1:
                for x in range(state.shape[0]):
                    for y in range(state.shape[1]):
                        pov = self.state[x-2:x+2, y-2:y+2]
                        lens = ndi.convolve(pov,c0)
                        # Determine best step and record the directions
                        # self.choose_step(pov,lens, self.state)
            # else:
            self.state[self.position[0],self.position[1]] += 1
            if animate:
                reel.append([plt.imshow(state, 'gray_r')])
            random_walk.append(self.position)
        if animate:
            a = animation.ArtistAnimation(f,reel,interval=70,blit=True,repeat_delay=900)
            plt.show()
        return random_walk

    def choose_step(self, pov, conv, world):
        thoughts = np.random.randint(1, 9, self.depth)


def main():
    w = 250
    h = 250
    state = np.zeros((w, h))
    state = utility.ImageProcessing.draw_centered_box(state, 15, False)
    cell = Cell(100, 3, utility.spawn_random_point(state), state)
    random_walk = cell.generate_random_steps(True)
    print "Generated " + str(len(random_walk)) + " Random Steps"


if __name__ == '__main__':
    main()
