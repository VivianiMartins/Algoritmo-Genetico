import numpy as np

_cache_max_dias = {}

def validaSolucao(individuo, qtdeDiasDoMes, tipo, dadosFuncionarios, inicial=False):
    """
    Verifica se a escala de um indivíduo (matriz 2D) é válida perante as regras.

    Entrada:
      individuo: array [funcionarios x dias]
      tipo: inteiro, tipo (1=escala, 2=reescala)
      dadosFuncionarios: array numpy com dados dos funcionários [Cargo, Turno, Inicio, Fim, Dias...]
      inicial: False para validação normal, True para validação da população inicial

    Saída:
      True se for válido, False se quebrar alguma regra.
    """

    if tipo == 1:
        # verificação do total de escalas por mês
        if qtdeDiasDoMes not in _cache_max_dias:
            _cache_max_dias[qtdeDiasDoMes] = int(np.ceil(qtdeDiasDoMes / 2))

        if np.any(np.sum(individuo, axis=1) > _cache_max_dias[qtdeDiasDoMes]):
            return False

        # verificação se não há 1's consecutivos
        array_ultimos_dias = np.array([funcionario[-1] for funcionario in dadosFuncionarios])
        matriz_comparacao = np.hstack((array_ultimos_dias.reshape(-1, 1), individuo))
        consecutivos = (matriz_comparacao[:, 1:] == 1) & (matriz_comparacao[:, :-1] == 1)
        if np.any(consecutivos):
            return False

    else:
        pass #implementar para reescala depois


    return True