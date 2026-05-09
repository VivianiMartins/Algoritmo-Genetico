import numpy as np
from geraPopulacaoInicial import geraPopulacaoInicial
from funcaoFitness import funcaoFitness
from salvarExcel import salvar_excel
from selecao import selecao
from cruzamento import cruzamento

def algoritmoGenetico(funcionarios, qtdeIndividuos, numDiasMes, tipo, diaReescala, turno, qtd_blocos, geracoes, nomes, farmaceuticos, auxiliares, qtd_pais):
    """
    Executa o Algoritmo Genético completo ao longo de várias gerações.

    Entrada:
      populacao: array 3D [funcionários x dias x indivíduos]
      qtdeIndividuos:
      dadosFuncionarios: array numpy com [Cargo, Turno, Inicio, Fim, Dias...]
      qtd_pais: quantidade de pais a serem selecionados
      qtd_blocos: em quantas partes os auxiliares serão divididos no cruzamento
      turno: 1 para diurno, 0 para reescala (usa dias existentes)
      farmaceuticos: total de farmacêuticos no turno
      auxiliares: total de auxiliares no turno

    Saída:
        populacaoAtual: Matriz com a última população gerada
        historico_individuos: Lista contendo o melhor indivíduo de cada geração
        historico_fitness: Lista contendo a nota do melhor indivíduo de cada geração
        melhor_individuo_global: O melhor indivíduo absoluto encontrado em todas as gerações
    """
    print(f"\n--- Iniciando População Inicial (Turno {turno}) ---")

    # ---------------------------------------------------------
    # População inicial
    # ---------------------------------------------------------
    populacaoAtual = geraPopulacaoInicial(funcionarios, qtdeIndividuos, numDiasMes, tipo, diaReescala)
    salvar_excel( populacao=populacaoAtual, lista_nomes_cargos=nomes, farmaceuticos=farmaceuticos, auxiliares=auxiliares, caminho_arquivo='0_população_inicial.xlsx', num_dias_mes=numDiasMes, salvar_completo=True, somatorio=True)

    historico_individuos = []
    historico_fitness = []

    melhor_individuo_global = None
    melhor_fitness_global = -np.inf  # Começa com o menor valor possível

    for geracao in range(geracoes):
        print(f"\n>> Processando Geração {geracao + 1}/{geracoes} <<")

        # ---------------------------------------------------------
        # Ftness
        # ---------------------------------------------------------
        resultadoFitness = funcaoFitness(populacaoAtual, numDiasMes, tipo, turno, farmaceuticos, auxiliares)

        melhor_idx = np.argmax(resultadoFitness)  # Pega o índice da maior nota
        melhor_fitness_geracao = resultadoFitness[melhor_idx]
        melhor_individuo_geracao = populacaoAtual[:, :, melhor_idx].copy()

        historico_individuos.append(melhor_individuo_geracao)
        historico_fitness.append(melhor_fitness_geracao)

        if melhor_fitness_geracao > melhor_fitness_global:
            melhor_fitness_global = melhor_fitness_geracao
            melhor_individuo_global = melhor_individuo_geracao.copy()

        # ---------------------------------------------------------
        # Seleção
        # ---------------------------------------------------------
        selecionados = selecao(resultadoFitness, qtd_pais)
        notas_formatadas = [f"{nota:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.') for nota in
                            resultadoFitness[selecionados]]

        print(f"   Índices selecionados: {selecionados}")
        print(f"   Fitness dos selecionados: {notas_formatadas}")
        print(
            f"   Melhor Fitness da Geração: {melhor_fitness_geracao:,.2f}".replace(',', '_').replace('.', ',').replace(
                '_', '.'))


        if geracao < geracoes - 1:
            # ---------------------------------------------------------
            # Cruzamento
            # ---------------------------------------------------------
            populacaoAtual = cruzamento(selecionados, populacaoAtual, funcionarios, qtdeIndividuos, qtd_blocos, turno, farmaceuticos, auxiliares)
            # ---------------------------------------------------------
            # Mutação - ainda pensando em como fazer
            # ---------------------------------------------------------


    return populacaoAtual, historico_individuos, historico_fitness, melhor_individuo_global