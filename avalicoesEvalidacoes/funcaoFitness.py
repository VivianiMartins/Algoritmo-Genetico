import math
import numpy as np
from avalicoesEvalidacoes._to_int_safe import _to_int_safe

def funcaoFitness(populacao, num_dias_mes, tipo, turno, funcionarios, farmaceuticos, auxiliares):
    """
    Avaliação da população, atribuindo valores de acordo com que chega na solução ideal
    """

    avaliacaoFitness = np.zeros(populacao.shape[2])
    if (turno == 1):
        max_auxiliar = int(auxiliares // 2)
        min_auxiliar = 16
    else:
        max_auxiliar = int(auxiliares // 2)
        min_auxiliar = 12

    for cont in range(populacao.shape[2]):
        individuo = populacao[:, :, cont]
        soma_temp = 0.0

        # separando farmaceuticos de auxilixares:
        farmaceuticos_temp = individuo[:farmaceuticos, :]
        auxiliares_temp = individuo[farmaceuticos:, :]

        if auxiliares_temp.shape[0] != auxiliares or farmaceuticos_temp.shape[0] != farmaceuticos:
            raise ValueError("Número de auxiliares ou farmacêuticos na população não corresponde ao esperado para o turno.")

        x_array = np.sum(farmaceuticos_temp, axis=0) #0 são as colunas
        y_array = np.sum(auxiliares_temp, axis=0)

        # ---------------------------------------------------------
        # Avaliar se trabalha em férias ou licença
        # ---------------------------------------------------------
        pontuacao_ferias = 0

        for f_idx in range(individuo.shape[0]):
            linha = individuo[f_idx, :]
            dados_func = funcionarios[f_idx]

            inicio = _to_int_safe(dados_func[2]) if len(dados_func) > 2 else 0
            fim = _to_int_safe(dados_func[3]) if len(dados_func) > 3 else 0

            violou = False
            if inicio > 0 and fim > 0:
                if inicio > fim:
                    if np.any(linha[:fim] == 1): violou = True
                else:
                    if np.any(linha[inicio - 1:fim] == 1): violou = True

            if violou:
                if turno == 1: pontuacao_ferias -= 1
                else: pontuacao_ferias += 0 #deixei apenas para eu não me perder
            else:
                pontuacao_ferias += 1

        soma_temp += pontuacao_ferias

        # ---------------------------------------------------------
        # avaliando farmacêuticos
        # ---------------------------------------------------------
        x_safe = np.where(x_array == 0, 1, x_array)
        parcelas_farm = ((1 / x_safe) ** (-1 + x_safe))
        parcelas_farm = np.where(x_array == 0, 0.0, parcelas_farm)

        if turno == 1: parcelas_farm = np.where(x_array != 1, -parcelas_farm, parcelas_farm)  #se o valor for diferente de 1, ele será negativado

        # ---------------------------------------------------------
        # avaliando auxiliares
        # ---------------------------------------------------------
        if turno == 1:
            parcelas_aux = ((1 / y_array) ** (-24 + (y_array / 4.13))) / 12719551155127680000000000
        else:
            parcelas_aux = ((1 / y_array) ** (-15 + (y_array / 3.66))) / 1716960112564.01


        if turno == 1:
            fora_limites_aux = (y_array < min_auxiliar) | (y_array > max_auxiliar) #se for menor que min_auxiliar ou maior que max_auxiliar
            parcelas_aux = np.where(fora_limites_aux, -parcelas_aux, parcelas_aux) #seu resultado se torna negativo

        soma_temp += np.sum(parcelas_farm) + np.sum(parcelas_aux)

        # ---------------------------------------------------------
        # avaliando total de dias trabalhados por funcionário (min e max)
        # ---------------------------------------------------------
        max_permitido = num_dias_mes / 2
        divisor1 = None
        divisor2 = None

        if max_permitido == 14:
            divisor1 = 3.6
            divisor2 = 387817958882.02
        elif max_permitido == 14.5:
            divisor1 = 3.7
            divisor2 = 1929237609118.39
        elif max_permitido == 15:
            divisor1 = 3.66
            divisor2 = 6627088070357.77
        elif max_permitido == 15.5:
            divisor1 = 3.745
            divisor2 = 33069062888363.5

        if divisor1 and divisor2 is not None:
            z_array = np.sum(individuo, axis=1)  # 1 são as linhas
            z_safe = np.where(z_array == 0, 1, z_array)
            parcelas = ((1 / z_safe) ** (-max_permitido + (z_safe / divisor1))) / divisor2
            parcelas = np.where(z_array == 0, 0.0, parcelas)

            if turno == 1:
                limite_dias = math.ceil(max_permitido)
                fora_limite_dias = (z_array > limite_dias) #caso esteja fora do limite
                parcelas = np.where(fora_limite_dias, -parcelas, parcelas) #sua nota fica negativa

            soma_temp += np.sum(parcelas)

        avaliacaoFitness[cont] = soma_temp

    return avaliacaoFitness