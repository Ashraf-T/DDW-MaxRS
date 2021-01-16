from algo import approx_MaxRS, exactMaxRS, exactMaxRS_Naive
from exact.record_file import PointFile
from data_generator import DataGenerator
from point import Point
import random
import matplotlib.pyplot as plt
import logging
import os
import time
import seaborn as sns
import numpy as np
import ast
from parameters import Experiment_Setup
from plots import Plots
import sys
from experiment import Experiment

parameters_range = {'j': [1, 2, 4, 8], 'p': [1, 0.9, 0.8, 0.7, 0.6], 'decay_factor': [0.9, 0.8, 0.7, 0.6],
                   'rect': [1, 1.5, 2, 2.5, 3], 'n_0': [500, 1000, 5000, 10000, 50000, 100000]}

parameters_default_values = {'n_0': 5000, 'p': 1, 'decay_factor': 0.9, 'a': 1, 'b':1, 'ratio':2}

if __name__ == "__main__":

    if len(sys.argv) < 1:
        print("needs at least 1 argument: (j/p/R/lambda/n0)")
        exit()

    param = sys.argv[1]
    param_values = parameters_range[param]

    evaluation = Plots()
    agg_results = {}

    max_iter = 5
    run = 1

    for param_val in param_values:

        # TODO: set the experiment_setup parameter based on param_va
        agg_results[param_values] = {}
        evaluation.create_sub_folder(run)

        results = {'perf':{'exact': [[0] * Experiment_Setup.time_steps]*max_iter, 'approx': [[0] * Experiment_Setup.time_steps]*max_iter},
                   'time':{'exact': [[0] * Experiment_Setup.time_steps]*max_iter, 'approx': [[0] * Experiment_Setup.time_steps]*max_iter}}

        # for iter in range(max_iter):


