import matplotlib.pyplot as plt, matplotlib.animation as animation
import numpy as np


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


def feed_steps_to_state(start, state, steps):
    history = list()
    visual = []
    for step in steps:
        x = start[0]
        y = start[1]
        state[x, y] = 0
        directions = {1: [x-1, y-1],
                      2: [x, y-1],
                      3: [x+1, y-1],
                      4: [x-1, y],
                      5: [x, y],
                      6: [x+1, y],
                      7: [x-1, y+1],
                      8: [x, y+1],
                      9: [x+1, y+1]}

        # If there's something already there,
        # leave the particle before moving on
        if step != 5 and state[directions[step][0],directions[step][1]] == 1:
            state[x, y] = 1
            history.append(state)
            break
        elif step != 5:
            start = directions[step]
            state[start[0],start[1]] = 1
            history.append(state)
    return history


def splice_timeline(series1, series2):
    """
    Sequentially add each element from
    one list [series1] to the end of the
    second list [series2]. Returns the new
    combined list. 
    :param series1: 
    :param series2: 
    :return series2: 
    """
    for item in series1:
        series2.append(item)
    return series2


def main():
    n_steps = 500
    n_particles = 500
    dimensions = [250, 250]
    center_mass_size = 3

    # Numbering scheme for direction keys
    # [[1,2,3],
    #  [4,5,6],
    #  [7,8,9]]
    state = np.zeros(dimensions)
    center_x = int(state.shape[0]) / 2
    center_y = int(state.shape[1]) / 2
    # Put a box in the center
    state[center_x - center_mass_size:center_x + center_mass_size,
          center_y - center_mass_size:center_y + center_mass_size] = 1

    data = []

    for particle in range(n_particles):
        start = create_start(10, np.zeros((250, 250)), False)
        steps = np.random.randint(1, 9, n_steps)

        print "Starting from "+str(start)

        frames = feed_steps_to_state(start, state, steps)
        # data = splice_timeline(frames, data)
        state = frames.pop()
        data.append([plt.imshow(state, 'gray_r')])

    a = animation.ArtistAnimation(plt.figure(), data, interval=50,blit=True,repeat_delay=500)
    plt.show()


if __name__ == '__main__':
    main()
