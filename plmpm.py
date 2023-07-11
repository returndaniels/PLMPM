from pymoo.core.problem import ElementwiseProblem
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
