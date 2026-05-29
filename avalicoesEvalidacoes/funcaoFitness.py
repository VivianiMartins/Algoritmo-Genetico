import math
import numpy as np

def funcaoFitness(populacao, num_dias_mes, tipo, turno, funcionarios, farmaceuticos, auxiliares, penalidade=False):
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
            raise ValueError(
                "Número de auxiliares ou farmacêuticos na população não corresponde ao esperado para o turno.")

        x_array = np.sum(farmaceuticos_temp, axis=0) #0 são as colunas
        y_array = np.sum(auxiliares_temp, axis=0)


        # ---------------------------------------------------------
        # Avaliar se trabalha em férias ou licença - fazer depois
        # ---------------------------------------------------------
        pontuacao_ferias = 0

        for f_idx in range(individuo.shape[0]):
            linha = individuo[f_idx, :]
            dados_func = funcionarios[f_idx]

            def _to_int_safe(x):
                try:
                    if x is None:
                        return 0
                    if isinstance(x, (int, np.integer)):
                        return int(x)
                    if isinstance(x, float) and np.isnan(x):
                        return 0
                    return int(float(x))
                except Exception:
                    return 0

            inicio = _to_int_safe(dados_func[2]) if len(dados_func) > 2 else 0
            fim = _to_int_safe(dados_func[3]) if len(dados_func) > 3 else 0

            violou = False
            if inicio > 0 and fim > 0:
                if inicio > fim:
                    for d in range(1, fim + 1):
                        if linha[d - 1] == 1: violou = True
                        break
                else:
                    for d in range(inicio, fim + 1):
                        if linha[d - 1] == 1: violou = True
                        break

            if violou:
                if penalidade: pontuacao_ferias += -1
                else: pontuacao_ferias += 0
            else: pontuacao_ferias += 1

        soma_temp += pontuacao_ferias

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
            parcelas = ((1 / z_array) ** (-max_permitido + (z_array / divisor1))) / divisor2

            if penalidade:
                limite_dias = math.ceil(max_permitido)
                fora_limite_dias = (z_array > limite_dias) #caso esteja fora do limite
                parcelas = np.where(fora_limite_dias, -parcelas, parcelas) #sua nota fica negativa

            soma_temp += np.sum(parcelas)

        avaliacaoFitness[cont] = soma_temp

    return avaliacaoFitness