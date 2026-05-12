import numpy as np
from geraPopulacaoInicial import geraPopulacaoInicial
from funcaoFitness import funcaoFitness
from mutacao import mutacao
from salvarExcel import salvar_excel
from selecao import selecao
from cruzamento import cruzamento

def algoritmoGenetico(funcionarios, qtdeIndividuos, numDiasMes, tipo, diaReescala, turno, qtd_blocos, geracoes, nomes, farmaceuticos, auxiliares, qtd_pais):
    """
    Executa o Algoritmo Genético completo ao longo de várias gerações.
    """

    # ---------------------------------------------------------
    # População inicial
    # ---------------------------------------------------------
    populacaoAtual = geraPopulacaoInicial(funcionarios, qtdeIndividuos, numDiasMes, tipo, diaReescala)
    salvar_excel( populacao=populacaoAtual, lista_nomes_cargos=nomes, farmaceuticos=farmaceuticos, auxiliares=auxiliares, caminho_arquivo='0_população_inicial.xlsx', num_dias_mes=numDiasMes, salvar_completo=True, somatorio=True)

    historico_individuos = []
    historico_fitness = []

    historico_selecionados_fitness = []
    historico_selecionados_indices = []
    historico_melhor_idx = []
    historico_fitness_todos = []

    melhor_individuo_global = None
    melhor_fitness_global = -np.inf  # Começa com o menor valor possível
    melhor_geracao_global = 0
    melhor_id_global = 0

    for geracao in range(geracoes):
        print(f"\n>> Processando Geração {geracao + 1}/{geracoes} <<")

        # ---------------------------------------------------------
        # Ftness
        # ---------------------------------------------------------
        resultadoFitness = funcaoFitness(populacaoAtual, numDiasMes, tipo, turno, farmaceuticos, auxiliares)
        historico_fitness_todos.append(resultadoFitness.copy())

        melhor_idx = np.argmax(resultadoFitness)  # Pega o índice da maior nota
        melhor_fitness_geracao = resultadoFitness[melhor_idx]
        melhor_individuo_geracao = populacaoAtual[:, :, melhor_idx].copy()

        historico_individuos.append(melhor_individuo_geracao)
        historico_fitness.append(melhor_fitness_geracao)
        historico_melhor_idx.append(melhor_idx)

        if melhor_fitness_geracao > melhor_fitness_global:
            melhor_fitness_global = melhor_fitness_geracao
            melhor_individuo_global = melhor_individuo_geracao.copy()
            melhor_geracao_global = geracao + 1
            melhor_id_global = melhor_idx

        # ---------------------------------------------------------
        # Seleção
        # ---------------------------------------------------------
        selecionados = selecao(resultadoFitness, qtd_pais)
        historico_selecionados_indices.append(selecionados)
        historico_selecionados_fitness.append(resultadoFitness[selecionados])

        if geracao < geracoes - 1:
            # ---------------------------------------------------------
            # Cruzamento
            # ---------------------------------------------------------
            populacaoAtual = cruzamento(selecionados, populacaoAtual, funcionarios, qtdeIndividuos, qtd_blocos, turno, farmaceuticos, auxiliares, numDiasMes)
            # ---------------------------------------------------------
            # Mutação - ainda pensando em como fazer
            # ---------------------------------------------------------
            populacaoAtual = mutacao(populacaoAtual, funcionarios, turno, farmaceuticos, auxiliares, numDiasMes)

    return (populacaoAtual, historico_individuos, historico_fitness, melhor_individuo_global, historico_selecionados_fitness, historico_selecionados_indices, historico_melhor_idx, melhor_geracao_global,
            melhor_id_global, historico_fitness_todos)