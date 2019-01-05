# Random Walks
Try out ``python imageine.py box random_walk``
and watch a random walk, using N Steps (you get to choose how many). 

![Example Output](https://raw.githubusercontent.com/TylersDurden/Robots/master/RandomWalkEx.png)

# Diffusion Limited Aggregation
When many points are left to walk randomly, and are told that if they hit another point they can stop,
interesting crystalline structures tend to grow. Using ``python dla2.py -chk``, you can watch this 
process occur with over 2000 points given 150 random steps each. In this simulation I let the particles
die in place and remain on screen if they complete all 150 steps without hitting anything or going off
screen. 

![dlaExample1](https://raw.githubusercontent.com/TylersDurden/Robots/master/Lattice.png)

A second example with a different initial condition: 

![dlaEx2](https://raw.githubusercontent.com/TylersDurden/Robots/master/cube_growth.png)

A video example of the process occuring: 

![dlaExVid](https://raw.githubusercontent.com/TylersDurden/Robots/master/dlaEx.mp4)
