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

    Saída:
      populacao: matriz 3D [qtdeFuncionarios x qtdeDiasDoMes x qtdeIndividuos]
                Cada fatia populacao[:,:,i] é um indivíduo (escala completa)
                Linhas: funcionários | Colunas: dias do mês
                Valores: 0 (não trabalha) ou 1 (trabalha)
    """
    qtdePessoasDoTurno = funcionariosDoTurno.shape[0]

    populacao = np.zeros((qtdePessoasDoTurno, qtdeDiasDoMes, qtdeIndividuos))

    for contIndividuo in range(qtdeIndividuos):

        for contPessoa in range(qtdePessoasDoTurno):
            if tipo == 1:
                individuo = np.zeros(qtdeDiasDoMes)
            else:
                individuo = funcionariosDoTurno[contPessoa, 4:].copy()

            individuo = validaSolucao(individuo, funcionariosDoTurno[contPessoa, :], qtdeDiasDoMes, tipo)

            populacao[contPessoa, :, contIndividuo] = individuo

        if (contIndividuo + 1) % max(1, qtdeIndividuos // 10) == 0:  # Calcula se é múltiplo de 10%
            print(f'Progresso: {contIndividuo+1}/{qtdeIndividuos} indivíduos gerados ({(contIndividuo+1)/qtdeIndividuos*100:.1f}%)')  # Imprime progresso

    #Salva em arquivo para visualização completa (opcional)
    #np.savetxt('populacao_visualizacao.txt', populacao.reshape(populacao.shape[0] * populacao.shape[2], populacao.shape[1]), fmt='%d', header=f'Populacao {populacao.shape} - Funcionarios x Dias (repetido por individuo)')

    print('População gerada com sucesso!')  # Confirma que terminou
    # Retorna a população gerada
    return populacao
