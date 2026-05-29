import numpy as np
from salvarExcel import salvar_excel
from geraPopulacaoInicial import geraPopulacaoInicial
from funcaoFitness import funcaoFitness
from selecao.maximax_maximin import maximax_maximin
from selecao.roleta import roleta
from selecao.elitista import elitista
from selecao.torneio import torneio
from cruzamento.blocos import blocos

def algoritmoGenetico(funcionarios, nomes, farmaceuticos, auxiliares, turno, tipo, num_dias_mes, dia_reescala_inicio, dia_reescala_fim,
                qtde_individuos, geracoes, penalidade_fitness, elitismo, selecao, qtd_pais, tamanho_grupos_torneios, cruzamento, qtd_blocos, mutacao, taxa_mutacao):
    """
    Executa o Algoritmo Genético completo ao longo de várias gerações.
    """
    # Para Testes: Seed é um valor inicial que "inicializa" o gerador de números aleatórios (PRNG - Pseudo-Random Number Generator). Mesmo seed = mesmos números aleatórios: Toda vez que roda o código com seed(42), obtém os mesmos números "aleatórios" na mesma ordem.
    #np.random.seed(42)

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

    # ---------------------------------------------------------
    # População inicial
    # ---------------------------------------------------------
    populacao_atual = geraPopulacaoInicial(funcionarios, qtde_individuos, num_dias_mes, tipo, dia_reescala_inicio, dia_reescala_fim)
    salvar_excel( populacao=populacao_atual, lista_nomes_cargos=nomes, farmaceuticos=farmaceuticos, auxiliares=auxiliares, caminho_arquivo='0_população_inicial.xlsx', num_dias_mes=num_dias_mes, salvar_completo=True, somatorio=True)

    if elitismo: qtde_individuos = qtde_individuos - 1

    for geracao in range(geracoes):
        print(f"\n>> Processando Geração {geracao + 1}/{geracoes} <<")

        # ---------------------------------------------------------
        # Fitness
        # ---------------------------------------------------------
        resultado_fitness = funcaoFitness(populacao_atual, num_dias_mes, tipo, turno, farmaceuticos, auxiliares, penalidade=penalidade_fitness)

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
        if selecao == 1: selecionados = roleta(resultado_fitness, qtd_pais)
        elif selecao == 2: selecionados = elitista(resultado_fitness, qtd_pais)
        elif selecao == 3: selecionados = torneio(resultado_fitness, qtd_pais, tamanho_grupos_torneios)
        elif selecao == 4: selecionados = maximax_maximin(resultado_fitness, qtd_pais)

        historico_selecionados_indices.append(selecionados)
        historico_selecionados_fitness.append(resultado_fitness[selecionados])

        if geracao < geracoes - 1:
            # ---------------------------------------------------------
            # Cruzamento
            # ---------------------------------------------------------
            if cruzamento == 1: populacao_atual = blocos(selecionados, populacao_atual, funcionarios, qtde_individuos, qtd_blocos, turno, farmaceuticos, auxiliares, num_dias_mes)


            # ---------------------------------------------------------
            # Mutação - refazer
            # ---------------------------------------------------------
            #populacao_atual = mutacao(populacao_atual, funcionarios, turno, farmaceuticos, auxiliares, num_dias_mes)

            if elitismo: populacao_atual[:, :, -1] = melhor_individuo_global

    return (populacao_atual, historico_individuos, historico_fitness, melhor_individuo_global, historico_selecionados_fitness, historico_selecionados_indices, historico_melhor_idx, melhor_geracao_global,
            melhor_id_global, historico_fitness_todos)