import numpy as np

_cache_max_dias = {}
_cache_diasDisponiveis = {}

def geraPopulacaoInicial(funcionarios, qtde_individuos, num_dias_mes, tipo, dia_reescala_inicio, dia_reescala_fim):
    """
    Gera população inicial para algoritmo genético de escalas de trabalho, dimensão: (funcionarios, num_dias_mes, qtde_individuos)
    """

    if num_dias_mes not in _cache_max_dias:
        _cache_max_dias[num_dias_mes] = int(np.ceil(num_dias_mes / 2))
    maxDiasTrabalhados = _cache_max_dias[num_dias_mes]

    if num_dias_mes not in _cache_diasDisponiveis:
        _cache_diasDisponiveis[num_dias_mes] = np.arange(1, num_dias_mes + 1)
    diasDisponiveis = _cache_diasDisponiveis[num_dias_mes]

    template_zero = np.zeros(num_dias_mes, dtype=np.int8)
    ultimos_dias_anteriores = funcionarios[:, -1].astype(int)

    qtdePessoasDoTurno = funcionarios.shape[0]
    populacao = np.zeros((qtdePessoasDoTurno, num_dias_mes, qtde_individuos), dtype=np.int8)

    for contIndividuo in range(qtde_individuos):
        for contPessoa in range(qtdePessoasDoTurno):
            prev_historico = ultimos_dias_anteriores[contPessoa]
            dadosFuncionario = funcionarios[contPessoa, :]

            if tipo == 1:
                funcionario = template_zero.copy()
                contDiasTrabalhados = 0
                prev = prev_historico

                for d in diasDisponiveis:
                    if contDiasTrabalhados >= maxDiasTrabalhados:
                        break
                    if prev == 1:
                        prev = 0
                    else:
                        trabalha = np.random.random() > 0.3
                        funcionario[d - 1] = int(trabalha)
                        if trabalha:
                            contDiasTrabalhados += 1
                            prev = 1
                        else:
                            prev = 0
            else:
                funcionario = dadosFuncionario[contPessoa:]

            populacao[contPessoa, :, contIndividuo] = funcionario

    return populacao
