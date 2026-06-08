import numpy as np
from avalicoesEvalidacoes.validaSolucao import validaSolucao

def geraPopulacaoInicialReescala(cargos_ok, matriz_para_reescalar, matriz_nao_reescalar, janela_troca_troca, id_troca,
                                 num_dias_mes, cargo_troca, qtd_colaboradores_reescala, qtd_colaboradores_cargos_ok,
                                 dia_reescala, turno, qtde_individuos, taxa_troca_ideal):
    """
    Gera população inicial válida para algoritmo genético de escalas de trabalho.
    taxa_troca_ideal: probabilidade de usar os candidatos ideais.
    """
    ultimos_dias_anteriores = [linha[:1] for linha in matriz_para_reescalar]
    reescalar = [linha[1:] for linha in matriz_para_reescalar]
    dias_resto_mes = len(reescalar[0]) if reescalar else 0
    total_colaboradores = qtd_colaboradores_reescala + qtd_colaboradores_cargos_ok
    array_nao_reescalar = np.array(matriz_nao_reescalar, dtype=np.int8)
    reescalar_array = np.array(matriz_para_reescalar, dtype=np.int8)
    array_cargos_ok = np.array(cargos_ok, dtype=np.int8)
    num_colunas_matriz = reescalar_array.shape[1]

    # Procurar os melhores candidatos para reescala
    mask_validos = np.ones(qtd_colaboradores_reescala, dtype=bool)
    if 0 <= id_troca < qtd_colaboradores_reescala: mask_validos[id_troca] = False
    indices_validos = np.where(mask_validos)[0]
    # CASO 1: Dia anterior (0), Dia da troca (1) e Dia seguinte (2) livres
    mask_c1_ideal = np.zeros(qtd_colaboradores_reescala, dtype=bool)
    caso1_indexes = []
    caso2_indexes = []
    if num_colunas_matriz >= 3:
        mask_dia0_zero = reescalar_array[:, 0] == 0
        mask_dia1_zero = reescalar_array[:, 1] == 0
        mask_dia2_zero = reescalar_array[:, 2] == 0
        mask_c1_ideal = mask_validos & mask_dia0_zero & mask_dia1_zero & mask_dia2_zero
        if mask_c1_ideal.any(): caso1_indexes = np.where(mask_c1_ideal)[0].tolist()
    # CASO 2: Possui dois ou mais dias consecutivos com folga (em qualquer lugar)
    if num_colunas_matriz >= 2:
        mask_consecutivos = (reescalar_array[:, :-1] == 0) & (reescalar_array[:, 1:] == 0)
        mask_c2 = mask_validos & mask_consecutivos.any(axis=1) & ~mask_c1_ideal
        caso2_indexes = np.where(mask_c2)[0].tolist()

    populacao = np.zeros((total_colaboradores, num_dias_mes, qtde_individuos), dtype=np.int8)
    janela = np.zeros((qtd_colaboradores_reescala, dias_resto_mes, qtde_individuos), dtype=np.int8)
    reescalar_base_cortada = np.array(reescalar, dtype=np.int8)

    for cont_individuo in range(qtde_individuos):
        individuo_matriz = np.copy(reescalar_base_cortada)
        usar_ideal = np.random.random() <= taxa_troca_ideal
        tem_candidatos = len(caso1_indexes) > 0 or len(caso2_indexes) > 0

        if usar_ideal and tem_candidatos:
            if len(caso1_indexes) > 0:
                substituto = np.random.choice(caso1_indexes)
            else:
                substituto = np.random.choice(caso2_indexes)
        else:
            substituto = np.random.choice(indices_validos)
            individuo_matriz[substituto, :] = np.random.randint(0, 2, size=dias_resto_mes)


        individuo_matriz[id_troca, 0] = 0  # Tira o funcionário da escala
        individuo_matriz[substituto, 0] = 1  # Coloca o substituto sorteado
        janela[:, :, cont_individuo] = individuo_matriz

        individuo_quase_completo = np.hstack((array_nao_reescalar, individuo_matriz))
        if cargo_troca == 1:
            #individuo_quase_completo irá se juntar com cargos_ok verticalmente: primeiras linhas individuo_quase_completo, depois cargos_ok
            individuo_completo = np.vstack((individuo_quase_completo, array_cargos_ok))
        else:
            # individuo_quase_completo irá se juntar com cargos_ok verticalmente: primeiras linhas cargos_ok e depois individuo_quase_completo
            individuo_completo = np.vstack((array_cargos_ok, individuo_quase_completo))

        populacao[:qtd_colaboradores_reescala, :, cont_individuo] = individuo_completo
        #refazer daqui
        #populacao[:, :, cont_individuo] = validaSolucao(individuo=populacao[:, :, cont_individuo],nm_dias_mes=num_dias_mes, funcionarios=funcionarios, turno=turno, farmaceuticos=farmaceuticos, auxiliares=auxiliares)

    return populacao