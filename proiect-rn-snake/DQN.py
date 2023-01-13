from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import keras
import random
import numpy as np
import os 

GAMMA = 0.95 # discount rate
EPSILON = 1.0 # exploration rate
EPSILON_DECAY = 0.992
EPSILON_MIN = 0.01
MEMORY = 2000 #experience replay
LEARNING_RATE = 0.001


class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=MEMORY)
        self.gamma = GAMMA
        self.epsilon = EPSILON
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY
        self.learning_rate = LEARNING_RATE
        self.model = self._build_model()
        isExist = os.path.exists("snake.h5")
        if isExist:
            print("exista")
            self.model = keras.models.load_model("snake.h5")
            self.epsilon= self.epsilon_min
        else:
            self.model = self._build_model()
        

    def _build_model(self):
        model = Sequential()
        model.add(Dense(10, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state,verbose = 0)
        return np.argmax(act_values[0])


    def replay(self, batch_size):
        mb = random.sample(self.memory, min(len(self.memory), batch_size))

        states = []
        next_states = []
        actions = []
        rewards = []
        targets = []
        for state, action, reward, next_state, done in mb:
            states.append(np.asarray(state))
            next_states.append(np.asarray(next_state))
            actions.append(np.asarray(action))
            rewards.append(np.asarray(reward))
        ##########################################################################
        if len(states) >= 32:
            states = np.array(states).reshape(32, 6)
            next_states = np.asarray(next_states).reshape(32, 6)
            targets = rewards.copy()
            if not done:
                targets = rewards + self.gamma * np.amax(self.model.predict(next_states,batch_size=32,verbose = 0)[0])
            target_f = self.model.predict(states,batch_size=32,verbose = 0)
            target_f[0][actions] = targets
            self.model.fit(states, target_f, batch_size=32, verbose=0)
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay


    def save_model(self):
        self.model.save("snake.h5")