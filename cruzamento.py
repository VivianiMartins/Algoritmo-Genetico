import numpy as np
from validaSolucao import validaSolucao

def cruzamento(selecionados, populacao, dadosFuncionarios, qtd_filhos, quantidade_blocos, turno, farmaceuticos, auxiliares, numDiasMes):
    """
    Cruzamento dos indivíduos selecionados utilizando blocos:
    O bloco 1 para os farmacêuticos: sorteio entre todos, sem perder a ordem.
    O bloco dos auxiliares: sorteado entre a 'quantidade_blocos' definida,
    mantendo a ordem dentro de cada bloco.
    """
    individuosSelecionados = populacao[:, :, selecionados]
    num_pais_selecionados = individuosSelecionados.shape[2]
    num_funcionarios_total = individuosSelecionados.shape[0]
    filhos_gerados = []

    for i in range(0, num_pais_selecionados - 1, 2):
        pai_1 = individuosSelecionados[:, :, i]
        pai_2 = individuosSelecionados[:, :, i+1]

        farms_1 = pai_1[:farmaceuticos, :]
        auxiliares_1 = pai_1[farmaceuticos:, :]
        farms_2 = pai_2[:farmaceuticos, :]
        auxiliares_2 = pai_2[farmaceuticos:, :]

        padroes_farm = np.random.randint(0, 2, size=(qtd_filhos, farmaceuticos)) # Sorteio interno do Bloco 1 (3 moedas, uma para cada farmacêutico)
        padroes_aux = np.random.randint(0, 2, size=(qtd_filhos, quantidade_blocos)) # Sorteio dos quantidade_blocos de auxiliares (quantidade_blocos moedas, uma por bloco)

        blocos_linhas = np.array_split(np.arange(auxiliares), quantidade_blocos) #divide a fila sequencial de auxiliares na quantidade_blocos

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
            for b, indices_bloco in enumerate(blocos_linhas):
                if padroes_aux[filho_idx, b] == 0:
                    filho_aux[indices_bloco, :] = auxiliares_1[indices_bloco, :]
                else:
                    filho_aux[indices_bloco, :] = auxiliares_2[indices_bloco, :]

            filho_completo = np.vstack((filho_farm, filho_aux))

            eh_valido = validaSolucao(filho_completo, numDiasMes, 1, dadosFuncionarios, turno, farmaceuticos, auxiliares)

            filhos_gerados.append(eh_valido)

    if len(filhos_gerados) > 0:
        filhos_finais = np.stack(filhos_gerados, axis=2)
        qtde_total_filhos_esperada = (num_pais_selecionados // 2) * qtd_filhos

        if filhos_finais.shape[2] != qtde_total_filhos_esperada:
            print(f"Aviso do Cruzamento: Foram gerados {filhos_finais.shape[2]} filhos válidos "
                  f"de um total esperado de {qtde_total_filhos_esperada}.")
    else:
        filhos_finais = np.empty((num_funcionarios_total, numDiasMes, 0))
        print("Aviso Crítico: Nenhum filho gerado passou nas regras de validação!")

    return filhos_finais