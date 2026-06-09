import numpy as np

def _pode_trabalhar(idx, dia, individuo_valido, dias_disp_func, array_ultimos_dias, num_dias_mes, blocked_mask,
                    max_dias):
    """Retorna True se o funcionário pode ser escalado no dia solicitado, respeitando todas as regras."""
    # 1. Já está escalado ou está bloqueado por férias/licença?
    if blocked_mask[idx, dia] or individuo_valido[idx, dia] == 1: return False

    # 2. O dia específico está disponível nas regras de licença?
    dias_disp = dias_disp_func[idx] if dias_disp_func[idx] is not None else range(1, num_dias_mes + 1)
    if (dia + 1) not in dias_disp: return False

    # 3. Trabalhou ontem ou vai trabalhar amanhã?
    ontem = array_ultimos_dias[idx] if dia == 0 else individuo_valido[idx, dia - 1]
    amanha = 0 if dia == num_dias_mes - 1 else individuo_valido[idx, dia + 1]

    # Retorna True apenas se tiver folga ontem e amanhã E não estourou o limite de dias no mês
    return ontem == 0 and amanha == 0 and np.sum(individuo_valido[idx, :]) < max_dias