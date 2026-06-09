import numpy as np
from avalicoesEvalidacoes.validaSolucaoReescala import validaSolucaoReescala

def geraPopulacaoInicialReescala(cargos_ok, matriz_para_reescalar, matriz_nao_reescalar, janela_troca, id_troca, id_troca_recorte,
                                 num_dias_mes, cargo_troca, farmaceuticos, auxiliares,
                                 idx_dia_reescala, turno, qtde_individuos, taxa_troca_ideal, nomes, escala_original_numerica):
    """
    Gera população inicial válida para algoritmo genético de escalas de trabalho.
    taxa_troca_ideal: probabilidade de usar os candidatos ideais.
    """
    reescalar = matriz_para_reescalar[:, 1:]
    dias_resto_mes = reescalar.shape[1]
    total_colaboradores = farmaceuticos + auxiliares
    num_colunas_matriz = matriz_para_reescalar.shape[1]
    qtd_colaboradores_reescala = farmaceuticos if cargo_troca == 1 else auxiliares

    # Procurar os melhores candidatos para reescala
    mask_validos = np.ones(qtd_colaboradores_reescala, dtype=bool)

    if 0 <= id_troca_recorte < qtd_colaboradores_reescala: mask_validos[id_troca_recorte] = False

    indices_validos = np.where(mask_validos)[0]

    # CASO 1: Dia anterior, Dia da troca e Dia seguinte livres
    caso1_indexes = []
    caso2_indexes = []

    mask_dia_anterior_livre = matriz_para_reescalar[:, 0] == 0
    mask_dia_troca_livre = matriz_para_reescalar[:, 1] == 0

    if 2 < num_colunas_matriz:
        mask_dia_seguinte_livre = matriz_para_reescalar[:, 2] == 0
        mask_c1_ideal = mask_validos & mask_dia_anterior_livre & mask_dia_troca_livre & mask_dia_seguinte_livre
    else:
        mask_c1_ideal = mask_validos & mask_dia_anterior_livre & mask_dia_troca_livre

    if mask_c1_ideal.any():
        caso1_indexes = np.where(mask_c1_ideal)[0].tolist()

    # CASO 2: Possui dois ou mais dias consecutivos com folga (em qualquer lugar)
    if num_colunas_matriz >= 2:
        mask_consecutivos = (matriz_para_reescalar[:, :-1] == 0) & (matriz_para_reescalar[:, 1:] == 0)
        mask_c2 = mask_validos & mask_consecutivos.any(axis=1) & mask_dia_troca_livre & ~mask_c1_ideal
        caso2_indexes = np.where(mask_c2)[0].tolist()

    indices_livres_dia = np.where(mask_validos & mask_dia_troca_livre)[0]
    indices_validos_fallback = indices_livres_dia if len(indices_livres_dia) > 0 else indices_validos

    populacao = np.zeros((total_colaboradores, num_dias_mes, qtde_individuos), dtype=np.int8)
    janela = np.zeros((qtd_colaboradores_reescala, dias_resto_mes, qtde_individuos), dtype=np.int8)

    for cont_individuo in range(qtde_individuos):
        individuo_matriz = np.copy(reescalar)
        usar_ideal = np.random.random() <= taxa_troca_ideal
        tem_candidatos = len(caso1_indexes) > 0 or len(caso2_indexes) > 0

        if usar_ideal and tem_candidatos:
            if len(caso1_indexes) > 0: substituto = np.random.choice(caso1_indexes)
            else: substituto = np.random.choice(caso2_indexes)
        else:
            substituto = np.random.choice(indices_validos_fallback)
            individuo_matriz[substituto, :] = np.random.randint(0, 2, size=dias_resto_mes)

        individuo_matriz[id_troca_recorte, 0] = 0  # Tira o funcionário da escala
        individuo_matriz[substituto, 0] = 1  # Coloca o substituto sorteado

        janela[:, :, cont_individuo] = individuo_matriz
        individuo_quase_completo = np.hstack((matriz_nao_reescalar, individuo_matriz))

        if cargo_troca == 1: individuo_completo = np.vstack((individuo_quase_completo, cargos_ok))
        else: individuo_completo = np.vstack((cargos_ok, individuo_quase_completo))

        individuo_valido = validaSolucaoReescala(individuo_completo, num_dias_mes, turno, farmaceuticos, auxiliares, cargo_troca, id_troca, idx_dia_reescala, nomes, escala_original_numerica)
        populacao[:, :, cont_individuo] = individuo_valido

    return populacao