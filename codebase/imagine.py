import sys, numpy as np, scipy.ndimage as ndi
import matplotlib.pyplot as plt, matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
import spatial, utility


class Shape:
    label = ''
    dims = []
    hardcoded_shapes = {'box': [[0,0,0,0,0,0,0,0],
                                [0,1,1,1,1,1,1,0],
                                [0,1,1,1,1,1,1,0],
                                [0,1,1,1,1,1,1,0],
                                [0,1,1,1,1,1,1,0],
                                [0,1,1,1,1,1,1,0],
                                [0,1,1,1,1,1,1,0],
                                [0,0,0,0,0,0,0,0]],
                        'circle': np.ones(dims)}

    def __init__(self, hasName, name):
        if hasName:
            if name in self.hardcoded_shapes.keys():
                self.label = name

    def scale_box(self, factor, verbose):
        """
        Take a [Shape].box primitive, and
        scale it up by the factor given.
        If verbose, show the box before and after.
        :param factor:
        :param verbose:
        :return:
        """
        # Take the small box primitive and scale it
        box = np.array(self.hardcoded_shapes['box'])
        current_box_dims = [int(np.sqrt(box.sum())),
                            int(np.sqrt(box.sum()))]
        # Define new box dimensions before white padding
        new_dims = [int(factor * current_box_dims[0]),
                    int(factor * current_box_dims[0])]
        newbox = np.ones(new_dims)
        # Add the white space padding around the box
        row_padding = np.zeros((1, new_dims[0]+2))
        col_padding = np.zeros((new_dims[1], 1))
        newbox = np.concatenate((col_padding, newbox, col_padding),1)
        newbox = np.concatenate((row_padding, newbox, row_padding),0)
        # If verbose, show the box
        if verbose:
            print "Box Dims: " + str(current_box_dims) + \
                  "  [" + str(box.shape) + "]"
            print "New Box Dims: " + str(new_dims) + \
                  "  [" + str(newbox.shape) + "]"

            f, ax = plt.subplots(1, 2)
            ax[0].imshow(box, 'gray_r')
            ax[1].imshow(newbox, 'gray_r')
            plt.show()
        return newbox

    def make_circle(self, radius, verbose):
        npts = np.pi*(radius*radius)
        if verbose:
            print str(npts) + " Points will be in the Circle"

        # Initialize the circle template
        dim = int(np.sqrt(npts) + radius/10)
        self.hardcoded_shapes['circle'] = np.zeros((dim, dim))
        circle = np.zeros((dim, dim))
        print circle.shape

        # start with a little box
        center_adj = int(dim/4)
        circle[center_adj-radius:center_adj+radius,center_adj-radius:center_adj+radius] = 1
        self.hardcoded_shapes['circle'] = circle

        # Maybe you can make an awkward jagged box
        # With some matrix math?
        r0 = [[0,0,1],
              [0,1,1],
              [1,1,1]]

        r1 = [[1,0,0],
              [1,1,0],
              [1,1,1]]

        r2 = [[1,1,1],
              [1,1,0],
              [1,0,0]],

        r3 = [[1,1,1],
              [0,1,1],
              [0,0,1]]
        low2 = [[1,1,1],
                [1,1,1],
                [0,0,0]]

        s0 = [[1,1,1],
              [1,1,1],
              [1,1,1]]

        rowH = np.concatenate((r0, s0, s0, s0, s0, r1), 1)
        midl = np.concatenate((s0, s0, s0, s0, s0, s0), 1)
        rowL = np.concatenate((r3, s0, s0, s0, s0, np.rot90(r3)), 1)

        circle = np.concatenate((rowH, midl,midl, rowL), 0)
        plt.imshow(circle, 'gray_r')
        plt.show()

    def show(self):
        if self.label in self.hardcoded_shapes.keys():
            plt.imshow(self.hardcoded_shapes[self.label],'gray_r')
            plt.title(self.label)
            plt.show()


