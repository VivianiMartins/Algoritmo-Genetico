import numpy as np
from algoritmoGeneticoReescala.avalicoesEvalidacoes.validaSolucaoReescala import validaSolucaoReescala
from algoritmoGeneticoReescala.extrairCorteReescalar import extrairCorteReescalar


def blocosReescala(selecionados, populacao, nomes, qtde_individuos, qtd_blocos, turno, farmaceuticos, auxiliares, num_dias_mes, dia_reescala, id_troca, idx_dia_reescala, cargo_troca, cargos_ok, matriz_nao_reescalar, escala_original_numerica):
    """
    Cruzamento dos indivíduos selecionados utilizando blocos:
    O bloco 1 para os farmacêuticos: sorteio entre todos, sem perder a ordem.
    O bloco dos auxiliares: sorteado entre a 'qtd_blocos' definida,
    mantendo a ordem dentro de cada bloco.
    """
    individuos_selecionados = populacao[:, :, selecionados]
    num_pais_selecionados = individuos_selecionados.shape[2]
    num_funcionarios_total = farmaceuticos + auxiliares
    corte_selecionados = []
    filhos_gerados = []

    #aqui tenho que separar as matrizes
    for pai in range(num_pais_selecionados):
        matriz_para_reescalar = extrairCorteReescalar(individuos_selecionados[:, :, pai], farmaceuticos, num_dias_mes, dia_reescala, cargo_troca)
        corte_selecionados.append(matriz_para_reescalar)

    if cargo_troca == 1:
        padroes = np.random.randint(0, 2, size=(qtde_individuos, farmaceuticos))
    else:
        padroes = np.random.randint(0, 2, size=(qtde_individuos, qtd_blocos))
        blocos_linhas = np.array_split(np.arange(auxiliares), qtd_blocos)

    #toda a lógica de geração de indivíduo será de acordo com o cargo_troca, o outro não precisa ser feito
    for filho_idx in range(qtde_individuos):
        idx_p1, idx_p2 = np.random.choice(num_pais_selecionados, size=2, replace=False)
        pai_1 = corte_selecionados[idx_p1]
        pai_2 = corte_selecionados[idx_p2]
        filho = np.zeros_like(pai_1)

        if cargo_troca == 1: # farmacêuticos
            for linha in range(farmaceuticos):
                if padroes[filho_idx, linha] == 0:
                    filho[linha, :] = pai_1[linha, :]
                else:
                    filho[linha, :] = pai_2[linha, :]
        else: # auxiliares
            for b, indices_bloco in enumerate(blocos_linhas):
                if padroes[filho_idx, b] == 0:
                    filho[indices_bloco, :] = pai_1[indices_bloco, :]
                else:
                    filho[indices_bloco, :] = pai_2[indices_bloco, :]

        
        individuo_quase_completo = np.hstack((matriz_nao_reescalar, filho))
        if cargo_troca == 1: individuo_completo = np.vstack((individuo_quase_completo, cargos_ok))
        else: individuo_completo = np.vstack((cargos_ok, individuo_quase_completo))
        eh_valido = validaSolucaoReescala(individuo_completo, num_dias_mes, turno, farmaceuticos, auxiliares, cargo_troca, id_troca, idx_dia_reescala, nomes, escala_original_numerica)
        filhos_gerados.append(eh_valido)

    if len(filhos_gerados) > 0:
        filhos_finais = np.stack(filhos_gerados, axis=2)
        if filhos_finais.shape[2] != qtde_individuos:
            print(f"Aviso do Cruzamento: Foram gerados {filhos_finais.shape[2]} filhos válidos "
                  f"de um total esperado de {qtde_individuos}.")
    else:
        filhos_finais = np.empty((num_funcionarios_total, num_dias_mes, 0))
        print("Aviso Crítico: Nenhum filho gerado passou nas regras de validação!")

    return filhos_finais