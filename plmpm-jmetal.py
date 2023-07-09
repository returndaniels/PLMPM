from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator.crossover import SBXCrossover
from jmetal.operator.mutation import PolynomialMutation
from jmetal.operator.selection import BinaryTournamentSelection
from jmetal.util.termination_criterion import StoppingByEvaluations
import numpy as np
import matplotlib.pyplot as plt


class PLMPM(FloatProblem):
    def __init__(self, c, f, a, b):
        num_platforms = len(c)
        num_wells = len(c[0])
        num_capacities = len(f[0])
        n_var = num_platforms * num_wells + num_platforms * num_capacities
        super().__init__(
            # number_of_variables=n_var,
            # number_of_objectives=1,
            # number_of_constraints=3 * num_platforms,
        )
        self.c = c
        self.f = f
        self.a = a
        self.b = b
        self.lower_bound = np.zeros(n_var)
        self.upper_bound = np.ones(n_var)

    def get_name(self) -> str:
        return "PLMPM"

    def get_number_of_constraints(self) -> int:
        return self.number_of_constraints

    def get_number_of_objectives(self) -> int:
        return self.number_of_objectives

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        x = solution.variables
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

        solution.objectives[0] = -objective
        solution.constraints = np.array(constraints)

        return solution


# Parâmetros do problema
c = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]  # Custo de perfuração
f = [[10, 20], [30, 40]]  # Custo de instalação
a = [1, 2, 3, 4, 5]  # Estimativa de produção mensal de cada poço
b = [10, 20]  # Capacidade das plataformas

problem = PLMPM(c, f, a, b)

algorithm = NSGAII(
    problem=problem,
    population_size=40,
    offspring_population_size=10,
    mutation=PolynomialMutation(probability=0.9, distribution_index=15),
    crossover=SBXCrossover(probability=0.9, distribution_index=15),
    selection=BinaryTournamentSelection(),
)

termination = StoppingByEvaluations(max_evaluations=40)
algorithm.run()

X = np.array([s.variables for s in algorithm.get_result()])
F = np.array([-s.objectives[0] for s in algorithm.get_result()])
xl, xu = problem.lower_bound, problem.upper_bound

plt.figure(figsize=(7, 5))
plt.scatter(X[:, 0], X[:, 1] * len(X), s=30, facecolors="none", edgecolors="r")
plt.xlim(xl[0], xu[0])
plt.ylim(xl[1], xu[1])
plt.title("Design Space")
plt.show()
