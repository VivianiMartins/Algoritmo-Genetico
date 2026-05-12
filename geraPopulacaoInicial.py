import numpy as np

_cache_max_dias = {}
_cache_diasDisponiveis = {}

def geraPopulacaoInicial(funcionariosDoTurno, qtdeIndividuos, qtdeDiasDoMes, tipo, diaReescala):
    """
    Gera população inicial para algoritmo genético de escalas de trabalho, dimensão:
    matriz 3D [qtdeFuncionarios x qtdeDiasDoMes x qtdeIndividuos]
    Cada fatia populacao[:,:,i] é um indivíduo (escala completa)
    Valores: 0 (não trabalha) ou 1 (trabalha)
    População não randômica, pois respeita:
            Não há 1's consecultivos
            Verifica o último dia do mês anterior
            Não ultrapassa o máximo de dias trabalhados por mês
    """

    if qtdeDiasDoMes not in _cache_max_dias:
        _cache_max_dias[qtdeDiasDoMes] = int(np.ceil(qtdeDiasDoMes / 2))
    maxDiasTrabalhados = _cache_max_dias[qtdeDiasDoMes]

    if qtdeDiasDoMes not in _cache_diasDisponiveis:
        _cache_diasDisponiveis[qtdeDiasDoMes] = np.arange(1, qtdeDiasDoMes + 1)
    diasDisponiveis = _cache_diasDisponiveis[qtdeDiasDoMes]

    template_zero = np.zeros(qtdeDiasDoMes, dtype=np.int8)
    ultimos_dias_anteriores = funcionariosDoTurno[:, -1].astype(int)

    qtdePessoasDoTurno = funcionariosDoTurno.shape[0]
    populacao = np.zeros((qtdePessoasDoTurno, qtdeDiasDoMes, qtdeIndividuos), dtype=np.int8)

    for contIndividuo in range(qtdeIndividuos):
        for contPessoa in range(qtdePessoasDoTurno):
            prev_historico = ultimos_dias_anteriores[contPessoa]
            dadosFuncionario = funcionariosDoTurno[contPessoa, :]

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
