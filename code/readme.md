# PE-CA1-99210142-Seyyed Sajjad Mirzababaie

## M/M/1 queue Python3 simulator

According to Wikipedia in queueing theory, M/M/1 is a queue with 1 server, whereby arrivals follow a Poisson process while job service time is an exponential distribution.Simulation is implemented as [simulation.py](#empty) and analytical approach is implemented by [analyze.py](#empty) and all you need to simulate is to run the [main.py](#empty) file.

## Input

[parameters.conf](#empty) first line is **Teta** and second line is **Mu**.

## Output

Analytical and simulation result for lambda = [5,10,15] is stored within [result.csv](#empty) according to the following header :

- Teta

- Mu

- Lambda

- Analysis_type

- PB

- PD

## Objects

### Event

Event object includes three attribute:

- Time

- Process ID

- Type :
  1. Arrival

  2. Departure

  3. Deadline

### Process

Process Objects has following attributes:

- Process ID

- Arrival

- Deadline

- Service Time
