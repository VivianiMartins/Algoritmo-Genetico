import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from algoritmoGenetico import algoritmoGenetico
from transformarListaEntrada import transformarListaEntrada
from salvarExcel import salvar_excel

def funcaoPrincipal():
    tempoInicio = time.time()  # Inicia o cronômetro para medir o tempo total de execução

    listaFuncionarios_df = pd.read_csv('listaFuncionarios.csv')
    listaFuncionarios = listaFuncionarios_df.values.tolist()

    funcDiurnos, funcNoturnos, numDiasMesAnterior, nomesDiurnos, nomesNoturnos, farmaceuticosDiurnos, farmaceuticosNoturnos, auxiliaresDiurnos, auxiliaresNoturnos = transformarListaEntrada( listaFuncionarios)

    print('\n========== RELATÓRIO DE FUNCIONÁRIOS ==========')
    print(f'Total de funcionários: {len(listaFuncionarios)}')
    print(f'Funcionários diurnos: {funcDiurnos.shape[0]}')
    print(f'Funcionários noturnos: {funcNoturnos.shape[0]}')
    print('==============================================\n')

    # =========================================================================
    # Algoritmo genético
    # =========================================================================
    qtdeIndividuos = 20
    geracoes = 10
    qtd_pais = 2
    qtd_blocos = 10
    tipo = 1
    turno = 1
    numDiasMes = 31
    diaReescala = 0

    if tipo not in [1, 2]:
        raise ValueError("Deve ser 1 para escala ou 2 para reescala")
    elif tipo == 1:
        print('=========== Geração para escala ===========\n')
    else:
        print('=========== Geração para reescala ===========\n')

    funcionarios_turno = funcDiurnos if turno == 1 else funcNoturnos
    nomes_turno = nomesDiurnos if turno == 1 else nomesNoturnos
    farm_turno = farmaceuticosDiurnos if turno == 1 else farmaceuticosNoturnos
    aux_turno = auxiliaresDiurnos if turno == 1 else auxiliaresNoturnos

    populacaoFinal, historico_individuos, historico_fitness, melhor_individuo_global = algoritmoGenetico( funcionarios_turno, qtdeIndividuos, numDiasMes, tipo, diaReescala, turno, qtd_blocos, geracoes, nomes_turno, farm_turno, aux_turno, qtd_pais)

    tempoTotal = time.time() - tempoInicio
    print(f'\nTempo Total: {tempoTotal:.2f} segundos ({tempoTotal / 60:.2f} minutos)')


    # =========================================================================
    # Visualização de resultados
    # =========================================================================
    print("\nSalvando resultados em planilhas...")

    # População Final
    salvar_excel( populacao=populacaoFinal, lista_nomes_cargos=nomes_turno, farmaceuticos=farm_turno, auxiliares=aux_turno, caminho_arquivo='1_populacao_final.xlsx', num_dias_mes=numDiasMes, salvar_completo=True, somatorio=True )

    # Salvar Histórico de Indivíduos - os melhores de cada geração
    historico_3d = np.stack(historico_individuos, axis=2)
    salvar_excel(populacao=historico_3d, lista_nomes_cargos=nomes_turno, farmaceuticos=farm_turno, auxiliares=aux_turno, caminho_arquivo='2_historico_melhores_geracao.xlsx', num_dias_mes=numDiasMes,salvar_completo=True, somatorio=True)

    # Melhor Indivíduo
    melhor_global_3d = np.expand_dims(melhor_individuo_global, axis=2)
    salvar_excel( populacao=melhor_global_3d, lista_nomes_cargos=nomes_turno, farmaceuticos=farm_turno, auxiliares=aux_turno, caminho_arquivo='3_melhor_escala_global.xlsx', num_dias_mes=numDiasMes, salvar_completo=False, somatorio=True)

    # Gráfico de Histórico de Fitness
    print("Gerando gráfico de evolução do fitness...")
    plt.figure(figsize=(10, 6))
    geracoes_eixo_x = range(1, len(historico_fitness) + 1)  # Eixo X = Gerações (1, 2, 3...), Eixo Y = Valores do Fitness
    plt.plot(geracoes_eixo_x, historico_fitness, marker='o', linestyle='-', color='#4472C4', linewidth=2)
    plt.title('Evolução do Fitness da Escala ao longo das Gerações', fontsize=14, fontweight='bold')
    plt.xlabel('Gerações', fontsize=12)
    plt.ylabel('Melhor Pontuação (Fitness)', fontsize=12)
    plt.ticklabel_format(style='plain', axis='y') # Formata o eixo Y para não mostrar notação científica
    plt.xticks(geracoes_eixo_x) # Garante que o eixo X mostre apenas números inteiros
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout() # Salva a imagem e mostra na tela
    plt.savefig('4_grafico_evolucao_fitness.png', dpi=300)
    plt.show()

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    funcaoPrincipal()  # Chama a função principal
