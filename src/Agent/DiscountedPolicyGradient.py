"""
Implements a policy-gradient agent with discounted rewards
"""

import Agent
import numpy as np

import PolicyGradient

class DiscountedPolicyGradient(PolicyGradient.PolicyGradient):
    """
    Implements a policy-gradient agent with discounted rewards
    """

    def __init__(self, gamma=0.9, beta=0.1, T = 0.1):
        PolicyGradient.PolicyGradient.__init__(self, beta, T)
        self.gamma = 0.9

    def update_theta(self, reward):
        discount = 1
        self.trajectory.reverse()
        for state, action in self.trajectory:
            actions = self.theta[state].keys()
            for action_ in actions:
                val = self.theta[state][action]
                if action == action_:
                    update = discount * self.beta * reward * (1 - val)
                else:
                    update = discount * self.beta * reward * (-val)
                self.theta[state][action] += update
            discount *= self.gamma

