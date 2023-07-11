import org.moeaframework.core.*;
import org.moeaframework.core.operator.*;
import org.moeaframework.core.operator.real.*;
import org.moeaframework.core.problem.*;
import org.moeaframework.core.solution.*;
import org.moeaframework.core.variable.*;

public class PLMPM {

    private double[][] c;
    private double[][] f;
    private double[] a;
    private double[] b;
    private int numPlatforms;
    private int numWells;
    private int numCapacities;

    public PLMPM(double[][] c, double[][] f, double[] a, double[] b) {
        super(1, 3 * c.length);
        this.c = c;
        this.f = f;
        this.a = a;
        this.b = b;
        this.numPlatforms = c.length;
        this.numWells = c[0].length;
        this.numCapacities = f[0].length;
    }

    @Override
    public void evaluate(Solution solution) {
        double[] x = ((RealVariable) solution.getVariable(0)).toArray();

        double[][] x_ij = new double[numPlatforms][numWells];
        double[][] y_ik = new double[numPlatforms][numCapacities];

        int index = 0;
        for (int i = 0; i < numPlatforms; i++) {
            for (int j = 0; j < numWells; j++) {
                x_ij[i][j] = x[index];
                index++;
            }
        }

        for (int i = 0; i < numPlatforms; i++) {
            for (int k = 0; k < numCapacities; k++) {
                y_ik[i][k] = x[index];
                index++;
            }
        }

        double[] constraints = new double[getNumConstraints()];

        // Restrição: Cada poço deve ser atendido por uma única plataforma
        for (int j = 0; j < numWells; j++) {
            double sum = 0;
            for (int i = 0; i < numPlatforms; i++) {
                sum += x_ij[i][j];
            }
            constraints[j] = sum - 1;
        }

        // Restrição: Capacidade das plataformas deve ser suficiente para atender a demanda dos poços
        for (int i = 0; i < numPlatforms; i++) {
            double sum1 = 0;
            double sum2 = 0;
            for (int j = 0; j < numWells; j++) {
                sum1 += a[j] * x_ij[i][j];
            }
            for (int k = 0; k < numCapacities; k++) {
                sum2 += b[k] * y_ik[i][k];
            }
            constraints[numWells + i] = sum1 - sum2;
        }

        // Restrição: No máximo uma plataforma pode ser aberta em cada localização
        for (int i = 0; i < numPlatforms; i++) {
            double sum = 0;
            for (int k = 0; k < numCapacities; k++) {
                sum += y_ik[i][k];
            }
            constraints[numWells + numPlatforms + i] = sum - 1;
        }

        double objective = 0;

        for (int i = 0; i < numPlatforms; i++) {
            for (int j = 0; j < numWells; j++) {
                objective += c[i][j] * x_ij[i][j];
            }
        }

        for (int i = 0; i < numPlatforms; i++) {
            for (int k = 0; k < numCapacities; k++) {
                objective += f[i][k] * y_ik[i][k];
            }
        }

        solution.setObjective(0, -objective);
        solution.setConstraints(constraints);
    }

    @Override
    public Solution newSolution() {
        Solution solution = new Solution(1, getNumConstraints());
        solution.setVariable(0, new RealVariable(0, 1, numPlatforms * numWells + numPlatforms * numCapacities));
        return solution;
    }

    public static void main(String[] args) {
        double[][] c = {{1, 2, 3, 4, 5}, {6, 7, 8, 9, 10}};
        double[][] f = {{10, 20}, {30, 40}};
        double[] a = {1, 2, 3, 4, 5};
        double[] b = {10, 20};

        Problem problem = new PLMPM(c, f, a, b);

        Algorithm algorithm = new NSGA2(problem, 40);
        algorithm.setVariation(new SBX(0.9, 15.0), new PM(20.0));

        int maxEvaluations = 40;
        while (algorithm.getNumberOfEvaluations() < maxEvaluations) {
            algorithm.step();
        }

        NondominatedPopulation result = algorithm.getResult();
        double[][] objectives = result.getObjectives();
        double[][] variables = result.getVariables();

        // Código para visualizar os resultados
        // ...
    }
}
