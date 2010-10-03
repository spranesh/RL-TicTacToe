#!/usr/bin/env python
"""
Bandit TestBed
Experimental test bed for bandit problems
"""

import Runner

import re
import Agent
import Environment

__time__ = 0

class ArgumentError(StandardError):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

def post_act_hook(env, agent, state, actions, action):
    """Do something after an action has been chosen"""
    pass
    #print env
    #global __time__
    #if action in env.optimal_actions(state, actions):
    #    print __time__, 1,
    #else:
    #    print __time__, 0,

def post_react_hook(env, agent, state, actions, reward, episode_ended):
    """Do something after the environment handles an action"""
    global __time__
    if episode_ended:
        print reward
    __time__ += 1

def main(epochs, agent_str, agent_args, env_str, env_args):
    """RL Testbed.
    @arg epochs: Number of episodes to run for
    @arg agent_str: String name of agent
    @arg agent_args: Arguments to the agent constructor
    @arg env_str: String name of environment
    @arg env_args: Arguments to the environment constructor
    """
    # Load agent and environment

    agent, env = load(agent_str, agent_args, env_str, env_args)
    runner = Runner.Runner(agent, env)
    runner.post_act_hook = post_act_hook
    runner.post_react_hook = post_react_hook

    runner.run(epochs)
    for state in agent.theta: 
        print state
        print agent.theta[state]

def load(agent_str, agent_args, env_str, env_args):
    """Try to load a class for agents or environment"""
    try:
        mod = __import__("Agent.%s"%(agent_str), fromlist=[Agent])
        assert( hasattr(mod, agent_str) )
        agent = getattr(mod, agent_str)
        agent = agent(*agent_args)
    except (ImportError, AssertionError):
        raise ArgumentError("Agent '%s' could not be found"%(agent_str))

    try:
        mod = __import__("Environment.%s"%(env_str), fromlist=[Environment])
        assert( hasattr(mod, env_str) )
        env = getattr(mod, env_str)
        env = env(*env_args)
    except (ImportError, AssertionError):
        raise ArgumentError("Environment '%s' could not be found"%(env_str))

    return agent, env

def print_help(args):
    """Print help"""
    print "Usage: %s <epochs> <agent> <environment>" % (args[0])

def convert(arg):
    """Convert string arguments to numbers if possible"""
    if arg.isdigit():
        return int(arg)
    elif re.match("[0-9]*\.[0-9]+", arg):
        return float(arg)
    else:
        return arg

if __name__ == "__main__":
    import sys
    def main_wrapper():
        """Wrapper around the main call - converts input arguments"""
        try:
            if "-h" in sys.argv[1:]:
                print_help(sys.argv)
            elif len(sys.argv) < 4:
                raise ValueError("Too few arguments")
            elif len(sys.argv) > 4:
                raise ValueError("Too many arguments")
            else:
                epochs = sys.argv[1]
                if not epochs.isdigit():
                    raise ValueError("Epochs must be a valid integer")
                else:
                    epochs = int(sys.argv[1])

                agent_str = sys.argv[2].split(":")
                agent_args = [convert(arg) for arg in agent_str[1:]]
                agent_str = agent_str[0]

                env_str = sys.argv[3].split(":")
                env_args = [convert(arg) for arg in env_str[1:]]
                env_str = env_str[0]

                main(epochs, agent_str, agent_args, env_str, env_args)
        except ArgumentError as error:
            print "[Error]: %s" % (str(error))
            print_help(sys.argv)
            sys.exit(1)
    main_wrapper()
