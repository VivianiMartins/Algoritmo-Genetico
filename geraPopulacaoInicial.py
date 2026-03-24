import numpy as np
from validaSolucao import validaSolucao

def geraPopulacaoInicial(funcionariosDoTurno, qtdeIndividuos, qtdeDiasDoMes, escala, diaReescala):
    """
    Gera população inicial para algoritmo genético de escalas de trabalho

    Entrada:
      funcionariosDoTurno: matriz com dados dos funcionários
                          [Cargo, Turno, Inicio, Fim, Dia1, Dia2, ..., DiaN]
      qtdeIndividuos: número de indivíduos (soluções) na população
      qtdeDiasDoMes: número de dias no mês
      escala: 1 para escala (gera do zero), 0 para reescala (usa dias existentes)

    Saída:
      populacao: matriz 3D [qtdeFuncionarios x qtdeDiasDoMes x qtdeIndividuos]
                Cada fatia populacao[:,:,i] é um indivíduo (escala completa)
                Linhas: funcionários | Colunas: dias do mês
                Valores: 0 (não trabalha) ou 1 (trabalha)
    """
    # Parâmetros
    qtdePessoasDoTurno = funcionariosDoTurno.shape[0]

    # Inicializa a população 3D
    # Dimensões: [funcionários, dias, indivíduos]
    populacao = np.zeros((qtdePessoasDoTurno, qtdeDiasDoMes, qtdeIndividuos))

    print('Gerando população inicial...')
    print(f'Funcionários: {qtdePessoasDoTurno} | Dias: {qtdeDiasDoMes} | Indivíduos: {qtdeIndividuos}')

    # Gera cada indivíduo da população
    for contIndividuo in range(qtdeIndividuos):
        # Para cada funcionário neste indivíduo
        for contPessoa in range(qtdePessoasDoTurno):
            if escala == 1:
                # ESCALA: Gera escala inicial vazia (do zero)
                individuo = np.zeros(qtdeDiasDoMes)
            else:
                # REESCALA: Usa os dias já existentes do funcionário
                # Os dias estão da posição 5 em diante em funcionariosDoTurno
                individuo = funcionariosDoTurno[contPessoa, 4:].copy()

            # Valida e ajusta a solução de acordo com as regras
            individuo = validaSolucao(individuo, funcionariosDoTurno[contPessoa, :], qtdeDiasDoMes, escala)

            # Armazena a escala deste funcionário neste indivíduo
            populacao[contPessoa, :, contIndividuo] = individuo

        # Feedback de progresso a cada 10% dos indivíduos
        if (contIndividuo + 1) % max(1, qtdeIndividuos // 10) == 0:
            print(f'Progresso: {contIndividuo+1}/{qtdeIndividuos} indivíduos gerados ({(contIndividuo+1)/qtdeIndividuos*100:.1f}%)')

    print('População gerada com sucesso!')
    return populacao
