"""
Implements a policy-gradient agent with averaged rewards
"""

import Agent
import numpy as np

import PolicyGradient

class AveragedPolicyGradient(PolicyGradient.PolicyGradient):
    """
    Implements a policy-gradient agent with averaged rewards
    """

    avg_reward = {}
    N = {}

    def update_theta(self, reward):
        self.trajectory.reverse()
        for state, action in self.trajectory:
            if not self.N.has_key(state):
                self.N[state] = 0
                self.avg_reward[state] = 0
            n = self.N[state]
            avg_reward = self.avg_reward[state]
            n += 1
            avg_reward += (reward - avg_reward)/float(n)

            actions = self.theta[state].keys()
            for action_ in actions:
                val = self.theta[state][action]
                if action == action_:
                    update = self.beta * avg_reward * (1 - val)
                else:
                    update = self.beta * avg_reward * (-val)
                self.theta[state][action] += update

            self.N[state] = n
            self.avg_reward[state] = avg_reward