def random_walk(point, nsteps, space, verbose, show, save, frame_rate):
    rand = np.random.randint(1, 10, nsteps)
    steps = []
    for step in rand:
        steps.append(point.directions[step])
    if verbose:
        print "Random Walk: \n" + str(steps)
    if show:
        f = plt.figure()
    data = list()
    walk = []
    steps = []
    # do the random walk
    for move in rand:
        # TODO: should check if xloc, yloc are in the space bounds!
        try:
            steps.append([point.xloc, point.yloc])
            space[point.xloc, point.yloc] = point.value
            space = point.move(move, space)
        except IndexError:
            pass
        if show:
            walk.append([plt.imshow(space, 'gray_r')])
        else:
            walk.append(space)
        data.append(space)
    if show and not save:
        a = animation.ArtistAnimation(f, walk, interval=frame_rate, blit=True, repeat_delay=900)
        plt.title('Random Walk ['+str(nsteps)+' steps]')
    plt.show()
    if show and save:
        a = animation.ArtistAnimation(f, walk, interval=frame_rate, blit=True, repeat_delay=900)
        # plt.title('Random Walk [' + str(nsteps) + ' steps]')
        fileNameOut = 'random_walk_' + str(nsteps) + 'steps.mp4'
        writer = FFMpegWriter(fps=frame_rate, metadata=dict(artist='Me'), bitrate=1800)
        a.save(fileNameOut, writer=writer)
    return data, steps


def random_walk_eval(history, start, steps):
    first = steps.pop(0)
    last = steps.pop()
    dx = last[0] - first[0]
    dy = last[1] - first[1]

    distance = np.sqrt((dx*dx)+(dy*dy))

    print str(len(history)) + " Steps Taken."
    print "Started At " + str(first)
    print "Ended At " + str(last)
    print "Net Distance Travelled: "+str(distance)
    
    final = history.pop()
    tiles_eaten = start.sum() - final.sum()
    total_tiles = final.shape[0]*final.shape[1]

    print str(tiles_eaten)+' Tiles Eaten ['+str(100*tiles_eaten/total_tiles)+"%]"

    f, ax = plt.subplots(1, 2)
    ax[0].imshow(start, 'gray_r')
    ax[0].set_title('Start')
    ax[1].imshow(final, 'gray_r')
    ax[1].set_title('Final')
    plt.show()


def record_walk(walk_data, frame_rate):
    nsteps = len(walk_data)
    file_name = 'random_walk_' + str(nsteps) + '_steps.mp4'
    print str(nsteps) + ' steps'
    utility.ImageProcessing.render(walk_data, False,frame_rate=frame_rate,
                                   save=True, fileNameOut=file_name)


def main():

    if 'box' in sys.argv:
        # Make A Box
        box = Shape(True, 'box')
        # box.show()

        # Example of scaling the box 30x
        cage = box.scale_box(15, True)

        initial_state = cage.copy()

        # Put a point in the center of big box
        center_x = int(cage.shape[0]/2)
        center_y = int(cage.shape[1]/2)
        start = [center_x, center_y]

        # Make the point 'aware'
        firefly = spatial.Point(start, 3)
        # firefly.show(cage)

        if 'random_walk' in sys.argv:
            # Show the animation?
            isVisual = False

            # Simulate the point taking a random walk through the space
            # history0, steps0 = random_walk(firefly, 50, cage, verbose=False, show=isVisual,
            #                              save=False, frame_rate=20)
            nsteps = int(input('How many steps for random walk?: '))
            if '-v' in sys.argv:
                isVisual = True
            history, steps = random_walk(firefly, nsteps, cage, verbose=False, show=isVisual,
                                         save=False, frame_rate=20)

            # Evaluate the random walk
            random_walk_eval(history, initial_state, steps)
            # record_walk(history, 20)


if __name__ == '__main__':
    main()


