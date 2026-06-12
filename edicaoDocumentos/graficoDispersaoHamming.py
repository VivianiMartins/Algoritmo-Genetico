import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

def graficoDispersaoHamming(historico_hamming, qtde_individuos, historico_alteracoes):
    """
    Gera e salva o gráfico de dispersão da Distância de Hamming de toda a população
    ao longo das gerações, destacando a média.
    """
    print("Salvando histórico completo de Hamming...")
    df_fitness = pd.DataFrame(historico_hamming)
    df_fitness.index = [f"Geração {i + 1}" for i in range(len(historico_hamming))]
    df_fitness.columns = [f"Indivíduo {i}" for i in range(qtde_individuos)]
    df_fitness.to_excel('7_historico_todos_hamming.xlsx', index_label="Geração/Indivíduo")


    print("Gerando gráfico de dispersão do histórico de Hamming...")
    # Configuração inicial do gráfico
    plt.figure(figsize=(14, 7))
    geracoes_eixo_x = list(range(1, len(historico_hamming) + 1))
    medias_geracao = []

    # Plota os pontos de cada indivíduo por geração
    for i, geracao_x in enumerate(geracoes_eixo_x):
        valores_hamming = historico_hamming[i]
        medias_geracao.append(np.mean(valores_hamming))

        # Cria uma lista com o número da geração repetido para alinhar no eixo X
        x_vals = [geracao_x] * len(valores_hamming)

        # Plota a dispersão dos indivíduos da geração atual
        plt.scatter(x_vals, valores_hamming, color='gray', alpha=0.5, edgecolor='black', s=25, zorder=2)

    # Plota a linha da média da população ao longo das gerações
    plt.plot(geracoes_eixo_x, medias_geracao, color='red', linestyle='--', linewidth=2,
             label='Média de Hamming da População', zorder=3)

    # Customização de títulos e eixos
    plt.title('Distribuição da Distância de Hamming por Geração', fontsize=14, fontweight='bold')
    plt.xlabel('Gerações', fontsize=12)
    plt.ylabel('Distância de Hamming', fontsize=12)
    plt.legend(loc='upper right', framealpha=0.9)

    # Ajustes de formatação dos eixos
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=20))

    # Margem dinâmica nos limites do eixo Y
    y_min, y_max = plt.ylim()
    plt.ylim(y_min - (y_max - y_min) * 0.05, y_max + (y_max - y_min) * 0.1)

    # Grade de fundo e salvamento
    plt.grid(True, linestyle='--', alpha=0.5, zorder=1)
    plt.tight_layout()

    # Salva o arquivo com um nome descritivo diferente do original
    plt.savefig('8_grafico_dispersao_hamming.png', dpi=300)
    plt.show()

    print("Salvando histórico completo de alterações...")
    df_fitness = pd.DataFrame(historico_alteracoes)
    df_fitness.index = [f"Geração {i + 1}" for i in range(len(historico_alteracoes))]
    df_fitness.columns = [f"Indivíduo {i}" for i in range(qtde_individuos)]
    df_fitness.to_excel('9_historico_todas_alteracoes.xlsx', index_label="Geração/Indivíduo")

    print("Gerando gráfico de dispersão do histórico das alterações...")
    # Configuração inicial do gráfico
    plt.figure(figsize=(14, 7))
    geracoes_eixo_x = list(range(1, len(historico_alteracoes) + 1))
    medias_geracao = []

    # Plota os pontos de cada indivíduo por geração
    for i, geracao_x in enumerate(geracoes_eixo_x):
        valores_alteracoes = historico_alteracoes[i]
        medias_geracao.append(np.mean(valores_alteracoes))

        # Cria uma lista com o número da geração repetido para alinhar no eixo X
        x_vals = [geracao_x] * len(valores_alteracoes)

        # Plota a dispersão dos indivíduos da geração atual
        plt.scatter(x_vals, valores_alteracoes, color='gray', alpha=0.5, edgecolor='black', s=25, zorder=2)

    # Plota a linha da média da população ao longo das gerações
    plt.plot(geracoes_eixo_x, medias_geracao, color='red', linestyle='--', linewidth=2,
             label='Média de Hamming da População', zorder=3)

    # Customização de títulos e eixos
    plt.title('Distribuição das alterações por Geração', fontsize=14, fontweight='bold')
    plt.xlabel('Gerações', fontsize=12)
    plt.ylabel('Alterações', fontsize=12)
    plt.legend(loc='upper right', framealpha=0.9)

    # Ajustes de formatação dos eixos
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=20))

    # Margem dinâmica nos limites do eixo Y
    y_min, y_max = plt.ylim()
    plt.ylim(y_min - (y_max - y_min) * 0.05, y_max + (y_max - y_min) * 0.1)

    # Grade de fundo e salvamento
    plt.grid(True, linestyle='--', alpha=0.5, zorder=1)
    plt.tight_layout()

    # Salva o arquivo com um nome descritivo diferente do original
    plt.savefig('10_grafico_dispersao_alterações.png', dpi=300)
    plt.show()