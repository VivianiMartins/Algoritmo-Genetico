import pandas as pd
import time
from transformarListaFuncionarios import transformarListaFuncionarios
from geraPopulacaoInicial import geraPopulacaoInicial

def funcaoPrincipal_AG():
    tempoInicio = time.time()  # Inicia o cronômetro para medir o tempo total de execução

    listaFuncionarios_df = pd.read_csv('listaFuncionarios.csv')
    listaFuncionarios = listaFuncionarios_df.values.tolist()

    funcDiurnos, funcNoturnos, numDiasMes = transformarListaFuncionarios(listaFuncionarios)

    print('\n========== RELATÓRIO DE FUNCIONÁRIOS ==========')
    print(f'Total de funcionários: {len(listaFuncionarios)}')
    print(f'Funcionários diurnos: {funcDiurnos.shape[0]}')
    print(f'Funcionários noturnos: {funcNoturnos.shape[0]}')
    print('==============================================\n')

    #%%% Parâmetros para o Algoritmo genético %%%
    qtdeIndividuos = 5
    tipo = 1 # criar input para usuário, algo para o fim
    numDiasMes = 31
    diaReescala = 0 #ideal seria automatizar esta conta, algo para o fim

    if tipo not in [1, 2]:
        raise ValueError("Deve ser 1 para escala ou 2 para reescala")
    elif tipo== 1:  # Verifica se é geração de nova escala
        print('=========== Geração para escala ===========\n\n')
    else:  # Se for reescala (escala == 2)
        print('=========== Geração para reescala ===========\n\n')

    #%% Gerando as populações iniciais %%#
    populacaoDiurna = geraPopulacaoInicial(funcDiurnos, qtdeIndividuos, numDiasMes, tipo, diaReescala)

    # Pega o indivíduo 5 completo (toda a escala)
    individuo5 = populacaoDiurna[:, :, 4]  # Seleciona o 5º indivíduo (índice 4, 0-based)

    # Pega a escala do funcionário de férias no individuo 5 (assuming 14 is 13 in 0-based)
    escalaFunc14 = populacaoDiurna[13, :, 4]  # Seleciona escala do 14º funcionário no 5º indivíduo

    # Keyboard equivalent - pausa para o usuário ver os resultados
    input("Press Enter to continue...")  # Aguarda entrada do usuário para continuar

    # RESULTADO
    tempoTotal = time.time() - tempoInicio  # Calcula tempo total de execução
    print(f'Dimensões da população: {populacaoDiurna.shape[0]} x {populacaoDiurna.shape[1]} x {populacaoDiurna.shape[2]}')  # Imprime forma da matriz
    print(f'Tempo Total: {tempoTotal:.2f} segundos ({tempoTotal/60:.2f} minutos)')  # Imprime tempo total
    # populacaoNoturna = geraPopulacaoInicial(funcNoturnos, qtdeIndividuos, numDiasMes)  # Linha comentada para noturnos

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    funcaoPrincipal_AG()  # Chama a função principal
