import numpy as np

def torneio(resultado_fitness, qtd_pais, tamanho_grupos_torneios):
    """
    Seleção da população, utilizando a estratégia de seleção por torneio
    """

    selecionados = np.arange(len(resultado_fitness)).tolist()

    if len(selecionados) <= qtd_pais:
        selecionados.sort(key=lambda idx: resultado_fitness[idx], reverse=True)
        return selecionados

    np.random.shuffle(selecionados)

    while len(selecionados) > qtd_pais:
        tamanho = len(selecionados)
        vencedores_estimados = (tamanho + tamanho_grupos_torneios - 1) // tamanho_grupos_torneios

        if (tamanho <= (tamanho_grupos_torneios * 2 - 1)) or (vencedores_estimados < qtd_pais):
            while len(selecionados) > qtd_pais:
                if (len(selecionados) + 1) // 2 < qtd_pais:
                    confrontos_necessarios = len(selecionados) - qtd_pais
                    proxima_fase = []

                    for i in range(0, 2 * confrontos_necessarios, 2):
                        dupla = selecionados[i:i + 2]
                        fitness_sub = np.asarray(resultado_fitness)[dupla]
                        order = np.argsort(fitness_sub)[::-1]
                        dupla = [dupla[i] for i in order]
                        proxima_fase.append(dupla[0])

                    proxima_fase.extend(selecionados[2 * confrontos_necessarios:])
                    selecionados = proxima_fase
                else:
                    proxima_fase = []
                    for i in range(0, len(selecionados), 2):
                        dupla = selecionados[i:i + 2]
                        fitness_sub = np.asarray(resultado_fitness)[dupla]
                        order = np.argsort(fitness_sub)[::-1]
                        dupla = [dupla[i] for i in order]
                        proxima_fase.append(dupla[0])
                    selecionados = proxima_fase
            break

        # -----------------------------------------------------------------
        # Torneio Padrão - grupos
        # -----------------------------------------------------------------
        proxima_fase = []

        for i in range(0, len(selecionados), tamanho_grupos_torneios):
            grupo = selecionados[i:i + tamanho_grupos_torneios]
            fitness_sub = np.asarray(resultado_fitness)[grupo]
            order = np.argsort(fitness_sub)[::-1]
            grupo = [grupo[i] for i in order]
            proxima_fase.append(grupo[0])

        selecionados = proxima_fase

    return selecionados[:qtd_pais]