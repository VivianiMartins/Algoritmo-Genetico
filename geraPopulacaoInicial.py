import numpy as np
from avalicoesEvalidacoes.validaSolucao import validaSolucao  # Ajuste o caminho se necessário

_cache_max_dias = {}

def geraPopulacaoInicial(funcionarios, qtde_individuos, num_dias_mes, tipo, dia_reescala_inicio, dia_reescala_fim, turno, farmaceuticos, auxiliares):
    """
    Gera população inicial válida para algoritmo genético de escalas de trabalho,
    dimensão: (funcionarios, num_dias_mes, qtde_individuos)
    """

    if num_dias_mes not in _cache_max_dias:
        _cache_max_dias[num_dias_mes] = int(np.ceil(num_dias_mes / 2))
    max_dias_trabalhados = _cache_max_dias[num_dias_mes]

    ultimos_dias_anteriores = funcionarios[:, -1].astype(int)

    qtde_pessoas_do_turno = funcionarios.shape[0]
    populacao = np.zeros((qtde_pessoas_do_turno, num_dias_mes, qtde_individuos), dtype=np.int8)

    for cont_individuo in range(qtde_individuos):
        for cont_pessoa in range(qtde_pessoas_do_turno):
            prev_historico = ultimos_dias_anteriores[cont_pessoa]
            dados_funcionario = funcionarios[cont_pessoa, :]

            if tipo == 1:
                funcionario = np.zeros(num_dias_mes, dtype=np.int8)
                cont_dias_trabalhados = 0
                prev = prev_historico

                for d in range(num_dias_mes):
                    if cont_dias_trabalhados >= max_dias_trabalhados:
                        break
                    if prev == 1:
                        prev = 0
                    else:
                        trabalha = np.random.random() > 0.3
                        if trabalha:
                            funcionario[d] = 1
                            cont_dias_trabalhados += 1
                            prev = 1
                        else:
                            prev = 0
            else:
                funcionario = dados_funcionario[:num_dias_mes].astype(np.int8)

            populacao[cont_pessoa, :, cont_individuo] = funcionario

        populacao[:, :, cont_individuo] = validaSolucao(individuo=populacao[:, :, cont_individuo], num_dias_mes=num_dias_mes, tipo=tipo, funcionarios=funcionarios, turno=turno, farmaceuticos=farmaceuticos, auxiliares=auxiliares)

    return populacao