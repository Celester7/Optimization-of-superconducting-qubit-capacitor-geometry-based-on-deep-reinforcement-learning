
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import random
#import gym
from collections import deque
import T1_cal
import Q3D
#import mpl_toolkits.axisartist as ast
from scipy.interpolate import CubicSpline, interp1d
import math

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


e = 1.60217657e-19  # electron charge
hbar = 1.0545718E-34  # Plank's reduced
basic_g = 56.703
max_T1 = 450 
class Actor(nn.Module):  
    def __init__(self, state_dim, action_dim, max_action,min_action):
        super(Actor, self).__init__()
        self.layer1 = nn.Linear(state_dim, 64)  
        self.layer2 = nn.Linear(64, 32)       
        self.layer3 = nn.Linear(32, 16)
        self.layer4 = nn.Linear(16, action_dim)  
        self.max_action = max_action
        self.min_action = min_action
    def forward(self, x):
        x = x.float()
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        x = torch.relu(self.layer3(x))
        x = torch.tanh(self.layer4(x))
        max_a = torch.tensor(self.max_action, dtype=torch.float32)
        min_a = torch.tensor(self.min_action, dtype=torch.float32)
        x = (max_a - min_a) * (x + 1) / 2 + min_a
        return x
 
class Critic(nn.Module): 
    def __init__(self, state_dim, action_dim):
        super(Critic, self).__init__()
        self.layer1 = nn.Linear(state_dim + action_dim, 64)
        self.layer2 = nn.Linear(64, 32)
        self.layer3 = nn.Linear(32, 16)
        self.layer4 = nn.Linear(16, 1)
    def forward(self, x, u):
        x = torch.relu(self.layer1(torch.cat([x, u], 1)))
        x = torch.relu(self.layer2(x))
        x = torch.relu(self.layer3(x))
        x = self.layer4(x)
        return x
 
class DDPG:
    def __init__(self, state_dim, action_dim, max_action,min_action):
        self.actor = Actor(state_dim, action_dim, max_action,min_action)
        self.actor_target = Actor(state_dim, action_dim, max_action,min_action)
        self.actor_target.load_state_dict(self.actor.state_dict())
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=8e-4)  
                
        self.critic = Critic(state_dim, action_dim)
        self.critic_target = Critic(state_dim, action_dim)
        self.critic_target.load_state_dict(self.critic.state_dict())
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=4e-3)  
 
        self.replay_buffer = deque(maxlen=30000)
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.max_action = max_action
        self.min_action = min_action
    
    def select_action(self, state, epsilon,action_range):
        if np.random.uniform() < epsilon:
            a=np.array(action_range)
            r = np.random.rand(2)
            action = r * (a[:,1] - a[:,0]) +  a[:,0] 
            print({"random_action":action})
        else:
            inputs = torch.tensor(state, dtype=torch.float).unsqueeze(0)
            action = self.actor(inputs).squeeze(0)
            action = action.detach().numpy()
            print({"train_action":action})
        return action

    def train(self, batch_size, gamma, tau):
        if len(self.replay_buffer) < batch_size:
            return
        samples = list(self.replay_buffer)
        sample_weights = [abs(s[2]) + 0.1 for s in samples]  
        total_weight = sum(sample_weights)
        probs = [w / total_weight for w in sample_weights]
        samples = random.choices(samples, weights=probs, k=batch_size)
        print({"samples":samples})
        state, action, reward, next_state, done = zip(*samples)  
        state = torch.tensor(np.array(state), dtype=torch.float32)
        action = torch.tensor(np.array(action), dtype=torch.float32)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float32)
        reward = torch.tensor(np.array(reward), dtype=torch.float32).view(-1, 1)
        done = torch.tensor(np.array(done), dtype=torch.float32).view(-1, 1)
        next_action = self.actor_target(next_state).detach()  
        target_Q = self.critic_target(next_state, next_action).detach()  
        target_Q = reward + gamma * target_Q * (1 - done)
        current_Q = self.critic(state, action)
        critic_loss = nn.MSELoss()(current_Q, target_Q)
        self.critic_optimizer.zero_grad() 
        critic_loss.backward() 
        torch.nn.utils.clip_grad_norm_(self.critic.parameters(), max_norm=1.0)  
        self.critic_optimizer.step() 
        actor_loss = -self.critic(state, self.actor(state)).mean() 
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.actor.parameters(), max_norm=1.0) 
        self.actor_optimizer.step()
        for param, target_param in zip(self.actor.parameters(), self.actor_target.parameters()):
            target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)
        for param, target_param in zip(self.critic.parameters(), self.critic_target.parameters()):
            target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)
    
    def store_transition(self, state, action, reward, next_state, done):
        current_sample = (tuple(state), tuple(action))
        recent_samples = [(tuple(round(x,4) for x in s), tuple(round(x,4) for x in a)) for s,a,r,ns,d in list(self.replay_buffer)[-100:]]
        if current_sample in recent_samples:
            return
        if reward >= 1.5:
            self.replay_buffer.appendleft( (state, action, reward, next_state, done) )  
        else:
            self.replay_buffer.append((state, action, reward, next_state, done))

    def save_models(self, episode_count,dir_path1):
        torch.save(self.actor.state_dict(), str(dir_path1) + '/actor_' + str(episode_count) + '_policy.pth')
        torch.save(self.critic.state_dict(), str(dir_path1) + '/critic_' + str(episode_count) + '_value.pth')
        print("======================================")
        print("Models saved successfully!")
        print("======================================")

    def load_models(self, episode_count,dir_path1):
        self.actor.load_state_dict(torch.load(str(dir_path1) +'/actor_' + str(episode_count) + '_policy.pth'))
        self.critic.load_state_dict(torch.load(str(dir_path1) + '/critic_' + str(episode_count) + '_value.pth'))
        print("======================================")
        print("Models loaded successfully!")
        print("======================================")

