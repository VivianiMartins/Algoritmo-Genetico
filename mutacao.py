import numpy as np
from validaSolucao import validaSolucao

def mutacao(populacao, funcionarios, turno, farmaceuticos, auxiliares, num_dias_mes):
    """
    Aplica a mutação na população.
    Sorteia um dia (excluindo primeiro e último).
    Se o dia for par: flipa os dias do dia sorteado até o fim do mês.
    Se o dia for ímpar: flipa os dias do início do mês até o dia sorteado.
    """

    mutados = []

    for i in range(populacao.shape[2]):
        mutante = populacao[:, :, i].copy()
        dia_sorteado = np.random.randint(1, num_dias_mes - 1) #sortear um dia do mês excluindo o primeiro e último

        if dia_sorteado % 2 == 0:  # par: flipa do dia sorteado até o fim (para a frente)
            mutante[:, dia_sorteado:] = 1 - mutante[:, dia_sorteado:]
        else: #ímpar: flipa do início até o dia sorteado (para trás)
            mutante[:, :dia_sorteado + 1] = 1 - mutante[:, :dia_sorteado + 1]

        eh_valido = validaSolucao(mutante, num_dias_mes, 1, funcionarios, turno, farmaceuticos, auxiliares)
        mutados.append(eh_valido)

    populacao_mutada = np.stack(mutados, axis=2)

    return populacao_mutada