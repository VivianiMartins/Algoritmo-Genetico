import numpy as np

def cruzamento(selecionados, populacao, qtd_filhos):
    """
    Cruzamento dos indivíduos selecionados utilizando 5 pontos de corte iniciais:
    O bloco 1 para os farmacêuticos, e 4 blocos (quartos) para os auxiliares.
    Dentro do bloco 1 há o sorteio entre todos, sem perder a ordem.
    Os outros são sorteados entre eles, sem perder a ordem dos auxiliares.

    Entrada:
      selecionados: lista ou array contendo os índices dos individuos selecionados
      populacao: array 3D [funcionários x dias x indivíduos]
      qtd_filhos: quantidade de filhos a serem gerados por par de pais

    Saída:
      filhos_finais: array 3D [funcionários x dias x total_de_filhos_gerados]
    """
    individuosSelecionados = populacao[:, :, selecionados]
    farmaceuticos = 3

    num_funcionarios_total = individuosSelecionados.shape[0]
    num_dias = individuosSelecionados.shape[1]
    num_pais_selecionados = individuosSelecionados.shape[2]
    num_auxiliares = num_funcionarios_total - farmaceuticos

    filhos_gerados = []

    for i in range(0, num_pais_selecionados - 1, 2):
        pai_1 = individuosSelecionados[:, :, i]
        pai_2 = individuosSelecionados[:, :, i+1]

        farms_1 = pai_1[:farmaceuticos, :]
        auxiliares_1 = pai_1[farmaceuticos:, :]
        farms_2 = pai_2[:farmaceuticos, :]
        auxiliares_2 = pai_2[farmaceuticos:, :]

        padroes_farm = np.random.randint(0, 2, size=(qtd_filhos, farmaceuticos)) # Sorteio interno do Bloco 1 (3 moedas, uma para cada farmacêutico)
        padroes_aux = np.random.randint(0, 2, size=(qtd_filhos, 4))  # Sorteio dos 4 blocos de auxiliares (4 moedas, uma por bloco)

        quartos_linhas = np.array_split(np.arange(num_auxiliares), 4)

        for filho_idx in range(qtd_filhos):
            filho_farm = np.zeros_like(farms_1)
            filho_aux = np.zeros_like(auxiliares_1)

            # farmacêuticos
            for linha in range(farmaceuticos):
                if padroes_farm[filho_idx, linha] == 0:
                    filho_farm[linha, :] = farms_1[linha, :]
                else:
                    filho_farm[linha, :] = farms_2[linha, :]

           #auxiliares
            for b, indices_bloco in enumerate(quartos_linhas):
                if padroes_aux[filho_idx, b] == 0:
                    filho_aux[indices_bloco, :] = auxiliares_1[indices_bloco, :]
                else:
                    filho_aux[indices_bloco, :] = auxiliares_2[indices_bloco, :]

            filho_completo = np.vstack((filho_farm, filho_aux))
            filhos_gerados.append(filho_completo)


    if len(filhos_gerados) > 0: #validacao das dimensões (passar para validaSolucao e usar as outras validações de lá)
        filhos_finais = np.stack(filhos_gerados, axis=2)
        qtde_total_filhos_esperada = (num_pais_selecionados // 2) * qtd_filhos
        shape_esperado = (num_funcionarios_total, num_dias, qtde_total_filhos_esperada)

        if filhos_finais.shape != shape_esperado:
            raise ValueError(f"ALERTA CRÍTICO: Dimensões corrompidas no cruzamento!\n"
                             f"Esperado: {shape_esperado}\n"
                             f"Obtido:   {filhos_finais.shape}")
    else:
        filhos_finais = np.empty((num_funcionarios_total, num_dias, 0))

    return filhos_finais