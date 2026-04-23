from geraEscalaAlternada import geraEscalaAlternada
from processarLicensa import processar_licensa

def validaSolucao(individuo, dadosFuncionario, qtdeDiasDoMes, tipo):
    """
    Valida e gera uma escala alternada válida para o funcionário, considerando regras.

    Entrada:
      individuo: array numpy com a escala atual [1 x dias] (pode estar vazio/zerado ou preenchido)
      dadosFuncionario: array numpy com [Cargo, Turno, Inicio, Fim, Dias...]
      qtdeDiasDoMes: inteiro, número de dias no mês
      tipo: inteiro, tipo de escala (1=nova, 0=reescala)

    Saída:
      individuoValido: array numpy [1 x dias] com escala válida (0=não trabalha, 1=trabalha)
    """

    # individuoPreValido, diasDisponiveis = processar_licensa(individuo, dadosFuncionario, qtdeDiasDoMes, tipo)

    individuoPreValido = individuo.copy()

    diasDisponiveis = list(range(1, qtdeDiasDoMes + 1)) #temporário até usar processa_licensa
    individuoValido = geraEscalaAlternada(individuoPreValido, diasDisponiveis, qtdeDiasDoMes, tipo, dadosFuncionario)

    return individuoValido
