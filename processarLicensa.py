import numpy as np

def processar_licensa(individuo, dadosFuncionario, qtdeDiasDoMes, tipo):
    """
    Processa o período de férias do funcionário e retorna a escala inicial e dias disponíveis.

    Entrada:
      individuo: vetor com a escala atual [1 x dias]
      dadosFuncionario: vetor com [Cargo, Turno, Inicio, Fim, Dias...]
      qtdeDiasDoMes: número de dias no mês
      tipo: tipo de escala (0=reescala, 1=nova)

    Saída:
      individuoValido: vetor [1 x dias] com escala inicial (com férias bloqueadas)
      diasDisponiveis: lista de dias disponíveis para trabalho
    """
    # Extrai as datas de início e fim das férias do funcionário
    inicio = dadosFuncionario[2]  # Data de início das férias (índice 2)
    fim = dadosFuncionario[3]  # Data de fim das férias (índice 3)

    # Valida se as datas estão dentro do intervalo do mês
    if inicio > qtdeDiasDoMes:  # Se início é maior que o número de dias
        raise ValueError(f'ERRO: Data de inicio ({inicio}) está fora do intervalo de dias do mês (1-{qtdeDiasDoMes})!')  # Lança erro
    if fim > qtdeDiasDoMes:  # Se fim é maior que o número de dias
        raise ValueError(f'ERRO: Data de fim ({fim}) está fora do intervalo de dias do mês (1-{qtdeDiasDoMes})!')  # Lança erro

    # Inicializa o indivíduo válido baseado no tipo de escala
    if not tipo:  # Se escala == 0 (reescala), usa a existente
        individuoValido = individuo.copy()  # Copia a escala atual
    else:  # Se escala == 1 (nova), inicia com zeros
        individuoValido = np.zeros(qtdeDiasDoMes)  # Vetor de zeros para nova escala

    # Verifica se há período de ausência (férias)
    if inicio > 0 or fim > 0:  # Se há férias (valores > 0)
        # Há período de ausência, precisa bloquear os dias de férias

        if inicio > fim:  # Caso especial: período atravessa o mês (ex: 28-2)
            # Bloqueia de início até o fim do mês
            for d in range(int(inicio), qtdeDiasDoMes + 1):  # Loop de início a último dia
                individuoValido[d-1] = 0  # Define como não trabalha (0)

            # Dias disponíveis: antes do início
            diasDisponiveis = list(range(1, int(inicio))) if inicio > 1 else []  # Lista de 1 a início-1

        else:  # Período normal dentro do mês
            # Bloqueia de início até fim
            for d in range(int(inicio), int(fim) + 1):  # Loop de início a fim
                individuoValido[d-1] = 0  # Define como não trabalha (0)

            # Dias disponíveis: antes de início e depois de fim
            diasDisponiveis = []  # Inicializa lista vazia

            # Adiciona dias antes do início, se existirem
            if inicio > 1:  # Se início > 1
                diasDisponiveis.extend(range(1, int(inicio)))  # Adiciona 1 a início-1

            # Adiciona dias depois do fim, se existirem
            if fim < qtdeDiasDoMes:  # Se fim < total de dias
                diasDisponiveis.extend(range(int(fim) + 1, qtdeDiasDoMes + 1))  # Adiciona fim+1 a último dia

    else:  # Não há férias
        # Todos os dias estão disponíveis
        diasDisponiveis = list(range(1, qtdeDiasDoMes + 1))  # Lista de todos os dias

    return individuoValido, diasDisponiveis