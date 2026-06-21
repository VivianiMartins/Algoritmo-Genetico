import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def recriarGrafico(caminho_arquivo, salvar=False):
    """
    Lê o arquivo de histórico salvo e recria o gráfico de dispersão e evolução.

    Parâmetros:
    - caminho_arquivo (str): Caminho para o arquivo .xlsx ou .csv
    - salvar (bool): Se True, salva o gráfico como imagem .png
    """
    print(f">> Lendo dados de: {caminho_arquivo}")

    if caminho_arquivo.endswith('.csv'):
        df = pd.read_csv(caminho_arquivo, index_col=0)
    else:
        df = pd.read_excel(caminho_arquivo, index_col=0)

    geracoes_eixo_x = list(range(1, len(df) + 1))

    melhores_por_geracao = df.max(axis=1).values
    medias_geracao = df.mean(axis=1).values

    nota_campea = np.max(melhores_por_geracao)
    geracao_campea = np.argmax(melhores_por_geracao) + 1  # +1 porque o índice começa em 0

    # =========================================================================
    # Construção do Gráfico
    # =========================================================================
    plt.figure(figsize=(14, 7))

    # 1. Plota a dispersão de todos os indivíduos (bolinhas cinzas)
    for i, geracao_x in enumerate(geracoes_eixo_x):
        notas_geracao = df.iloc[i].values
        x_vals = [geracao_x] * len(notas_geracao)
        plt.scatter(x_vals, notas_geracao, color='gray', alpha=0.5, edgecolor='black', s=25, zorder=2)

    # 2. Plota a Média da População
    plt.plot(geracoes_eixo_x, medias_geracao, color='red', linestyle='--', linewidth=2, label='Média da População',
             zorder=3)

    # 3. Plota o Melhor da Geração
    plt.plot(geracoes_eixo_x, melhores_por_geracao, color='#4472C4', marker='o', markersize=4, linestyle='-',
             linewidth=2, label='Melhor da Geração', zorder=4)

    # 4. Destaque para o Melhor Global (Estrela Dourada)
    #plt.scatter(geracao_campea, nota_campea, color='gold', edgecolor='black', marker='*', s=350, zorder=10, label=f'Melhor Global (Gen {geracao_campea}: {nota_campea:.2f})')

    # Configurações visuais do gráfico
    #plt.title('Distribuição e Evolução do Fitness', fontsize=14, fontweight='bold')
    #plt.xlabel('Gerações', fontsize=12)
    #plt.ylabel('Pontuação (Fitness)', fontsize=12)
    #plt.title('Distribuição e Evolução do Fitness', fontsize=12, fontweight='bold')
    plt.title('Distribuição e Evolução das penalizações', fontsize=12, fontweight='bold')
    plt.xlabel('Gerações', fontsize=10)
    #plt.ylabel('Pontuação (Fitness)', fontsize=10)
    plt.ylabel('Penalizações', fontsize=10)

    plt.legend(loc='lower right', framealpha=0.9)
    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=20))

    y_min, y_max = plt.ylim()
    plt.ylim(y_min - (y_max - y_min) * 0.05, y_max + (y_max - y_min) * 0.1)

    plt.grid(True, linestyle='--', alpha=0.5, zorder=1)
    plt.tight_layout()

    if salvar:
        nome_imagem = caminho_arquivo.split('.')[0] + '_grafico_recriado.pdf'
        #nome_imagem = caminho_arquivo.split('.')[0] + '_grafico_recriado.png'
        plt.savefig(nome_imagem, dpi=300)
        print(f">> Gráfico salvo com sucesso como: {nome_imagem}")

    plt.show()



if __name__ == "__main__":
    import argparse

    # Cria o interpretador de comandos do terminal
    parser = argparse.ArgumentParser(description="Recria gráficos a partir de planilhas do Algoritmo Genético.")

    # Argumento obrigatório: o caminho do arquivo
    parser.add_argument("arquivo", type=str, help="Caminho para o arquivo CSV ou Excel")

    # Argumento opcional: a flag para salvar a imagem
    parser.add_argument("--salvar", action="store_true", help="Use essa flag se quiser salvar o gráfico em PNG")

    args = parser.parse_args()

    # Chama a função passando o que você digitou no terminal
    recriarGrafico(args.arquivo, salvar=args.salvar)