class TopologyEnvironment:  
    def __init__(self,dir_path1,dir_path2, action_range):  
        self.action_range = action_range  
        self.state = None  
        self.t1_indicator = 0  
        self.previous_t1_indicator = 0
        self.visited_states = set()
        self.h=0
        self.l=40
        self.reset(dir_path1,dir_path2)  
  
    def reset(self,dir_path1,dir_path2):  
        self.topology = [self.h,self.l]
        self.state=self.topology
        self.visited_states.clear()
        self.t1_indicator, _ ,T1,g,wq,Cq,x_new,y_smooth1,y_smooth2,y_smooth3,y_smooth4, EC= self.calculate_t1(self.topology,dir_path1,dir_path2, basic_T1 = 0, basic_g = 0, basic_EC = 0)  # 假设有一个方法来计算T1  
        return self.topology, self.t1_indicator, T1, g, EC
    
    def is_done(self, reward):
        if reward>1.3:
            return True
        else:
            return False

    def step(self, action,dir_path1,dir_path2, basic_T1, basic_g, basic_EC,width = 430):  
        new_state = self.state 
        self.h=action[0]
        self.l=action[1]
        new_state = action
        self.state = new_state
        reward, state,T1,g,wq,Cq,x_new,y_smooth1,y_smooth2,y_smooth3,y_smooth4, EC = self.calculate_t1(new_state,dir_path1,dir_path2, basic_T1, basic_g, basic_EC,width)
        done = self.is_done(reward)  
        self.previous_t1_indicator = self.t1_indicator
        self.t1_indicator = T1
        return self.state, reward, done, action,T1,g,wq,Cq,x_new,y_smooth1,y_smooth2,y_smooth3,y_smooth4, EC

    def calculate_t1(self, state, dir_path1, dir_path2, basic_T1, basic_g, basic_EC, width = 430):  
        h=state[0]
        l=state[1]

        n = int(width/(l/2)) + 1
        x = [i*l/2 for i in range(n)]

        if width%(l/2) != 0:
            n += 1
            x.append(width)

        y1 = np.ones(len(x))*90
        y2 = []
        for i in range(len(x)-1):
            if i%2 == 0:
                y2.append(0)
            elif i%4 == 1:
                y2.append(h)
            elif i%4 == 3:
                y2.append(-h)
        if h == 0:
            y2.append(0)
        else:
            y2.append(y2[-1]+((width-(n-2)*l/2)/l/2*h)*(-1)**int((n+1)%4/2+1))
            
        l_lamda=math.sqrt(h**2+(l/2)**2)
        s = l_lamda/(l/2)  
        y3 = [y2[i]-30*s for i in range(len(y2))]
        y4 = y1-30*s-90*2

        d = -30*s+30
        y4 = [y4[i]-d for i in range(len(y4))]
        y3 = [y3[i]-d for i in range(len(y3))]
        y2 = [y2[i]-d for i in range(len(y2))]
        y1 = [y1[i]-d for i in range(len(y1))]
        cs1 = CubicSpline(x, y1)
        cs2 = CubicSpline(x, y2)
        cs3 = CubicSpline(x, y3)  
        cs4 = CubicSpline(x, y4)
        x_new = np.arange(0, width, 1)
        y_smooth1 = cs1(x_new) 
        y_smooth2 = cs2(x_new) 
        y_smooth3 = cs3(x_new) 
        y_smooth4 = cs4(x_new)

        plt.figure(figsize=(10, 5))
        plt.plot(x, y1, 'o')
        plt.plot(x_new, y_smooth1, '-')
        plt.plot(x, y2, 'o') 
        plt.plot(x_new, y_smooth2, '-')
        plt.plot(x, y3, 'o')
        plt.plot(x_new, y_smooth3, '-')
        plt.plot(x, y4, 'o')
        plt.plot(x_new, y_smooth4, '-')
        
        array=[]
        for i in range(len(x_new)):
            array.append(x_new[i]-width/2)

        y_smooth1 = [y + 15 for y in y_smooth1]
        y_smooth2 = [y + 15 for y in y_smooth2]
        y_smooth3 = [y + 15 for y in y_smooth3]
        y_smooth4 = [y + 15 for y in y_smooth4]
        
        Path = Q3D.get_Q3D(array,y_smooth1,y_smooth2,y_smooth3,y_smooth4,width,dir_path1)
        T1,g,wq,Cq = T1_cal.T1_purcell(Path)
        
        plt.xlabel("T1="+str(f"{T1:.3f}")+"_g="+str(f"{g:.3f}")+"_wq="+str(f"{wq:.3f}")+"_Cq="+str(f"{Cq*1e15:.3f}"))

        path=dir_path2+"/T1="+str(f"{T1:.3f}")+"_h="+str(f"{state[0]:.3f}")+"_l="+str(f"{state[1]:.3f}")+".png"  #T1
        
        plt.savefig(path,dpi=600)
        plt.close()
        EC = e**2 / 2 / Cq / hbar / 2 / np.pi / 1E6
        print({"T1":T1,"g":g,"wq":wq,"Cq":Cq, "EC":EC})
        
        w1 = 0.5
        w2 = 0.25
        w3 = 0.25
        if basic_T1 == 0:
            reward = 0.5
        else:
            reward = w1*T1/basic_T1-w2*abs(g/basic_g-1)-w3*abs(EC/basic_EC-1) 
        
            if T1 > basic_T1:
                reward += 0.2
            if abs(g/basic_g-1) > 0.2 or abs(EC/basic_EC-1) > 0.2:
                reward -= 0.3

            reward = np.clip(reward, -1.0, 2.0) 
             
        return reward, state, T1,g,wq,Cq,x_new,y_smooth1,y_smooth2,y_smooth3,y_smooth4, EC
    


