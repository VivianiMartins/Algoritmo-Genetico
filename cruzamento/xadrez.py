import numpy as np
from avalicoesEvalidacoes.validaSolucao import validaSolucao

def xadrez(selecionados, populacao, funcionarios, qtde_individuos, turno, farmaceuticos, auxiliares, num_dias_mes):
    """
    Cruzamento Block-wise (Bw) 2D conforme a literatura.
    Faz cortes verticais (a cada 7 dias) e horizontais (metades das equipes).
    """
    individuos_selecionados = populacao[:, :, selecionados]
    num_pais_selecionados = individuos_selecionados.shape[2]
    num_funcionarios_total = individuos_selecionados.shape[0]

    filhos_gerados = []

    # cortes verticais (blocos de 7 dias / 1 semana)
    cortes_verticais = list(range(0, num_dias_mes, 7))
    if cortes_verticais[-1] != num_dias_mes: cortes_verticais.append(num_dias_mes)

    # cortes horizontais (Metades, conforme o artigo)
    meio_farm = max(1, farmaceuticos // 2)
    meio_aux = max(1, auxiliares // 2)
    cortes_horizontais = [ (0, meio_farm), (meio_farm, farmaceuticos), (farmaceuticos, farmaceuticos + meio_aux), (farmaceuticos + meio_aux, num_funcionarios_total)]

    while len(filhos_gerados) < qtde_individuos:
        idx_p1, idx_p2 = np.random.choice(num_pais_selecionados, 2, replace=False)
        pai_1 = individuos_selecionados[:, :, idx_p1]
        pai_2 = individuos_selecionados[:, :, idx_p2]

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

        filho_valido = validaSolucao(filho, num_dias_mes, funcionarios, turno, farmaceuticos, auxiliares)
        filhos_gerados.append(filho_valido)

    if len(filhos_gerados) > 0:
        filhos_finais = np.stack(filhos_gerados, axis=2)
    else:
        filhos_finais = np.empty((num_funcionarios_total, num_dias_mes, 0))
        print("Aviso Crítico: Nenhum filho gerado!")

    return filhos_finais