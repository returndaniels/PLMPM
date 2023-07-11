from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np


class PLMPM(ElementwiseProblem):
    def __init__(
        self, num_platforms, num_wells, num_capacities, c, f, a, b, DW, DQ, DO, DP
    ):
        super().__init__(
            n_var=num_platforms * num_wells + num_platforms * num_capacities,
            n_obj=3,
            n_constr=3 * num_platforms,
            xl=np.zeros(36),
            xu=np.ones(36),
        )

        self.num_platforms = num_platforms
        self.num_wells = num_wells
        self.num_capacities = num_capacities
        self.c = c
        self.f = f
        self.a = a
        self.b = b
        self.DW = DW
        self.DQ = DQ
        self.DO = DO
        self.DP = DP

    def _evaluate(self, x, out, *args, **kwargs):
        x_ij = [
            x[i * self.num_wells : (i + 1) * self.num_wells]
            for i in range(self.num_platforms)
        ]
        y_ik = [
            x[
                self.num_platforms * self.num_wells
                + i * self.num_capacities : self.num_platforms * self.num_wells
                + (i + 1) * self.num_capacities
            ]
            for i in range(self.num_platforms)
        ]

        # minimizar os custos
        z1 = sum(
            self.c[i][j] * x_ij[i][j]
            for i in range(self.num_platforms)
            for j in range(self.num_wells)
        ) + sum(
            self.f[i][k] * y_ik[i][k]
            for i in range(self.num_platforms)
            for k in range(self.num_capacities)
        )

        # maximizar a produção de petróleo
        z2 = sum(
            -self.a[j] * x_ij[i][j]
            for i in range(self.num_platforms)
            for j in range(self.num_wells)
        )

        z3 = 0.0  # minimizar danos ambientais
        for i in range(self.num_platforms):
            # Objetivo: sum_{i in I} [sum_{j in J}(DW_{j}+DQ_{ij})x_{ij}+sum_{k in K}(DO_{i}+DP_{ik})y_{ik}
            z3 += sum(
                [
                    (self.DW[j] + self.DQ[i][j]) * x_ij[i][j]
                    for j in range(self.num_wells)
                ]
            )
            z3 += sum(
                [
                    (self.DO[i] + self.DP[i][k]) * y_ik[i][k]
                    for k in range(self.num_capacities)
                ]
            )

        constraints = []
        for i in range(self.num_platforms):
            # Soma dos elementos de cada linha deve ser igual a 1
            g1 = sum([x_ij[i][j] for j in range(self.num_wells)]) - 1

            # Soma dos elementos de cada linha deve ser igual a 1
            g2 = sum([y_ik[i][k] for k in range(self.num_capacities)]) - 1

            # Restrição: sum_{j in J} a_{j}x_{ij} - sum_{k in K} b_{k}y_{ik} ≤ 0
            sum_a = sum([self.a[j] * x_ij[i][j] for j in range(self.num_wells)])
            sum_b = sum([self.b[k] * y_ik[i][k] for k in range(self.num_capacities)])
            g3 = sum_a - sum_b

            constraints.append(g1)
            constraints.append(g2)
            constraints.append(g3)

        out["F"] = np.column_stack([z1, z2, z3])
        out["G"] = np.column_stack(constraints)


# tamanho do conjunto que representa possíveis locais para instalação de plataformas de petróleo (I)
num_platforms = 3
# tamanho do conjunto que representa possíveis locais para instalação de poços de petróleo (J)
num_wells = 10
# conjunto que representa os níveis de capacidade das plataformas de petróleo (K)
num_capacities = 2
# custo de perfuração de um poço de petróleo j ∈ J a partir de uma plataforma na localização i ∈ I
c = [
    [5, 8, 6, 9, 7, 6, 4, 5, 3, 7],
    [7, 6, 5, 8, 6, 4, 9, 7, 6, 5],
    [4, 5, 3, 7, 6, 8, 6, 9, 7, 6],
]
#  custo para construção e instalação de uma plataforma de petróleo na localização i ∈ I com nível de capacidade k ∈ K
f = [
    [6, 5],
    [7, 4],
    [3, 8],
]
# estimativa de produção mensal de um poço de petróleo j ∈ J;
a = [
    3000,
    4500,
    6000,
    3600,
    2400,
    5100,
    2700,
    3300,
    3900,
    5400,
]
# capacidade de uma plataforma de nível k ∈ K;
b = [16000, 15000]
# custos com danos ambientais esperados, referentes à abertura/exploração do poço de petróleo j ∈ J
DW = [
    310782,
    474140,
    663646,
    261669,
    174145,
    151671,
    507921,
    939078,
    115599,
    149953,
]
# custos com danos ambientais esperados, referentes à instalação e/ou funcionamento da plataforma de petróleo i ∈ I;
DO = [90000, 135000, 180000]
# custos com danos ambientais esperados, referentes à possíveis rupturas nas tubulações de conexão entre a plataforma
# de petróleo i ∈ I e o poço j ∈ J;
DQ = [
    [
        395729,
        689619,
        548398,
        831475,
        299864,
        287818,
        737374,
        645187,
        820220,
        92386,
    ],
    [
        185233,
        94087,
        632542,
        572771,
        793997,
        974831,
        818750,
        361304,
        463313,
        836669,
    ],
    [
        94918,
        185338,
        380086,
        914520,
        91802,
        788721,
        498847,
        761448,
        885344,
        397285,
    ],
]
# custos com danos ambientais esperados, referentes à instalação e/ou funcionamento da plataforma i ∈ I com nível
# de capacidade k ∈ K;
DP = [[203684, 276239], [261388, 211061], [248587, 78777]]


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
        # pop_size=100,
        pop_size=40,
        n_offsprings=10,
        sampling=FloatRandomSampling(),
        # crossover=SBX(prob=0.65, eta=15),
        crossover=SBX(prob=0.9, eta=15),
        # mutation=PM(eta=1 / (num_platforms * num_wells + num_platforms * num_capacities)),
        mutation=PM(eta=20),
        eliminate_duplicates=True,
    )

    termination = get_termination("n_gen", 400)
    res = minimize(
        problem, algorithm, termination, seed=1, save_history=True, verbose=False
    )

    X = res.X
    F = res.F

    print(X)
    plot3d(F)
    # plot2d(F)


if __name__ == "__main__":
    solve_plmpm()
