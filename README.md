# Othello AI
Othello AI is based on Alpha Zero and uses reinforcement learning to play games of Othello. Othello AI learns primarily from self play, but can also learn using players that play with a random strategy or a pure Monte Carlo Search Tree. 

## TOC
1. Requirements
2. Training
3. Running the Simulator
4. Testing

## Requirements
Othello AI requires `Python >= 3.7.3`.

Othello AI should be run using a pytorch Docker image. Details coming soon.

## Training
Othello AI can be trained by executing the following command:
```
$ ./bin/start.sh
```
To stop training, run:
```
$ ./bin/stop.sh
```

## Running the Simulator
Use the following format to run the simulator:
```
simulator/run.py [OPTIONS] P1_TYPE P2_TYPE

Options:
  -v, --verbose  Print more output.
  -t, --train    Generate training data.
  --help         Show this message and exit.
```

`P1_TYPE` and `P2_TYPE` should be one of `["random", "mcts", "<model_filename>"]`. If a model name is used and the filename is passed in as a player type, the file must be located in the Othello AI home directory.

### Samples
Generate training data in verbose mode based on games between a random player and a player using a Monte Carlo Tree Search strategy.
```
$ simulator/run.py -v -t random mcts
```

Play a single game in verbose mode between a player using "saved_othello_model.10" and a player using a Monte Carlo Tree Search strategy.
```
$ simulator/run.py -v saved_othello_model.10 mcts
```

Generate training data based on games between two players using "saved_othello_model.10".
```
$ simulator/run.py -t saved_othello_model.10 saved_othello_model.10
```

## Testing
Details coming soon.