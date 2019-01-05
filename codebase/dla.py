import matplotlib.pyplot as plt, matplotlib.animation as animation
import numpy as np
import utility

class walker:
    steps = []
    position = []
    state = [[]]
    DATA = []
    END = {}
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
        self.DATA, self.END = self.random_walk(self.generate_random_steps())

    def generate_random_steps(self):
        rsteps = np.random.randint(3, 10, self.depth)
        steps = list()
        for step in rsteps:
            steps.append(self.directions[step])
        return steps

    def random_walk(self, step_keys):
        self.state[int(self.position[0]), int(self.position[1])] = 0
        CenterBox = [int(self.state.shape[0]/2), int(self.state.shape[1]/2)]
        END_PT = {}
        #f = plt.figure()
        history = []
        visual = []
        for step in step_keys:
            # if self.position[0] < self.state.shape[0] and self.position[0]<=0:
            #     self.state[0, int(self.position[1])] = 1
            # if self.position[1] < self.state.shape[1] and self.position[1]<=0:
            #     self.state[int(self.position[0]), 0] = 1
            history.append(self.state)
            if step == 'u_left':
                self.position[0]-=1
                self.position[1]-=1
                #continue
            if step == 'up':
                self.position[1]-=1
                #continue
            if step =='u_right':
                self.position[0]+=1
                self.position[1]-=1
                #continue
            if step == 'left':
                self.position[0]-=1
            if step == 'self':
                continue
            if step == 'right':
                self.position[0]+=1

            if step == 'd_left':
                self.position[0]-=1
                self.position[1]+=1

            if step == 'down':
                self.position[1]-=1

            if step == 'd_right':
                self.position[0]+=1
                self.position[1]+=1

            visual.append([plt.imshow(self.state,'gray_r')])
            try:
                if self.state[self.position[0],self.position[1]] == 1:
                    break
                self.state[int(self.position[0]), int(self.position[1])] = 1
            except IndexError:
                print "Out of Bounds!" + str(self.position)
                END_PT[step] = self.position
                break
        return history, END_PT


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
        particle = 0
        final = np.zeros((int(self.dimensions[0]*1.25),
                          int(self.dimensions[1]*1.25)))
        film = []
        while particle < self.depth:
            p = self.add_walker()
            film = self.merge_history(p.DATA,film)
            self.state = p.DATA.pop()
            particle += 1
        f = plt.figure()
        a = animation.ArtistAnimation(f,film,interval=10,blit=True,repeat_delay=900)
        plt.title(str(len(film))+' steps total')

        print "Simulation Finished! Beginning Rendering Process."
        plt.show()

    def merge_history(self, dataA, dataB):
        for obj in dataA:
            dataB.append([plt.imshow(obj,'gray_r')])
        return dataB

    def add_walker(self):
        start = np.array([np.random.randint(0+20, self.state.shape[0]-20, 1),
                          np.random.randint(0+20, self.state.shape[1]-20, 1)])
        print "starting at ["+str(start[0])+','+str(start[1])+"]"
        w = walker(start, self.state, self.nsteps)
        return w


def main():

    randomlyDiffuse(50, 100, [100, 100])


if __name__ == '__main__':
    main()
