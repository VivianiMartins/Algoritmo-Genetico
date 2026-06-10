import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .salvarExcel import salvarExcel

def resultadosTeste(populacao_final, historico_individuos, historico_fitness, melhor_individuo_global,
                    hist_sel_fit, hist_sel_idx, hist_melhor_idx, geracao_campea, id_campeao,
                    historico_fitness_todos, nomes_turno, farm_turno, aux_turno, num_dias_mes, qtde_individuos):
    """
    Gera e salva todos os resultados dos testes:
    - Planilhas Excel com populações e históricos
    - Gráficos de evolução e dispersão de fitness
    """
    # =========================================================================
    # Visualização de resultados
    # =========================================================================
    # População Final
    salvarExcel(populacao=populacao_final, lista_nomes_cargos=nomes_turno, farmaceuticos=farm_turno, auxiliares=aux_turno, caminho_arquivo='1_populacao_final.xlsx', num_dias_mes=num_dias_mes, salvar_completo=True, somatorio=True)

    # Salvar Histórico de Indivíduos - os melhores de cada geração
    historico_3d = np.stack(historico_individuos, axis=2)
    salvarExcel(populacao=historico_3d, lista_nomes_cargos=nomes_turno, farmaceuticos=farm_turno, auxiliares=aux_turno, caminho_arquivo='2_historico_melhores_individuos_geracao.xlsx', num_dias_mes=num_dias_mes, salvar_completo=True, somatorio=True)

    # Melhor Indivíduo
    melhor_global_3d = np.expand_dims(melhor_individuo_global, axis=2)
    salvarExcel(populacao=melhor_global_3d, lista_nomes_cargos=nomes_turno, farmaceuticos=farm_turno, auxiliares=aux_turno, caminho_arquivo='3_melhor_escala.xlsx', num_dias_mes=num_dias_mes, salvar_completo=False, somatorio=False)

    # ---------------------------------------------------------
    # Historico selecionados
    # ---------------------------------------------------------
    print("Gerando gráfico de individuos selecionadoss...")
    plt.figure(figsize=(14, 7))
    geracoes_eixo_x = list(range(1, len(historico_fitness) + 1))

    # Plota a linha do MELHOR indivíduo
    plt.plot(geracoes_eixo_x, historico_fitness, marker='o', markersize=5, linestyle='-', color='#4472C4',
             linewidth=2, label='Melhor da Geração')

    # Define um "salto" para não poluir os textos se houver muitas gerações
    total_gens = len(geracoes_eixo_x)
    salto_textos = max(1, total_gens // 25)

    for i, geracao_x in enumerate(geracoes_eixo_x):
        nota_melhor = historico_fitness[i]
        id_melhor = hist_melhor_idx[i]

        if i % salto_textos == 0 or i == total_gens - 1:
            plt.annotate(f'id:{id_melhor}', (geracao_x, nota_melhor), textcoords="offset points", xytext=(0, 10),
                         ha='center', va='bottom', fontsize=10, color='darkblue', weight='bold')

    for i, geracao_x in enumerate(geracoes_eixo_x):
        notas_selecionados = hist_sel_fit[i]
        indices_selecionados = hist_sel_idx[i]

        for j in range(len(notas_selecionados)):
            nota = notas_selecionados[j]
            indice = indices_selecionados[j]

            plt.scatter(geracao_x, nota, color='red', zorder=5, alpha=0.6, s=5)

            #if i % salto_textos == 0 or i == total_gens - 1:
             #   plt.annotate(f'id:{indice}', (geracao_x, nota), textcoords="offset points", xytext=(6, 0), ha='left', va='center', fontsize=8, color='darkred')

    # Destaque para o melhor Global
    nota_campea = historico_fitness[geracao_campea - 1]
    plt.scatter(geracao_campea, nota_campea, color='gold', edgecolor='black', marker='*', s=200, zorder=10,
                label=f'Melhor Global (Gen {geracao_campea})')

    plt.scatter([], [], color='red', label='Indivíduos Selecionados')
    plt.legend(loc='lower right', framealpha=0.9)
    plt.title(f'Indivíduos selecionados ao longo de {total_gens} Gerações', fontsize=14, fontweight='bold')
    plt.xlabel('Gerações', fontsize=12)
    plt.ylabel('Pontuação (Fitness)', fontsize=12)

    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=20))

    y_min, y_max = plt.ylim()
    plt.ylim(y_min, y_max + (y_max - y_min) * 0.15)

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('4_grafico_individuos_selecionados.png', dpi=300)
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