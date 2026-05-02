import pandas as pd
import time

from cruzamento import cruzamento
from funcaoFitness import funcaoFitness
from salvarExcel import salvar_excel
from selecao import selecao
from transformarListaEntrada import transformarListaEntrada
from geraPopulacaoInicial import geraPopulacaoInicial

def funcaoPrincipal_AG():
    tempoInicio = time.time()  # Inicia o cronômetro para medir o tempo total de execução

    listaFuncionarios_df = pd.read_csv('listaFuncionarios.csv')
    listaFuncionarios = listaFuncionarios_df.values.tolist()

    funcDiurnos, funcNoturnos, numDiasMes, nomesDiurnos, nomesNoturnos = transformarListaEntrada(listaFuncionarios)

    print('\n========== RELATÓRIO DE FUNCIONÁRIOS ==========')
    print(f'Total de funcionários: {len(listaFuncionarios)}')
    print(f'Funcionários diurnos: {funcDiurnos.shape[0]}')
    print(f'Funcionários noturnos: {funcNoturnos.shape[0]}')
    print('==============================================\n')

    #%%% Parâmetros para o Algoritmo genético %%%
    qtdeIndividuos = 10
    tipo = 1 # criar input para usuário, algo para o fim - 1 é escala e 2 é reescala
    turno = 1 # criar input para usuário, algo para o fim - 1 é diurno e 2 é noturno
    numDiasMes = 31
    diaReescala = 0 #ideal seria automatizar esta conta, algo para o fim

    if tipo not in [1, 2]:
        raise ValueError("Deve ser 1 para escala ou 2 para reescala")
    elif tipo== 1:  # Verifica se é geração de nova escala
        print('=========== Geração para escala ===========\n\n')
    else:  # Se for reescala (escala == 2)
        print('=========== Geração para reescala ===========\n\n')

    #%% Gerando as populações iniciais %%#

    # Diurno #
    populacaoDiurna = geraPopulacaoInicial(funcDiurnos, qtdeIndividuos, numDiasMes, tipo, diaReescala)

    #salvar_excel( populacao=populacaoDiurna, lista_nomes_cargos=nomesDiurnos, caminho_arquivo='população_inicial_diurna.xlsx', num_dias_mes=numDiasMes, salvar_completo=True, somatorio=True)
    resultadoFitness = funcaoFitness(populacaoDiurna, numDiasMes, tipo, turno)
    selecionados = selecao(resultadoFitness, num_selecionados=2)
    nova_populacao = cruzamento(selecionados, populacaoDiurna, qtd_filhos = 6)

    tempoTotal = time.time() - tempoInicio  # Calcula tempo total de execução até o momento
    print(f'Tempo Total: {tempoTotal:.2f} segundos ({tempoTotal/60:.2f} minutos)')



    # Noturno #
    #populacaoNoturna = geraPopulacaoInicial(funcNoturnos, qtdeIndividuos, numDiasMes, tipo, diaReescala)
    #salvar_excel( populacao=populacaoNoturna, lista_nomes_cargos=nomesNoturnos, caminho_arquivo='população_inicial_noturna.xlsx', num_dias_mes=numDiasMes, salvar_completo=True, somatorio=True)
    #tempoTotal = time.time() - tempoInicio  # Calcula tempo total de execução até o momento
    #print(f'Tempo Total: {tempoTotal:.2f} segundos ({tempoTotal / 60:.2f} minutos)')

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    funcaoPrincipal_AG()  # Chama a função principal
