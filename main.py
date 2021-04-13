"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Main Module
This module runs the entire COVID-19 Contact Visualizer. # TODO: Make this better after done.

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
import visualization
import data_processing
import random
from simulation import Simulation


def run_degrees_example() -> None:
    """ Run the example degrees risk visualization using the sample graph of people.
    """
    graph = data_processing.load_graph_csv('data/persons.csv', 'data/connections.csv')
    init_infected = {'WJ5751'}

    visualization.render_degrees_apart(graph, init_infected)


def run_degrees_example_generated() -> None:
    """ Run the example degrees risk visualization using the sample graph of people.
    """
    graph = data_processing.generate_connected_graph(50)
    init_infected = {random.choice(list(graph.get_people()))}

    visualization.render_degrees_apart(graph, init_infected)


def run_simulation_example() -> None:
    """ Run the example simulation using the sample graph of people.
    """
    # graph = data_processing.load_graph_csv('data/persons.csv', 'data/connections.csv')
    sim = Simulation()
    sim.run(10)


def run_simulation_example_with_degrees_preview() -> None:
    """ Run the example simulation using the sample graph of people, using the degree preview.
    """
    # graph = data_processing.load_graph_csv('data/persons.csv', 'data/connections.csv')
    sim = Simulation()
    sim.run(12, with_degrees=True)


if __name__ == '__main__':
    # visualize degree graph
    run_simulation_example()
