import numpy as np
from algoritmoGeneticoReescala.avalicoesEvalidacoes.validaSolucaoReescala import validaSolucaoReescala

def geraPopulacaoInicialReescala(cargos_ok, matriz_para_reescalar, matriz_nao_reescalar, id_troca, id_troca_recorte,
                                 num_dias_mes, cargo_troca, farmaceuticos, auxiliares,
                                 idx_dia_reescala, turno, qtde_individuos, nomes, escala_original_numerica, dias_resto_mes):
    """
    Gera população inicial válida para algoritmo genético de escalas de trabalho.
    taxa_troca_ideal: probabilidade de usar os candidatos ideais.
    """
    reescalar = matriz_para_reescalar[:, 1:]
    total_colaboradores = farmaceuticos + auxiliares
    qtd_colaboradores_reescala = farmaceuticos if cargo_troca == 1 else auxiliares

    populacao = np.zeros((total_colaboradores, num_dias_mes, qtde_individuos), dtype=np.int8)
    janela = np.zeros((qtd_colaboradores_reescala, dias_resto_mes, qtde_individuos), dtype=np.int8)

    for cont_individuo in range(qtde_individuos):
        individuo_matriz = np.copy(reescalar)

        individuo_matriz[id_troca_recorte, 0] = 0  # Tira o funcionário da escala

        janela[:, :, cont_individuo] = individuo_matriz
        individuo_quase_completo = np.hstack((matriz_nao_reescalar, individuo_matriz))

        if cargo_troca == 1: individuo_completo = np.vstack((individuo_quase_completo, cargos_ok))
        else: individuo_completo = np.vstack((cargos_ok, individuo_quase_completo))

        individuo_valido = validaSolucaoReescala(individuo_completo, num_dias_mes, turno, farmaceuticos, auxiliares, cargo_troca, id_troca, idx_dia_reescala, nomes, escala_original_numerica)
        populacao[:, :, cont_individuo] = individuo_valido

    return populacao