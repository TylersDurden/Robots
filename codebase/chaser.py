import matplotlib.pyplot as plt, matplotlib.animation as animation
import sys, os, numpy as np, utility, scipy.ndimage as ndi


class Chase:
    prey_location = []
    pred_location = []
    state = [[]]
    n_steps = 0

    def __init__(self, initial_state, length):
        self.state = initial_state
        self.n_steps = length
        self.Prey = self.initialize_prey()
        self.Predator = self.initialize_predator()

    def initialize_prey(self):
        prey = utility.spawn_random_point(self.state)
        self.state[prey[0], prey[1]] = 10
        self.prey_location = prey
        return Prey(self.prey_location, self.state)

    def initialize_predator(self):
        predator = utility.spawn_random_point(self.state)
        self.state[predator[0], predator[1]] = -10
        self.pred_location = predator
        return Predator(self.pred_location, self.state)

    def chase_loop(self):
        state_changes = []
        self.pred_location, next_state = self.Predator.look_for_prey()
        state_changes.append(next_state)
        self.state = next_state
        # Update state
        if not self.Prey.alarmed:
            prey_moves, prey_changes = self.Prey.move_randomly()
            for change in prey_changes:
                state_changes.append(next_state)
            self.state = change
        ''' |==============||  CHASE_LOOP  ||==============|
        [1] Prey is unaware of Predator initially, so 
        first move is made by predator to check if it can
        see the prey. If it can it begins pursuit.
        
        [2] If in pursuit, prey will do it's best to evade
        else it is moving randomly. If predator is chasing
        prey, it will do it's best to follow prey. As it moves
        prey leaves behind a fleeting trail of it's presence. 
        
        [3] If predator gets within a designated kill radius 
        of prey, it wins the chase. If prey stays alive for all 
        steps it wins the chase by default. Additionally, the
        path of prey whose distance remains largest over time 
        should be scored as higher than one who survives but only
        very narrowly. 
        |==============||==============||==============| '''

    def run(self):
        for time_step in range(self.n_steps):
            self.chase_loop()


class Prey:
    location = []
    state = [[]]
    size = 0
    alarmed = False

    def __init__(self, loc, world):
        self.location = loc
        self.state = world

    def move_randomly(self):
        decisions = {1: [self.location[0]-1, self.location[1]-1],
                     2: [self.location[0], self.location[1]-1],
                     3: [self.location[0]+1, self.location[1]-1],
                     4: [self.location[0]-1, self.location[1]],
                     5: [self.location[0], self.location[1]],
                     6: [self.location[0]+1, self.location[1]],
                     7: [self.location[0]-1, self.location[1]+1],
                     8: [self.location[0], self.location[1]+1],
                     9: [self.location[0]+1, self.location[1]+1]}
        steps = np.random.randint(1, 10, 3)
        moves = []
        states = []
        for step in steps:
            self.state[self.location[0], self.location[1]] = 1
            self.location = decisions[step]
            moves.append(decisions[step])
            self.state[self.location[0], self.location[1]] = 10
            states.append(self.state)
        return moves, states

    def evade(self):
        predator = np.where(np.array(self.state) == np.array(self.state).min())
        print "EVADING PREDATOR AT " + str(predator)


class Predator:
    location = []
    state = [[]]

    def __init__(self, pos, world):
        self.location = pos
        self.state = world

    def look_for_prey(self):
        fov = [[1,1,1,1,1,1,1,1],
               [1,1,1,1,1,1,1,1],
               [1,1,1,1,1,1,1,1],
               [1,1,1,0,0,1,1,1],
               [1,1,1,0,0,1,1,1],
               [1,1,1,1,1,1,1,1],
               [1,1,1,1,1,1,1,1],
               [1,1,1,1,1,1,1,1]]
        world = ndi.convolve(np.array(self.state), np.array(fov))
        prey_loc = np.where(np.array(self.state) == world.max())

        print "FOUND PREY " + str(prey_loc)
        dx = prey_loc[0] - self.location[0]
        dy = prey_loc[1] - self.location[1]

        print '['+str(dx) + "," + str(dy)+']'
        # ==========
        # _1_ | 2__
        #  3  | 4
        # ==========
        # [1]: <-dx, +dy>
        # [2]: <+dx, +dy>
        # [3]: <-dx, -dy>
        # [4]: <+dx, -dy>
        return self.location, self.state


def choose_dimensions():
    resolution = {}
    shape = []
    ii = 0
    for i in range(25,125,25):
        ii += 1
        resolution[ii] = [12 * i, 10 * i]
        print str(ii) + " " + str(resolution[ii])
    try:
        shape = resolution[int(input('Enter a Selection: '))]
    except KeyError:
        print "Invalid Selection!"
        exit(0)
    return shape


def main():
    if '-d' in sys.argv:
        dims = choose_dimensions()
    else:
        dims = [250, 250]
    initial_state = np.zeros((dims[0], dims[1]))

    # ## ### #### ##### Now Initialize the game ##### #### ### ## #
    game = Chase(initial_state, 2)

    print "PREDATOR @ [" + str(game.pred_location[0]) + ',' + str(game.pred_location[1])+']'
    print "PREY @ [" + str(game.prey_location[0]) + ',' + str(game.prey_location[1]) + ']'
    # ## ### #### ##### ###### ###### ###### ##### #### ### ## #

    game.run()
    # plt.imshow(game.state, 'gray_r')
    # plt.show()


if __name__ == '__main__':
    main()
