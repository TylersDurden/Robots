import matplotlib.pyplot as plt, matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
import numpy as np, scipy.ndimage as ndi


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


