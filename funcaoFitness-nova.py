import math
import numpy as np

def funcaoFitnessNova(populacao, numDiasMes, tipo, turno, farmaceuticos, auxiliares):
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
        parcelas_farm = (1 / x_array) ** (-1 + x_array)
        #se for diferente de 1, sua nota será negativa -(1 / x_array) ** (-1 + x_array) apenas para os que estão fora dos limites


        # ---------------------------------------------------------

        # ---------------------------------------------------------
        # avaliando auxiliares
        # ---------------------------------------------------------
        if turno == 1:
            # se não for np.any(y_array < minAuxiliar) or np.any(y_array > maxAuxiliar))
            parcelas_aux = ((1 / y_array) ** (-24 + (y_array / 4.13))) / 12719551155127680000000000
            # caso contrario sua nota seria dada - ((1 / y_array) ** (-24 + (y_array / 4.13))) / 12719551155127680000000000 apenas para os que estão fora dos limites
        else:
            #se não for np.any(y_array < minAuxiliar) or np.any(y_array > maxAuxiliar))
            parcelas_aux = ((1 / y_array) ** (-15 + (y_array / 3.66))) / 1716960112564.01
            #caso contrario sua nota seria dada - ((1 / y_array) ** (-15 + (y_array / 3.66))) / 1716960112564.01 apenas para os que estão fora dos limites

        somaTemp += np.sum(parcelas_farm) + np.sum(parcelas_aux)

        if somaTemp != -np.inf:
            # ---------------------------------------------------------
            # avaliando total de dias trabalhados por funcionário (min e max)
            # ---------------------------------------------------------
            maxPermitido = numDiasMes/2
            limite_dias = math.ceil(maxPermitido)
            divisor1 = None
            divisor2 = None

            if maxPermitido == 14:
                divisor1 = 3.6
                divisor2 = 387817958882.02
            elif maxPermitido == 14.5:
                divisor1 = 3.66
                divisor2 = 1716960112564.01
            elif maxPermitido == 15:
                divisor1 = 3.66
                divisor2 = 6627088070357.77
            elif maxPermitido == 15.5:
                divisor1 = 3.75
                divisor2 = 33019357466522.7

            if divisor1 and divisor2 is not None:
                z_array = np.sum(individuo, axis=1)  # 1 são as linhas
                # para cada um de z_array:
                # caso o valor da soma seja maior que
                # seu valor será -(((1 / z_array) ** (-maxPermitido + (z_array / divisor1))) / divisor2) apenas para os que estão fora do limite
                #caso contrário, a conta é como abaixo
                parcelas = ((1 / z_array) ** (-maxPermitido + (z_array / divisor1))) / divisor2
                somaTemp += np.sum(parcelas)

            # ---------------------------------------------------------
            # Avaliar se trabalha em férias ou licença - fazer depois
            # ---------------------------------------------------------


        avaliacaoFitness[cont] = somaTemp

    return avaliacaoFitness