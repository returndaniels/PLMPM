import sys

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
import matplotlib.pyplot as plt
from PLMPM import *
from parameters import *


def plot3d(F):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(F[:, 0], [abs(y) for y in F[:, 1]], F[:, 2], c="r", marker="o")
    ax.set_xlabel("Custos de construção de plataformas")
    ax.set_ylabel("Produção de petróleo")
    ax.set_zlabel("Danos ambientais")
    plt.title("Localização de Plataformas de Petróleo")
    plt.show()


def plot2d(F):
    plt.scatter(
        F[:, 0], [abs(y) for y in F[:, 1]], c=F[:, 2], cmap="viridis", s=30, alpha=0.7
    )
    plt.xlabel("Custos de construção de plataformas")
    plt.ylabel("Produção de petróleo")
    plt.title("Localização de Plataformas de Petróleo")
    plt.show()


def solve_plmpm():
    problem = PLMPM(
        num_platforms, num_wells, num_capacities, c, f, a, b, DW, DQ, DO, DP
    )

    algorithm = NSGA2(
        pop_size=pop_size,
        n_offsprings=10,
        sampling=BinaryRandomSampling(),
        crossover=TwoPointCrossover(prob=crossover_prob),
        mutation=BitflipMutation(prob=mutation_prob),
        eliminate_duplicates=True,
    )

    termination = get_termination("n_gen", n_gen)
    res = minimize(
        problem, algorithm, termination, seed=1, save_history=True, verbose=False
    )

    return (res.X, res.F)


def show_solution(solutions):
    for s in range(len(solutions)):
        x = solutions[s]
        x_ij = [x[i * num_wells : (i + 1) * num_wells] for i in range(num_platforms)]
        y_ik = [
            x[
                num_platforms * num_wells
                + i * num_capacities : num_platforms * num_wells
                + (i + 1) * num_capacities
            ]
            for i in range(num_platforms)
        ]
        w1 = [
            f"x{(i,j)}" if x_ij[i][j] else x_ij[i][j]
            for i in range(num_platforms)
            for j in range(num_wells)
        ]
        w2 = [
            f"y{(i,k)}" if y_ik[i][k] else y_ik[i][k]
            for i in range(num_platforms)
            for k in range(num_capacities)
        ]
        print(f"S{s} - X(i,j):\t{' '.join(list(filter(bool, w1)))}")
        print(f"S{s} - Y(i,k):\t{' '.join(list(filter(bool, w2)))}")


if __name__ == "__main__":
    print("O programa já está rodando.")
    print("Estamos buscando as Soluções Eficientes de Pareto")
    print("Isso pode levar algum tempo.\n")
    print("[=== Configurações ===]")
    print(f"Número de gerações: {n_gen}")
    print(f"Tamanho da população: {pop_size}")
    print(f"Probabilidade de cruzamento: {round(crossover_prob, 3):.3f}")
    print(f"Probabilidade de mutação: {round(mutation_prob, 3):.3f}")
    X, F = solve_plmpm()

    print("Soluções encontradas! Veja o gráfico.\n\n")
    print("Veja abaixo as Soluções Eficientes de Pareto:\n")
    show_solution(X)
    if len(sys.argv) > 1 and sys.argv[1] == "--plot3d":
        plot3d(F)
    else:
        plot2d(F)
