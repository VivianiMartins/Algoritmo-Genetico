import numpy as np

def elitista(resultado_fitness, qtd_pais):
    """
    Seleção da população, utilizando a estratégia de seleção por elitismo
    """

    indices_ordenados = np.argsort(-resultado_fitness)
    selecionados = indices_ordenados[:qtd_pais]

    return selecionados.tolist()