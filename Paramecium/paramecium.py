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
        actions = golgi.GolgiApparatus(self.life_time, 3, self.pos)
        actions.burst()
        return actions.seed.decision_tree


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
