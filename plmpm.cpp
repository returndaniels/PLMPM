#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <pagmo/algorithms/nsga2.hpp>
#include <pagmo/algorithms/sade.hpp>
#include <pagmo/archipelago.hpp>
#include <pagmo/problem.hpp>
#include <pagmo/problem/base.hpp>
#include <pagmo/types.hpp>
#include <pagmo/population.hpp>
#include <pagmo/problem/zdt.hpp>

using namespace pagmo;
using namespace std;

class PLMPM : public problem_base {
public:
    PLMPM(const vector<vector<int>>& c, const vector<vector<int>>& f, const vector<int>& a, const vector<int>& b)
        : problem_base(0, 1, 3 * c.size(), 0, 0, 0, problem_info("PLMPM")), c(c), f(f), a(a), b(b) {}

    vector<double> fitness(const vector<double>& x) const {
        int num_platforms = c.size();
        int num_wells = c[0].size();
        int num_capacities = f[0].size();

        vector<vector<double>> x_ij(num_platforms, vector<double>(num_wells, 0.0));
        vector<vector<double>> y_ik(num_platforms, vector<double>(num_capacities, 0.0));

        int var_index = 0;
        for (int i = 0; i < num_platforms; i++) {
            for (int j = 0; j < num_wells; j++) {
                x_ij[i][j] = x[var_index];
                var_index++;
            }
        }

        for (int i = 0; i < num_platforms; i++) {
            for (int k = 0; k < num_capacities; k++) {
                y_ik[i][k] = x[var_index];
                var_index++;
            }
        }

        vector<double> constraints;

        // Restrição: Cada poço deve ser atendido por uma única plataforma
        for (int j = 0; j < num_wells; j++) {
            double sum_x_ij = 0.0;
            for (int i = 0; i < num_platforms; i++) {
                sum_x_ij += x_ij[i][j];
            }
            constraints.push_back(sum_x_ij - 1);
        }

        // Restrição: Capacidade das plataformas deve ser suficiente para atender a demanda dos poços
        for (int i = 0; i < num_platforms; i++) {
            double sum_a_x_ij = 0.0;
            for (int j = 0; j < num_wells; j++) {
                sum_a_x_ij += a[j] * x_ij[i][j];
            }

            double sum_b_y_ik = 0.0;
            for (int k = 0; k < num_capacities; k++) {
                sum_b_y_ik += b[k] * y_ik[i][k];
            }

            constraints.push_back(sum_a_x_ij - sum_b_y_ik);
        }

        // Restrição: No máximo uma plataforma pode ser aberta em cada localização
        for (int i = 0; i < num_platforms; i++) {
            double sum_y_ik = 0.0;
            for (int k = 0; k < num_capacities; k++) {
                sum_y_ik += y_ik[i][k];
            }
            constraints.push_back(sum_y_ik - 1);
        }

        double objective = 0.0;

        for (int i = 0; i < num_platforms; i++) {
            for (int j = 0; j < num_wells; j++) {
                objective += c[i][j] * x_ij[i][j];
            }
        }

        for (int i = 0; i < num_platforms; i++) {
            for (int k = 0; k < num_capacities; k++) {
                objective += f[i][k] * y_ik[i][k];
            }
        }

        return { -objective };
    }

    vector<double> get_ub() const {
        int num_platforms = c.size();
        int num_wells = c[0].size();
        int num_capacities = f[0].size();
        vector<double> ub(num_platforms * num_wells + num_platforms * num_capacities, 1.0);
        return ub;
    }

    vector<double> get_lb() const {
        int num_platforms = c.size();
        int num_wells = c[0].size();
        int num_capacities = f[0].size();
        vector<double> lb(num_platforms * num_wells + num_platforms * num_capacities, 0.0);
        return lb;
    }

private:
    vector<vector<int>> c;
    vector<vector<int>> f;
    vector<int> a;
    vector<int> b;
};

int main() {
    vector<vector<int>> c = {{1, 2, 3, 4, 5}, {6, 7, 8, 9, 10}};
    vector<vector<int>> f = {{10, 20}, {30, 40}};
    vector<int> a = {1, 2, 3, 4, 5};
    vector<int> b = {10, 20};

    PLMPM problem(c, f, a, b);

    algorithm::nsga2 algo;
    algo.set_verbosity(1);

    population pop(algorithm::sade().evolve(problem, 1).get_population().champion().vector());

    pop = algo.evolve(pop);

    const auto& f = pop.get_f();
    const auto& x = pop.get_x();

    for (size_t i = 0; i < pop.size(); ++i) {
        cout << "Objective: " << f[i][0] << endl;
        cout << "Variables: ";
        for (double val : x[i]) {
            cout << val << " ";
        }
        cout << endl;
    }

    return 0;
}
