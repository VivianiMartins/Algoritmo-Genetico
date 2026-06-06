import numpy as np
from avalicoesEvalidacoes._to_int_safe import _to_int_safe

def processarLicenca(funcionario, funcionarios, num_dias_mes, tipo):
    """
    Processa período de licença/ferias para um funcionário.
    """
    inicio = _to_int_safe(funcionarios[2]) if len(funcionarios) > 2 else 0
    fim = _to_int_safe(funcionarios[3]) if len(funcionarios) > 3 else 0

    individuo_valido = funcionario.copy().astype(np.int8)

    if inicio > fim:
        individuo_valido[:fim] = 0
        dias_disponiveis = list(range(0, fim + 1))
    else:
        individuo_valido[inicio - 1:fim] = 0

        dias_disponiveis = []
        if inicio > 1:
            dias_disponiveis.extend(range(1, inicio))
        if fim < num_dias_mes:
            dias_disponiveis.extend(range(fim + 1, num_dias_mes + 1))

    return individuo_valido, dias_disponiveis