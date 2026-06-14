import numpy as np
import pandas as pd
import time
from algoritmoGeneticoEscala.algoritmoGeneticoEscala import algoritmoGeneticoEscala
from algoritmoGeneticoReescala.algoritmoGeneticoReescala import algoritmoGeneticoReescala
from edicaoDocumentos.graficoDispersaoHamming import graficoDispersaoHamming

from edicaoDocumentos.resultadosTeste import resultadosTeste
from edicaoDocumentos.transformarEntradaDoisTurnos import transformarEntradaDoisTurnos
from edicaoDocumentos.transformarEntradaReescala import transformarEntradaReescala

def funcaoPrincipal():

    # =========================================================================
    # Parâmetros
    # =========================================================================
    tipo = 2 #1 para escala ou 2 para reescala
    turno = 1 #1 para diurno ou 2 para noturno
    # __________________________________________________________________________________________________________________
    # Parâmetros do algoritmo genético
    qtde_individuos = 50
    geracoes = 1500

    elitismo = True  # False para não manter o melhor indivíduo na próxima geração e True manter o melhor na próxima geração

    selecao = 3 #1 para roleta; 2 para elitismo; 3 para torneio; 4 para Maximax e Maximin
    qtd_pais = 2
    tamanho_grupos_torneios = 5 #tamanho dos grupos para seleção por torneio (deve ser menor que a quantidade de indivíduos)

    cruzamento = 3 #1 por blocos (cortes horizontais); 2 xadrez(cortes verticais e horizontais); 3 percentagem de herança e ordem sorteadas (cortes verticais)
    qtd_blocos = 0

    mutacao = 2  # 1 bit flip em bloco sorteado a partir de uma linha; 2 bit flip em apenas um gene
    probabilidade_mutacao = 0.2 #probabilidade do indivíduo ser mutado
    #__________________________________________________________________________________________________________________
    #usado apenas na escala
    num_dias_mes = 30  # total de dias do mês

    # usados apenas na reescala:
    dia_reescala = 12  # dia que tem que achar outro para substituir o funcionario abaixo
    funcionario = 'Enzo Ramos'  # nome do funcionario que irá sair

    # __________________________________________________________________________________________________________________
    if tipo not in [1, 2]: raise ValueError("Deve ser 1 para escala ou 2 para reescala")
    elif tipo == 1: print('=========== Geração para escala ===========\n')
    else: print('=========== Geração para reescala ===========\n')

    if tamanho_grupos_torneios <= 1: tamanho_grupos_torneios = 2 #caso inserir menor que 1

    tempo_inicio = time.time()  # Inicia o cronômetro para medir o tempo total de execução

    if tipo == 1:
        lista_funcionarios_df = pd.read_csv('algoritmoGeneticoEscala/listaFuncionarios.csv')
        lista_funcionarios = lista_funcionarios_df.values.tolist()

        (func_diurnos, func_noturnos, num_dias_mes_anterior, nomes_diurnos, nomes_noturnos, farmaceuticos_diurnos, farmaceuticos_noturnos,
         auxiliares_diurnos, auxiliares_noturnos) = transformarEntradaDoisTurnos(lista_funcionarios)

        funcionarios_turno = func_diurnos if turno == 1 else func_noturnos
        nomes_turno = nomes_diurnos if turno == 1 else nomes_noturnos
        farm_turno = farmaceuticos_diurnos if turno == 1 else farmaceuticos_noturnos
        aux_turno = auxiliares_diurnos if turno == 1 else auxiliares_noturnos


        (populacao_final, historico_individuos, historico_fitness, melhor_individuo_global, hist_sel_fit, hist_sel_idx, hist_melhor_idx,
         geracao_campea, id_campeao, historico_fitness_todos) = algoritmoGeneticoEscala(funcionarios_turno, nomes_turno, farm_turno, aux_turno, turno, num_dias_mes,
                      qtde_individuos, geracoes, elitismo, selecao, qtd_pais, tamanho_grupos_torneios, cruzamento, qtd_blocos, mutacao, probabilidade_mutacao)

        tempo_total = time.time() - tempo_inicio
        print(f'\nTempo Total: {tempo_total:.2f} segundos ({tempo_total / 60:.2f} minutos)')

        print(
            f"\n\n A Melhor Escala Global foi encontrada na Geração {geracao_campea} (ID do indivíduo: {id_campeao})!")

        resultadosTeste(populacao_final, historico_individuos, historico_fitness, melhor_individuo_global,
                        hist_sel_fit, hist_sel_idx, hist_melhor_idx, geracao_campea, id_campeao,
                        historico_fitness_todos, nomes_turno, farm_turno, aux_turno, num_dias_mes, qtde_individuos)

    elif tipo == 2:
        lista_funcionarios_df = pd.read_excel('algoritmoGeneticoReescala/melhor_escala_ag.xlsx', engine='openpyxl')
        lista_funcionarios = lista_funcionarios_df.values.tolist()

        cargos_ok, matriz_para_reescalar, matriz_nao_reescalar, nomes, nomes_lista, funcionario_troca, id_troca, num_dias_mes, cargo_troca, qtd_colaboradores_reescala, qtd_colaboradores_cargos_ok, dias_resto_mes = transformarEntradaReescala(lista_funcionarios, dia_reescala, funcionario)

        if qtd_colaboradores_reescala == 0:
            print(f"\n>> Funcionário não encontrado para reescala ou não encontrado substitutos <<")
        else:
            funcionarios = np.array(lista_funcionarios, dtype=object)
            escala_original_numerica = funcionarios[:,5:].astype(np.int8)

            if cargo_troca == 1:
                farmaceuticos = qtd_colaboradores_reescala
                auxiliares = qtd_colaboradores_cargos_ok
            else:
                farmaceuticos = qtd_colaboradores_cargos_ok
                auxiliares = qtd_colaboradores_reescala

            (populacao_final, historico_individuos, historico_fitness, melhor_individuo_global, hist_sel_fit, hist_sel_idx, hist_melhor_idx,
         geracao_campea, id_campeao, historico_fitness_todos, historico_hamming, historico_alteracoes) = algoritmoGeneticoReescala(cargos_ok, matriz_para_reescalar, matriz_nao_reescalar, nomes, nomes_lista, id_troca, num_dias_mes, cargo_troca, farmaceuticos, auxiliares, dias_resto_mes,
                              escala_original_numerica, dia_reescala, turno,
                              qtde_individuos, geracoes, elitismo, selecao, qtd_pais, tamanho_grupos_torneios, cruzamento, qtd_blocos, mutacao, probabilidade_mutacao)

            tempo_total = time.time() - tempo_inicio
            print(f'\nTempo Total: {tempo_total:.2f} segundos ({tempo_total / 60:.2f} minutos)')

            print(
                f"\n\n A Melhor Escala Global foi encontrada na Geração {geracao_campea} (ID do indivíduo: {id_campeao})!")

            resultadosTeste(populacao_final, historico_individuos, historico_fitness, melhor_individuo_global,
                            hist_sel_fit, hist_sel_idx, hist_melhor_idx, geracao_campea, id_campeao,
                            historico_fitness_todos, nomes_lista, farmaceuticos, auxiliares, num_dias_mes, qtde_individuos)

            graficoDispersaoHamming(historico_hamming, qtde_individuos, historico_alteracoes)

if __name__ == "__main__":
    funcaoPrincipal()
