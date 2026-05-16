import numpy as np

from cruzamentoBlocoMelhorGobal import cruzamentoBlocoMelhorGlobal
from funcaoFitnessNova import funcaoFitnessNova
from geraPopulacaoInicial import geraPopulacaoInicial
from funcaoFitness import funcaoFitness
from mutacao import mutacao
from salvarExcel import salvar_excel
from selecaoRoleta import selecaoRoleta
from cruzamentoBloco import cruzamentoBloco
from selecaoElite import selecaoElite


def algoritmoGenetico(funcionarios, qtdeIndividuos, numDiasMes, tipo, diaReescala, turno, qtd_blocos, geracoes, nomes, farmaceuticos, auxiliares, qtd_pais, penalidade, fitness, selecao, cruzamento):
    """
    Executa o Algoritmo Genético completo ao longo de várias gerações.
    """
    # Para Testes: Seed é um valor inicial que "inicializa" o gerador de números aleatórios (PRNG - Pseudo-Random Number Generator).
    # Mesmo seed = mesmos números aleatórios: Toda vez que você roda o código com seed(42), obtém os mesmos números "aleatórios" na mesma ordem.
    np.random.seed(42)

    # ---------------------------------------------------------
    # População inicial
    # ---------------------------------------------------------
    populacao_atual = geraPopulacaoInicial(funcionarios, qtdeIndividuos, numDiasMes, tipo, diaReescala)
    salvar_excel( populacao=populacao_atual, lista_nomes_cargos=nomes, farmaceuticos=farmaceuticos, auxiliares=auxiliares, caminho_arquivo='0_população_inicial.xlsx', num_dias_mes=numDiasMes, salvar_completo=True, somatorio=True)

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
        resultado_fitness = []
        if fitness==1:
            resultado_fitness = funcaoFitness(populacao_atual, numDiasMes, tipo, turno, farmaceuticos, auxiliares)
        elif fitness == 2:
            resultado_fitness = funcaoFitnessNova(populacao_atual, numDiasMes, tipo, turno, farmaceuticos, auxiliares, penalidade=penalidade)

        historico_fitness_todos.append(resultado_fitness.copy())

        melhor_idx = np.argmax(resultado_fitness)  # Pega o índice da maior nota
        melhor_fitness_geracao = resultado_fitness[melhor_idx]
        melhor_individuo_geracao = populacao_atual[:, :, melhor_idx].copy()

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
        selecionados = []
        if selecao == 1:
            selecionados = selecaoRoleta(resultado_fitness, qtd_pais)
        elif selecao == 2:
            selecionados = selecaoElite(resultado_fitness, qtd_pais)

        historico_selecionados_indices.append(selecionados)
        historico_selecionados_fitness.append(resultado_fitness[selecionados])

        if geracao < geracoes - 1:
            # ---------------------------------------------------------
            # Cruzamento
            # ---------------------------------------------------------
            if cruzamento == 1:
                populacao_atual = cruzamentoBloco(selecionados, populacao_atual, funcionarios, qtdeIndividuos, qtd_blocos, turno, farmaceuticos, auxiliares, numDiasMes)
            elif cruzamento == 2:
                populacao_atual = cruzamentoBlocoMelhorGlobal(selecionados, populacao_atual, funcionarios, qtdeIndividuos, qtd_blocos, turno, farmaceuticos, auxiliares, numDiasMes, melhor_individuo_global)

            # ---------------------------------------------------------
            # Mutação - ainda pensando em como fazer
            # ---------------------------------------------------------
            populacao_atual = mutacao(populacao_atual, funcionarios, turno, farmaceuticos, auxiliares, numDiasMes)

            if cruzamento == 2:
                populacao_atual[:, :, -1] = melhor_individuo_global

    return (populacao_atual, historico_individuos, historico_fitness, melhor_individuo_global, historico_selecionados_fitness, historico_selecionados_indices, historico_melhor_idx, melhor_geracao_global,
            melhor_id_global, historico_fitness_todos)