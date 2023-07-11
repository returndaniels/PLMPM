# PLMPM - Problema de Localização Multiobjetivo de Plataformas de Petróleo Multicapacitada

Este projeto aborda o Problema de Localização Multiobjetivo de Plataformas de Petróleo Multicapacitada (PLMPM), que é um desafio complexo enfrentado pela indústria de petróleo. O objetivo é selecionar locais para instalação de plataformas e determinar a capacidade das instalações, visando otimizar três objetivos principais: minimizar os custos de investimentos, maximizar a produção e reduzir os impactos ambientais.

## Como Funciona

Diferente dos problemas de otimização monoobjetivo, as abordagens multiobjetivo não possuem uma única solução ótima que atenda a todos os objetivos simultaneamente. Isso ocorre devido ao trade-off (conflito de interesses) existente entre os objetivos, o que é comum nesses problemas. Objetivos conflitantes implicam que melhorar um objetivo pode levar a uma piora em outro.

O PLMPM é classificado como NP-Difícil, o que significa que encontrar a solução ótima é computacionalmente inviável. Para resolver problemas de programação matemática com mais de um objetivo, é necessário definir um conjunto de soluções que represente o trade-off entre os objetivos. Esse conjunto de soluções é chamado de Soluções Eficientes de Pareto, ou Pareto Ótimo. São soluções que não podem ser melhoradas em um objetivo sem piorar em outro. Buscaremos as Soluções Eficientes de Pareto através do algoritmo NSGA-II.

### Algoritmo NSGA-II

O NSGA-II (Non-dominated Sorting Genetic Algorithm II) é um algoritmo genético evolutivo multiobjetivo amplamente utilizado para resolver problemas de otimização multiobjetivo. Foi proposto por Deb et al. em 2002 como uma extensão do NSGA original.

O NSGA-II incorpora várias técnicas eficientes para manter um conjunto de soluções não dominadas ao longo das gerações, aproximando-se da fronteira de Pareto. Ele usa uma combinação de classificação não dominada, operadores genéticos (cruzamento e mutação) e seleção para criar uma nova população de soluções candidatas que evolui em direção a uma melhor aproximação do conjunto de Pareto.

O programa está implementado na linguagem Python e utiliza as bibliotecas numpy e pymoo.

## Pré-requisitos

Antes de executar o programa, certifique-se de ter as seguintes bibliotecas instaladas:

- numpy
- pymoo

Para instalar as bibliotecas, você pode seguir os seguintes passos:

1. Abra o terminal ou prompt de comando.
2. Execute o seguinte comando para instalar a biblioteca numpy:

```bash
pip install numpy
```

3. Execute o seguinte comando para instalar a biblioteca pymoo:

```bash
pip install pymoo

```

## Arquivos

- `PLMPM.py`: Contém a definição da classe PLMPM, que implementa o problema de localização multiobjetivo de plataformas de petróleo multicapacitada.
- `parameters.py`: Define os parâmetros do problema, como número de plataformas, número de poços, custos, capacidades, etc.
- `plmpm-solver.py`: Programa principal que chama a classe PLMPM para resolver o problema e exibir a visualização da frente de Pareto.

## Executando o Programa

Para executar o programa principal, abra o terminal ou prompt de comando e navegue até o diretório onde os arquivos estão localizados. Em seguida, execute o seguinte comando:

```bash
python plmpm-solver.py
```

Isso exibirá uma visualização 2D da frente de Pareto, mostrando as soluções eficientes encontradas.

Também é possível exibir uma visualização 3D da frente de Pareto. Para isso, execute o seguinte comando:


```bash
python plmpm-solver.py --plot3d
```

Isso exibirá uma visualização 3D da frente de Pareto.

## Contribuições

Contribuições são bem-vindas! Se você tiver alguma melhoria, correção de bug ou sugestão de recurso, fique à vontade para enviar um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).
