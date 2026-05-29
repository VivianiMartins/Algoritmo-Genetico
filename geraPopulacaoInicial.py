import numpy as np

_cache_max_dias = {}
_cache_dias_disponiveis = {}

def geraPopulacaoInicial(funcionarios, qtde_individuos, num_dias_mes, tipo, dia_reescala_inicio, dia_reescala_fim):
    """
    Gera população inicial para algoritmo genético de escalas de trabalho, dimensão: (funcionarios, num_dias_mes, qtde_individuos)
    """

    if num_dias_mes not in _cache_max_dias:
        _cache_max_dias[num_dias_mes] = int(np.ceil(num_dias_mes / 2))
    max_dias_trabalhados = _cache_max_dias[num_dias_mes]

    if num_dias_mes not in _cache_dias_disponiveis:
        _cache_dias_disponiveis[num_dias_mes] = np.arange(1, num_dias_mes + 1)
    dias_disponiveis = _cache_dias_disponiveis[num_dias_mes]

    template_zero = np.zeros(num_dias_mes, dtype=np.int8)
    ultimos_dias_anteriores = funcionarios[:, -1].astype(int)

    qtde_pessoas_do_turno = funcionarios.shape[0]
    populacao = np.zeros((qtde_pessoas_do_turno, num_dias_mes, qtde_individuos), dtype=np.int8)

    for contIndividuo in range(qtde_individuos):
        for contPessoa in range(qtde_pessoas_do_turno):
            prev_historico = ultimos_dias_anteriores[contPessoa]
            dados_funcionario = funcionarios[contPessoa, :]

            if tipo == 1:
                funcionario = template_zero.copy()
                cont_dias_trabalhados = 0
                prev = prev_historico

                for d in dias_disponiveis:
                    if cont_dias_trabalhados >= max_dias_trabalhados:
                        break
                    if prev == 1:
                        prev = 0
                    else:
                        trabalha = np.random.random() > 0.3
                        funcionario[d - 1] = int(trabalha)
                        if trabalha:
                            cont_dias_trabalhados += 1
                            prev = 1
                        else:
                            prev = 0
            else:
                funcionario = dados_funcionario[contPessoa:]

            populacao[contPessoa, :, contIndividuo] = funcionario

    return populacao
