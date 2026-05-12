import numpy as np
from processarLicensa import processar_licensa
from validaSolucao import validaSolucao

_cache_max_dias = {}
_cache_diasDisponiveis = {}  #temporário até usar processa_licensa

def geraPopulacaoInicial(funcionariosDoTurno, qtdeIndividuos, qtdeDiasDoMes, tipo, diaReescala, turno):
    """
    Gera população inicial para algoritmo genético de escalas de trabalho

    Entrada:
      funcionariosDoTurno: matriz com dados dos funcionários
                          [Cargo, Turno, Inicio, Fim, Dia1, Dia2, ..., DiaN]
      qtdeIndividuos: número de indivíduos (soluções) na população
      qtdeDiasDoMes: número de dias no mês
      tipo: 1 para escala (gera do zero), 2 para reescala (usa dias existentes)
      diaReescala: dia para reescala
      turno: 1 para diurno, 0 para reescala (usa dias existentes)

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

    # Parâmetros de negócio (ajuste conforme necessário)
    farmaceuticos = 3
    if turno == 1:
        maxAuxiliar, minAuxiliar = 24, 16
    else:
        maxAuxiliar, minAuxiliar = 15, 12

    contIndividuo = 0

    while contIndividuo < qtdeIndividuos:
        individuo_temp = np.zeros((qtdePessoasDoTurno, qtdeDiasDoMes), dtype=np.int8)

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

            individuo_temp[contPessoa, :] = funcionario

        # Validação do indivíduo
        individuo_reparado = validaSolucao(individuo_temp, qtdeDiasDoMes, tipo, funcionariosDoTurno, turno)

        #Aqui só aceita se estiver em todas as regras
        valido = validaIndividuo(individuo_reparado, ultimos_dias_anteriores, maxDiasTrabalhados, farmaceuticos, minAuxiliar, maxAuxiliar, tipo)

        if valido:
            populacao[:, :, contIndividuo] = individuo_reparado
            contIndividuo += 1
            # print(f"Indivíduo {contIndividuo}/{qtdeIndividuos} gerado com sucesso!")

    return populacao

#Colocar em outro arquivo
def validaIndividuo(individuo_reparado, ultimos_dias_anteriores, maxDiasTrabalhados, farmaceuticos, minAuxiliar, maxAuxiliar, tipo):
    """
    Realiza uma verificação estrita para garantir que o indivíduo não viola nenhuma
    regra de negócio após a fase de reparo.
    """
    valido = True

    if tipo == 1:
        # A. Checa consecutivos (incluindo mês passado)
        matriz_comp = np.hstack((ultimos_dias_anteriores.reshape(-1, 1), individuo_reparado))
        if np.any((matriz_comp[:, 1:] == 1) & (matriz_comp[:, :-1] == 1)):
            valido = False

        # B. Checa limite de dias no mês
        elif np.any(np.sum(individuo_reparado, axis=1) > maxDiasTrabalhados):
            valido = False

        # C. Checa cobertura diária (Min/Max)
        else:
            farm_dia = np.sum(individuo_reparado[:farmaceuticos, :], axis=0)
            aux_dia = np.sum(individuo_reparado[farmaceuticos:, :], axis=0)

            # Se algum dia não tiver exatamente 1 farmacêutico
            if np.any(farm_dia != 1):
                valido = False
            # Se algum dia estiver fora dos limites de auxiliares
            elif np.any(aux_dia < minAuxiliar) or np.any(aux_dia > maxAuxiliar):
                valido = False

    return valido