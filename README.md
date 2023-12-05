# Algoritmos-evolutivos-paralelizables-con-CUDA

## Description
This repository contains an autonomous car simulation project using Python, Pygame, and the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The goal is to simulate a vehicle that learns to navigate a track, avoiding obstacles and staying within boundaries, using an evolutionary neural network.

## Features
- Simulation of an autonomous car in a graphical environment.
- Use of the NEAT algorithm to evolve the neural network.
- Control of the car's direction and speed based on the neural network output.
- Visualization of the car and track using Pygame.

## Requirements
- Python 3.x
- Pygame
- NEAT-Python
- Numpy (optional, depending on how you process the track image)


## Project Structure
- `car.py`: Contains the definition of the `Car` class and logic to load the neural network.
- `main.py`: Main script to run the simulation.
- `config-feedforward.txt`: NEAT configuration used to train the neural network.
- `winner.pkl`: Stores the weights of the winning neural network (you need to generate this file).
- `track.png`: Track image for the simulation.
- `car.png`: Image of the car used in the simulation.

## Customization
You can modify the track and the car by changing `track.png` and `car.png`. Additionally, you can adjust NEAT parameters in `config-feedforward.txt` to experiment with different network configurations.
