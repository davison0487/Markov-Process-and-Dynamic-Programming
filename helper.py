import numpy as np
import gym
import gym_minigrid
from utils import *

MF = 0 # Move Forward
TL = 1 # Turn Left
TR = 2 # Turn Right
PK = 3 # Pickup Key
UD = 4 # Unlock Door

def terminal_cost (env, info, destination):
    #destination = {'Key','Door','Goal'}
    
    if destination == 'Key':
        target = info['key_pos']
    elif destination == 'Door':
        target = info['door_pos']
    elif destination == 'Goal':
        target = info['goal_pos']
    else:
        print('Error input')
        return 1
    
    direction = [0,1,2,3] # 0: [1, 0], 1: [0, -1], 2: [-1, 0], 3: [0, 1]
    v = np.zeros([ info['width'], info['height'], len(direction) ])
    
    for i in range(info['width']):
        for j in range(info['height']):
            for k in direction:
                if i == target[0] and j == target[1]:
                    v[i,j,k] = 0
                elif isinstance(env.grid.get(i, j), gym_minigrid.minigrid.Wall):
                    v[i,j,k] = 1000000
                else:
                    v[i,j,k] = 1000
    return v


def stage_cost(env, info, control, destination):
    #control = { 'MF': 0 , 'TL,': 1 , 'TR': 2 }
    #destination = {'Key','Door','Goal'}
    
    direction = [0,1,2,3] # 0: [1, 0], 1: [0, -1], 2: [-1, 0], 3: [0, 1]
    v = np.zeros([ info['width'], info['height'], len(direction) ])

    if destination == 'Key':
        target = info['key_pos']
    elif destination == 'Door':
        target = info['door_pos']
    elif destination == 'Goal':
        target = info['goal_pos']
    
    for i in range(info['width']):
        for j in range(info['height']):
            for k in direction:
                if isinstance(env.grid.get(i, j), gym_minigrid.minigrid.Wall):
                    v[i,j,k] = 1000000
                    continue
                pos = np.array([i,j])
                if control == MF:
                    pos = move_forward(pos, k, info)
                    v[i,j,k] = norm(pos, target)
                elif control == TL:
                    index = (k + 1) % 4
                    v[i,j,k] = norm(pos, target) + direction_cost(pos, index, target, env)
                else:
                    index = (k - 1) % 4
                    v[i,j,k] = norm(pos, target) + direction_cost(pos, index, target, env)
    return v


def cost_t_plus_1(v_next, info, control, destination, t):
    direction = [0,1,2,3] # 0: [1, 0], 1: [0, -1], 2: [-1, 0], 3: [0, 1]
    v = np.zeros([ info['width'], info['height'], len(direction) ])
    
    for i in range(info['width']):
        for j in range(info['height']):
            for k in direction:
                pos = np.array([i,j])
                if control == MF:
                    [x, y] = move_forward(pos, k, info)
                    v[i,j,k] = v_next[x,y,k]
                elif control == TL:
                    index = (k + 1) % 4
                    v[i,j,k] = v_next[pos[0], pos[1], index]
                else:
                    index = (k - 1) % 4
                    v[i,j,k] = v_next[pos[0],pos[1], index]
    return v
    

def move_forward(pos, index, info):
    direc = dict([ (0,[1,0]), (1,[0,-1]), (2,[-1,0]), (3,[0,1]) ])
    width = info['width']
    height = info['height']
    
    pos += direc[index]
    if pos[0] < 0:
        pos[0] = 0
    if pos[0] > width-1:
        pos[0] = width-1
    if pos[1] < 0:
        pos[1] = 0
    if pos[1] > height-1:
        pos[1] = height-1
    return pos

    
def direction_cost(pos, index, target, env):
    direc = dict([ (0,[1,0]), (1,[0,-1]), (2,[-1,0]), (3,[0,1]) ])
    front = pos + direc[index]
    '''
    if isinstance(env.grid.get(front[0], front[1]), gym_minigrid.minigrid.Wall):
        return 1000000
    '''
    if norm(pos, target) > norm(front, target):
        return -0.01
    elif norm(pos, target) < norm(front, target):
        return 0.01
    else:
        return 0
    

