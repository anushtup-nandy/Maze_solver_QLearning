'''
class for the MAZE:
    used Tkinter
    added walls, pitts
    Size is 10x10
    pixel size is 50x50 of each cell
'''

#---importing all the libraries---
import tkinter as tk
import numpy as np
import random
import time 

#---SIZE---
UNIT=50 #pixels per cell basically horizontally and vertically
MAZE_H=10
MAZE_W=10

#defining the origin
origin=np.array([UNIT/2, UNIT/2])

#CLASS maze:
class Maze(tk.Tk, object):
    def __init__(self, agentXY, goalXY, walls=[], pits=[]):
        super(Maze, self).__init__()

        self.action_space=['u', 'd', 'l', 'r']
        self.n_actions=len(self.action_space)
        self.wallblocks=[]
        self.pitblocks=[]
        self.UNIT=40
        self.MAZE_H=100
        self.MAZE_W=100
        self.title('MAZE')
        self.geometry('{0}x{1}'.format(MAZE_H*UNIT, MAZE_W*UNIT))
        self.build_shape_maze(agentXY, goalXY, walls, pits)
    
    '''
        adding walls , pitts, goals, and agents
    '''
    def add_wall(self, x,y):
        wall_center = origin + np.array([UNIT * x, UNIT*y])
        self.wallblocks.append(self.canvas.create_rectangle(
            wall_center[0] - 15, wall_center[1] - 15,
            wall_center[0] + 15, wall_center[1] + 15,
            fill='red'))
        
    def add_pitt(self,x,y):
        pit_center = origin + np.array([UNIT * x, UNIT*y])
        self.pitblocks.append(self.canvas.create_rectangle(
            pit_center[0] - 15, pit_center[1] - 15,
            pit_center[0] + 15, pit_center[1] + 15,
            fill='brown'))
    
    def add_agent(self, x=0, y=0):
        agent_center = origin + np.array([UNIT * x, UNIT*y])
        self.agent = self.canvas.create_rectangle(
            agent_center[0] - 15, agent_center[1] - 15,
            agent_center[0] + 15, agent_center[1] + 15,
            fill='blue')
    
    def add_goal(self, x=10, y=10):
        goal_center=origin+np.array([UNIT*x, UNIT*y])
        self.goal= self.canvas.create_oval(goal_center[0] - 15, goal_center[1] - 15,
            goal_center[0] + 15, goal_center[1] + 15,
            fill='black')

    '''
        Building the maze
    '''
    def build_shape_maze(self, agentXY, goalXY, walls, pits):
        self.canvas=tk.Canvas(self, bg='white', height=MAZE_H*UNIT, width=MAZE_W*UNIT)

        #creating the gridworld:
        for i in range(0, MAZE_W*UNIT, UNIT):
            x0, y0, x1, y1=i, 0, i, MAZE_H*UNIT
            self.canvas.create_line(x0,y0,x1,y1)
        for i in range(0,MAZE_H*UNIT, UNIT):
            x0, y0, x1, y1=0, i, MAZE_W*UNIT, i
            self.canvas.create_line(x0,y0,x1,y1)
        
        for a,b in walls:
            self.add_wall(a,b)
        for a,b in pits:
            self.add_pitt(a,b)

        self.add_goal(goalXY[0],goalXY[1])
        self.add_agent(agentXY[0],agentXY[1])
        self.canvas.pack()

    def reset(self, value = 1, resetAgent=True):
        self.update()
        time.sleep(0.2)
        if(value == 0):
            return self.canvas.coords(self.agent)
        else:
            #Reset Agent
            if(resetAgent):
                self.canvas.delete(self.agent)
                self.agent = self.canvas.create_rectangle(origin[0] - 15, origin[1] - 15,
                origin[0] + 15, origin[1] + 15,
                fill='red')
    
            return self.canvas.coords(self.agent)

    '''
        Rewards and step
    ''' 
    def Reward(self, cr_state, action, nxt_state):
        reverse=False
        if nxt_state == self.canvas.coords(self.goal):
            reward = 1
            done = True
            nxt_state = 'terminal'
        elif nxt_state in [self.canvas.coords(w) for w in self.wallblocks]:
            reward = -0.3
            done = False
            nxt_state = cr_state
            reverse=True
        elif nxt_state in [self.canvas.coords(w) for w in self.pitblocks]:
            reward = -10
            done = True
            nxt_state = 'terminal'
            reverse=False
        else:
            reward = -0.1
            done = False
        return reward,done, reverse
    
    def step(self,action):  #basicallt the step-dynamics 
        s = self.canvas.coords(self.agent)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_W - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_H - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action-=UNIT
        
        self.canvas.move(self.agent, base_action[0], base_action[1])

        s_ = self.canvas.coords(self.agent) #next_state

        reward, done, reverse=self.Reward(s, action, s_)

        if (reverse):
            self.canvas.move(self.agent, -base_action[0], -base_action[1])  # move agent back
            s_ = self.canvas.coords(self.agent)  

        return s_, reward, done
         
    def render(self, sim_speed=.01):
        time.sleep(sim_speed)
        self.update()

def update():
    for i in range(10):
        print('i is :', i)
        s= env.reset()
        
        while True:
            env.render()
            a=1
            s,r,done=env.step(a)
            if done:
                break

if __name__=='__main__':
    env=Maze()
    env.after(100, update)
    env.mainloop()
