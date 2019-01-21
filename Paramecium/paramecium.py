import sys, utility, numpy as np
import golgi


class Paramecium:
    life_time = 100
    pos = []
    state = [[]]

    def __init__(self, position, world):
        self.pos = position
        self.state = world
        print self.run()

    def run(self):
        actions = golgi.GolgiApparatus(self.life_time, 9, self.pos)
        actions.burst()
        random_route = actions.seed.decision_tree
        for step in random_route:
            # print str(actions.seed.random_steps.pop()) + " : " + str(random_route[step])
            perceptron(self.state,self.pos,{actions.seed.random_steps, random_route})


class perceptron:
    directions = {}
    Rules = {}
    world = [[]]
    pos = []

    action = {}

    def __init__(self, state, position, percept):
        self.world = state
        self.pos = position
        self.action = self.action_reaction(percept)

    def action_reaction(self, percept):
        self.directions = {1:[self.pos[0]-1, self.pos[1]-1],
                           2:[self.pos[0], self.pos[1]-1],
                           3:[self.pos[0]+1,self.pos[1]-1],
                           4:[self.pos[0]-1,self.pos[1]],
                           5:[self.pos],
                           6:[self.pos[0]+1,self.pos[1]],
                           7:[self.pos[0]-1,self.pos[1]+1],
                           8:[self.pos[0],self.pos[1]+1],
                           9:[self.pos[0]+1,self.pos[1]+1]}


def define_dimensions():
    width = int(input('Enter Width: '))
    height = int(input('Enter Height: '))
    return [width, height]


def main():
    if '-d' in sys.argv:    # Debug Mode
        initial_state = np.zeros((250, 250))
    else:
        initial_state = np.zeros(define_dimensions())
    # Create a paramecium
    cell = utility.spawn_random_point(initial_state)
    Paramecium(cell,initial_state)


if __name__ == '__main__':
    main()
