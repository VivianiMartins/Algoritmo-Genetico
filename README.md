## Sobre o Projeto

Este repositório contém a implementação do trabalho de conclusão de curso (TCC) em **Ciência da Computação** apresentado ao **Instituto Federal de Goiás — Câmpus Anápolis**.

**Título:** *Reescala em Saúde: Aplicação de Algoritmos Genéticos para Substituição de Falta Conforme Legislação Trabalhista*

**Objetivo:** Desenvolver um sistema baseado em algoritmos genéticos para gerar e reajustar escalas de trabalho de funcionários em estabelecimentos de saúde (farmácias), considerando:
- Dois turnos de trabalho: Diurno e Noturno.
- Dois cargos: Farmacêutico e Auxiliar.
- Licenças e férias dentro da legislação trabalhista
- Regras de alternância e distribuição equitativa

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

# Parâmetros do AG
qtde_individuos = 50
geracoes = 1500
elitismo = True

# seleção: 1=roleta, 2=elitista, 3=torneio, 4=maximax/maximin
selecao = 2
qtd_pais = 2
tamanho_grupos_torneios = 0

# cruzamento: 1=blocos, 2=xadrez, 3=percentagem/ordem sorteada
cruzamento = 1
qtd_blocos = 45

# mutação: 1=bit-flip bloco, 2=bit-flip gene
mutacao = 2
probabilidade_mutacao = 0.2
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
  - algoritmoGeneticoReescala.py, melhor_escala_ag.xlsx
  - Subpastas equivalentes às do modo escala.
- edicaoDocumentos/ — utilitários:
  - transformarEntradaDoisTurnos.py, transformarEntradaReescala.py, salvarExcel.py, resultadosTeste.py, graficoDispersaoHamming.py
- selecao/ — implementações de métodos de seleção (roleta, torneio, elitista, etc).

---
Saídas geradas
----------
- Arquivos Excel:
  - 1_populacao_final.xlsx — população final (todas as soluções).
  - 2_historico_melhores_individuos_geracao.xlsx — melhores por geração.
  - 3_melhor_escala.xlsx — melhor indivíduo (escala).
  - 5_historico_todos_fitness.xlsx — histórico de fitness (todas as gerações e indivíduos).
  - Reescala: 7_historico_todos_hamming.xlsx, 9_historico_todas_alteracoes.xlsx.
- Gráficos (PNG):
  - 4_grafico_individuos_selecionados.png
  - 6_grafico_dispersao_populacao.png
  - 8_grafico_dispersao_hamming.png
  - 10_grafico_dispersao_alterações.png