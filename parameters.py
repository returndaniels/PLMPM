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
