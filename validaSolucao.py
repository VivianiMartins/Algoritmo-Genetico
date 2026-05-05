import numpy as np

_cache_max_dias = {}

def validaSolucao(individuo, qtdeDiasDoMes, tipo, dadosFuncionarios, turno):
    """
    Verifica se a escala de um indivíduo (matriz 2D) é válida perante as regras.

    Entrada:
      individuo: array [funcionarios x dias]
      tipo: inteiro, tipo (1=escala, 2=reescala)
      dadosFuncionarios: array numpy com dados dos funcionários [Cargo, Turno, Inicio, Fim, Dias...]
      turno: 1 para diurno, 0 para reescala (usa dias existentes)

    Saída:
      individuo (array 2D consertado)
    """

    ind_reparado = individuo.copy()
    farmaceuticos = 3
    if (turno == 1):
        maxAuxiliar = 24
        minAuxiliar = 16
    else:
        maxAuxiliar = 15
        minAuxiliar = 12

    if tipo == 1:
        # ---------------------------------------------------------
        # Verificação do mês anterior + 1's consecutivos
        # ---------------------------------------------------------
        array_ultimos_dias = np.array([funcionario[-1] for funcionario in dadosFuncionarios])
        matriz_comparacao = np.hstack((array_ultimos_dias.reshape(-1, 1), ind_reparado))
        consecutivos = (matriz_comparacao[:, 1:] == 1) & (matriz_comparacao[:, :-1] == 1) #matriz de True/False do exato tamanho do 'ind_reparado'
        if np.any(consecutivos):
            ind_reparado[consecutivos] = 0 # corrige para 0 onde estava com 1. 111 (false, true, true) virará 100, por exemplo. 110 (false, true, false) virará 100.

        # ---------------------------------------------------------
        # verificação do total de escalas por mês
        # ---------------------------------------------------------
        if qtdeDiasDoMes not in _cache_max_dias:
            _cache_max_dias[qtdeDiasDoMes] = int(np.ceil(qtdeDiasDoMes / 2))
        max_dias = _cache_max_dias[qtdeDiasDoMes]
        somas = np.sum(ind_reparado, axis=1)
        excesso = somas - max_dias #retorna vetor com quantos dias foram excedidos por cada funcionário (negativo ou zero se não excedeu)
        se_excedeu = excesso > 0 #vetor booleano

        if np.any(se_excedeu):
            funcionarios_com_excesso = np.where(se_excedeu)[0]

            for func_idx in funcionarios_com_excesso:
                dias_trabalhados = np.where(ind_reparado[func_idx, :] == 1)[0]
                dias_trabalhados = dias_trabalhados[dias_trabalhados != 0] # Exclui o dia 0, que representa o dia anterior
                dias_para_folgar = np.random.choice(dias_trabalhados, size=excesso[func_idx], replace=False)
                ind_reparado[func_idx, dias_para_folgar] = 0

        # ---------------------------------------------------------
        # min e max de funcionários por turno (pode não ser atendido o min, que será penalizado na fitness)
        # ---------------------------------------------------------
        num_auxiliares = ind_reparado.shape[0] - farmaceuticos

        for dia in range(qtdeDiasDoMes): #validacao por dia
            #farmacêuticos
            farm_trabalhando = np.where(ind_reparado[:farmaceuticos, dia] == 1)[0]
            qtde_farm = len(farm_trabalhando)

            if qtde_farm > 1:
                remover = np.random.choice(farm_trabalhando, size=(qtde_farm - 1), replace=False) # sorteia os excedentes para folgar, deixando apenas 1
                ind_reparado[remover, dia] = 0
            elif qtde_farm == 0:
                candidatos = []
                for f in range(farmaceuticos): #tenta achar candidatos que não tenham trabalhado no dia anterior ou no dia seguinte, e que não tenham atingido o limite de dias trabalhados no mês
                    ontem = array_ultimos_dias[f] if dia == 0 else ind_reparado[f, dia - 1]
                    amanha = 0 if dia == qtdeDiasDoMes - 1 else ind_reparado[f, dia + 1]
                    if ontem == 0 and amanha == 0 and np.sum(ind_reparado[f, :]) < max_dias:
                        candidatos.append(f)

                if candidatos:
                    escolhido = np.random.choice(candidatos)
                    ind_reparado[escolhido, dia] = 1

            # auxiliares
            aux_trabalhando = np.where(ind_reparado[farmaceuticos:, dia] == 1)[0]
            qtde_aux = len(aux_trabalhando)

            if qtde_aux > maxAuxiliar:
                remover = np.random.choice(aux_trabalhando, size=(qtde_aux - maxAuxiliar), replace=False)
                ind_reparado[remover + farmaceuticos, dia] = 0
            elif qtde_aux < minAuxiliar:
                falta = minAuxiliar - qtde_aux
                candidatos = []

                for a in range(num_auxiliares):
                    idx = a + farmaceuticos

                    if ind_reparado[idx, dia] == 0:
                        ontem = array_ultimos_dias[idx] if dia == 0 else ind_reparado[idx, dia - 1]
                        amanha = 0 if dia == qtdeDiasDoMes - 1 else ind_reparado[idx, dia + 1]
                        if ontem == 0 and amanha == 0 and np.sum(ind_reparado[idx, :]) < max_dias:
                            candidatos.append(idx)

                if candidatos:
                    qtd_adicionar = min(falta, len(candidatos))
                    escolhidos = np.random.choice(candidatos, size=qtd_adicionar, replace=False)
                    ind_reparado[escolhidos, dia] = 1

        # ---------------------------------------------------------
        # férias ou licença - fazer depois
        # ---------------------------------------------------------

    else:
        pass  # implementar para reescala depois

    return ind_reparado