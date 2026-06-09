import numpy as np
from avalicoesEvalidacoes._pode_trabalhar import _pode_trabalhar
from avalicoesEvalidacoes.processarLicenca import processarLicenca
_cache_max_dias = {}

def validaSolucao(individuo, num_dias_mes, funcionarios, turno, farmaceuticos, auxiliares):
    """
    Verifica se a escala de um indivíduo (matriz 2D) é válida perante as regras e retorna individuo (array 2D consertado)
    """

    individuo_valido = individuo.copy()
    max_auxiliar = int(auxiliares // 2)
    min_auxiliar = 16 if turno == 1 else 12

    # ---------------------------------------------------------
    # Aplicar bloqueio de férias/licença para cada funcionário
    # ---------------------------------------------------------
    num_func = individuo_valido.shape[0]
    blocked_mask = np.zeros_like(individuo_valido, dtype=bool)
    dias_disponiveis_por_func = [None] * num_func

    for f_idx in range(num_func):
        linha = individuo_valido[f_idx, :].copy()
        dados_func = funcionarios[f_idx]
        linha_corrigida, dias_disp = processarLicenca(linha, dados_func, num_dias_mes)
        individuo_valido[f_idx, :] = linha_corrigida
        dias_disponiveis_por_func[f_idx] = dias_disp
        blocked_mask[f_idx, :] = (linha_corrigida == 0) & (linha != 0)

    individuo_valido[blocked_mask] = 0

    # ---------------------------------------------------------
    # Verificação do mês anterior + 1's consecutivos
    # ---------------------------------------------------------
    array_ultimos_dias = np.array([funcionario[-1] for funcionario in funcionarios])
    matriz_comparacao = np.hstack((array_ultimos_dias.reshape(-1, 1), individuo_valido))
    consecutivos = (matriz_comparacao[:, 1:] == 1) & (matriz_comparacao[:, :-1] == 1)
    if np.any(consecutivos): individuo_valido[consecutivos] = 0

    # ---------------------------------------------------------
    # verificação do total de escalas por mês
    # ---------------------------------------------------------
    if num_dias_mes not in _cache_max_dias:
        _cache_max_dias[num_dias_mes] = int(np.ceil(num_dias_mes / 2))
    max_dias = _cache_max_dias[num_dias_mes]
    somas = np.sum(individuo_valido, axis=1)
    excesso = somas - max_dias  # retorna vetor com quantos dias foram excedidos por cada funcionário (negativo ou zero se não excedeu)
    se_excedeu = excesso > 0  # vetor booleano

    if np.any(se_excedeu):
        funcionarios_com_excesso = np.where(se_excedeu)[0]

        for func_idx in funcionarios_com_excesso:
            dias_trabalhados = np.where(individuo_valido[func_idx, :] == 1)[0]
            dias_trabalhados = dias_trabalhados[dias_trabalhados != 0]
            dias_para_folgar = np.random.choice(dias_trabalhados, size=excesso[func_idx], replace=False)
            individuo_valido[func_idx, dias_para_folgar] = 0

    # ---------------------------------------------------------
    # min e max de funcionários por turno (pode não ser atendido o min, que será penalizado na fitness)
    # ---------------------------------------------------------
    num_auxiliares = individuo_valido.shape[0] - farmaceuticos

    for dia in range(num_dias_mes):  # validacao por dia
        # farmacêuticos
        farm_trabalhando = np.where(individuo_valido[:farmaceuticos, dia] == 1)[0]
        qtde_farm = len(farm_trabalhando)

        if qtde_farm > 1:
            remover = np.random.choice(farm_trabalhando, size=(qtde_farm - 1), replace=False)
            individuo_valido[remover, dia] = 0
        elif qtde_farm == 0:
            candidatos = [f for f in range(farmaceuticos) if
                          _pode_trabalhar(f, dia, individuo_valido, dias_disponiveis_por_func, array_ultimos_dias, num_dias_mes, blocked_mask, max_dias)]
            if candidatos:
                individuo_valido[np.random.choice(candidatos), dia] = 1

        # auxiliares
        aux_trabalhando = np.where(individuo_valido[farmaceuticos:, dia] == 1)[0]
        qtde_aux = len(aux_trabalhando)

        if qtde_aux > max_auxiliar:
            remover = np.random.choice(aux_trabalhando, size=(qtde_aux - max_auxiliar), replace=False)
            individuo_valido[remover + farmaceuticos, dia] = 0
        elif qtde_aux < min_auxiliar:
            falta = min_auxiliar - qtde_aux
            candidatos = [a + farmaceuticos for a in range(num_auxiliares) if
                          _pode_trabalhar(a + farmaceuticos, dia, individuo_valido, dias_disponiveis_por_func, array_ultimos_dias, num_dias_mes, blocked_mask, max_dias)]

            if candidatos:
                qtd_adicionar = min(falta, len(candidatos))
                escolhidos = np.random.choice(candidatos, size=qtd_adicionar, replace=False)
                individuo_valido[escolhidos, dia] = 1
            # se não houver candidatos, não faz nada e espera-se que seja eliminado na próxima geração por causa do fitness baixo (0 ou -inf)



    return individuo_valido