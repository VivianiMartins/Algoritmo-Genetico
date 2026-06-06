import numpy as np
from avalicoesEvalidacoes.processarLicenca import processarLicenca

_cache_max_dias = {}

def validaSolucao(individuo, num_dias_mes, tipo, funcionarios, turno, farmaceuticos, auxiliares):
    """
    Verifica se a escala de um indivíduo (matriz 2D) é válida perante as regras e retorna individuo (array 2D consertado)
    """

    individuo_valido = individuo.copy()

    if (turno == 1):
        max_auxiliar = int(auxiliares // 2)
        min_auxiliar = 16
    else:
        max_auxiliar = int(auxiliares // 2)
        min_auxiliar = 12

    if tipo == 1:
        # ---------------------------------------------------------
        # Aplicar bloqueio de férias/licença para cada funcionário
        # ---------------------------------------------------------
        num_func = individuo_valido.shape[0]
        blocked_mask = np.zeros_like(individuo_valido, dtype=bool)
        dias_disponiveis_por_func = [None] * num_func

        for f_idx in range(num_func):
            linha = individuo_valido[f_idx, :].copy()
            dados_func = funcionarios[f_idx]
            linha_corrigida, dias_disp = processarLicenca(linha, dados_func, num_dias_mes, tipo)
            individuo_valido[f_idx, :] = linha_corrigida
            dias_disponiveis_por_func[f_idx] = dias_disp
            blocked_mask[f_idx, :] = (linha_corrigida == 0) & (linha != 0)

        individuo_valido[blocked_mask] = 0

        # ---------------------------------------------------------
        # Verificação do mês anterior + 1's consecutivos
        # ---------------------------------------------------------
        array_ultimos_dias = np.array([funcionario[-1] for funcionario in funcionarios])
        matriz_comparacao = np.hstack((array_ultimos_dias.reshape(-1, 1), individuo_valido))
        consecutivos = (matriz_comparacao[:, 1:] == 1) & (matriz_comparacao[:, :-1] == 1) #matriz de True/False do exato tamanho do 'individuo_valido'
        if np.any(consecutivos):
            individuo_valido[consecutivos] = 0 # corrige para 0 onde estava com 1. 111 (false, true, true) virará 100, por exemplo. 110 (false, true, false) virará 100.

        # ---------------------------------------------------------
        # verificação do total de escalas por mês
        # ---------------------------------------------------------
        if num_dias_mes not in _cache_max_dias:
            _cache_max_dias[num_dias_mes] = int(np.ceil(num_dias_mes / 2))
        max_dias = _cache_max_dias[num_dias_mes]
        somas = np.sum(individuo_valido, axis=1)
        excesso = somas - max_dias #retorna vetor com quantos dias foram excedidos por cada funcionário (negativo ou zero se não excedeu)
        se_excedeu = excesso > 0 #vetor booleano

        if np.any(se_excedeu):
            funcionarios_com_excesso = np.where(se_excedeu)[0]

            for func_idx in funcionarios_com_excesso:
                dias_trabalhados = np.where(individuo_valido[func_idx, :] == 1)[0]
                dias_trabalhados = dias_trabalhados[dias_trabalhados != 0] # Exclui o dia 0, que representa o dia anterior
                dias_para_folgar = np.random.choice(dias_trabalhados, size=excesso[func_idx], replace=False)
                individuo_valido[func_idx, dias_para_folgar] = 0

        # ---------------------------------------------------------
        # min e max de funcionários por turno (pode não ser atendido o min, que será penalizado na fitness)
        # ---------------------------------------------------------
        num_auxiliares = individuo_valido.shape[0] - farmaceuticos

        for dia in range(num_dias_mes): #validacao por dia
            #farmacêuticos
            farm_trabalhando = np.where(individuo_valido[:farmaceuticos, dia] == 1)[0]
            qtde_farm = len(farm_trabalhando)

            if qtde_farm > 1:
                remover = np.random.choice(farm_trabalhando, size=(qtde_farm - 1), replace=False) # sorteia os excedentes para folgar, deixando apenas 1
                individuo_valido[remover, dia] = 0
            elif qtde_farm == 0:
                candidatos = []
                for f in range(farmaceuticos): #tenta achar candidatos que não tenham trabalhado no dia anterior ou no dia seguinte, e que não tenham atingido o limite de dias trabalhados no mês
                    dias_disp = dias_disponiveis_por_func[f] if dias_disponiveis_por_func[f] is not None else list( range(1, num_dias_mes + 1))
                    dia_1based = dia + 1

                    if dia_1based not in dias_disp: continue

                    ontem = array_ultimos_dias[f] if dia == 0 else individuo_valido[f, dia - 1]
                    amanha = 0 if dia == num_dias_mes - 1 else individuo_valido[f, dia + 1]

                    if blocked_mask[f, dia]: continue

                    if ontem == 0 and amanha == 0 and np.sum(individuo_valido[f, :]) < max_dias: candidatos.append(f)

                if candidatos:
                    escolhido = np.random.choice(candidatos)
                    individuo_valido[escolhido, dia] = 1
                    individuo_valido[blocked_mask] = 0
                #se não houver candidatos, não faz nada e espera-se que seja eliminado na próxima geração por causa do fitness baixo (0 ou -inf)

            # auxiliares
            aux_trabalhando = np.where(individuo_valido[farmaceuticos:, dia] == 1)[0]
            qtde_aux = len(aux_trabalhando)

            if qtde_aux > max_auxiliar:
                remover = np.random.choice(aux_trabalhando, size=(qtde_aux - max_auxiliar), replace=False) #sorteia quem irá remover, pelo seu índice
                individuo_valido[remover + farmaceuticos, dia] = 0
            elif qtde_aux < min_auxiliar:
                falta = min_auxiliar - qtde_aux
                candidatos = []

                for a in range(num_auxiliares):
                    idx = a + farmaceuticos

                    dias_disp = dias_disponiveis_por_func[idx] if dias_disponiveis_por_func[idx] is not None else list(
                        range(1, num_dias_mes + 1))
                    dia_1based = dia + 1

                    if dia_1based not in dias_disp: continue

                    if individuo_valido[idx, dia] == 0:
                        ontem = array_ultimos_dias[idx] if dia == 0 else individuo_valido[idx, dia - 1]
                        amanha = 0 if dia == num_dias_mes - 1 else individuo_valido[idx, dia + 1]

                        if blocked_mask[idx, dia]: continue
                        if ontem == 0 and amanha == 0 and np.sum(individuo_valido[idx, :]) < max_dias: candidatos.append(idx)

                if candidatos:
                    qtd_adicionar = min(falta, len(candidatos))
                    escolhidos = np.random.choice(candidatos, size=qtd_adicionar, replace=False)
                    individuo_valido[escolhidos, dia] = 1
                    individuo_valido[blocked_mask] = 0
                # se não houver candidatos, não faz nada e espera-se que seja eliminado na próxima geração por causa do fitness baixo (0 ou -inf)
    else:
        pass  # implementar para reescala depois

    return individuo_valido