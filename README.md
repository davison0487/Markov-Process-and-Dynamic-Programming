# Markov Process and Dynamic Programming
Motion planning is a crucial part in robotics problems. Usually there are obstacles in different environments and we cannot simply ignore noises. Hence, we need to determine a best policy for the robot at current state to make decisions for control input. In this project, we are working in a door and key environment. The goal is to get our agent to goal location. If the agent ever encounter a door, he has to pick up the key in order to unlock and get pass the door. However, there are some cases that there exists a short cut that he can walk directly to treasure location without going through the door. We are assuming our environment is well observed by the robot (agent) and every motion input is non-stochastic. By applying Markov Decision Process and dynamic programming algorithm, we can obtain a best policy to reach the goal at each time step and each state.


### 1. doorkey.py
Main script generates optimal policy and saves into gif files into './gif' with implementation of dynamic programming algorithm 

### 2. helper.py
Some self-built functions including terminal_cost(), stage_cost() and other usefull functions.

### 3. utils.py
You might find some useful tools in utils.py
- **step()**: Move your agent
- **generate_random_env()**: Generate a random environment for debugging
- **load_env()**: Load the test environments
- **save_env()**: Save the environment for reproducing results
- **plot_env()**: For a quick visualization of your current env, including: agent, key, door, and the goal
- **draw_gif_from_seq()**: Draw and save a gif image from a given action sequence. **Please notice that you have to submit the gif!**

### 4. example.py
The example.py shows you how to interact with the utilities in utils.py, and also gives you some examples of interacting with gym-minigrid directly.


# Results

The following three environments are normal cases that we need to pick up the key and unlock the door to reach the goal. Results are fantastic.
 
![image](https://github.com/davison0487/Markov-Process-and-Dynamic-Programming/blob/main/gif/doorkey-5x5-normal.gif)

[TL, PK, TR, UD, MF, MF, TR]

Note that in doorkey-6x6-normal case, there are two initial choices which are MF and TR, both are fine. However, according to my implementation, it tends to move forward if it will bring robot closer to goal. As a result, it chooses MF instead of TR
 
 ![image](https://github.com/davison0487/Markov-Process-and-Dynamic-Programming/blob/main/gif/doorkey-6x6-normal.gif)
 
[MF, TR, PK, MF, MF, MF, TR, MF, UD, MF, MF, TR, MF, MF]

There is something interesting in 8x8 normal case. Take a look at robot decision after it has walk pass the door (highlighted part). As I mentioned before that the robot tends to move forward, which is not the case here. This is because after turning right, the block in front of robot actually have smaller distance than the block of moving forward. As a result, it chooses to turn right here.

![image](https://github.com/davison0487/Markov-Process-and-Dynamic-Programming/blob/main/gif/doorkey-8x8-normal.gif)

[TL, MF, TR, MF, MF, MF, TR, PK, TR, MF, MF, MF, MF, TR, UD, MF, MF, TR, MF, MF, MF, MF, MF, TL]


Now let’s try environments that exist a direct path leads to the goal without using key and door. Turns out that my implementation of action cost works just fine. The agent walk directly to the treasure without considering the key.
 
![image](https://github.com/davison0487/Markov-Process-and-Dynamic-Programming/blob/main/gif/doorkey-6x6-direct.gif)

[TL, TL, MF]
  
![image](https://github.com/davison0487/Markov-Process-and-Dynamic-Programming/blob/main/gif/doorkey-8x8-direct.gif)

[TL, MF, MF]

Things can get complicated if the environment exist a path, but it’s not the shortest path to treasure. Normally, agent will choose to use key and door since it is shorter. What if picking up key and unlocking door are very energy costly job? Here I included policies for both scenarios. The second scenario can be considered as the robot is very bad at doing such job (which is true for robot in some sense), thus it will have huge action cost. To implement this situation, we simply alter the value of PK and UD action cost to a very large value.
For huge cost scenario in 6x6 environment, the robot kind of stuck in a loop of turning during its adventure. Interestingly, it didn’t happen in 8x8 environment, I am still figuring out why this is happening.
  
![image](https://github.com/davison0487/Markov-Process-and-Dynamic-Programming/blob/main/gif/doorkey-6x6-shortcut-huge-action-cost.gif)

[PK, TL, TL, UD, MF]
[TL, MF, TR, TR, TL, TR, TL, MF, TL, MF,
MF, TL, MF, MF, MF, TL, MF, MF]


Also, for this 8x8 environment, we need extra time horizon since the “shortcut” is actually longer. T=25 would be sufficient.
  
![image](https://github.com/davison0487/Markov-Process-and-Dynamic-Programming/blob/main/gif/doorkey-8x8-shortcut-huge-action-cost.gif)

[MF, TR, PK, TR, MF, TR, MF, UD, MF]
[TL, MF, TR, MF, MF, MF, TR, MF, MF, TL, MF, 
MF, TL, MF, MF, MF, MF, TL, MF, MF, MF, MF]
