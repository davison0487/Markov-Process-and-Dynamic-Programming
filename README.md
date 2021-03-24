# Markov Process and Dynamic Programming

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
