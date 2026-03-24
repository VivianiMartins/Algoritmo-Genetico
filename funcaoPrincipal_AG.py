import pandas as pd
import time
import numpy as np
from transformarListaFuncionarios import transformarListaFuncionarios
from geraPopulacaoInicial import geraPopulacaoInicial

def funcaoPrincipal_AG():
    # ============================================================
    # INICIAR CONTADOR DE TEMPO
    # ============================================================
    tempoInicio = time.time()  # Inicia cronômetro

    # importando a tabela com os funcionários contendo: nome, cargo, turno e férias.
    listaFuncionarios_df = pd.read_csv('listaFuncionarios.csv')
    listaFuncionarios = listaFuncionarios_df.values.tolist()

    # terei duas matrizes de funcionarios por turno:
    funcDiurnos, funcNoturnos, numDiasMes = transformarListaFuncionarios(listaFuncionarios)
    tempoDecorrido = time.time() - tempoInicio

    print('\n========== RELATÓRIO DE FUNCIONÁRIOS ==========')
    print(f'Total de funcionários: {len(listaFuncionarios)}')
    print(f'Funcionários diurnos: {funcDiurnos.shape[0]}')
    print(f'Funcionários noturnos: {funcNoturnos.shape[0]}')
    print('==============================================\n')

    #%%% Parâmetros %%%
    qtdeIndividuos = 5
    escala = 1  # 1 para escala, 0 para reescala
    # se for escala, tem que modificar a quantidade de dias do mês para o do mês seguinte
    numDiasMes = 31
    diaReescala = 0

    if escala == 1:
        print('=========== Geração para escala ===========\n\n')
    else:
        print('=========== Geração para reescala ===========\n\n')

    # Gerando as populações iniciais de cada turno separadamente:
    populacaoDiurna = geraPopulacaoInicial(funcDiurnos, qtdeIndividuos, numDiasMes, escala, diaReescala)

    # Pega o indivíduo 5 completo (toda a escala)
    individuo5 = populacaoDiurna[:, :, 4]  # matriz [funcionários x dias]

    # Pega a escala do funcionário de férias no individuo 5 (assuming 14 is 13 in 0-based)
    escalaFunc14 = populacaoDiurna[13, :, 4]  # vetor [1 x dias]

    # keyboard equivalent
    input("Press Enter to continue...")

    # RESULTADO
    tempoTotal = time.time() - tempoInicio  # Tempo total de execução
    print(f'Dimensões da população: {populacaoDiurna.shape[0]} x {populacaoDiurna.shape[1]} x {populacaoDiurna.shape[2]}')
    print(f'Tempo Total: {tempoTotal:.2f} segundos ({tempoTotal/60:.2f} minutos)')
    # populacaoNoturna = geraPopulacaoInicial(funcNoturnos, qtdeIndividuos, numDiasMes)

if __name__ == "__main__":
    funcaoPrincipal_AG()
