import pandas as pd

# 1. Carregar o arquivo corrigido enviado por você
nome_arquivo = 'alteracoes_penalizacoes_medias.xlsx'
if nome_arquivo.endswith('.csv'):
    df = pd.read_csv(nome_arquivo, index_col=0)
else:
    df = pd.read_excel(nome_arquivo, index_col=0)

# 2. Limpar o índice para garantir que temos apenas números inteiros (ex: "Geração 1" -> 1)
df.index = df.index.str.extract(r'(\d+)')[0].astype(int)
df = df.sort_index()

# 3. Montar a estrutura do cabeçalho da longtable do seu TCC
latex_code = r"""\begin{longtable}{c|cc|cc|c|cc|cc}
    \caption{Evolução das penalizações e alterações durante as gerações} \label{tab:evolucao_penalizacoes} \\
    \hline
    \textbf{ } & \multicolumn{2}{c|}{\textbf{Penalizações}} & \multicolumn{2}{c|}{\textbf{Alterações}} &
    \textbf{ } & \multicolumn{2}{c|}{\textbf{Penalizações}} & \multicolumn{2}{c}{\textbf{Alterações}} \\ \hline
    
    \textbf{Gen.} & \textbf{Melhor} & \textbf{Média} & \textbf{Melhor} & \textbf{Média} & 
    \textbf{Gen.} & \textbf{Melhor} & \textbf{Média} & \textbf{Melhor} & \textbf{Média} \\ \hline
    \endfirsthead
    
    \multicolumn{10}{c}{{\tablename\ \thetable{} -- Continuação da página anterior}} \\ \hline
    \textbf{ } & \multicolumn{2}{c|}{\textbf{Penalizações}} & \multicolumn{2}{c|}{\textbf{Alterações}} &
    \textbf{ } & \multicolumn{2}{c|}{\textbf{Penalizações}} & \multicolumn{2}{c}{\textbf{Alterações}} \\ \hline
    
    \textbf{Gen.} & \textbf{Melhor} & \textbf{Média} & \textbf{Melhor} & \textbf{Média} & 
    \textbf{Gen.} & \textbf{Melhor} & \textbf{Média} & \textbf{Melhor} & \textbf{Média} \\ \hline
    \endhead
    
    \hline
    \endlastfoot
"""

# 4. Combinar os dados em 2 blocos paralelos
for i in range(1, 751):
    g1, g2 = i, i + 750

    # Dados do Bloco 1 (Gerações 1 a 750)
    m1 = f"{df.loc[g1, 'Melhor']:.4f}"
    med1 = f"{df.loc[g1, 'Média']:.4f}"
    m1A = f"{df.loc[g1, 'MelhorA']:.0f}"
    med1A = f"{df.loc[g1, 'MédiaA']:.2f}"

    # Dados do Bloco 2 (Gerações 751 a 1500)
    m2 = f"{df.loc[g2, 'Melhor']:.4f}"
    med2 = f"{df.loc[g2, 'Média']:.4f}"
    m2A = f"{df.loc[g2, 'MelhorA']:.0f}"
    med2A = f"{df.loc[g2, 'MédiaA']:.2f}"

    # Adicionar a linha formatada ao código LaTeX
    latex_code += f"    {g1} & {m1} & {med1} & {m1A} & {med1A} & {g2} & {m2} & {med2} & {m2A} & {med2A} \\\\\n"

# Fechamento da tabela
latex_code += r"\end{longtable}"

# 5. Salvar o código em um arquivo .tex estruturado
with open('tabela_penalizacoes.tex', 'w', encoding='utf-8') as f:
    f.write(latex_code)

print("Finalizado! O arquivo 'tabela_penalizacoes.tex' foi gerado perfeitamente com as médias corrigidas.")