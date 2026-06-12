import numpy as np

from algoritmoGeneticoReescala.avalicoesEvalidacoes.funcaoFitnessReescala import funcaoFitnessReescala
from algoritmoGeneticoReescala.cruzamento.blocosReescala import blocosReescala
from algoritmoGeneticoReescala.cruzamento.porcentagenSorteioReescala import percentagensSorteioReescala
from algoritmoGeneticoReescala.cruzamento.xadrezReescala import xadrezReescala
from algoritmoGeneticoReescala.geraPopulacaoInicialReescala import geraPopulacaoInicialReescala
from algoritmoGeneticoReescala.mutacao.bitFlipBlocoReescala import bitFlipBlocoReescala
from algoritmoGeneticoReescala.mutacao.bitFlipGeneReescala import bitFlipGeneReescala
from edicaoDocumentos.salvarExcel import salvarExcel
from selecao.elitista import elitista
from selecao.maximaxMaximin import maximaxMaximin
from selecao.roleta import roleta
from selecao.torneio import torneio


def algoritmoGeneticoReescala(cargos_ok, matriz_para_reescalar, matriz_nao_reescalar, nomes, nomes_lista, id_troca, num_dias_mes, cargo_troca, farmaceuticos, auxiliares, dias_resto_mes,
                              escala_original_numerica, dia_reescala, turno,
                              qtde_individuos, geracoes, elitismo, selecao, qtd_pais, tamanho_grupos_torneios, cruzamento, qtd_blocos, mutacao, probabilidade_mutacao):
    """
    Executa o Algoritmo Genético completo ao longo de várias gerações.
    """
    # Para Testes: Seed é um valor inicial que "inicializa" o gerador de números aleatórios (PRNG - Pseudo-Random Number Generator). Mesmo seed = mesmos números aleatórios: Toda vez que roda o código com seed(42), obtém os mesmos números "aleatórios" na mesma ordem.
    np.random.seed(42)

    historico_individuos = []
    historico_fitness = []
    historico_hamming = []
    historico_alteracoes = []
    historico_selecionados_fitness = []
    historico_selecionados_indices = []
    historico_melhor_idx = []
    historico_fitness_todos = []
    melhor_individuo_global = None
    melhor_fitness_global = -np.inf  # Começa com o menor valor possível
    melhor_geracao_global = 0
    melhor_id_global = 0
    id_troca_recorte = id_troca if cargo_troca == 1 else id_troca - farmaceuticos
    idx_dia_reescala = dia_reescala - 1


    # ---------------------------------------------------------
    # População inicial
    # ---------------------------------------------------------
    populacao_atual = geraPopulacaoInicialReescala(cargos_ok, matriz_para_reescalar, matriz_nao_reescalar, id_troca, id_troca_recorte, num_dias_mes, cargo_troca, farmaceuticos, auxiliares, idx_dia_reescala, turno, qtde_individuos, nomes, escala_original_numerica, dias_resto_mes)
    salvarExcel(populacao=populacao_atual, lista_nomes_cargos=nomes_lista, farmaceuticos=farmaceuticos, auxiliares=auxiliares, caminho_arquivo='0_população_inicial.xlsx', num_dias_mes=num_dias_mes, salvar_completo=True, somatorio=True)

    for geracao in range(geracoes):
        print(f"\n>> Processando Geração {geracao + 1}/{geracoes} <<")

        # ---------------------------------------------------------
        # Fitness
        # ---------------------------------------------------------
        resultado_fitness, hamming, alteracoes = funcaoFitnessReescala(populacao_atual, num_dias_mes, turno, nomes, farmaceuticos, auxiliares, escala_original_numerica, dias_resto_mes, cargo_troca)

        historico_fitness_todos.append(resultado_fitness.copy())
        historico_hamming.append(hamming.copy())
        historico_alteracoes.append(alteracoes.copy())
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
        elif selecao == 4: selecionados = maximaxMaximin(resultado_fitness, qtd_pais, qtde_individuos)

        historico_selecionados_indices.append(selecionados)
        historico_selecionados_fitness.append(resultado_fitness[selecionados])

        if geracao < geracoes - 1:
            # ---------------------------------------------------------
            # Cruzamento
            # ---------------------------------------------------------
            if cruzamento == 1: populacao_atual = blocosReescala(selecionados, populacao_atual, nomes, qtde_individuos, qtd_blocos, turno, farmaceuticos, auxiliares, num_dias_mes, dia_reescala, id_troca, idx_dia_reescala, cargo_troca, cargos_ok, matriz_nao_reescalar, escala_original_numerica)
            elif cruzamento == 2: populacao_atual = xadrezReescala(selecionados, populacao_atual, nomes, qtde_individuos, turno, farmaceuticos, auxiliares, num_dias_mes, dia_reescala, id_troca, idx_dia_reescala, cargo_troca, cargos_ok, matriz_nao_reescalar, escala_original_numerica, dias_resto_mes)
            elif cruzamento == 3: populacao_atual = percentagensSorteioReescala(selecionados, populacao_atual, nomes, qtde_individuos, turno, farmaceuticos, auxiliares, num_dias_mes, dia_reescala, id_troca, idx_dia_reescala, cargo_troca, cargos_ok, matriz_nao_reescalar, escala_original_numerica)

            # ---------------------------------------------------------
            # Mutação
            # ---------------------------------------------------------
            if mutacao == 1: populacao_atual = bitFlipBlocoReescala(probabilidade_mutacao, populacao_atual, turno, farmaceuticos, auxiliares, num_dias_mes, dia_reescala, cargo_troca, cargos_ok, matriz_nao_reescalar, escala_original_numerica, id_troca, idx_dia_reescala, nomes, dias_resto_mes)
            elif mutacao == 2: populacao_atual = bitFlipGeneReescala(probabilidade_mutacao, populacao_atual, turno, farmaceuticos, auxiliares, num_dias_mes, dia_reescala, cargo_troca, cargos_ok, matriz_nao_reescalar, escala_original_numerica, id_troca, idx_dia_reescala, nomes, dias_resto_mes)

        if elitismo: populacao_atual[:, :, -1] = melhor_individuo_global

    return (populacao_atual, historico_individuos, historico_fitness, melhor_individuo_global, historico_selecionados_fitness, historico_selecionados_indices, historico_melhor_idx, melhor_geracao_global,
            melhor_id_global, historico_fitness_todos, historico_hamming, historico_alteracoes)