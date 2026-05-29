import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from algoritmoGenetico import algoritmoGenetico
from transformarListaEntrada import transformarListaEntrada
from salvarExcel import salvar_excel

def funcaoPrincipal():
    tempoInicio = time.time()  # Inicia o cronômetro para medir o tempo total de execução

    listaFuncionarios_df = pd.read_csv('listaFuncionarios.csv')
    listaFuncionarios = listaFuncionarios_df.values.tolist()

    funcDiurnos, funcNoturnos, numDiasMesAnterior, nomesDiurnos, nomesNoturnos, farmaceuticosDiurnos, farmaceuticosNoturnos, auxiliaresDiurnos, auxiliaresNoturnos = transformarListaEntrada( listaFuncionarios)

    # =========================================================================
    # Algoritmo genético
    # =========================================================================
    tipo = 1 #1 para escala ou 2 para reescala
    turno = 1 #1 para diurno ou 2 para noturno
    num_dias_mes = 30 #total de dias do mês

    dia_reescala_inicio = 0 #dia em que começa a reescala
    dia_reescala_fim = 0  # dia em que termina a reescala

    qtde_individuos = 30
    geracoes = 50

    penalidade_fitness = True #False para não aplicar penalidade e True para aplicar penalidade
    elitismo = True  # False para não manter o melhor indivíduo na próxima geração e True manter o melhor na próxima geração

    selecao = 1 #1 para roleta; 2 para elitismo; 3 para torneio; 4 para Maximax e Maximin
    qtd_pais = 2
    tamanho_grupos_torneios = 5

    cruzamento = 1 #1 para cruzamento com bloco
    qtd_blocos = 10

    mutacao = 1  # 1 mutação por sorteio da linha
    taxa_mutacao = 0.1 #probabilidade do indivíduo ser mutato


    if tipo not in [1, 2]:
        raise ValueError("Deve ser 1 para escala ou 2 para reescala")
    elif tipo == 1:
        print('=========== Geração para escala ===========\n')
    else:
        print('=========== Geração para reescala ===========\n')

    if tamanho_grupos_torneios <= 1: tamanho_grupos_torneios = 2 #caso inserir menor que 1

    funcionarios_turno = funcDiurnos if turno == 1 else funcNoturnos
    nomes_turno = nomesDiurnos if turno == 1 else nomesNoturnos
    farm_turno = farmaceuticosDiurnos if turno == 1 else farmaceuticosNoturnos
    aux_turno = auxiliaresDiurnos if turno == 1 else auxiliaresNoturnos

    (populacaoFinal, historico_individuos, historico_fitness, melhor_individuo_global, hist_sel_fit, hist_sel_idx, hist_melhor_idx, geracao_campea, id_campeao,
     historico_fitness_todos) = algoritmoGenetico( funcionarios_turno, nomes_turno, farm_turno, aux_turno, turno,
                                                   tipo, num_dias_mes, dia_reescala_inicio, dia_reescala_fim,
                                                   qtde_individuos, geracoes,
                                                   penalidade_fitness, elitismo, selecao, qtd_pais, tamanho_grupos_torneios, cruzamento, qtd_blocos, mutacao, taxa_mutacao)

    tempoTotal = time.time() - tempoInicio
    print(f'\nTempo Total: {tempoTotal:.2f} segundos ({tempoTotal / 60:.2f} minutos)')

    print(f"\n\n A Melhor Escala Global foi encontrada na Geração {geracao_campea} (ID do indivíduo: {id_campeao})!")

    # =========================================================================
    # Visualização de resultados
    # =========================================================================
    # População Final
    salvar_excel( populacao=populacaoFinal, lista_nomes_cargos=nomes_turno, farmaceuticos=farm_turno, auxiliares=aux_turno, caminho_arquivo='1_populacao_final.xlsx', num_dias_mes=num_dias_mes, salvar_completo=True, somatorio=True )

    # Salvar Histórico de Indivíduos - os melhores de cada geração
    historico_3d = np.stack(historico_individuos, axis=2)
    salvar_excel(populacao=historico_3d, lista_nomes_cargos=nomes_turno, farmaceuticos=farm_turno, auxiliares=aux_turno, caminho_arquivo='2_historico_melhores_geracao.xlsx', num_dias_mes=num_dias_mes,salvar_completo=True, somatorio=True)

    # Melhor Indivíduo
    melhor_global_3d = np.expand_dims(melhor_individuo_global, axis=2)
    salvar_excel( populacao=melhor_global_3d, lista_nomes_cargos=nomes_turno, farmaceuticos=farm_turno, auxiliares=aux_turno, caminho_arquivo='3_melhor_escala_global.xlsx', num_dias_mes=num_dias_mes, salvar_completo=False, somatorio=True)

    # Gráfico de Histórico de Fitness
    print("Gerando gráfico de evolução do fitness...")
    plt.figure(figsize=(14, 7))  # Aumentei um pouco a largura
    geracoes_eixo_x = list(range(1, len(historico_fitness) + 1))

    # Plota a linha do MELHOR indivíduo
    plt.plot(geracoes_eixo_x, historico_fitness, marker='o', markersize=5, linestyle='-', color='#4472C4',
             linewidth=2, label='Melhor da Geração')

    # Define um "salto" para não poluir os textos se houver muitas gerações
    total_gens = len(geracoes_eixo_x)
    salto_textos = max(1, total_gens // 25)  # Vai mostrar no máximo uns 25 textos no gráfico

    for i, geracao_x in enumerate(geracoes_eixo_x):
        nota_melhor = historico_fitness[i]
        id_melhor = hist_melhor_idx[i]

        # Só escreve o ID se for o momento do 'salto' ou se for a última geração
        if i % salto_textos == 0 or i == total_gens - 1:
            plt.annotate(f'id:{id_melhor}', (geracao_x, nota_melhor), textcoords="offset points", xytext=(0, 10),
                         ha='center', va='bottom', fontsize=9, color='darkblue', weight='bold')

    for i, geracao_x in enumerate(geracoes_eixo_x):
        notas_selecionados = hist_sel_fit[i]
        indices_selecionados = hist_sel_idx[i]

        for j in range(len(notas_selecionados)):
            nota = notas_selecionados[j]
            indice = indices_selecionados[j]

            # Adiciona o ponto (com alpha=0.6 para dar transparência se houver sobreposição)
            plt.scatter(geracao_x, nota, color='red', zorder=5, alpha=0.6, s=30)

            if i % salto_textos == 0 or i == total_gens - 1:
                plt.annotate(f'id:{indice}', (geracao_x, nota), textcoords="offset points", xytext=(6, 0),
                             ha='left', va='center', fontsize=8, color='darkred')

    # Destaque para o melhor Global (Usa as variáveis geracao_campea e id_campeao)
    nota_campea = historico_fitness[geracao_campea - 1]
    plt.scatter(geracao_campea, nota_campea, color='gold', edgecolor='black', marker='*', s=350, zorder=10,
                label=f'Melhor Global (Gen {geracao_campea})')

    plt.scatter([], [], color='red', label='Indivíduos Selecionados')
    plt.legend(loc='lower right', framealpha=0.9)
    plt.title(f'Evolução do Fitness ao longo de {total_gens} Gerações', fontsize=14, fontweight='bold')
    plt.xlabel('Gerações', fontsize=12)
    plt.ylabel('Pontuação (Fitness)', fontsize=12)

    plt.ticklabel_format(style='plain', axis='y')

    # Faz o eixo X pular números de forma inteligente (ex: 10, 20, 30) em vez de todos de 1 a 100
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=20))

    y_min, y_max = plt.ylim()
    plt.ylim(y_min, y_max + (y_max - y_min) * 0.15)  # Aumentou a folga no topo para caber a estrela e textos

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('4_grafico_evolucao_fitness.png', dpi=300)
    plt.show()

    # ---------------------------------------------------------
    # Historico total da fitness
    # ---------------------------------------------------------
    print("Salvando histórico completo de fitness...")
    df_fitness = pd.DataFrame(historico_fitness_todos)
    df_fitness.index = [f"Geração {i + 1}" for i in range(len(historico_fitness_todos))]
    df_fitness.columns = [f"Indivíduo {i}" for i in range(qtde_individuos)]
    df_fitness.to_excel('5_historico_todos_fitness.xlsx', index_label="Geração/Indivíduo")

    print("Gerando gráfico de dispersão de toda a população...")
    plt.figure(figsize=(14, 7))
    geracoes_eixo_x = list(range(1, len(historico_fitness_todos) + 1))
    medias_geracao = []

    for i, geracao_x in enumerate(geracoes_eixo_x):
        notas_geracao = historico_fitness_todos[i]
        medias_geracao.append(np.mean(notas_geracao))
        x_vals = [geracao_x] * len(notas_geracao)
        plt.scatter(x_vals, notas_geracao, color='gray', alpha=0.5, edgecolor='black', s=25, zorder=2)

    plt.plot(geracoes_eixo_x, medias_geracao, color='red', linestyle='--', linewidth=2, label='Média da População', zorder=3)
    plt.plot(geracoes_eixo_x, historico_fitness, color='#4472C4', marker='o', markersize=4, linestyle='-', linewidth=2, label='Melhor da Geração', zorder=4)
    plt.title('Distribuição do Fitness de Todos os Indivíduos por Geração', fontsize=14, fontweight='bold')
    plt.xlabel('Gerações', fontsize=12)
    plt.ylabel('Pontuação (Fitness)', fontsize=12)
    plt.legend(loc='lower right', framealpha=0.9)
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=20))
    y_min, y_max = plt.ylim()
    plt.ylim(y_min - (y_max - y_min) * 0.05, y_max + (y_max - y_min) * 0.1)
    plt.grid(True, linestyle='--', alpha=0.5, zorder=1)
    plt.tight_layout()
    plt.savefig('6_grafico_dispersao_populacao.png', dpi=300)
    plt.show()

if __name__ == "__main__":  # Verifica se o script está sendo executado diretamente
    funcaoPrincipal()  # Chama a função principal
