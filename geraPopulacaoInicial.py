import numpy as np
from validaSolucao import validaSolucao

def geraPopulacaoInicial(funcionariosDoTurno, qtdeIndividuos, qtdeDiasDoMes, tipo, diaReescala):
    """
    Gera população inicial para algoritmo genético de escalas de trabalho

    Entrada:
      funcionariosDoTurno: matriz com dados dos funcionários
                          [Cargo, Turno, Inicio, Fim, Dia1, Dia2, ..., DiaN]
      qtdeIndividuos: número de indivíduos (soluções) na população
      qtdeDiasDoMes: número de dias no mês
      tipo: 1 para escala (gera do zero), 0 para reescala (usa dias existentes)
      diaReescala: dia para reescala

    Saída:
      populacao: matriz 3D [qtdeFuncionarios x qtdeDiasDoMes x qtdeIndividuos]
                Cada fatia populacao[:,:,i] é um indivíduo (escala completa)
                Linhas: funcionários | Colunas: dias do mês
                Valores: 0 (não trabalha) ou 1 (trabalha)
    """
    qtdePessoasDoTurno = funcionariosDoTurno.shape[0]
    populacao = np.zeros((qtdePessoasDoTurno, qtdeDiasDoMes, qtdeIndividuos), dtype=np.int8)
    template_zero = np.zeros(qtdeDiasDoMes, dtype=np.int8)

    for contIndividuo in range(qtdeIndividuos):
        for contPessoa in range(qtdePessoasDoTurno):
            dados_funcionario = funcionariosDoTurno[contPessoa, :]

            if tipo == 1:
                individuo = template_zero.copy()
            else:
                individuo = dados_funcionario[4:]

            individuo = validaSolucao(individuo, dados_funcionario, qtdeDiasDoMes, tipo)
            populacao[contPessoa, :, contIndividuo] = individuo

    return populacao
