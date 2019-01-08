import matplotlib.pyplot as plt, matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter
import resource, os, numpy as np


def swap(fname, destroy):
    """

    :param fname:
    :param destroy:
    :return:
    """
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def hexify(cmd):
    """
     Return a given command in forms
    [slash]:\xdead\xbeef
    [hex]: 0xdeadbeef
    :param cmd:
    :return (dict) payload:
    """
    payload = {'slash':[],
               'hex':[]}
    for letter in list(cmd):
        payload['slash'].append('\\x'+letter.encode('hex'))
        payload['hex'].append('0x'+letter.encode('hex'))
    return payload


def check_mem_usage():
    """
    Return the amount of RAM usage, in bytes, being consumed currently.
    :return (integer) memory:
    """
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return mem


def ind2sub(index,dims):
    """
    Given an index and array dimensions,
    convert an index to [x,y] subscript pair.
    :param index:
    :param dims:
    :return tuple - subscripts :
    """
    subs = []
    ii = 0
    for y in range(dims[1]):
        for x in range(dims[0]):
            if index==ii:
                subs = [x,y]
            ii +=1
    return subs


def sub2ind(subs, dims):
    """
    Given a 2D Array's subscripts, return it's
    flattened index
    :param subs:
    :param dims:
    :return:
    """
    ii = 0
    indice = 0
    for y in range(dims[1]):
        for x in range(dims[0]):
            if subs[0] == x and subs[1] == y:
                indice = ii
            ii += 1
    return indice


def console_color_printing(line, color, bold, italic):
    """
    Utility method for print to console with alternative
    colors and font changes.
    :param line:
    :param color:
    :param isbold:
    :param isitalic:
    :return:
    """
    line_out = ''
    if bold:
        line_out += '\33[1m'
    if italic:
        line_out += '\33[3m'
    colors = {'rbg': '\33[41m',     # Red Background
              'wbg':'\33[7m',       # White Background
              'bbg':'\33[100m',     # black Background
              'red': '\33[31m',
              'green': '\33[92m',
              'blue': '\33[34m',
              'purple': '\33[35m',
              'brown':'\33[46m',
              'blink':'\33[5m',
              '':''}
    try:
        line_out += colors[color] + line
    except KeyError:
        print "The Color-Key "+color+" is NOT valid! "
        print colors
    # Terminate the font changes on console
    line_out += '\33[0m'
    return line_out


def spawn_random_point(state):
    # Initialize a random position
    x = np.random.randint(0, state.shape[0], 1, dtype=int)
    y = np.random.randint(0, state.shape[1], 1, dtype=int)
    return [x, y]


class ImageProcessing:

    @staticmethod
    def simple_seed(width, height, isColor, bit_depth):
        if isColor:
            r = np.random.randint(0, bit_depth, width * height).reshape((width, height))
            g = np.random.randint(0, bit_depth, width * height).reshape((width, height))
            b = np.random.randint(0, bit_depth, width * height).reshape((width, height))
            return np.array([r, g, b])
        else:
            return np.random.randint(0, bit_depth, width * height).reshape((width, height))

    @staticmethod
    def filter_preview(images):
        f, ax = plt.subplots(1, len(images.keys()))
        II = 0
        for image in images.keys():
            ax[II].imshow(images[image], 'gray_r')
            ax[II].set_title(image)
            II += 1
        plt.show()

    @staticmethod
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


class Console:
    END = '\33[0m'
    RED = '\33[31m'
    GRN = '\33[92m'
    BLU = '\33[34m'
    PRP = '\33[35m'
    BRN = '\33[46m'
    WBG = '\33[7m'
    RBG = '\33[41m'
    BLD = '\33[1m'
    ITA = '\33[3m'


