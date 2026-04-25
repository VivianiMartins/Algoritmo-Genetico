import numpy as np

_cache_max_dias = {}

def geraEscalaAlternada(individuo, diasDisponiveis, qtdeDiasDoMes, tipo, dadosFuncionario):
    """
    Gera escala alternada nos dias disponíveis para um funcionário, seguindo regras de trabalho.

    Entrada:
      individuo: array numpy [1 x dias] com a escala inicial (pode ter dias já definidos)
      diasDisponiveis: lista de inteiros, dias disponíveis para trabalho (1-based)
      qtdeDiasDoMes: inteiro, número total de dias no mês
      tipo: inteiro, tipo de escala (1=nova escala, 0=reescala - não implementado)
      dadosFuncionario: array numpy com dados do funcionário [Cargo, Turno, Inicio, Fim, Dias...]

    Saída:
      individuo: array numpy [1 x dias] com escala atualizada (0=não trabalha, 1=trabalha)

    Regras aplicadas:
      - Não permite 1's consecutivos (dias de trabalho seguidos), com preferencial por alternância
      - Limite máximo de dias trabalhados: ceil(qtdeDiasDoMes/2)
      - Primeiro dia do mês segue o último do anterior
      - Usa probabilidade aleatória (70% chance de trabalhar) quando possível
    """
    if qtdeDiasDoMes not in _cache_max_dias:
        _cache_max_dias[qtdeDiasDoMes] = int(np.ceil(qtdeDiasDoMes / 2))
    maxDiasTrabalhados = _cache_max_dias[qtdeDiasDoMes]

    contDiasTrabalhados = 0

    if tipo == 1:
        prev = int(dadosFuncionario[-1]) #Aqui verifica o último dia do mês anterior
        for d in diasDisponiveis:
            if contDiasTrabalhados >= maxDiasTrabalhados:
                break

            if prev == 1:
                individuo[d - 1] = 0
                prev = 0
            else:
                trabalha = np.random.random() > 0.3  # Probabilidade de 70% sim e 30% não
                individuo[d - 1] = int(trabalha)
                if trabalha:
                    contDiasTrabalhados += 1
                    prev = 1
                else:
                    prev = 0
    else:
        pass #implementar para reescala depois

    return individuo