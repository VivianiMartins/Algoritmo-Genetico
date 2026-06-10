import numpy as np
from algoritmoGeneticoReescala.avalicoesEvalidacoes.validaSolucaoReescala import validaSolucaoReescala
from algoritmoGeneticoReescala.extrairCorteReescalar import extrairCorteReescalar

def bitFlipBlocoReescala(probabilidade_mutacao, populacao, turno, farmaceuticos, auxiliares, num_dias_mes, dia_reescala, cargo_troca, cargos_ok, matriz_nao_reescalar, escala_original_numerica, id_troca, idx_dia_reescala, nomes, dias_resto_mes):
    """
    Aplica a mutação na população baseada em uma probabilidade.
    Se a mutação ocorrer: Sorteia um dia (excluindo primeiro e último).
    Se o dia for par: flipa os dias do dia sorteado até o fim do mês.
    Se o dia for ímpar: flipa os dias do início do mês até o dia sorteado.
    """
    mutados = []

    for i in range(populacao.shape[2]):
        individuo_atual = populacao[:, :, i].copy()
        individuo_atual = extrairCorteReescalar(individuo_atual, farmaceuticos, num_dias_mes, dia_reescala, cargo_troca)

        if np.random.random() <= probabilidade_mutacao:
            dia_sorteado = np.random.randint(1, dias_resto_mes - 1) #sortear um dia do mês excluindo o primeiro e último

            if dia_sorteado % 2 == 0:  # par: flipa do dia sorteado até o fim (para a frente)
                individuo_atual[:, dia_sorteado:] = 1 - individuo_atual[:, dia_sorteado:]
            else:  # ímpar: flipa do início até o dia sorteado (para trás)
                individuo_atual[:, :dia_sorteado + 1] = 1 - individuo_atual[:, :dia_sorteado + 1]

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