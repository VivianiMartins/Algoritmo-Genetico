import pandas as pd

# 1. Carregar o arquivo corrigido enviado por você
nome_arquivo = 'melhor_media_fitness.xlsx'
if nome_arquivo.endswith('.csv'):
    df = pd.read_csv(nome_arquivo, index_col=0)
else:
    df = pd.read_excel(nome_arquivo, index_col=0)

# 2. Limpar o índice para garantir que temos apenas números inteiros (ex: "Geração 1" -> 1)
df.index = df.index.str.extract(r'(\d+)')[0].astype(int)
df = df.sort_index()

# 3. Montar a estrutura do cabeçalho da longtable do seu TCC
latex_code = r"""\begin{longtable}{ccc|ccc|ccc}
    \caption{Evolução do Fitness do Algoritmo Genético ao longo de 1500 Gerações} \label{tab:evolucao_fitness} \\
    \hline
    \textbf{Gen.} & \textbf{Melhor} & \textbf{Média} & \textbf{Gen.} & \textbf{Melhor} & \textbf{Média} & \textbf{Gen.} & \textbf{Melhor} & \textbf{Média} \\ \hline
    \endfirsthead

    \multicolumn{9}{c}{{\tablename\ \thetable{} -- Continuação da página anterior}} \\ \hline
    \textbf{Gen.} & \textbf{Melhor} & \textbf{Média} & \textbf{Gen.} & \textbf{Melhor} & \textbf{Média} & \textbf{Gen.} & \textbf{Melhor} & \textbf{Média} \\ \hline
    \endhead

    \hline
    \endlastfoot
"""

# 4. Combinar os dados em 3 blocos paralelos (1-500, 501-1000, 1001-1500)
for i in range(1, 501):
    g1, g2, g3 = i, i + 500, i + 1000

    # Dados do Bloco 1 (Gerações 1 a 500)
    m1 = f"{df.loc[g1, 'Melhor']:.4f}"
    med1 = f"{df.loc[g1, 'Média']:.4f}"

    # Dados do Bloco 2 (Gerações 501 a 1000)
    m2 = f"{df.loc[g2, 'Melhor']:.4f}"
    med2 = f"{df.loc[g2, 'Média']:.4f}"

    # Dados do Bloco 3 (Gerações 1001 a 1500)
    m3 = f"{df.loc[g3, 'Melhor']:.4f}" if g3 in df.index else ""
    med3 = f"{df.loc[g3, 'Média']:.4f}" if g3 in df.index else ""

    # Adicionar a linha formatada ao código LaTeX
    latex_code += f"    {g1} & {m1} & {med1} & {g2} & {m2} & {med2} & {g3} & {m3} & {med3} \\\\\n"

# Fechamento da tabela
latex_code += r"\end{longtable}"

# 5. Salvar o código em um arquivo .tex estruturado
with open('tabela_fitness_corrigida.tex', 'w', encoding='utf-8') as f:
    f.write(latex_code)

print("Finalizado! O arquivo 'tabela_fitness_corrigida.tex' foi gerado perfeitamente com as médias corrigidas.")