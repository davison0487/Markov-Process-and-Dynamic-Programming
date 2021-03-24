import numpy as np
import gym
import gym_minigrid
from utils import *
from example import example_use_of_gym_env
from helper import *
from matplotlib.pyplot import plot

MF = 0 # Move Forward
TL = 1 # Turn Left
TR = 2 # Turn Right
PK = 3 # Pickup Key
UD = 4 # Unlock Door

def doorkey_problem(env):
    '''
    You are required to find the optimal path in
        doorkey-5x5-normal.env
        doorkey-6x6-normal.env
        doorkey-8x8-normal.env
        
        doorkey-6x6-direct.env
        doorkey-8x8-direct.env
        
        doorkey-6x6-shortcut.env
        doorkey-8x8-shortcut.env
        
    Feel Free to modify this fuction
    '''
    # Initial condition
    prior = {}
    prior['pos'] = env.agent_pos
    prior['dir'] = env.dir_vec
    prior['front'] = env.front_pos
    
    # Get door status
    door = env.grid.get(info['door_pos'][0], info['door_pos'][1])
    is_open = door.is_open
    
    # Determine whether agent is carrying a key
    is_carrying = env.carrying is not None
    
    optim_act_seqq = [TL, MF, PK, TL, UD, MF, MF, MF, MF, TR, MF]
    
    return optim_act_seqq

    
def dynamic_programming(env, info, destination, t_horizon = 20):
    #destination = {'Key','Door','Goal'}
    direction = [0,1,2,3] # 0: [1, 0], 1: [0, -1], 2: [-1, 0], 3: [0, 1]
    
    v = np.zeros([ info['width'], info['height'], len(direction), t_horizon ])
    policy = np.zeros([ info['width'], info['height'], len(direction), t_horizon ])
        
    t_horizon -= 1
    v[:,:,:,t_horizon] = terminal_cost(env, info, destination)
    q = np.zeros([ info['width'], info['height'], len(direction), t_horizon, 3])
    
    for t in range(t_horizon-1, -1, -1):
        q[:,:,:,t,MF] = stage_cost(env, info, MF, destination) + cost_t_plus_1(v[:,:,:,t+1], info, MF, destination, t)
        q[:,:,:,t,TL] = stage_cost(env, info, TL, destination) + cost_t_plus_1(v[:,:,:,t+1], info, TL, destination, t)
        q[:,:,:,t,TR] = stage_cost(env, info, TR, destination) + cost_t_plus_1(v[:,:,:,t+1], info, TR, destination, t)
        for i in range(info['width']):
            for j in range(info['height']):
                for k in direction:
                    v[i,j,k,t] = min(q[i,j,k,t,:])
                    policy[i,j,k,t] = np.argmin(q[i,j,k,t,:])
    
    return policy, v


def dynamic_programming_shortcut(env, info, t_horizon = 20):
    destination = 'Goal'
    direction = [0,1,2,3] # 0: [1, 0], 1: [0, -1], 2: [-1, 0], 3: [0, 1]
    
    v = np.zeros([ info['width'], info['height'], len(direction), t_horizon ])
    policy = np.zeros([ info['width'], info['height'], len(direction), t_horizon ])
        
    t_horizon -= 1
    v[:,:,:,t_horizon] = terminal_cost_shortcut(env, info)
    q = np.zeros([ info['width'], info['height'], len(direction), t_horizon, 3])
    
    for t in range(t_horizon-1, -1, -1):
        q[:,:,:,t,MF] = stage_cost_shortcut(env, info, MF) + cost_t_plus_1(v[:,:,:,t+1], info, MF, destination, t)
        q[:,:,:,t,TL] = stage_cost_shortcut(env, info, TL) + cost_t_plus_1(v[:,:,:,t+1], info, TL, destination, t)
        q[:,:,:,t,TR] = stage_cost_shortcut(env, info, TR) + cost_t_plus_1(v[:,:,:,t+1], info, TR, destination, t)
        
        for i in range(info['width']):
            for j in range(info['height']):
                for k in direction:
                    v[i,j,k,t] = min(q[i,j,k,t,:])
                    policy[i,j,k,t] = np.argmin(q[i,j,k,t,:])
    return policy


