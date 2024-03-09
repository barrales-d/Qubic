# AI implementation for Qubic(3D tic-tac-toe)
#### Created for my CPSC 481 AI course final project

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

**Goal State:** 4 pieces in a row in any possible configuration

## Game Logic
Everything under GameLogic was created by [Sasidharan Mahalingam](https://github.com/sasidharan-m/qubic-solver/tree/master)

I've only copied the files necessary to have a working Qubic game in python 

His repository contains his implementation of AI for Qubic and more games so check it out!