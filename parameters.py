
class Experiment_Setup:

    x_ratio = 2
    y_ratio = 2

    x_max = 100
    x_min = 0
    y_max = 100
    y_min = 0

    a = 1
    b = 1

    w_init = 1
    decay_factor = 0.9 # lambda
    p = 1
    n_0 = 5000
    time_steps = 100 # total time steps

class ExactEnv:

    height = Experiment_Setup.a
    width = Experiment_Setup.b

    Sample_Num = 1000

    Max_Coord = max(Experiment_Setup.x_max, Experiment_Setup.y_max)
    Min_Coord = min(Experiment_Setup.x_min, Experiment_Setup.y_min)

    max = max(Max_Coord + width, Max_Coord + height)
    min = min(Min_Coord - width, Min_Coord - height)

