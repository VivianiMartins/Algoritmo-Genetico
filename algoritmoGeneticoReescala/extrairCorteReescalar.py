import numpy as np

def extrairCorteReescalar(individuo, farmaceuticos, num_dias_mes, dia_reescala, cargo_troca):
    """
    Transforma a lista de funcionários em matrizes separadas de reescala e calcula a quantidade de pessoas.
    """
    num_colunas = len(individuo[0])
    dias_ok = num_colunas - (num_dias_mes - dia_reescala) - 1
    dias_a_reescalar = dias_ok

    if cargo_troca == 1:
        reescala = individuo[:farmaceuticos]
    else:
        reescala = individuo[farmaceuticos:]

    matriz_para_reescalar = [linha[dias_a_reescalar:] for linha in reescala]
    matriz_para_reescalar = np.array(matriz_para_reescalar, dtype=np.int8)

    return matriz_para_reescalar