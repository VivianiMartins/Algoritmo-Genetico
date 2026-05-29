import numpy as np

def processarLicensa(individuo_linha, funcionarios, num_dias_mes, tipo):
    """
    Processa período de licença/ferias para um funcionário.
    """

    def _to_int_safe(x):
        try:
            if x is None:
                return 0
            if isinstance(x, (int, np.integer)):
                return int(x)
            if isinstance(x, float) and np.isnan(x):
                return 0
            return int(float(x))
        except Exception:
            return 0

    inicio = _to_int_safe(funcionarios[2]) if len(funcionarios) > 2 else 0
    fim = _to_int_safe(funcionarios[3]) if len(funcionarios) > 3 else 0

    if inicio < 0 or fim < 0:
        raise ValueError(f"Datas de férias inválidas: inicio={inicio}, fim={fim}")

    if inicio > num_dias_mes:
        raise ValueError(f'ERRO: Data de inicio ({inicio}) está fora do intervalo de dias do mês (1-{num_dias_mes})!')
    if fim > num_dias_mes:
        raise ValueError(f'ERRO: Data de fim ({fim}) está fora do intervalo de dias do mês (1-{num_dias_mes})!')

    # inicializa vetor conforme tipo
    if tipo == 0:
        individuo_valido = individuo_linha.copy().astype(np.int8)
    else:
        individuo_valido = np.zeros(num_dias_mes, dtype=np.int8)

    dias_disponiveis = []

    if inicio <= 0 and fim <= 0:
        dias_disponiveis = list(range(1, num_dias_mes + 1))
        return individuo_valido, dias_disponiveis

    if inicio > fim:
        for d in range(inicio, num_dias_mes + 1):
            individuo_valido[d - 1] = 0
        dias_disponiveis = list(range(1, inicio)) if inicio > 1 else []
    else:
        for d in range(inicio, fim + 1):
            individuo_valido[d - 1] = 0
        if inicio > 1:
            dias_disponiveis.extend(range(1, inicio))
        if fim < num_dias_mes:
            dias_disponiveis.extend(range(fim + 1, num_dias_mes + 1))

    return individuo_valido, dias_disponiveis