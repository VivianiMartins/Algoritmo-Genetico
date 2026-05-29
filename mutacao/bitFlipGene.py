import numpy as np
from avalicoesEvalidacoes.validaSolucao import validaSolucao

def bitFlipGene(probabilidade_mutacao, populacao, funcionarios, turno, farmaceuticos, auxiliares, num_dias_mes, tipo):
    """
    Aplica a mutação tradicional (Bit-Flip simples) em um único gene.
    Se o indivíduo for sorteado para mutar:
    Sorteia um funcionário aleatório e um dia aleatório do mês.
    Inverte apenas esse dia específico (de folga para trabalho ou vice-versa).
    """
    mutados = []
    num_funcionarios_total = populacao.shape[0]

    for i in range(populacao.shape[2]):
        individuo_atual = populacao[:, :, i].copy()

        if np.random.random() <= probabilidade_mutacao:
            funcionario_sorteado = np.random.randint(0, num_funcionarios_total)  # Sorteia um funcionário aleatório
            dia_sorteado = np.random.randint(0, num_dias_mes)  # Sorteia um dia aleatório do mês
            individuo_atual[funcionario_sorteado, dia_sorteado] = 1 - individuo_atual[funcionario_sorteado, dia_sorteado]
            individuo_atual = validaSolucao(individuo_atual, num_dias_mes, tipo, funcionarios, turno, farmaceuticos, auxiliares)

        mutados.append(individuo_atual)

    populacao_mutada = np.stack(mutados, axis=2)

    return populacao_mutada