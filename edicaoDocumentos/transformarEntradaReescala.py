import numpy as np
from edicaoDocumentos.encontrarFuncionario import encontrarFuncionario

def transformarEntradaReescala(lista_funcionarios, dia_reescala, funcionario):
    """
    Transforma a lista de funcionários em matrizes separadas de reescala e calcula a quantidade de pessoas.
    """
    num_linhas = len(lista_funcionarios)
    if num_linhas == 0:
        return [], [], [], [], [], 0, 0, 0, 0, 0

    num_colunas = len(lista_funcionarios[0])
    num_dias_mes = num_colunas - 5
    dias_ok = num_colunas - (num_dias_mes - dia_reescala) - 1
    dias_a_reescalar = dias_ok - 1 #vai pegar um dia antes para comparar

    funcionario_troca, id_troca, cargo_troca = encontrarFuncionario(lista_funcionarios, funcionario)

    if funcionario_troca[dias_ok] == 0:
        print(f"\n>> O funcionário {funcionario},não está escalado dia {dia_reescala} <<")
        return [], [], [], [], [], 0, 0, 0, 0, 0


    if cargo_troca == 0:
        return [], [], [], [], [], 0, 0, 0, 0, 0

    idx_divisao = next((i for i, linha in enumerate(lista_funcionarios) if str(linha[1]).strip().lower() == "auxiliar"), num_linhas)

    if cargo_troca == 1:
        reescala = lista_funcionarios[:idx_divisao]
        cargos_ok = lista_funcionarios[idx_divisao:]
    else:
        reescala = lista_funcionarios[idx_divisao:]
        cargos_ok = lista_funcionarios[:idx_divisao]

    qtd_colaboradores_reescala = len(reescala)
    qtd_colaboradores_cargos_ok = len(cargos_ok)

    matriz_nao_reescalar = [linha[:dias_ok] for linha in reescala]
    matriz_para_reescalar = [linha[dias_a_reescalar:] for linha in reescala]

    matriz_nao_reescalar = np.array(matriz_nao_reescalar, dtype=object)
    matriz_para_reescalar = np.array(matriz_para_reescalar, dtype=np.int8)
    cargos_ok_array = np.array(cargos_ok, dtype=object)
    nomes_nao_reescalar = matriz_nao_reescalar[:, :5]
    matriz_nao_reescalar = matriz_nao_reescalar[:, 5:].astype(np.int8)

    if qtd_colaboradores_cargos_ok > 0: nomes_cargos_ok = cargos_ok_array[:, :5]
    else: nomes_cargos_ok = np.empty((0, 5), dtype=object)

    if qtd_colaboradores_cargos_ok > 0: cargos_ok = cargos_ok_array[:, 5:].astype(np.int8)
    else: cargos_ok = np.empty((0, num_dias_mes), dtype=np.int8)

    if cargo_troca == 1: nomes = np.vstack((nomes_nao_reescalar, nomes_cargos_ok))
    else: nomes = np.vstack((nomes_cargos_ok, nomes_nao_reescalar))

    return cargos_ok, matriz_para_reescalar, matriz_nao_reescalar, nomes, funcionario_troca, id_troca, num_dias_mes, cargo_troca, qtd_colaboradores_reescala, qtd_colaboradores_cargos_ok