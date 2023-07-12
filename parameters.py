# tamanho do conjunto que representa possíveis locais para instalação de plataformas de petróleo (I)
num_platforms = 3
# tamanho do conjunto que representa possíveis locais para instalação de poços de petróleo (J)
num_wells = 10
# conjunto que representa os níveis de capacidade das plataformas de petróleo (K)
num_capacities = 2
# custo de perfuração de um poço de petróleo j ∈ J a partir de uma plataforma na localização i ∈ I
c = [
    [500000, 800000, 600000, 900000, 700000, 600000, 400000, 500000, 300000, 700000],
    [700000, 600000, 500000, 800000, 600000, 400000, 900000, 700000, 600000, 500000],
    [400000, 500000, 300000, 700000, 600000, 800000, 600000, 900000, 700000, 600000],
]
#  custo para construção e instalação de uma plataforma de petróleo na localização i ∈ I com nível de capacidade k ∈ K
f = [
    [6000000, 5000000],
    [7000000, 4000000],
    [3000000, 8000000],
]
# estimativa de produção mensal de um poço de petróleo j ∈ J;
a = [
    30000,
    45000,
    60000,
    36000,
    24000,
    51000,
    27000,
    33000,
    39000,
    54000,
]
# capacidade de uma plataforma de nível k ∈ K;
b = [160000, 150000]
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

n_gen = 4000
pop_size = 200
crossover_prob = 0.65
mutation_prob = 1 / (num_platforms * num_wells + num_platforms * num_capacities)
