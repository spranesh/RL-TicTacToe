"""
Generic Value Based agent
"""

import Agent
from numpy import random

def state_(state):
    """Create a hashable by converting to a tuple"""
    return tuple( [ tuple( row ) for row in state ] )

class ValueAgent(Agent.Agent):
    """
    Generic Value-based agent
    """

    Q = {}

    def __init__(self, gamma = 0.9, alpha = 0.8, e = 0.1):
        Agent.Agent.__init__(self)
        self.gamma = gamma
        self.alpha = alpha
        self.e = e
        self.old_state = None
        self.old_action = None

    def update_Q(self, state, action, state_, action_, reward):
        raise NotImplemented()

    def act(self, state, actions, reward, episode_ended):
        # epsilon-greedy
        state = state_(state)
        if not self.Q.has_key(state):
            self.Q[state] = {}
            for action in actions:
                self.Q[state][action] = 0

        # Explore
        if random.random() < self.e:
            action = actions[random.randint(len(actions))]
        # Exploit
        else:
            action = max(actions, key = lambda x: self.Q[state][x])
        self.old_state = state
        self.old_action = action

        # Update actions
        if episode_ended:
            self.update_Q(self.old_state, self.old_action, None, None, reward)
        else:
            self.update_Q(self.old_state, self.old_action, state, action, reward)


        return action

