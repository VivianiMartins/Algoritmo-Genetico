import numpy as np
from algoritmoGeneticoReescala.avalicoesEvalidacoes.validaSolucaoReescala import validaSolucaoReescala
from algoritmoGeneticoReescala.extrairCorteReescalar import extrairCorteReescalar


def xadrezReescala(selecionados, populacao, nomes, qtde_individuos, turno, farmaceuticos, auxiliares, num_dias_mes, dia_reescala, id_troca, idx_dia_reescala, cargo_troca, cargos_ok, matriz_nao_reescalar, escala_original_numerica, dias_resto_mes):
    """
    Cruzamento Block-wise (Bw) 2D conforme a literatura.
    Faz cortes verticais (a cada 7 dias) e horizontais (metades das equipes).
    """
    individuos_selecionados = populacao[:, :, selecionados]
    num_pais_selecionados = individuos_selecionados.shape[2]
    num_funcionarios_total = farmaceuticos + auxiliares
    corte_selecionados = []
    filhos_gerados = []

    # aqui tenho que separar as matrizes
    for pai in range(num_pais_selecionados):
        matriz_para_reescalar = extrairCorteReescalar(individuos_selecionados[:, :, pai], farmaceuticos, num_dias_mes, dia_reescala, cargo_troca)
        corte_selecionados.append(matriz_para_reescalar)

    # cortes verticais (blocos de 7 dias / 1 semana)
    cortes_verticais = list(range(0, dias_resto_mes, 7))
    if cortes_verticais[-1] != dias_resto_mes: cortes_verticais.append(dias_resto_mes)

    # cortes horizontais (Metades, conforme o artigo)
    if cargo_troca == 1:
        meio = max(1, farmaceuticos // 2)
        cortes_horizontais = [(0, meio), (meio, farmaceuticos)]
    else:
        meio = max(1, auxiliares // 2)
        cortes_horizontais = [ (0, (meio//2)), ((meio//2), meio), (meio, (meio +(meio//2))), ((meio +(meio//2)), auxiliares)]

    while len(filhos_gerados) < qtde_individuos:
        idx_p1, idx_p2 = np.random.choice(num_pais_selecionados, 2, replace=False)
        pai_1 = corte_selecionados[idx_p1]
        pai_2 = corte_selecionados[idx_p2]
        filho = np.zeros_like(pai_1)

        for i in range(len(cortes_verticais) - 1):
            col_inicio = cortes_verticais[i]
            col_fim = cortes_verticais[i + 1]

            for (lin_inicio, lin_fim) in cortes_horizontais:
                if lin_inicio == lin_fim: continue

                if np.random.random() > 0.5:
                    filho[lin_inicio:lin_fim, col_inicio:col_fim] = pai_1[lin_inicio:lin_fim, col_inicio:col_fim]
                else:
                    filho[lin_inicio:lin_fim, col_inicio:col_fim] = pai_2[lin_inicio:lin_fim, col_inicio:col_fim]

        individuo_quase_completo = np.hstack((matriz_nao_reescalar, filho))
        if cargo_troca == 1: individuo_completo = np.vstack((individuo_quase_completo, cargos_ok))
        else: individuo_completo = np.vstack((cargos_ok, individuo_quase_completo))
        eh_valido = validaSolucaoReescala(individuo_completo, num_dias_mes, turno, farmaceuticos, auxiliares, cargo_troca, id_troca, idx_dia_reescala, nomes, escala_original_numerica)
        filhos_gerados.append(eh_valido)

    if len(filhos_gerados) > 0:
        filhos_finais = np.stack(filhos_gerados, axis=2)
    else:
        filhos_finais = np.empty((num_funcionarios_total, num_dias_mes, 0))
        print("Aviso Crítico: Nenhum filho gerado!")

    return filhos_finais