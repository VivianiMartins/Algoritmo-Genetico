import numpy as np
from processarLicensa import processar_licensa

_cache_max_dias = {}
_cache_diasDisponiveis = {}  #temporário até usar processa_licensa

def geraPopulacaoInicial(funcionariosDoTurno, qtdeIndividuos, qtdeDiasDoMes, tipo, diaReescala):
    """
    Gera população inicial para algoritmo genético de escalas de trabalho

    Entrada:
      funcionariosDoTurno: matriz com dados dos funcionários
                          [Cargo, Turno, Inicio, Fim, Dia1, Dia2, ..., DiaN]
      qtdeIndividuos: número de indivíduos (soluções) na população
      qtdeDiasDoMes: número de dias no mês
      tipo: 1 para escala (gera do zero), 2 para reescala (usa dias existentes)
      diaReescala: dia para reescala

    Saída:
      populacao: matriz 3D [qtdeFuncionarios x qtdeDiasDoMes x qtdeIndividuos]
                Cada fatia populacao[:,:,i] é um indivíduo (escala completa)
                Linhas: funcionários | Colunas: dias do mês
                Valores: 0 (não trabalha) ou 1 (trabalha)
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

    for contPessoa in range(qtdePessoasDoTurno):
        prev_historico = ultimos_dias_anteriores[contPessoa]
        dadosFuncionario = funcionariosDoTurno[contPessoa, :]

        for contIndividuo in range(qtdeIndividuos):
            if tipo == 1:
                individuo = template_zero.copy()
                contDiasTrabalhados = 0
                prev = prev_historico

                for d in diasDisponiveis:
                    if contDiasTrabalhados >= maxDiasTrabalhados:
                        break
                    if prev == 1:
                        prev = 0
                    else:
                        trabalha = np.random.random() > 0.3
                        individuo[d - 1] = int(trabalha)
                        if trabalha:
                            contDiasTrabalhados += 1
                            prev = 1
                        else:
                            prev = 0
            # ver se ainda vou precisar de usar ValidaSolucao, pq tenho que gerar ela já válida

            else:
                individuo = dadosFuncionario[4:]

            populacao[contPessoa, :, contIndividuo] = individuo

    return populacao
