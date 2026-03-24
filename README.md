# Algoritmo Genético para Escalonamento de Funcionários

Este projeto implementa um algoritmo genético para gerar escalas de trabalho de funcionários, separando por turnos diurno e noturno, considerando férias e regras de alternância.

## Estrutura do Projeto

- `funcaoPrincipal_AG.py`: Script principal que executa o algoritmo.
- `transformarListaFuncionarios.py`: Processa a lista de funcionários do CSV.
- `geraPopulacaoInicial.py`: Gera a população inicial.
- `validaSolucao.py`: Valida e ajusta soluções individuais.
- `geraEscalaAlternada.py`: Gera escalas alternadas.
- `listaFuncionarios.csv`: Arquivo de dados dos funcionários.

## Como Executar

Certifique-se de ter Python instalado, junto com as bibliotecas `numpy` e `pandas`.

Para instalar as dependências:

```bash
pip install numpy pandas
```

Para executar o código:

```bash
python funcaoPrincipal_AG.py
```

O script irá carregar os dados, processar e gerar a população inicial, exibindo relatórios no terminal.

## Arquivo de Dados

O `listaFuncionarios.csv` deve ter o formato:

Nome,Cargo,Turno,Início,Fim,Dia1,Dia2,...,Dia30

Onde:
- Cargo: Farmacêutico ou Auxiliar
- Turno: Diurno ou Noturno
- Início/Fim: Dias de férias (0 se não houver)</content>
