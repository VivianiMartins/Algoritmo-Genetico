import numpy as np
from avalicoesEvalidacoes.validaSolucao import validaSolucao

def bitFlipBloco(probabilidade_mutacao, populacao, funcionarios, turno, farmaceuticos, auxiliares, num_dias_mes):
    """
    Aplica a mutação na população baseada em uma probabilidade.
    Se a mutação ocorrer: Sorteia um dia (excluindo primeiro e último).
    Se o dia for par: flipa os dias do dia sorteado até o fim do mês.
    Se o dia for ímpar: flipa os dias do início do mês até o dia sorteado.
    """

    mutados = []

    for i in range(populacao.shape[2]):
        individuo_atual = populacao[:, :, i].copy()

        if np.random.random() <= probabilidade_mutacao:
            dia_sorteado = np.random.randint(1, num_dias_mes - 1) #sortear um dia do mês excluindo o primeiro e último

            if dia_sorteado % 2 == 0:  # par: flipa do dia sorteado até o fim (para a frente)
                individuo_atual[:, dia_sorteado:] = 1 - individuo_atual[:, dia_sorteado:]
            else:  # ímpar: flipa do início até o dia sorteado (para trás)
                individuo_atual[:, :dia_sorteado + 1] = 1 - individuo_atual[:, :dia_sorteado + 1]

            individuo_atual = validaSolucao(individuo_atual, num_dias_mes, funcionarios, turno, farmaceuticos, auxiliares)

        mutados.append(individuo_atual)

    populacao_mutada = np.stack(mutados, axis=2)

    return populacao_mutada