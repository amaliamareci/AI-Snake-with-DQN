from DQN import DQN
from Enviroment import Enviroment,cube
from Player import *

import pygame
import matplotlib.pyplot as plt

MINI_BATCH = 32
EPISODES = 600
env = Enviroment(8)
agent = DQN(6, 3)

score_list = []
for e in range(EPISODES):
    total_reward = 0
    done = False
    state = np.reshape(env.reset(), [1, 6])
    while not done:
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        next_state = np.reshape(next_state, [1, 6])
        agent.remember(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
        env.render()

    print("episode: {}/{}, score: {}, reward: {}".format(e, EPISODES, env.player.score, total_reward))
    score_list.append(env.player.score)
    agent.replay(MINI_BATCH)

plt.plot(score_list)
plt.show()

agent.save_model()
pygame.quit()
