import numpy as np
from algoritmoGeneticoReescala.avalicoesEvalidacoes.validaSolucaoReescala import validaSolucaoReescala
from algoritmoGeneticoReescala.extrairCorteReescalar import extrairCorteReescalar

def bitFlipGeneReescala(probabilidade_mutacao, populacao, turno, farmaceuticos, auxiliares, num_dias_mes, dia_reescala, cargo_troca, cargos_ok, matriz_nao_reescalar, escala_original_numerica, id_troca, idx_dia_reescala, nomes, dias_resto_mes):
    """
    Aplica a mutação tradicional (Bit-Flip simples) em um único gene.
    Se o indivíduo for sorteado para mutar:
    Sorteia um funcionário aleatório e um dia aleatório do mês.
    Inverte apenas esse dia específico (de folga para trabalho ou vice-versa).
    """
    mutados = []
    num_funcionarios_total = farmaceuticos if cargo_troca == 1 else auxiliares

    for i in range(populacao.shape[2]):
        individuo_atual = populacao[:, :, i].copy()
        individuo_atual = extrairCorteReescalar(individuo_atual, farmaceuticos, num_dias_mes, dia_reescala, cargo_troca)

        if np.random.random() <= probabilidade_mutacao:
            funcionario_sorteado = np.random.randint(0, num_funcionarios_total)  # Sorteia um funcionário aleatório
            dia_sorteado = np.random.randint(0, dias_resto_mes)  # Sorteia um dia aleatório do mês
            individuo_atual[funcionario_sorteado, dia_sorteado] = 1 - individuo_atual[funcionario_sorteado, dia_sorteado]

            individuo_quase_completo = np.hstack((matriz_nao_reescalar, individuo_atual))
            if cargo_troca == 1: individuo_completo = np.vstack((individuo_quase_completo, cargos_ok))
            else: individuo_completo = np.vstack((cargos_ok, individuo_quase_completo))
            individuo_atual = validaSolucaoReescala(individuo_completo, num_dias_mes, turno, farmaceuticos, auxiliares, cargo_troca, id_troca, idx_dia_reescala, nomes, escala_original_numerica)
        else:
            individuo_quase_completo = np.hstack((matriz_nao_reescalar, individuo_atual))
            if cargo_troca == 1: individuo_atual = np.vstack((individuo_quase_completo, cargos_ok))
            else: individuo_atual = np.vstack((cargos_ok, individuo_quase_completo))

        mutados.append(individuo_atual)

    populacao_mutada = np.stack(mutados, axis=2)

    return populacao_mutada