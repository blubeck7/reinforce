"""
Main Module.

This module contains example of reinforcement learning.

Classes:

Functions:

Constants:

Exceptions:
"""


from reinforce import agent
from reinforce import tictactoe


# the fmdp is the history of moves made and contains the true function
# p(s', r|s, a) for the environment. Each agent has its own version of the fmdp
# so that each agent can have its own estimate of the environment's dynamcis
# and other agents' policies. 

agent_1 = agent.Agent("Agent X")
agent_1.set_fmdp(tictactoe.TicTacToeGame())
agent_1.set_policy(agent.RandomPolicy())
agent_1.run()



# if __name__ == "__main__":
    # main()
