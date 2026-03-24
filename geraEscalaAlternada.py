import numpy as np

def geraEscalaAlternada(individuo, diasDisponiveis, qtdeDiasDoMes, escala, dadosFuncionario):
    """
    Gera escala alternada nos dias disponíveis
    Regras:
      - Não pode haver 1's consecutivos
      - Total de 1's não pode passar de ceil(qtdeDiasDoMes/2)
      - Preferencialmente alternado
    """
    maxDiasTrabalhados = int(np.ceil(qtdeDiasDoMes / 2))
    contDiasTrabalhados = 0

    if escala == 1:
        prev = dadosFuncionario[-1]
        for d in diasDisponiveis:
            # Verifica se ainda pode alocar mais dias de trabalho
            if contDiasTrabalhados < maxDiasTrabalhados:
                if prev == 1:
                    # Se trabalhou no dia anterior, hoje não pode trabalhar
                    individuo[d-1] = 0
                    prev = 0
                else:
                    # Decide trabalhar
                    # 70% de chance de ser 1
                    trabalha = np.random.rand() > 0.3
                    individuo[d-1] = trabalha

                    if trabalha:
                        contDiasTrabalhados += 1
                        prev = 1
                    else:
                        prev = 0
            else:
                # Já atingiu o limite de dias trabalhados
                break

    return individuo
