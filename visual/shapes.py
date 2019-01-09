import matplotlib.pyplot as plt, matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
import resource, numpy as np, scipy.ndimage as ndi


def centered_box(dims, box_sz, preview):
    canvas = np.zeros(dims)
    center_x = int(dims[0]/2)
    center_y = int(dims[1]/2)
    # Draw Box
    canvas[center_x-box_sz:center_x+box_sz,
           center_y-box_sz:center_y+box_sz] = 1
    if preview:
        plt.imshow(canvas, 'gray_r')
        plt.title('Centered Box')
        plt.show()
    return canvas


def render(images, isColor, frame_rate, save, fileNameOut):
    """
    Render the given images, and either save the output or
    not based on the input parameter. If animation output is
    to be saved, it is named according to the input variable
    fileNameOut.
    :param images:
    :param isColor:
    :param frame_rate:
    :param save:
    :param fileNameOut:
    :return:
    """
    f = plt.figure()
    film = []
    for frame in images:
        if isColor:
            film.append([plt.imshow(frame)])
        else:
            film.append([plt.imshow(frame, 'gray_r')])
    a = animation.ArtistAnimation(f, film, interval=frame_rate,
                                  blit=True, repeat_delay=100)
    if save:
        writer = FFMpegWriter(fps=frame_rate, metadata=dict(artist='Me'), bitrate=1800)
        a.save(fileNameOut, writer=writer)
    plt.show()


def check_mem_usage():
    """
    Return the amount of RAM usage, in bytes, being consumed currently.
    :return (integer) memory used in bytes:
    """
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return mem


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


def preview_figures(plot_dic):
    """
    Preview images stored in a dict with the key as
    the title, and the value of that key being images
    :param plot_dic:
    :return:
    """
    f, ax = plt.subplots(1, len(plot_dic.keys()))
    plot = 0
    for shape in plot_dic.keys():
        ax[plot].imshow(plot_dic[shape], 'gray_r')
        ax[plot].set_title(shape)
        plot += 1
    plt.show()

