import sys

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
import matplotlib.pyplot as plt
from PLMPM import *
from parameters import *


def plot3d(F):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(F[:, 0], F[:, 1], F[:, 2], c="r", marker="o")
    ax.set_xlabel("Custos de construção de plataformas")
    ax.set_ylabel("Produção de petróleo")
    ax.set_zlabel("Danos ambientais")
    plt.title("Localização de Plataformas de Petróleo")
    plt.show()


def plot2d(F):
    plt.scatter(F[:, 0], F[:, 1], c=F[:, 2], cmap="viridis", s=30, alpha=0.7)
    plt.xlabel("Custos de construção de plataformas")
    plt.ylabel("Produção de petróleo")
    plt.title("Localização de Plataformas de Petróleo")
    plt.show()


def solve_plmpm():
    problem = PLMPM(
        num_platforms, num_wells, num_capacities, c, f, a, b, DW, DQ, DO, DP
    )

    algorithm = NSGA2(
        pop_size=100,
        n_offsprings=10,
        sampling=FloatRandomSampling(),
        crossover=SBX(prob=0.65, eta=15),
        mutation=PM(
            eta=1 / (num_platforms * num_wells + num_platforms * num_capacities)
        ),
        eliminate_duplicates=True,
    )

    termination = get_termination("n_gen", 4000)
    res = minimize(
        problem, algorithm, termination, seed=1, save_history=True, verbose=False
    )

    return res.F


if __name__ == "__main__":
    # Resolve PLMPM
    F = solve_plmpm()

    if len(sys.argv) > 1 and sys.argv[1] == "--plot3d":
        plot3d(F)
    else:
        plot2d(F)
