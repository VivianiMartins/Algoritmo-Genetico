## Sobre o Projeto

Este repositório contém a implementação do trabalho de conclusão de curso (TCC) em **Ciência da Computação** apresentado ao **Instituto Federal de Goiás — Câmpus Anápolis**.

**Título:** *Reescala em Saúde: Aplicação de Algoritmos Genéticos para Substituição de Falta Conforme Legislação Trabalhista*

**Objetivo:** Desenvolver um sistema baseado em algoritmos genéticos para gerar e reajustar escalas de trabalho de funcionários em estabelecimentos de saúde (farmácias), considerando:
- Dois turnos de trabalho: Diurno e Noturno.
- Dois cargos: Farmacêutico e Auxiliar.
- Licenças e férias dentro da legislação trabalhista.
- Regras de alternância e distribuição equitativa.

O projeto oferece duas funcionalidades principais:
1. **Geração de Escala:** criar uma nova escala do zero para um turno específico.
2. **Reescala:** substituir um funcionário em um dia específico e re-otimizar a escala para os dias restantes.

---
Requisitos
----------
- Python 3.8+ (testado com 3.10+; adapte se necessário)
- Bibliotecas Python:
  - numpy
  - pandas
  - matplotlib
  - openpyxl

Instalação rápida
-----------------
Recomenda-se usar um virtualenv:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install numpy pandas matplotlib openpyxl
````
---
Como executar
-----------------
O ponto de entrada principal é funcaoPrincipal.py. Execute:
```bash
python funcaoPrincipal.py
````
Antes de rodar, ajuste os parâmetros diretamente em funcaoPrincipal.py, descritos abaixo.

Parâmetros principais (funcaoPrincipal.py)
-----------------
No início da função funcaoPrincipal() estão os parâmetros mais importantes. Exemplo:
```bash
# tipo: 1 = escala, 2 = reescala
tipo = 2

# turno: 1 = diurno, 2 = noturno
turno = 1

# Parâmetros do algoritmo genético
qtde_individuos = 50
geracoes = 1500

# False para não manter o melhor indivíduo na próxima geração e True manter o melhor na próxima geração
elitismo = True

# Seleção: 1 para roleta; 2 para elitismo; 3 para torneio; 4 para Maximax e Maximin
selecao = 2
qtd_pais = 2
tamanho_grupos_torneios = 0 #tamanho dos grupos para seleção por torneio (deve ser menor que a quantidade de indivíduos)

# Cruzamento: 1 por blocos (cortes horizontais); 2 xadrez(cortes verticais e horizontais); 3 percentagem de herança e ordem sorteadas (cortes verticais)
cruzamento = 1
qtd_blocos = 45 #quantidade de blocos para o cruzamento por blocos (deve ser menor ou igual a quantidade de indivíduos)

# Mutação: 1 para bit flip em bloco sorteado a partir de uma linha; 2 para bit flip em apenas um gene
mutacao = 2
probabilidade_mutacao = 0.2  #probabilidade do indivíduo ser mutado
````

Parâmetros específicos:
- Para tipo == 1 (escala):
  - num_dias_mes: total de dias do mês (ex.: 30)
- Para tipo == 2 (reescala):
  - dia_reescala: dia que precisa ser reescalado (ex.: 12)
  - funcionario: nome exato do funcionário que será substituído (ex.: 'Enzo Ramos')

Modifique esses valores no arquivo funcaoPrincipal.py antes de executar.

---
Modos: Escala vs Reescala
-----------------
- Escala (tipo = 1):
    - Gera uma nova escala a partir do zero para um turno (diurno ou noturno).
    - Entrada: algoritmoGeneticoEscala/listaFuncionarios.csv
    - Saídas: populações e melhor escala em arquivos Excel e gráficos.
    
- Reescala (tipo = 2):
  - Ajusta uma escala já existente (normalmente a melhor escala encontrada) para substituir um funcionário num dia específico e re-otimizar os dias restantes.
  - Entrada principal: algoritmoGeneticoReescala/melhor_escala_ag.xlsx (geralmente saída do modo escala)
  - Parâmetros: dia_reescala, funcionario.
  - Saídas adicionais: históricos de Hamming e alterações, gráficos que mostram mudanças.

