import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plotarMultiplosTestes(caminho_arquivo, salvar=False):
    """
    Lê o arquivo de histórico salvo e plota a evolução de múltiplos testes.

    Parâmetros:
    - caminho_arquivo (str): Caminho para o arquivo .xlsx ou .csv
    - salvar (bool): Se True, salva o gráfico como imagem .pdf
    """
    print(f">> Lendo dados de: {caminho_arquivo}")

    # Leitura do arquivo
    if caminho_arquivo.endswith('.csv'):
        df = pd.read_csv(caminho_arquivo)
    else:
        df = pd.read_excel(caminho_arquivo)

    # O eixo X será uma lista de 1 até o número total de linhas (gerações)
    geracoes_eixo_x = list(range(1, len(df) + 1))

    # Identificamos as colunas dos testes (ignorando a primeira coluna 'Geração/Indivíduo')
    colunas_testes = df.columns[1:]

    # Definimos uma paleta de cores para os testes (você pode alterar como preferir)
    cores = ['#4472C4', '#ED7D31', '#70AD47', '#FFC000', '#A5A5A5', '#8E44AD', '#E74C3C', '#34495E']

    # =========================================================================
    # Construção do Gráfico
    # =========================================================================
    plt.figure(figsize=(14, 7))

    # Plota uma linha para cada teste encontrado no cabeçalho
    for i, nome_teste in enumerate(colunas_testes):
        valores_teste = df[nome_teste].values
        cor_atual = cores[i % len(cores)]  # Garante que não falte cor se houver mais testes

        plt.plot(geracoes_eixo_x, valores_teste, color=cor_atual, linestyle='-', linewidth=2,
                 label=nome_teste, zorder=4)

    # Configurações visuais do gráfico
    plt.xlabel('Gerações', fontsize=22)
    # plt.ylabel('Penalizações', fontsize=22)
    plt.ylabel('Pontuação (Fitness)', fontsize=22)  # Modifique conforme sua necessidade

    # Ajustes de Eixos e Tick labels
    plt.tick_params(axis='both', which='major', labelsize=22)

    # Legenda configurada para se adaptar bem à figura
    #plt.legend(loc='upper left', framealpha=0.8, fontsize=20)
    plt.legend(loc='lower right', framealpha=0.8, fontsize=22)

    plt.ticklabel_format(style='plain', axis='y')
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(150))
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=10))

    # Margens superior e inferior dinâmicas para o gráfico respirar
    y_min, y_max = plt.ylim()
    plt.ylim(y_min - (y_max - y_min) * 0.05, y_max + (y_max - y_min) * 0.1)

    plt.grid(True, linestyle='--', alpha=0.5, zorder=1)
    plt.tight_layout()

    # Salva o arquivo caso a flag seja verdadeira
    if salvar:
        nome_imagem = caminho_arquivo.split('.')[0] + '_comparacao_testes.pdf'
        plt.savefig(nome_imagem, dpi=300)
        print(f">> Gráfico salvo com sucesso como: {nome_imagem}")

    plt.show()


if __name__ == "__main__":
    import argparse

    # Cria o interpretador de comandos do terminal
    parser = argparse.ArgumentParser(
        description="Plota a evolução de múltiplos testes a partir de planilhas do Algoritmo Genético.")

    # Argumento obrigatório: o caminho do arquivo
    parser.add_argument("arquivo", type=str, help="Caminho para o arquivo CSV ou Excel")

    # Argumento opcional: a flag para salvar a imagem
    parser.add_argument("--salvar", action="store_true", help="Use essa flag se quiser salvar o gráfico em PDF")

    args = parser.parse_args()

    # Chama a função
    plotarMultiplosTestes(args.arquivo, salvar=args.salvar)