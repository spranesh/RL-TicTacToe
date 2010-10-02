"""Responsible for running agents and interacting with the environment"""

import Agent
import Environment
import copy

class Runner:
    def __init__(self, agent, environment):
        self.agent = agent
        self.environment = environment

    def post_act_hook(self, environment, agent, state, actions, action):
        print "Action %s taken"%(str(action))

    def post_react_hook(self, environment, agent, state, actions, reward):
        print "New State: %s, Actions: %s, Reward: %s"%(state, actions, reward)

    def run(self, epochs):
        state, actions = self.environment.start()
        reward = 0

        for i in xrange(epochs):
            action = self.agent.act(copy.deepcopy(state), actions, reward)
            self.post_act_hook(self.environment, self.agent, state, actions, action)
            state, actions, reward = self.environment.react(action)
            self.post_react_hook(self.environment, self.agent, state, actions, reward)

