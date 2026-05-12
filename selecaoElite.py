import numpy as np

def selecaoElite(resultadoFitness, qtd_pais):
    """
    Seleção da população, utilizando a estratégia de seleção por elitismo
    """

    indices_ordenados = np.argsort(-resultadoFitness)
    selecionados = indices_ordenados[:qtd_pais]

    return selecionados.tolist()