def main(path):
    env, info = load_env(path) # load an environment
    env_shortcut, info_shortcut = load_env(env_path)
    key, key_v = dynamic_programming(env,info,'Key')
    door, door_v = dynamic_programming(env,info,'Door')    
    goal, goal_v = dynamic_programming(env,info,'Goal')
    goal_shortcut = dynamic_programming_shortcut(env_shortcut,info, 20)
    
    optimal_policy = []
    
    actions = {
        0: env.actions.forward,
        1: env.actions.left,
        2: env.actions.right,
        3: env.actions.pickup,
        4: env.actions.toggle
        }
    
    # walk to key
    for t in range(len(key[0,0,0,:])):
        [x,y] = env.agent_pos
        index = agent_dir_to_index(env.dir_vec)
        [i,j] = env.front_pos
        if isinstance(env.grid.get(i,j), gym_minigrid.minigrid.Key):
            break
        optimal_policy.append(key[x,y,index,t])
        env.step(actions[ key[x,y,index,t] ])
    temp =  np.swapaxes(goal[:,:,:,0],0,1)
    
    # pick up the key
    optimal_policy.append(PK)
    env.step(actions[PK])
    
    # walk to door
    for t in range(len(door[0,0,0,:])):
        [x,y] = env.agent_pos
        index = agent_dir_to_index(env.dir_vec)
        optimal_policy.append(door[x,y,index,t])
        env.step(actions[ door[x,y,index,t] ])
        [i,j] = env.front_pos
        if isinstance(env.grid.get(i,j), gym_minigrid.minigrid.Door):
            break
    
    # unlock the door
    optimal_policy.append(UD)
    env.step( actions[UD] )
    optimal_policy.append(MF)
    env.step( actions[MF] )
    
    # walk to goal
    for t in range(len(goal[0,0,0,:])):
        [x,y] = env.agent_pos
        if isinstance(env.grid.get(x,y), gym_minigrid.minigrid.Goal):
            break
        index = agent_dir_to_index(env.dir_vec)
        optimal_policy.append(goal[x,y,index,t])
        env.step( actions[goal[x,y,index,t]] )
    
    ### short cut ###
    shortcut_policy = []
    success = False
    
    for t in range(len(goal_shortcut[0,0,0,:])):
        [x,y] = env_shortcut.agent_pos
        index = agent_dir_to_index(env_shortcut.dir_vec)
        shortcut_policy.append(goal_shortcut[x,y,index,t])
        
        if shortcut_policy[-1] == 0:
            [i,j] = env_shortcut.front_pos
            if isinstance(env_shortcut.grid.get(i,j), gym_minigrid.minigrid.Wall):
                success = False
                break
            if isinstance(env_shortcut.grid.get(i,j), gym_minigrid.minigrid.Door):
                success = False
                break
            if isinstance(env_shortcut.grid.get(i,j), gym_minigrid.minigrid.Key):
                success = False
                break
        
        env_shortcut.step(actions[ goal_shortcut[x,y,index,t] ])
        #plot_env(env_shortcut)
        [i,j] = env_shortcut.front_pos
        if isinstance(env_shortcut.grid.get(i,j), gym_minigrid.minigrid.Goal):
            shortcut_policy.append(0)
            success = True
            break
    
    if success == True:
        door_policy_cost = action_cost(optimal_policy)
        shortcut_policy_cost = action_cost(shortcut_policy)
        if shortcut_policy_cost < door_policy_cost:
            optimal_policy = shortcut_policy
    
    draw_gif_from_seq(optimal_policy, load_env(env_path)[0], './gif/test.gif')

    return optimal_policy, key_v, door_v, goal_v


def plot_value_curve(key_v, door_v, goal_v):
    # 0: [1, 0], 1: [0, -1], 2: [-1, 0], 3: [0, 1]
    # key pos = [2,5,3], [1,6,0]
    # door pos = [2,5,0]
    # goal pos = [6,5,3], [5,6,0]
    key_value_1 = key_v[2,5,3,:]
    key_value_2 = key_v[1,6,0,:]
    door_value = door_v[2,5,0,:]
    goal_value_1 = goal_v[6,5,3,:]
    goal_value_2 = goal_v[5,6,0,:]
    a=2


if __name__ == '__main__':
    ### determine which environment ###
    env_path = './envs/example-8x8.env'
    #env_path = './envs/doorkey-5x5-normal.env'
    #env_path = './envs/doorkey-6x6-normal.env'
    #env_path = './envs/doorkey-8x8-normal.env'
    #env_path = './envs/doorkey-6x6-direct.env'
    #env_path = './envs/doorkey-8x8-direct.env'
    #env_path = './envs/doorkey-6x6-shortcut.env'
    #env_path = './envs/doorkey-8x8-shortcut.env'
    policy, key_v, door_v, goal_v = main(env_path)
    plot_value_curve(key_v, door_v, goal_v)
    
     
    
    
    
    
    
    