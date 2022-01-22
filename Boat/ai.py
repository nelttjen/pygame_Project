# AI for Self Driving Car

# Importing the libraries

import random
import os
import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim
from torch.autograd import Variable


# Creating the architecture of the Neural Network

class Network(nn.Module):

    def __init__(self, input_size, nb_action, internal_size):
        super(Network, self).__init__()
        self.input_size = input_size
        self.nb_action = nb_action
        self.input = nn.Linear(input_size, internal_size)
        self.hidden1 = nn.Linear(internal_size, internal_size)
        self.output = nn.Linear(internal_size, nb_action)

    def forward(self, state):
        x = f.relu(self.input(state))
        x = f.relu(self.hidden1(x))
        q_values = self.output(x)
        return q_values


# Implementing Experience Replay

class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, event):
        self.memory.append(event)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        samples = zip(*random.sample(self.memory, batch_size))
        return map(lambda x: Variable(torch.cat(x, 0)), samples)


# Implementing Deep Q Learning

class Dqn:
    loss_func = nn.MSELoss()

    # loss_func = F.smooth_l1_loss
    def __init__(self, gamma, learnBuffer, model):
        self.gamma = gamma
        self.learnBuffer = learnBuffer
        self.reward_window = []
        self.model = model
        self.memory = ReplayMemory(100000)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.last_state = torch.Tensor(model.input_size).unsqueeze(0)
        self.last_action = 0
        self.last_reward = 0
        self.learn_count = 0
        self.learn_score = 0

    def select_action(self, state):
        out = self.model(Variable(state, volatile=True))
        out[torch.isnan(out)] = 0
        out[torch.isinf(out)] = 0
        probs = f.softmax(out * 100)  # T=100
        action = probs.multinomial(self.model.nb_action)
        return action.data[0, 0]

    def learn(self, batch_state, batch_next_state, batch_reward, batch_action):
        outputs = self.model(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1)
        next_outputs = self.model(batch_next_state).detach().max(1)[0]
        target = self.gamma * next_outputs + batch_reward
        td_loss = self.loss_func(outputs, target)
        self.optimizer.zero_grad()
        td_loss.backward(retain_graph=True)
        self.optimizer.step()
        self.learn_score = self.score()
        self.learn_count += 1

    def update(self, reward, new_signal):
        new_state = torch.Tensor(new_signal).float().unsqueeze(0)
        self.memory.push(
            (self.last_state, new_state, torch.LongTensor([int(self.last_action)]), torch.Tensor([self.last_reward])))
        action = self.select_action(new_state)
        if len(self.memory.memory) > self.learnBuffer:
            batch_state, batch_next_state, batch_action, batch_reward = self.memory.sample(self.learnBuffer)
            self.learn(batch_state, batch_next_state, batch_reward, batch_action)
        self.last_action = action
        self.last_state = new_state
        self.last_reward = reward
        self.reward_window.append(reward)
        if len(self.reward_window) > 1000:
            del self.reward_window[0]
        return action

    def score(self):
        return sum(self.reward_window) / (len(self.reward_window) + 1.)

    def save(self):
        torch.save({'state_dict': self.model.state_dict(),
                    'optimizer': self.optimizer.state_dict(),
                    }, 'last_brain.pth')

    def load(self):
        if os.path.isfile('last_brain.pth'):
            print("=> loading checkpoint... ")
            checkpoint = torch.load('last_brain.pth')
            self.model.load_state_dict(checkpoint['state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            print("done !")
        else:
            print("no checkpoint found...")
