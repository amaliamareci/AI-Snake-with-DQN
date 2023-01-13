import numpy as np

class Player():
    moving_x = 0
    moving_y = 0
    action = 0

    def __init__(self, position, useless_steps,size):
        self.size = size
        self.body = []
        self.alive = True
        self.useless_steps = 0
        self.score = 0
        for x in range(useless_steps):
            self.body.append(position)

        self.action = 3
        self.moving_x = 0
        self.moving_y = 1


    def update(self, env) -> float:
        self.useless_steps += 1

        if (self.useless_steps == 500):
            self.alive = False
            return -1

        position = tuple(np.array(self.body[0]) + (self.moving_x, self.moving_y))
        
        if (position == env.food):
            self.body.insert(0, position)
            self.score += 1
            env.place_food(self.body)
            self.useless_steps = 0
            return 1

        if (not self.check_collision(position)):
            self.body.pop()
            self.body.insert(0, position)
            return 0
        else:
            self.alive = False
            return -1


    def check_collision(self, position):
        if (position) in self.body[:len(self.body)-1]:
            return True
        if (position[0] < 0 or position[0] >= self.size):
            return True
        if (position[1] < 0 or position[1] >= self.size):
            return True
        return False


    def move(self, action):
        #action = 0 - straight 
        #action = 1 - right
        #action = 2 - left
        if (action == 0):
            return

        if action == 1:
            if self.action == 1:
                self.action = 2
            elif self.action == 2:
                self.action = 3
            elif self.action == 3:
                self.action = 4
            elif self.action == 4:
                self.action = 1  
        elif action == 2:
            if self.action == 1:
                self.action = 4
            elif self.action == 2:
                self.action = 1
            elif self.action == 3:
                self.action = 2
            elif self.action == 4:
                self.action = 3

        if self.action == 1: #up
            self.moving_x = 0
            self.moving_y = -1
        if self.action == 2: #right
            self.moving_x = 1
            self.moving_y = 0
        if self.action == 3: #down
            self.moving_x = 0
            self.moving_y = 1
        if self.action == 4: #left
            self.moving_x = -1
            self.moving_y = 0
