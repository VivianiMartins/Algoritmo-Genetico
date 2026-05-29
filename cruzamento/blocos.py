import numpy as np
from avalicoesEvalidacoes.validaSolucao import validaSolucao

def blocos(selecionados, populacao, funcionarios, qtde_individuos, qtd_blocos, turno, farmaceuticos, auxiliares, num_dias_mes, tipo):
    """
    Cruzamento dos indivíduos selecionados utilizando blocos:
    O bloco 1 para os farmacêuticos: sorteio entre todos, sem perder a ordem.
    O bloco dos auxiliares: sorteado entre a 'qtd_blocos' definida,
    mantendo a ordem dentro de cada bloco.
    """
    individuosSelecionados = populacao[:, :, selecionados]
    num_pais_selecionados = individuosSelecionados.shape[2]
    num_funcionarios_total = individuosSelecionados.shape[0]
    filhos_gerados = []

    padroes_farm = np.random.randint(0, 2, size=(qtde_individuos, farmaceuticos))
    padroes_aux = np.random.randint(0, 2, size=(qtde_individuos, qtd_blocos))
    blocos_linhas = np.array_split(np.arange(auxiliares), qtd_blocos)

    for filho_idx in range(qtde_individuos):
        idx_p1, idx_p2 = np.random.choice(num_pais_selecionados, size=2, replace=False)

        pai_1 = individuosSelecionados[:, :, idx_p1]
        pai_2 = individuosSelecionados[:, :, idx_p2]

        farms_1 = pai_1[:farmaceuticos, :]
        auxiliares_1 = pai_1[farmaceuticos:, :]
        farms_2 = pai_2[:farmaceuticos, :]
        auxiliares_2 = pai_2[farmaceuticos:, :]

        filho_farm = np.zeros_like(farms_1)
        filho_aux = np.zeros_like(auxiliares_1)

        # farmacêuticos
        for linha in range(farmaceuticos):
            if padroes_farm[filho_idx, linha] == 0:
                filho_farm[linha, :] = farms_1[linha, :]
            else:
                filho_farm[linha, :] = farms_2[linha, :]

        # auxiliares
        for b, indices_bloco in enumerate(blocos_linhas):
            if padroes_aux[filho_idx, b] == 0:
                filho_aux[indices_bloco, :] = auxiliares_1[indices_bloco, :]
            else:
                filho_aux[indices_bloco, :] = auxiliares_2[indices_bloco, :]

        filho_completo = np.vstack((filho_farm, filho_aux))

        eh_valido = validaSolucao(filho_completo, num_dias_mes, tipo, funcionarios, turno, farmaceuticos, auxiliares)

        filhos_gerados.append(eh_valido)

    if len(filhos_gerados) > 0:
        filhos_finais = np.stack(filhos_gerados, axis=2)
        if filhos_finais.shape[2] != qtde_individuos:
            print(f"Aviso do Cruzamento: Foram gerados {filhos_finais.shape[2]} filhos válidos "
                  f"de um total esperado de {qtde_individuos}.")
    else:
        filhos_finais = np.empty((num_funcionarios_total, num_dias_mes, 0))
        print("Aviso Crítico: Nenhum filho gerado passou nas regras de validação!")

    return filhos_finais