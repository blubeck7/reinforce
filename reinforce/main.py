"""
Main Module.

This module contains example of reinforcement learning.

Classes:

Functions:

Constants:

Exceptions:
"""


import agent
import tictactoe


def main():
    fmdp = tictactoe.TicTacToeGame()
    rand_agent = agent.RandomAgent("random", fmdp)

    fmdp.state.display()
    actions = fmdp.actions()
    print(actions)
    action = agent1.choose_action()
    print(action)

    return


if __name__ == "__main__":
    main()
