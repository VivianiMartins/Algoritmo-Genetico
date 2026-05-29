import numpy as np


def maximaxMaximin(resultado_fitness, qtd_pais, qtde_individuos):
    """
    Seleção de pais utilizando o método MX Parent Selection - Maximax e Maximin.
    """
    selecionados = []
    populacao_total = np.arange(qtde_individuos).tolist()

    while len(selecionados) < qtd_pais:

        tamanho_subpopulacao = max(2, qtde_individuos // 2)
        sub_populacao = np.random.choice(populacao_total, size=tamanho_subpopulacao, replace=False).tolist()

        sub_populacao.sort(key=lambda idx: resultado_fitness[idx], reverse=True)

        metade = len(sub_populacao) // 2
        grupo_maximo = sub_populacao[:metade]  # 1ª metade (melhores da sub-população)
        grupo_minimo = sub_populacao[metade:]  # 2ª metade (piores da sub-população)

        maximax = grupo_maximo[0]
        maximin = grupo_minimo[0]

        selecionados.append(maximax)

        if len(selecionados) < qtd_pais:
            selecionados.append(maximin)

    return selecionados