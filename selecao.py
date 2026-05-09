import numpy as np

def selecao(resultadoFitness, qtd_pais):
    """
        Seleção da população, utilizando a estratégia de seleção por roleta

        Entrada:
          resultadoFitness: array 1D com os valores de fitness de cada indivíduo da população
          qtd_pais: quantidade de indivíduos a selecionar, sempre PAR

        Saída:
              selecionados: array contendo os indivíduos selecionados
        """

    probabilidades = np.zeros(len(resultadoFitness))
    validos_mask = resultadoFitness != -np.inf #garante -inf com probabilidade 0

    if np.sum(validos_mask) < qtd_pais:
        raise ValueError("Erro: Não há indivíduos válidos suficientes para a seleção!")

    fitness_validos = np.copy(resultadoFitness[validos_mask])

    soma_total = np.sum(fitness_validos)
    if soma_total == 0:
        soma_total += 1e-10  # Evita divisão por zero

    probabilidades[validos_mask] = fitness_validos / soma_total
    indices_populacao = np.arange(len(resultadoFitness))

    # Essa é uma que constrói a roleta, calcula as fatias e já faz os sorteios. Tira o que já foi selecionado, com o replace=false.
    selecionados = np.random.choice( a=indices_populacao, size=qtd_pais, replace=False, p=probabilidades)

    return selecionados.tolist()