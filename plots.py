import time
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from parameters import Experiment_Setup
import logging

class Plots:

    def __init__(self):
        self.path = self.create_folder()
        self.path_runs = [self.path]

        pass

    def create_log_file(self, run):
        fileName = 'n_0 = {}, t = {}, lambda = {}, x_max, y_max=({}, {}), a, b=({}, {}), x_ratio, y_ratio=({}, {}), pr={}'.format(
            Experiment_Setup.n_0, Experiment_Setup.bb, str(Experiment_Setup.decay_factor), Experiment_Setup.x_max, Experiment_Setup.y_max, Experiment_Setup.a,
            Experiment_Setup.b, Experiment_Setup.x_ratio, Experiment_Setup.y_ratio, Experiment_Setup.p)
        logging.basicConfig(filename=os.path.join(self.path_runs[run], '{0}.log'.format(fileName)), filemode='w', level=logging.INFO)

        logging.info('number of init points: {}'.format(Experiment_Setup.n_0))
        logging.info('total #time_steps: {}'.format(Experiment_Setup.time_steps))
        logging.info('decay factor for all points is set to: {}'.format(Experiment_Setup.decay_factor))
        logging.info('target rectangle size is: {} * {}'.format(Experiment_Setup.a, Experiment_Setup.b))
        logging.info('cell ratios are: ({}, {})'.format(Experiment_Setup.y_ratio, Experiment_Setup.y_ratio))

    def create_folder(self):
        current_time = time.strftime('%Y-%m-%d_%H%M%S')

        path = os.path.join('output', current_time)
        os.makedirs(path)
        return path

    def create_sub_folder(self, run=1):

        self.path_runs[run] = os.path.join(self.path, 'run{}'.format(run))
        os.makedirs(self.path_runs[run])

        self.path_init_points = os.path.join(self.path_runs[run], 'points')
        os.makedirs(self.path_init_points)

        self.path_exact_data = os.path.join(self.path_runs[run], 'exact_data')
        os.makedirs(self.path_exact_data)

        self.path_plots = os.path.join(self.path_runs[run], 'plots')
        os.makedirs(self.path_plots)

    def median_outputs(self, results):

        output = {}
        if len(results) == 0:
            print('Error: no result')
        else:
            for key in results.keys():
                b = len(results[key][0])
                max_iter = len(results[key])
                output[key] = [0] * b

        for t in range(b):
            for key in output.keys():
                output[key][t] = np.median([results[key][it][t] for it in range(max_iter)])

        return output

    def avg_outputs(self, results):

        output = {}
        if len(results) == 0:
            print('Error: no result')
        else:
            for key in results.keys():
                output[key] = np.mean(results[key])
        return output

    def ratio_output(self, results):

        max_iter = len(results['exact'])
        b = len(results['exact'][0])

        output = {'approx_solution': [[0] * b] * max_iter}
        for it in range(max_iter):
            for t in range(b):
                output['approx'][it][t] = results['approx'][it][t] / results['exact'][it][t]
        return output

    def create_dict(self, grid_dict):
        res_dict = {}

        for key in grid_dict:
            res_dict[key] = grid_dict[key].getWeight()
        return res_dict

    def plot(self, results, b, name):

        sns.set_style("white")
        sns.set_context("paper")
        markers = ['s', 'o', 'v', 'x', 'p', '|']

        labels = {'dFactor': r'$\lambda$'+"={}", 'pr': "p={}", 'j': "j={}", 'rect': "R={0}x{0}"}
        step = 10

        fig1, ax1 = plt.subplots()
        i = 0
        for key in results.keys():
            ax1.plot(range(1, b, step), results[key]['perf']['approx'][1::step], label=labels[name].format(key),
                     marker=markers[i])
            i += 1
        ax1.set_xlim(1, b)
        ax1.set_ylim(0, 1.1)
        ax1.tick_params(axis='x', labelsize=14)
        ax1.tick_params(axis='y', labelsize=14)
        ax1.set_xlabel('time step', fontsize=17)
        ax1.set_ylabel('ratio to exact', fontsize=17)
        fig1.legend(fontsize=14)
        fig1.savefig(os.path.join(self.path, 'perf {}.eps'.format(name)), format='eps')
        fig1.savefig(os.path.join(self.path, 'perf {}.png'.format(name)), format='png', dpi=300)

    def bar_plot(self, results_u, results_g, name):

        sns.set_style("white")
        sns.set_context("paper")

        X = np.arange(len(results_u))
        ax = plt.subplot()
        ax.bar(X, results_u.values(), width=0.2, color='b', align='center', hatch="/")
        ax.bar(X - 0.2, results_g.values(), width=0.2, color='g', align='center', hatch="\\")
        ax.legend(('Uniform', 'Guassian'))
        if name == 'rect':
            x_ticks = ['{0}x{0}'.format(key) for key in results_u.keys()]
            plt.xticks(X, x_ticks)
        else:
            plt.xticks(X, results_u.keys())
        plt.savefig(os.path.join(self.path, 'bar_{}.eps'.format(name)), format='eps')
        plt.savefig(os.path.join(self.path, 'bar_{}.png'.format(name)), format='png', dpi=200)




