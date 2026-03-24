import numpy as np
from geraEscalaAlternada import geraEscalaAlternada

def validaSolucao(individuo, dadosFuncionario, qtdeDiasDoMes, escala):
    """
    Valida e gera uma escala válida para o funcionário

    Entrada:
      individuo: vetor com a escala atual [1 x dias] (pode estar vazio/zerado ou preenchido)
      dadosFuncionario: vetor com [Cargo, Turno, Inicio, Fim, Dias...]
      qtdeDiasDoMes: número de dias no mês

    Saída:
      individuoValido: vetor [1 x dias] com escala válida
    """
    # Extrai informações do funcionário
    inicio = dadosFuncionario[2]
    fim = dadosFuncionario[3]

    # Valida se inicio e fim estão dentro do intervalo válido
    if inicio > qtdeDiasDoMes:
        raise ValueError(f'ERRO: Data de inicio ({inicio}) está fora do intervalo de dias do mês (1-{qtdeDiasDoMes})!')

    if fim > qtdeDiasDoMes:
        raise ValueError(f'ERRO: Data de fim ({fim}) está fora do intervalo de dias do mês (1-{qtdeDiasDoMes})!')

    # Inicializa o indivíduo válido
    if not escala:
        # Mantém a escala existente como base
        individuoValido = individuo.copy()
    else:
        # Inicia com zeros para escala nova
        individuoValido = np.zeros(qtdeDiasDoMes)

    # Verifica se há período de ausência (férias/licença)
    if inicio > 0 or fim > 0:
        # Há período de ausência - precisa bloquear os dias

        if inicio > fim:  # Período atravessa a virada do mês
            # Bloqueia do inicio até o último dia do mês
            for d in range(int(inicio), qtdeDiasDoMes + 1):
                individuoValido[d-1] = 0  # Não trabalha

            # Dias disponíveis: de 1 até (inicio-1)
            diasDisponiveis = list(range(1, int(inicio))) if inicio > 1 else []

        else:
            # Período normal dentro do mesmo mês (ex: dia 10 ao dia 20)
            # Bloqueia de inicio até fim
            for d in range(int(inicio), int(fim) + 1):
                individuoValido[d-1] = 0  # Não trabalha

            # Dias disponíveis: antes do inicio e depois do fim
            diasDisponiveis = []

            # Adiciona dias antes do inicio (se existirem)
            if inicio > 1:
                diasDisponiveis.extend(range(1, int(inicio)))

            # Adiciona dias depois do fim (se existirem)
            if fim < qtdeDiasDoMes:
                diasDisponiveis.extend(range(int(fim) + 1, qtdeDiasDoMes + 1))

        # Gera escala alternada apenas nos dias disponíveis
        if diasDisponiveis:
            individuoValido = geraEscalaAlternada(individuoValido, diasDisponiveis, qtdeDiasDoMes, escala, dadosFuncionario)

    else:
        # Não há período de ausência - todos os dias estão disponíveis
        diasDisponiveis = list(range(1, qtdeDiasDoMes + 1))
        individuoValido = geraEscalaAlternada(individuoValido, diasDisponiveis, qtdeDiasDoMes, escala, dadosFuncionario)

    return individuoValido
