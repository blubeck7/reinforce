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


# the base fmdp is the history of moves made and contains the true function
# p(s', r|s, a) for the environment. Each agent has its own version of the fmdp
# so that each agent can have its own estimate of the environment's dynamcis
# and other agents' policies. 

base_fmdp = tictactoe.TicTacToeGame()
agent1 = agent.Agent("Agent 1", tictactoe.TicTacToeGame())
agent2 = agent.Agent("Agent 2", tictactoe.TicTacToeGame())
base_fmdp.set_agent(tictactoe.XAGENT, agent1)
base_fmdp.set_agent(tictactoe.OAGENT, agent2)

base_fmdp.display()
base_fmdp.do_turn()
# agent1.choose_action(base_fmdp)

# if __name__ == "__main__":
    # main()
