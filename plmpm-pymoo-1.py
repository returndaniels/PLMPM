from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt


class PLMPM(ElementwiseProblem):
    def __init__(self, c, f, a, b):
        num_platforms = len(c)
        num_wells = len(c[0])
        num_capacities = len(f[0])
        n_var = num_platforms * num_wells + num_platforms * num_capacities
        super().__init__(n_var=n_var, n_obj=1, n_constr=3 * num_platforms, xl=0, xu=1)
        self.c = c
        self.f = f
        self.a = a
        self.b = b

    def _evaluate(self, x, out, *args, **kwargs):
        num_platforms = len(self.c)
        num_wells = len(self.c[0])
        num_capacities = len(self.f[0])

        x_ij = [x[i * num_wells : (i + 1) * num_wells] for i in range(num_platforms)]
        y_ik = [
            x[
                num_platforms * num_wells
                + i * num_capacities : num_platforms * num_wells
                + (i + 1) * num_capacities
            ]
            for i in range(num_platforms)
        ]

        constraints = []

        # Restrição: Cada poço deve ser atendido por uma única plataforma
        for j in range(num_wells):
            constraints.append(np.sum(x_ij[i][j] for i in range(num_platforms)) - 1)

        # Restrição: Capacidade das plataformas deve ser suficiente para atender a demanda dos poços
        for i in range(num_platforms):
            constraints.append(
                np.sum(self.a[j] * x_ij[i][j] for j in range(num_wells))
                - np.sum(self.b[k] * y_ik[i][k] for k in range(num_capacities))
            )

        # Restrição: No máximo uma plataforma pode ser aberta em cada localização
        for i in range(num_platforms):
            constraints.append(np.sum(y_ik[i]) - 1)

        objective = sum(
            self.c[i][j] * x_ij[i][j]
            for i in range(num_platforms)
            for j in range(num_wells)
        ) + sum(
            self.f[i][k] * y_ik[i][k]
            for i in range(num_platforms)
            for k in range(num_capacities)
        )

        out["F"] = -objective.reshape(-1, 1)
        out["G"] = np.array(constraints)


# Parâmetros do problema
c = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]  # Custo de perfuração
f = [[10, 20], [30, 40]]  # Custo de instalação
a = [1, 2, 3, 4, 5]  # Estimativa de produção mensal de cada poço
b = [10, 20]  # Capacidade das plataformas

problem = PLMPM(c, f, a, b)

algorithm = NSGA2(
    pop_size=40,
    n_offsprings=10,
    sampling=FloatRandomSampling(),
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(eta=20),
    eliminate_duplicates=True,
)

termination = get_termination("n_gen", 40)
res = minimize(problem, algorithm, termination, seed=1, save_history=True, verbose=True)

X = res.X
F = res.F
xl, xu = problem.bounds()
plt.figure(figsize=(7, 5))
plt.scatter(X, F * len(X), s=30, facecolors="none", edgecolors="r")
plt.xlim(xl[0], xu[0])
plt.ylim(xl[1], xu[1])
plt.title("Design Space")
plt.show()
