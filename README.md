# Random Walks
Try out ``python imageine.py box random_walk``
and watch a random walk, using N Steps (you get to choose how many). 

![Example Output](https://raw.githubusercontent.com/TylersDurden/Robots/master/RandomWalkEx.png)

A video showing what a random walk looks like:
[Random Walking](https://raw.githubusercontent.com/TylersDurden/Robots/master/random_walking.mp4)


# Diffusion-Limited Aggregation
When many points are left to walk randomly, and are told that if they hit another point they can stop,
interesting crystalline structures tend to grow. Using ``python dla2.py -chk``, you can watch this 
process occur with over 5000+ points given 150 random steps each. In this simulation I let the particles
die in place and remain on screen if they complete all 150 steps without hitting anything or going off
screen. 

![dlaExample1](https://raw.githubusercontent.com/TylersDurden/Robots/master/Lattice.png)

A second example with a different initial condition [5500 Points]: 

![dlaEx2](https://raw.githubusercontent.com/TylersDurden/Robots/master/cube_growth.png)

A video example of the process occuring [2200 Points]: 

[dlaExVid](https://raw.githubusercontent.com/TylersDurden/Robots/master/dlaEx.mp4)

In dla2.py, particles are added on-screen sequentially (though their movements are precomputed 
offscreen for improved performance), greatly adding to the length of frames in the simulation (each particle added is captured in a frame, i.e. 5000 particles means 5000 frames). 

In this such DLA simulation, many particles can be initialized at once.The python program dla3.py
includes this new scheme. 

dla3 turns out to be significantly faster as well, considering how many
more particles and step combinations are added. 

![10KDLA](https://raw.githubusercontent.com/TylersDurden/Robots/master/10kDLA.png)

Here's a little screenshot demonstrating how much better the computation time scales for the diffusion limited
aggregation simulation when the random walk motion of particles is not only pre computed but rendered/simulated in
parallel, instead of sequentially like dla2.py 

![sdla_runtime](https://raw.githubusercontent.com/TylersDurden/Robots/master/computation_time.png)


Running points synchronously means less accumulate in the void from clouds of other dead points, and
hopefully because the programs computation scales better, we should be able to actually *see* the growth
of structures in a reasonable computation time with many more total points used. 

![SDLA](https://raw.githubusercontent.com/TylersDurden/Robots/master/synchronized_dla.mp4)

# Random Walk + Automata = Woah
This little program is really a testament to what you can do with one or two hundred lines of python code.
By designing the random walk to increment the pixels in it's path, and then having the automata eat up 
dense pixels spots, you can get a pretty wide variety of interesting results with only a little bit of code. 

![complex motion](https://raw.githubusercontent.com/TylersDurden/Robots/master/amoeba.mp4)
