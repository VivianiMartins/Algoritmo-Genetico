import math
import numpy as np

def funcaoFitness(populacao, numDiasMes, tipo, turno, farmaceuticos, auxiliares):
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

        if (np.any(x_array == 0) or np.any(x_array == 3) or np.any(x_array == 2) or
            np.any(y_array == 0) or np.any(y_array < minAuxiliar) or np.any(y_array > maxAuxiliar)):
            # somaTemp = -np.inf #voltar quando população inicial estiver calibrada corretamente
            somaTemp = somaTemp - 25000000.9999 # temporário, apenas para dar continuidade no algoritmo
        else:
            # ---------------------------------------------------------
            # avaliando farmacêuticos
            parcelas_farm = 3.825 * ((1 / x_array) ** (-1 + x_array))
            # ---------------------------------------------------------

            # ---------------------------------------------------------
            # avaliando auxiliares
            # ---------------------------------------------------------
            if turno == 1:
                parcelas_aux = 5 * ((10 / y_array) ** (-24 + (y_array / 1.875)))
            else:
                parcelas_aux = 0.000000125 * ((1 / y_array) ** (-15 + (y_array / 3.725)))

            somaTemp += np.sum(parcelas_farm) + np.sum(parcelas_aux)

        if somaTemp != -np.inf:
            # ---------------------------------------------------------
            # avaliando total de dias trabalhados por funcionário (min e max)
            # ---------------------------------------------------------
            maxPermitido = numDiasMes/2
            limite_dias = math.ceil(maxPermitido)
            divisor = None
            if maxPermitido == 14:
                divisor = 3.64
            elif maxPermitido == 14.5:
                divisor = 3.712
            elif maxPermitido == 15:
                divisor = 3.725
            elif maxPermitido == 15.5:
                divisor = 3.745

            if divisor is not None:
                z_array = np.sum(individuo, axis=1) #1 são as linhas
                if np.any(z_array == 0) or np.any(z_array > limite_dias):
                    #somaTemp = -np.inf #voltar quando população inicial estiver calibrada corretamente
                    somaTemp = somaTemp - 25000000.99999 #temporário, apenas para dar continuidade no algoritmo
                else:
                    parcelas = 0.000000125 * ((1 / z_array) ** (-maxPermitido + (z_array / divisor)))
                    somaTemp += np.sum(parcelas)

            # ---------------------------------------------------------
            # Avaliar se trabalha em férias ou licença - fazer depois
            # ---------------------------------------------------------
            #já é invalidado com -infinito

        avaliacaoFitness[cont] = somaTemp

    return avaliacaoFitness