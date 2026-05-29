import numpy as np

def maximax_maximin(resultado_fitness, qtd_pais):
    """
    Seleção de pais utilizando o método MX Parent Selection - Maximax e Maximin.

    """
    selecionados = []
    populacao_total = np.arange(len(resultado_fitness)).tolist()

    while len(selecionados) < qtd_pais:
        populacao_total.sort(key=lambda idx: resultado_fitness[idx])
        tamanho_subpopulacao = max(2, len(populacao_total) // 2)

        sub_populacao = populacao_total[:tamanho_subpopulacao]
        sub_populacao.sort(key=lambda idx: resultado_fitness[idx])

        metade = len(sub_populacao) // 2
        grupo_minimo = sub_populacao[:metade]
        grupo_maximo = sub_populacao[metade:]

        maximax = max(grupo_maximo, key=lambda idx: resultado_fitness[idx])
        maximin = max(grupo_minimo, key=lambda idx: resultado_fitness[idx])

        if len(selecionados) < qtd_pais:
            selecionados.append(maximax)
            if maximax in populacao_total:
                populacao_total.remove(maximax)

        if len(selecionados) < qtd_pais:
            selecionados.append(maximin)
            if maximin in populacao_total:
                populacao_total.remove(maximin)

        if len(populacao_total) < 2:
            populacao_total = np.arange(len(resultado_fitness)).tolist()

    return selecionados