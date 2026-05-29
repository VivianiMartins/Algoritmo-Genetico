import pandas as pd
import time
from algoritmoGenetico import algoritmoGenetico
from edicaoDocumentos.resultadosTeste import resultadosTeste
from edicaoDocumentos.transformarListaEntrada import transformarListaEntrada

def funcaoPrincipal():
    tempoInicio = time.time()  # Inicia o cronômetro para medir o tempo total de execução

    lista_funcionarios_df = pd.read_csv('listaFuncionarios.csv')
    lista_funcionarios = lista_funcionarios_df.values.tolist()

    func_diurnos, func_noturnos, num_dias_mes_anterior, nomes_diurnos, nomes_noturnos, farmaceuticos_diurnos, farmaceuticos_noturnos, auxiliares_diurnos, auxiliares_noturnos = transformarListaEntrada(lista_funcionarios)

    # =========================================================================
    # Algoritmo genético
    # =========================================================================
    tipo = 1 #1 para escala ou 2 para reescala
    turno = 1 #1 para diurno ou 2 para noturno
    num_dias_mes = 30 #total de dias do mês

    dia_reescala_inicio = 0 #dia em que começa a reescala
    dia_reescala_fim = 0  # dia em que termina a reescala

    qtde_individuos = 50
    geracoes = 500

    penalidade_fitness = True #False para não aplicar penalidade e True para aplicar penalidade
    elitismo = True  # False para não manter o melhor indivíduo na próxima geração e True manter o melhor na próxima geração

    selecao = 4 #1 para roleta; 2 para elitismo; 3 para torneio; 4 para Maximax e Maximin
    qtd_pais = 2
    tamanho_grupos_torneios = 5

    cruzamento = 1 #1 por blocos; 2 xadrez(cortes verticais e horizontais)
    qtd_blocos = 10

    mutacao = 2  # 1 bit flip em bloco sorteado a partir de uma linha; 2 bit flip em apenas um gene
    probabilidade_mutacao = 0.2 #probabilidade do indivíduo ser mutato


    if tipo not in [1, 2]: raise ValueError("Deve ser 1 para escala ou 2 para reescala")
    elif tipo == 1: print('=========== Geração para escala ===========\n')
    else: print('=========== Geração para reescala ===========\n')

    if tamanho_grupos_torneios <= 1: tamanho_grupos_torneios = 2 #caso inserir menor que 1

    funcionarios_turno = func_diurnos if turno == 1 else func_noturnos
    nomes_turno = nomes_diurnos if turno == 1 else nomes_noturnos
    farm_turno = farmaceuticos_diurnos if turno == 1 else farmaceuticos_noturnos
    aux_turno = auxiliares_diurnos if turno == 1 else auxiliares_noturnos

    (populacaoFinal, historico_individuos, historico_fitness, melhor_individuo_global, hist_sel_fit, hist_sel_idx, hist_melhor_idx,
     geracao_campea, id_campeao, historico_fitness_todos) = algoritmoGenetico(funcionarios_turno, nomes_turno, farm_turno,
                                                    aux_turno, turno,
                                                    tipo, num_dias_mes, dia_reescala_inicio, dia_reescala_fim,
                                                    qtde_individuos, geracoes,
                                                    penalidade_fitness, elitismo, selecao, qtd_pais, tamanho_grupos_torneios,
                                                    cruzamento, qtd_blocos, mutacao, probabilidade_mutacao)

    tempo_total = time.time() - tempoInicio
    print(f'\nTempo Total: {tempo_total:.2f} segundos ({tempo_total / 60:.2f} minutos)')

    print(f"\n\n A Melhor Escala Global foi encontrada na Geração {geracao_campea} (ID do indivíduo: {id_campeao})!")

    resultadosTeste(populacaoFinal, historico_individuos, historico_fitness, melhor_individuo_global,
                     hist_sel_fit, hist_sel_idx, hist_melhor_idx, geracao_campea, id_campeao,
                     historico_fitness_todos, nomes_turno, farm_turno, aux_turno, num_dias_mes, qtde_individuos)


if __name__ == "__main__":
    funcaoPrincipal()