---
Formato das entradas
-----------------
1 - CSV para geração de escala
- Caminho padrão: algoritmoGeneticoEscala/listaFuncionarios.csv
- Cabeçalho esperado (colunas): Nome,Cargo,Turno,início,Fim,1,2,3,...,N
- Descrição das colunas:
  - Nome: nome completo do funcionário (string).
  - Cargo: "Farmacêutico" ou "Auxiliar" (texto; case-insensitive).
  - Turno: "Diurno" ou "Noturno" (texto; case-insensitive).
  - início: dia inicial de licença/ferias (inteiro; 0 se não houver).
  - Fim: dia final de licença/ferias (inteiro; 0 se não houver).
  - 1..N: colunas correspondentes aos dias (podem ser usadas para marcar histórico/flags); o parser usa a estrutura para calcular num_dias_mes.

- Exemplo mínimo de linha: Ana Clara,Farmacêutico,Diurno,0,0,0,0,0,0,...,0.

Observações:
- transformarEntradaDoisTurnos converte o CSV lido por pandas.read_csv em matrizes separadas para diurno e noturno e retorna contagens de farmacêuticos/auxiliares, nomes e outras informações.
- Mantenha a ordem das colunas conforme o cabeçalho.

2 - XLSX para reescala
- Caminho padrão: algoritmoGeneticoReescala/melhor_escala_ag.xlsx
- Normalmente esse arquivo é a saída gerada por salvarExcel (o funcaoPrincipal.py já salva a melhor escala).
- Estrutura esperada:
  - Colunas: Funcionário, Cargo, Início licença, Fim licença, Último dia do mês anterior, Dia 1, Dia 2, ...
- Observação: transformarEntradaReescala separa farmacêuticos e auxiliares assumindo que há uma divisão entre eles (procura pela primeira linha cujo Cargo == "Auxiliar" para dividir); portanto mantenha a ordem (farmacêuticos antes de auxiliares) ou adapte a planilha para essa convenção.

---
Principais arquivos e localização
-----------------
- funcaoPrincipal.py — script de entrada; define parâmetros e orquestra execução.
- algoritmoGeneticoEscala/ — implementação para geração de escalas:
  - algoritmoGeneticoEscala.py, geraPopulacaoInicial.py, listaFuncionarios.csv
  - Subpastas: cruzamento/, mutacao/, avaliacoesEvalidacoes/
- algoritmoGeneticoReescala/ — implementação para reescala:
  - algoritmoGeneticoReescala.py, melhor_escala_ag.xlsx, geraPopulacaoInicialReescala.py, extrairCorteReescalar.py
  - Subpastas equivalentes às do modo escala.
- edicaoDocumentos/ — utilitários:
  - encontrarFuncionario.py, transformarEntradaDoisTurnos.py, transformarEntradaReescala.py, salvarExcel.py, resultadosTeste.py, graficoDispersaoHamming.py, plotarMultiplosTestes.py, recriarGrafico.py
- selecao/ — implementações de métodos de seleção (roleta, torneio, elitista, etc).
- avaliacoesEvalidacoes/ - impletações para ambos cenários
- Testes/ - pasta contendo teste para TCC
- Trabalho_de_Conclusão_de_Curso___Viviani_Martins_dos_Santos.pdf - texto resultante da impletmentação e pesquisa.
---
Saídas geradas
----------
- Arquivos Excel: 
  - 0_populacao_inicial.xlsx — população final (primeira população gerada).
  - 1_populacao_final.xlsx — população final (última população gerada).
  - 2_historico_melhores_individuos_geracao.xlsx — indivíduo com maior resultado da fitness por geração.
  - 3_melhor_escala.xlsx — indivíduo com maior resultado da fitness.
  - 5_historico_todos_fitness.xlsx — histórico de resultados da fitness por indivíduo em cada geração.
  * Reescala: 
    - 7_historico_todos_hamming.xlsx — histórico dos cálculos de hamming dos indivíduos ao longo das gerações.
    - 9_historico_todas_alteracoes.xlsx. — histórico das alterações dos indivíduos ao longo das gerações.
- Gráficos (PNG):
  - 4_grafico_individuos_selecionados.png — gráfico dos indivíduos selecionados ao longo das gerações.
  - 6_grafico_dispersao_populacao.png — gráfico de dispersão dos indivíduos ao longo das gerações.
  * Reescala:
    - 8_grafico_dispersao_hamming.png — gráfico de dispersão dos cálculos de hamming dos indivíduos ao longo das gerações.
    - 10_grafico_dispersao_alterações.png — gráfico de dispersão das alterações dos indivíduos ao longo das gerações.