def agent_dir_to_index(agent_dir):
    # 0: [1, 0], 1: [0, -1], 2: [-1, 0], 3: [0, 1]
    [x,y] = agent_dir
    if x == 1 and y == 0:
        return 0
    elif x == 0 and y == -1:
        return 1
    elif x == -1 and y == 0:
        return 2
    elif x == 0 and y == 1:
        return 3
    else:
        print("Error")
        return -1    

    
def norm(a,b):
    return np.sqrt( (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 )


def action_cost(policy):
    # direc = dict([ (0,[1,0]), (1,[0,-1]), (2,[-1,0]), (3,[0,1]) ])
    cost = dict ([ (0,2), (1,1), (2,1), (3,2000), (4,2000) ])
    count = 0;
    
    for i in policy:
        count += cost[i]
    
    return count
    
    
def terminal_cost_shortcut(env, info):
    
    target = info['goal_pos']
    
    direction = [0,1,2,3] # 0: [1, 0], 1: [0, -1], 2: [-1, 0], 3: [0, 1]
    v = np.zeros([ info['width'], info['height'], len(direction) ])
    
    for i in range(info['width']):
        for j in range(info['height']):
            for k in direction:
                if i == target[0] and j == target[1]:
                    v[i,j,k] = 0
                elif isinstance(env.grid.get(i, j), gym_minigrid.minigrid.Wall):
                    v[i,j,k] = 1000000
                elif isinstance(env.grid.get(i, j), gym_minigrid.minigrid.Key):
                    v[i,j,k] = 1000000
                elif isinstance(env.grid.get(i, j), gym_minigrid.minigrid.Door):
                    v[i,j,k] = 1000000
                else:
                    v[i,j,k] = 1000
    return v


def stage_cost_shortcut(env, info, control):
    #control = { 'MF': 0 , 'TL,': 1 , 'TR': 2 }
    
    direction = [0,1,2,3] # 0: [1, 0], 1: [0, -1], 2: [-1, 0], 3: [0, 1]
    v = np.zeros([ info['width'], info['height'], len(direction) ])

    target = info['goal_pos']
    
    for i in range(info['width']):
        for j in range(info['height']):
            for k in direction:
                if isinstance(env.grid.get(i, j), gym_minigrid.minigrid.Wall):
                    v[i,j,k] = 1000000
                    continue
                if isinstance(env.grid.get(i, j), gym_minigrid.minigrid.Key):
                    v[i,j,k] = 1000000
                    continue
                if isinstance(env.grid.get(i, j), gym_minigrid.minigrid.Door):
                    v[i,j,k] = 1000000
                    continue
                pos = np.array([i,j])
                if control == MF:
                    pos = move_forward(pos, k, info)
                    v[i,j,k] = norm(pos, target)
                elif control == TL:
                    index = (k + 1) % 4
                    v[i,j,k] = norm(pos, target) + direction_cost_shortcut(pos, index, target, env)
                else:
                    index = (k - 1) % 4
                    v[i,j,k] = norm(pos, target) + direction_cost_shortcut(pos, index, target, env)
    return v


def direction_cost_shortcut(pos, index, target, env):
    direc = dict([ (0,[1,0]), (1,[0,-1]), (2,[-1,0]), (3,[0,1]) ])
    front = pos + direc[index]
    
    if isinstance(env.grid.get(front[0], front[1]), gym_minigrid.minigrid.Wall):
        return 1000000
    if isinstance(env.grid.get(front[0], front[1]), gym_minigrid.minigrid.Key):
        return 1000000
    if isinstance(env.grid.get(front[0], front[1]), gym_minigrid.minigrid.Door):
        return 1000000
    
    if norm(pos, target) > norm(front, target):
        return -0.01
    elif norm(pos, target) < norm(front, target):
        return 0.01
    else:
        return 0