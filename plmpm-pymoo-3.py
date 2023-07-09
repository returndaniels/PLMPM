import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter


class PLMPM(Problem):
    def __init__(self, c, f, a, DW, DO, DQ, DP, R, b):
        num_platforms = len(c)
        num_wells = len(a)
        num_capacities = len(b)
        n_var = num_platforms * num_wells + num_platforms * num_capacities
        super().__init__(n_var=n_var, n_obj=3, n_constr=0, xl=0, xu=1)
        self.c = c
        self.f = f
        self.a = a
        self.DW = DW
        self.DO = DO
        self.DQ = DQ
        self.DP = DP
        self.R = R
        self.b = b

    def _evaluate(self, x, out, *args, **kwargs):
        # Número de locais de plataforma e poços de petróleo
        num_platforms = len(self.c)
        num_wells = len(self.a)
        num_capacities = len(self.b)

        # Cria arrays vazios para as saídas
        out["F"] = np.zeros((x.shape[0], self.n_obj))
        out["G"] = np.zeros((x.shape[0], self.n_constr))

        # Variáveis de decisão
        x_ij = x[:, :num_wells]
        y_ik = x[:, num_wells:]

        # Funções objetivo
        costs = np.zeros(x.shape[0])
        oil_productions = np.zeros(x.shape[0])
        environmental_impacts = np.zeros(x.shape[0])

        for k in range(x.shape[0]):
            for i in range(num_platforms):
                for j in range(num_wells):
                    costs += self.c[i][j] * x_ij[i, j]
                    oil_productions += self.a[j] * x_ij[i, j]
                    environmental_impacts += (self.DW[j] + self.DQ[j][i]) * x_ij[i, j]
                for j in range(num_capacities):
                    environmental_impacts += (self.DO[i] + self.DP[i][j]) * y_ik[i, j]

        # Atribui os valores aos índices corretos nas saídas
        out["F"][:, 0] = costs
        out["F"][:, 1] = -oil_productions
        out["F"][:, 2] = -environmental_impacts


# Parâmetros do problema
c = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Custo de perfuração
f = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]  # Custo de instalação
a = [100, 200, 300]  # Produção estimada
DW = [0.1, 0.2, 0.3]  # Custo danos ambientais (poço)
DO = [0.4, 0.5, 0.6]  # Custo danos ambientais (plataforma)
DQ = [
    [0.01, 0.02, 0.03],
    [0.04, 0.05, 0.06],
    [0.07, 0.08, 0.09],
]  # Custo danos ambientais (conexão)
DP = [
    [0.001, 0.002, 0.003],
    [0.004, 0.005, 0.006],
    [0.007, 0.008, 0.009],
]  # Custo danos ambientais (plataforma)
R = 1000  # Orçamento máximo
b = [50, 100, 150]  # Capacidades

num_platforms = len(c)
num_wells = len(c[0])
num_capacities = len(b)
n_var = num_platforms * num_wells + num_platforms * num_capacities

# problem = get_problem("zdt1")
problem = PLMPM(c, f, a, DW, DO, DQ, DP, R, b)

algorithm = NSGA2(
    pop_size=100,
    n_offsprings=1,
    sampling=FloatRandomSampling(),
    crossover=SBX(prob=0.65, eta=15),
    mutation=PM(eta=1 / n_var),
    eliminate_duplicates=True,
)

termination = get_termination("n_gen", 400)

res = minimize(problem, algorithm, termination, seed=1, save_history=True, verbose=True)


plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()
