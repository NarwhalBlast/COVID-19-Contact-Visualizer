"""CSC111 Project: COVID-19 Contact Visualizer

Module Description
==================
Simulation Module
This module contains ... epic gamer dabbing ! XD chug jug with me # TODO: Finish this description

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Simon Chen, Patricia Ding, Salman Husainie, Makayla Duffus
"""
import random

import networkx as nx

import data_processing
import dataclasses
import visualization as vis
from dataclasses import Graph
import plotly.graph_objects as go
from typing import Optional


class Simulation:
    """ A simulation of the graph over time.

    Instance Attributes:
        - _graph: The graph this simulation is representing.
        - _frames: A list of Plotly graph object frames
            (each frame represents one week in simulation time).
        - _init_infected: The set of initially infected people
        - _num_infected: The number of people who are initially infected
    """
    _graph: dataclasses.Graph
    _frames: list[go.Frame]
    _init_infected: set[str]
    _num_infected: int

    def __init__(self, graph: Optional[Graph] = None, num_infected: int = 1):
        if graph is not None:
            self._graph = graph
        else:
            self._graph = data_processing.generate_connected_graph(50)
        self._num_infected = num_infected
        self._init_infected = set()
        for _ in range(0, self._num_infected):
            self._init_infected.add(random.choice(list(self._graph.get_people())))
        self._frames = []

    def run(self, ticks: int, with_degrees: bool = False) -> None:
        """Run the simulation for a given amount of ticks.
        """
        self._graph.set_infected(self._init_infected)

        # Creates simulation buffer and infected sets.
        infected = self._init_infected
        buffer_infected = set()

        if with_degrees:
            self._graph.recalculate_degrees()
            graph_nx = self._graph.to_nx_with_degree_colour()
        else:
            graph_nx = self._graph.to_nx_with_simulation_colour()

        # Establishes a shared position of all notes in plotly pre-simulation
        pos = getattr(nx, 'spring_layout')(graph_nx)

        # Renders the initial state frame
        sliders_dict = {"steps": []}
        self._frames.append(vis.render_simulation_frame(self._graph, pos, 0, with_degrees))

        # Loops for the amount of ticks, rendering each frame as it goes
        for i in range(ticks):
            # Updates the infected and
            infected = infected.union(buffer_infected)
            self._graph.set_infected(buffer_infected)
            buffer_infected = set()
            # checking every connection where one node is infected
            for person in infected:
                for neighbour in self._graph.get_neighbours(person):
                    result = determine_infected(self._graph.get_weight(person, neighbour))

                    if result:
                        buffer_infected.add(neighbour.identifier)

            if with_degrees:
                self._graph.recalculate_degrees()

            # Renders the frame for the end of tick.
            self._frames.append(vis.render_simulation_frame(self._graph, pos, i, with_degrees))
            vis.update_slider(sliders_dict, i)

        vis.render_simulation_full(self._frames, sliders_dict, len(graph_nx.nodes))


def determine_infected(edge_weight: float) -> bool:
    """Determine if neighbour becomes infected and set the person's infected bool accordingly."""
    return random.choices([True, False], weights=(edge_weight, 1-edge_weight))[0]
