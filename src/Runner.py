"""Responsible for running agents and interacting with the environment"""

import copy

class Runner:
    """Responsible for running agents and interacting with the environment"""
    def __init__(self, agent, env):
        """
        @arg Agent
        @arg env
        """
        self.agent = agent
        self.env = env

    def post_act_hook(self, env, agent, state, actions, action):
        """ Function called after the agent returns an Action """
        print "Action %s taken" % (str(action))

    def post_react_hook(self, env, agent, state, actions, reward):
        """Function called after the environment acts on the Action"""
        print "New State: %s, Actions: %s, Reward: %s" % (
                state, actions, reward)

    def run(self, epochs):
        """ Simulate some epochs of running """

        state, actions = self.env.start()
        reward = 0

        for i in xrange(epochs):
            action = self.agent.act(copy.deepcopy(state), actions, reward)
            self.post_act_hook(self.env, self.agent, state, actions, action)
            state, actions, reward = self.env.react(action)
            self.post_react_hook(self.env, self.agent, state, actions, reward)

