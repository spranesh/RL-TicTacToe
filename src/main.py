#!/usr/bin/env python
"""
Bandit TestBed
Experimental test bed for bandit problems
"""

import Runner

import re
import Agent
import Environment

time = 0

def post_act_hook(environment, agent, state, actions, action):
    pass
    #print environment
    #global time
    #if action in environment.optimal_actions(state, actions):
    #    print time, 1,
    #else:
    #    print time, 0,

def post_react_hook(environment, agent, state, actions, reward):
    global time
    print reward
    time += 1

class ArgumentError(StandardError):
    def __init__(self, message=""):
        self.message = message

def main(epochs, agent, agentArgs, environment, environmentArgs):
    # Load agent and environment

    agent, environment = load(agent, agentArgs, environment, environmentArgs)
    runner = Runner.Runner(agent, environment)
    runner.post_act_hook = post_act_hook
    runner.post_react_hook = post_react_hook

    runner.run(epochs)

def help(args):
    print "Usage: %s <epochs> <agent> <environment>"%(args[0])

def convert(arg):
    if arg.isdigit():
        return int(arg)
    elif re.match("[0-9]*\.[0-9]+", arg):
        return float(arg)
    else:
        return arg

def load(agent, agentArgs, environment, environmentArgs):
    try:
        mod = __import__("Agent.%s"%(agent), fromlist=[Agent])
        assert( hasattr(mod, agent) )
        agent = getattr(mod, agent)
        agent = agent(*agentArgs)
    except (ImportError, AssertionError):
        raise ArgumentError("Agent '%s' could not be found"%(agent))

    try:
        mod = __import__("Environment.%s"%(environment), fromlist=[Environment])
        assert( hasattr(mod, environment) )
        environment = getattr(mod, environment)
        environment = environment(*environmentArgs)
    except (ImportError, AssertionError):
        raise ArgumentError("Environment '%s' could not be found"%(environment))

    return agent, environment

if __name__ == "__main__":
    import sys
    try:
        if "-h" in sys.argv[1:]:
            help(sys.argv)
        elif len(sys.argv) < 4:
            raise ArgumentError("Too few arguments")
        elif len(sys.argv) > 4:
            raise ArgumentError("Too many arguments")
        else:
            epochs = sys.argv[1]
            if not epochs.isdigit():
                raise ArgumentError("Epochs must be a valid integer")
            else:
                epochs = int(sys.argv[1])

            agent = sys.argv[2].split(":")
            agentArgs = [convert(arg) for arg in agent[1:]]
            agent = agent[0]

            environment = sys.argv[3].split(":")
            environmentArgs = [convert(arg) for arg in environment[1:]]
            environment = environment[0]

            main(epochs, agent, agentArgs, environment, environmentArgs)
    except ArgumentError as e:
        print "[Error]: %s"%(e.message)
        help(sys.argv)
        sys.exit(1)

