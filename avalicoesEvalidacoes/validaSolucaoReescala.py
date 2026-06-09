import numpy as np
from avalicoesEvalidacoes.processarLicenca import processarLicenca
from avalicoesEvalidacoes._pode_trabalhar import _pode_trabalhar
_cache_max_dias = {}

def validaSolucaoReescala(individuo, num_dias_mes, turno, farmaceuticos, auxiliares, cargo_troca, id_troca, idx_dia_reescala, nomes, escala_original_numerica):
    """
    Verifica se a escala de um indivíduo é válida.
    escala_original_numerica: matriz 2D apenas com os dias do mês da escala original (antes da reescala)
    """
    individuo_valido = individuo.copy()
    max_auxiliar = int(auxiliares // 2)
    min_auxiliar = 16 if turno == 1 else 12

    # ---------------------------------------------------------
    # 1. Identificação Dinâmica e Bloqueios Iniciais
    # ---------------------------------------------------------
    if individuo_valido[id_troca, idx_dia_reescala] != 0:
        individuo_valido[id_troca, idx_dia_reescala] = 0

    # Quem está cobrindo o turno neste indivíduo específico (Tem 1 agora, mas tinha 0 na base)
    substitutos_dinamicos = np.where(
        (individuo_valido[:, idx_dia_reescala] == 1) &
        (escala_original_numerica[:, idx_dia_reescala] == 0)
    )[0]

    # ---------------------------------------------------------
    # Aplicar bloqueio de férias/licença para cada funcionário
    # ---------------------------------------------------------
    num_func = individuo_valido.shape[0]
    blocked_mask = np.zeros_like(individuo_valido, dtype=bool)
    dias_disponiveis_por_func = [None] * num_func

    for f_idx in range(num_func):
        linha = individuo_valido[f_idx, :].copy()
        linha_corrigida, dias_disp = processarLicenca(linha, nomes[f_idx], num_dias_mes)
        individuo_valido[f_idx, :] = linha_corrigida
        dias_disponiveis_por_func[f_idx] = dias_disp
        blocked_mask[f_idx, :] = (linha_corrigida == 0) & (linha != 0)

    blocked_mask[id_troca, idx_dia_reescala] = True
    individuo_valido[blocked_mask] = 0

    # ---------------------------------------------------------
    # Verificação do mês anterior + 1's consecutivos
    # ---------------------------------------------------------
    substitutos_ativos = [sub for sub in substitutos_dinamicos if individuo_valido[sub, idx_dia_reescala] == 1] #ainda tenho substitutos?
    array_ultimos_dias = np.array([funcionario[-1] for funcionario in nomes])

    if not substitutos_ativos:
        inicio_idx = 0 if cargo_troca == 1 else farmaceuticos
        fim_idx = farmaceuticos if cargo_troca == 1 else individuo_valido.shape[0]

        candidatos_validos = []
        for i in range(inicio_idx, fim_idx):
            if i != id_troca and not blocked_mask[i, idx_dia_reescala] and individuo_valido[i, idx_dia_reescala] == 0:
                candidatos_validos.append(i)
        matriz_comparacao = np.hstack((array_ultimos_dias.reshape(-1, 1), individuo_valido))
        consecutivos = (matriz_comparacao[:, 1:] == 1) & (matriz_comparacao[:, :-1] == 1)
        if np.any(consecutivos): individuo_valido[consecutivos] = 0

        if candidatos_validos:
            novo_substituto = np.random.choice(candidatos_validos)
            individuo_valido[novo_substituto, idx_dia_reescala] = 1
            substitutos_ativos = [novo_substituto]
            substitutos_dinamicos = np.append(substitutos_dinamicos, novo_substituto)

    matriz_comparacao = np.hstack((array_ultimos_dias.reshape(-1, 1), individuo_valido))
    consecutivos = (matriz_comparacao[:, 1:] == 1) & (matriz_comparacao[:, :-1] == 1)
    for sub in substitutos_ativos:
        consecutivos[sub, idx_dia_reescala] = False
        if idx_dia_reescala + 1 < num_dias_mes:
            consecutivos[sub, idx_dia_reescala + 1] = False
    if np.any(consecutivos): individuo_valido[consecutivos] = 0

    # ---------------------------------------------------------
    # Verificação do total de escalas por mês
    # ---------------------------------------------------------
    if num_dias_mes not in _cache_max_dias:
        _cache_max_dias[num_dias_mes] = int(np.ceil(num_dias_mes / 2))

    somas = np.sum(individuo_valido, axis=1)
    excesso = somas - _cache_max_dias[num_dias_mes]

    for func_idx in np.where(excesso > 0)[0]:
        dias_trabalhados = np.where(individuo_valido[func_idx, :] == 1)[0]
        dias_trabalhados = dias_trabalhados[dias_trabalhados != 0]

        # Protege o idx_dia_reescala do sorteio de remoção se o funcionário for um dos substitutos
        if func_idx in substitutos_dinamicos:
            dias_trabalhados = dias_trabalhados[dias_trabalhados != idx_dia_reescala]

        qtd_remover = min(excesso[func_idx], len(dias_trabalhados))
        if qtd_remover > 0:
            dias_para_folgar = np.random.choice(dias_trabalhados, size=qtd_remover, replace=False)
            individuo_valido[func_idx, dias_para_folgar] = 0

    # ---------------------------------------------------------
    # min e max de funcionários por turno (pode não ser atendido o min, que será penalizado na fitness)
    # ---------------------------------------------------------
    num_auxiliares = individuo_valido.shape[0] - farmaceuticos

    for dia in range(num_dias_mes):# validacao por dia
        # farmacêuticos
        farm_trabalhando = np.where(individuo_valido[:farmaceuticos, dia] == 1)[0]
        qtde_farm = len(farm_trabalhando)

        if qtde_farm > 1:
            candidatos_remocao = farm_trabalhando
            if dia == idx_dia_reescala: # Protege os substitutos de serem removidos no dia da reescala
                candidatos_remocao = np.setdiff1d(farm_trabalhando, substitutos_dinamicos)
                if len(candidatos_remocao) == 0: candidatos_remocao = farm_trabalhando

            qtd_a_remover = min(qtde_farm - 1, len(candidatos_remocao))
            if qtd_a_remover > 0:
                remover = np.random.choice(candidatos_remocao, size=qtd_a_remover, replace=False)
                individuo_valido[remover, dia] = 0

        elif qtde_farm == 0:
            candidatos = [f for f in range(farmaceuticos) if
                          _pode_trabalhar(f, dia, individuo_valido, dias_disponiveis_por_func, array_ultimos_dias,
                                          num_dias_mes, blocked_mask, _cache_max_dias[num_dias_mes])]
            if candidatos:
                individuo_valido[np.random.choice(candidatos), dia] = 1

        # auxiliares
        aux_trabalhando = np.where(individuo_valido[farmaceuticos:, dia] == 1)[0]
        qtde_aux = len(aux_trabalhando)

        if qtde_aux > max_auxiliar:
            candidatos_remocao = aux_trabalhando
            if dia == idx_dia_reescala:
                # Transforma o ID global dos substitutos em ID relativo dos auxiliares
                subs_relativos = [s - farmaceuticos for s in substitutos_dinamicos if s >= farmaceuticos]
                candidatos_remocao = np.setdiff1d(aux_trabalhando, subs_relativos)
                if len(candidatos_remocao) == 0: candidatos_remocao = aux_trabalhando

            qtd_a_remover = min(qtde_aux - max_auxiliar, len(candidatos_remocao))
            if qtd_a_remover > 0:
                remover = np.random.choice(candidatos_remocao, size=qtd_a_remover, replace=False)
                individuo_valido[remover + farmaceuticos, dia] = 0

        elif qtde_aux < min_auxiliar:
            falta = min_auxiliar - qtde_aux
            candidatos = [a + farmaceuticos for a in range(num_auxiliares) if
                          _pode_trabalhar(a + farmaceuticos, dia, individuo_valido, dias_disponiveis_por_func,
                                          array_ultimos_dias, num_dias_mes, blocked_mask,
                                          _cache_max_dias[num_dias_mes])]
            if candidatos:
                escolhidos = np.random.choice(candidatos, size=min(falta, len(candidatos)), replace=False)
                individuo_valido[escolhidos, dia] = 1

    return individuo_valido