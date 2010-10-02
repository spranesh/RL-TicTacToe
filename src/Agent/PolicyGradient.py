"""
Implements a policy-gradient agent
"""

import Agent
import numpy as np
from numpy import random

class RandomDistribution:
    """Represents a generic random distribution"""
    def __init__(self, pdf):
        """Creates an arbitrary random distribution"""
        self.pdf = np.array(pdf)
        assert(self.pdf.all())
        
        self.cdf = self.__cdf(pdf)

    def __cdf(self, pdf):
        """Computes the CDF"""
        values = np.array(pdf)
        for i in xrange(1, len(values)):
            values[i] += values[i-1]
        return values
    
    def __search(self, value):
        """ Linear search for the value """
        for i in xrange(len(self.cdf)):
            if value < self.cdf[i]:
                return i
        else:
            raise ValueError()

    def sample(self):
        """ Sample from the distribution """
        return self.__search(random.random() * self.cdf[-1])

class GibbsDistribution(RandomDistribution):
    def __init__(self, pdf, T):
        """Creates an gibbs random distribution"""
        pdf = np.exp(np.array(pdf)/float(T))
        pdf /= sum(pdf)
        print pdf
        RandomDistribution.__init__(self, pdf)


def state_(state):
    """Create a hashable by converting to a tuple"""
    return tuple( [ tuple( row ) for row in state ] )

def count_moves(board):
    """Count the number of moves that have been played on the board
    @returns movedFirst?, moveNumber
    """
    count = abs(board).sum()
    return count/2

class PolicyGradient(Agent.Agent):
    r"""
    Implements a policy-gradient agent
    This performs the following update:
    p(s, a_i) <- p(s, a_i) + \alpha ( 1 - R_t \sum_j ... )
    Assuming a Gibbs-Boltzmann Distribution
    """

    theta = {}
    avg_reward = 0
    N = 0
    trajectory = []

    def __init__(self, beta = 0.1, T = 1):
        Agent.Agent.__init__(self)
        self.trajectory = []
        self.move_count = 0
        self.beta = beta
        self.T = T

    def init_state(self, state, actions):
        state = state_(state) 
        self.theta[state] = {}
        for action in actions:
            self.theta[state][action] = 0

    def detect_episode_boundary(self, state):
        count = self.move_count
        self.move_count = count_moves(state)
        return count > self.move_count

    def update_theta(self, reward):
        """Updates the action preferences (theta_i)"""
        if reward != -1:
            reward = 1
        self.N += 1
        self.avg_reward += (reward - self.avg_reward)/float(self.N)
        for state, action in self.trajectory:
            actions = self.theta[state].keys()
            for action_ in actions:
                val = self.theta[state][action]
                if action == action_:
                    update = self.beta * self.avg_reward * (1 - val)
                else:
                    update = self.beta * self.avg_reward * (-val)
                self.theta[state][action] += update

    def act(self, state, actions, reward, episode_ended):
        # Detect if the episode has finished
        if episode_ended:
            self.update_theta(reward)

        if not self.theta.has_key(state_(state)):
            self.init_state(state, actions)
        dist = GibbsDistribution( self.theta[state_(state)].values(), self.T)
        action = actions[ dist.sample() ]
        self.trajectory.append((state_(state), action))

        return action
