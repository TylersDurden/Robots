import matplotlib.pyplot as plt


class Point:
    xloc = 0
    yloc = 0
    value = 1

    # DIRECTIONAL_VALUED_INDICES
    # [[1,2,3],
    #  [4,5,6],
    #  [7,8,9]]

    directions = {1:'uleft',
                  2:'up',
                  3:'uright',
                  4:'left',
                  5:'self',
                  6:'right',
                  7:'dleft',
                  8:'down',
                  9:'dright'}

    cardinal = {'up': [xloc, yloc+1],
                'down': [xloc, yloc-1],
                'left': [xloc-1,yloc],
                'right': [xloc+1,yloc],
                'uleft': [xloc-1,yloc-1],
                'uright': [xloc+1,yloc-1],
                'dleft': [xloc-1,yloc+1],
                'dright': [xloc+1,yloc+1],
                'self': [xloc, yloc]}

    def __init__(self, pos, val):
        self.xloc = pos[0]
        self.yloc = pos[1]
        self.value = val

    def change_value(self, new_value):
        self.value = new_value

    def movement_calc(self, next_pos):
        """
        Return the difference between both current x
        and next position x, and between current y
        and the next position y. Returns [dx, dy]
        :param next_pos:
        :return [dx, dy]:
        """
        dx = next_pos[0] + self.xloc
        dy = next_pos[1] + self.yloc
        return [dx, dy]

    def get_neighborhood(self, state):
        u = 0
        l = 0
        r = self.state.shape[0]
        d = self.state.shape[1]

        if self.yloc - 1 > 0:
            u = self.yloc - 1
        if self.xloc - 1 > 0:
            l = self.xloc - 1
        if self.xloc + 1 < self.state.shape[0]:
            r = self.xloc + 1
        if self.yloc + 1 < self.state.shape[1]:
            d = self.yloc + 1

        hood = state[self.xloc-1:self.xloc+1,
                     self.yloc-1:self.yloc+1]

    def move(self, direction, state):
        if direction not in self.directions.keys():
            print "Invalid direction!"
            return 0
        else:
            # If moving, erase previous block
            state[self.xloc,self.yloc] = 0
            choice = self.directions[direction]
            newpos = self.cardinal[choice]
            next_pos = self.movement_calc(newpos)

            self.xloc = next_pos[0]
            self.yloc = next_pos[1]
        return state


    def show(self, state):
        state[self.xloc,self.yloc] = self.value
        plt.imshow(state,'gray_r')
        plt.show()