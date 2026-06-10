import numpy as np
from algoritmoGeneticoEscala.avaliacoesEvalidacoes.validaSolucaoEscala import validaSolucaoEscala
from algoritmoGeneticoReescala.avalicoesEvalidacoes.validaSolucaoReescala import validaSolucaoReescala
from algoritmoGeneticoReescala.extrairCorteReescalar import extrairCorteReescalar


def percentagensSorteioReescala(selecionados, populacao, nomes, qtde_individuos, turno, farmaceuticos, auxiliares, num_dias_mes, dia_reescala, id_troca, idx_dia_reescala, cargo_troca, cargos_ok, matriz_nao_reescalar, escala_original_numerica):
    """
    Cruzamento por porcentagem de herança e ordem sorteadas - cortes verticais. Para cada filho gerado:
    1. Sorteia-se a ordem dos pais (Quem é o Pai A e quem é o Pai B).
    2. Sorteia-se uma porcentagem.
    3. O filho recebe a primeira porcentagem do Pai A e o restante do Pai B.
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

    while len(filhos_gerados) < qtde_individuos:
        idx_p1, idx_p2 = np.random.choice(num_pais_selecionados, 2, replace=False)
        pai_1 = corte_selecionados[idx_p1]
        pai_2 = corte_selecionados[idx_p2]

        if np.random.random() > 0.5: pai_A, pai_B = pai_1, pai_2
        else: pai_A, pai_B = pai_2, pai_1

        porcentagem_pai_a = np.random.uniform(0.1, 0.9) #uniform(0.1, 0.9) para garantir um corte entre 10% e 90%.
        ponto_corte = int(porcentagem_pai_a * num_dias_mes)

        filho = np.zeros_like(pai_A)
        filho[:, :ponto_corte] = pai_A[:, :ponto_corte]
        filho[:, ponto_corte:] = pai_B[:, ponto_corte:]

        individuo_quase_completo = np.hstack((matriz_nao_reescalar, filho))
        if cargo_troca == 1:
            individuo_completo = np.vstack((individuo_quase_completo, cargos_ok))
        else:
            individuo_completo = np.vstack((cargos_ok, individuo_quase_completo))
        eh_valido = validaSolucaoReescala(individuo_completo, num_dias_mes, turno, farmaceuticos, auxiliares, cargo_troca, id_troca, idx_dia_reescala, nomes, escala_original_numerica)
        filhos_gerados.append(eh_valido)

    if len(filhos_gerados) > 0:
        filhos_finais = np.stack(filhos_gerados, axis=2)
    else:
        filhos_finais = np.empty((num_funcionarios_total, num_dias_mes, 0))
        print("Aviso Crítico: Nenhum filho gerado!")

    return filhos_finais