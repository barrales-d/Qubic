# Qai: AI implementation for Qubic(3D tic-tac-toe)
#### By: Diego Barrales,
#### Created for my CPSC 481 AI course final project

# Problem Statement
Qubic is a 3D tic-tac-toe variant in which two players take turns to place pieces on a 4x4x4 cube board consisting of 64 cells. The goal is to get four pieces lined up in a row. I will implement a competitive AI agent that humans can play against. In addition, I want to visualize the agent's thinking process through a simple graphical user interface that humans can use to play the game.
    
## State Space Representation
| Properties of Qubic Environment | Details |
|--|--|
| Fully observable | Full 4x4x4 board is observable |
| Multiple agents | Competitive  |
| Deterministic | Next state of 4x4x4 board is determined by current state of the board |
| Sequential | each decision can be made only once |
| Static | The agents take turns placing their piece on board |
| Discrete | can only make finite actions |
| Known | The rules of Qubic are known |

## State Space Search
**States:** Possible board positions

**Operators:** Placing their piece in an empty space in the board

**Initial State:** empty 4x4x4 board

**Goal State:** 4 pieces in a row in any possible configurations

# Programming Language
I will use Python as the primary programming language to implement the AI agent. Python offers various libraries that have been created and tested. Some libraries I am considering are PyTorch and OpenAI's Gym toolkit. For the GUI I want to implement, I will be using Pygame.
# Starting Code and Extensions
I have found a GitHub repository that contains the code necessary to implement the entire game loop for Qubic in the terminal; Sasidharan Mahalingam created this repository here: https://github.com/sasidharan-m/qubic-solver/tree/master. This repository also contains code for implementing different AI agents, but I only copied the code necessary for the base game loop. The extensions I will add to this starter code are my implementations of AI agents and a GUI that will take the existing game from the terminal into an actual game window display. 

# Algorithm and Appoarch
From my research, I will need to create a game tree and perform either a minimax search algorithm or an alpha-beta pruning algorithm. In addition, the game tree for a single state could grow reasonably large. Therefore, I think I should implement these algorithms with maximum depth in mind. 

# Timeline
I have copied the starting code enough to get a working Qubic game with two human players. The following steps will be implementing the two algorithms and adding a GUI. The GUI will be more time-consuming because I need to mix the starter code with the Pygame library. So, I will implement the algorithms first and ensure they are working correctly.

# Roles and Responsibilities
I am working alone on this project and have no experience with AI, but the resources I have been given will help me implement this AI agent quickly. I can use the starter code GitHub as a resource to ensure I am on the right track. Finally, I have taken a CPSC 386 game design course and have the experience needed with Pygame to implement the GUI. 