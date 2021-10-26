# oo-design

Casino games (Roulette and Craps) simulated using object orientated design best practices, with general classes such as `Table`, `Bet` and `Outcome` being shared between games. 

Several `Player` classes have been implemented to play with a variety of well-known betting strategies. Statistics are gathered over multiple runs of the simulation to compare the efficacy of these strategies (or which strategy loses the _least_ money).

Software quality:
- Complete with a full [pytest](https://docs.pytest.org/en/6.2.x/) test suite covering all code and functionality
- Typed, type checking with [mypy](https://github.com/python/mypy)
- Code formatting with [black](https://github.com/psf/black)

Design patterns explored:
- State
- Builder
- Factory
- Strategy
- Lazy initialization
- Wrap / extend

Repository of code from study of "Building Skills in Object-Oriented Design" by S. Lott.
