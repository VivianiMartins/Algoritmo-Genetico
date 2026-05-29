import math
import numpy as np

def funcaoFitness(populacao, numDiasMes, tipo, turno, farmaceuticos, auxiliares, penalidade=False):
    """
    Avaliação da população, atribuindo valores de acordo com que chega na solução ideal
    """

    avaliacaoFitness = np.zeros(populacao.shape[2])
    if (turno == 1):
        maxAuxiliar = int(auxiliares // 2)
        minAuxiliar = 16
    else:
        maxAuxiliar = int(auxiliares // 2)
        minAuxiliar = 12

    for cont in range(populacao.shape[2]):
        individuo = populacao[:, :, cont]
        somaTemp = 0.0

        # separando farmaceuticos de auxilixares:
        farmaceuticosTemp = individuo[:farmaceuticos, :]
        auxiliaresTemp = individuo[farmaceuticos:, :]

        if auxiliaresTemp.shape[0] != auxiliares or farmaceuticosTemp.shape[0] != farmaceuticos:
            raise ValueError("Número de auxiliares ou farmacêuticos na população não corresponde ao esperado para o turno.")

        x_array = np.sum(farmaceuticosTemp, axis=0) #0 são as colunas
        y_array = np.sum(auxiliaresTemp, axis=0)

        # ---------------------------------------------------------
        # avaliando farmacêuticos
        # ---------------------------------------------------------
        parcelas_farm = ((1 / x_array) ** (-1 + x_array))
        if penalidade:
            parcelas_farm = np.where(x_array != 1, -parcelas_farm, parcelas_farm)  #se o valor for diferente de 1, ele será negativado

        # ---------------------------------------------------------
        # avaliando auxiliares
        # ---------------------------------------------------------
        if turno == 1:
            parcelas_aux = ((1 / y_array) ** (-24 + (y_array / 4.13))) / 12719551155127680000000000
        else:
            parcelas_aux = ((1 / y_array) ** (-15 + (y_array / 3.66))) / 1716960112564.01


        if penalidade:
            fora_limites_aux = (y_array < minAuxiliar) | (y_array > maxAuxiliar) #se for menor que minAuxiliar ou maior que maxAuxiliar
            parcelas_aux = np.where(fora_limites_aux, -parcelas_aux, parcelas_aux) #seu resultado se torna negativo

        somaTemp += np.sum(parcelas_farm) + np.sum(parcelas_aux)

        # ---------------------------------------------------------
        # avaliando total de dias trabalhados por funcionário (min e max)
        # ---------------------------------------------------------
        maxPermitido = numDiasMes / 2
        divisor1 = None
        divisor2 = None

        if maxPermitido == 14:
            divisor1 = 3.6
            divisor2 = 387817958882.02
        elif maxPermitido == 14.5:
            divisor1 = 3.7
            divisor2 = 1929237609118.39
        elif maxPermitido == 15:
            divisor1 = 3.66
            divisor2 = 6627088070357.77
        elif maxPermitido == 15.5:
            divisor1 = 3.745
            divisor2 = 33069062888363.5

        if divisor1 and divisor2 is not None:
            z_array = np.sum(individuo, axis=1)  # 1 são as linhas
            parcelas = ((1 / z_array) ** (-maxPermitido + (z_array / divisor1))) / divisor2

            if penalidade:
                limite_dias = math.ceil(maxPermitido)
                fora_limite_dias = (z_array > limite_dias) #caso esteja fora do limite
                parcelas = np.where(fora_limite_dias, -parcelas, parcelas) #sua nota fica negativa

            somaTemp += np.sum(parcelas)

        # ---------------------------------------------------------
        # Avaliar se trabalha em férias ou licença - fazer depois
        # ---------------------------------------------------------

        avaliacaoFitness[cont] = somaTemp

    return avaliacaoFitness