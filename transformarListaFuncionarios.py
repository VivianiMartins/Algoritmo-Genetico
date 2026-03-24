import numpy as np

def transformarListaFuncionarios(listaFuncionarios):
    """
    Transforma a lista de funcionários em matrizes separadas por turno
    ESTRUTURA DO CSV (SEM CABEÇALHO):
    Coluna 1: Nome
    Coluna 2: Cargo
    Coluna 3: Turno
    Coluna 4: Inicio (numérico)
    Coluna 5: Fim (numérico)
    Colunas 6-35: Dias do mês (1-30)

    ESTRUTURA DA MATRIZ DE SAÍDA:
    Coluna 1: Cargo (1=Farmacêutico, 2=Auxiliar)
    Coluna 2: Turno (1=Diurno, 2=Noturno)
    Coluna 3: Inicio (0 se não existir)
    Coluna 4: Fim (0 se não existir)
    Colunas 5-34: Dias do mês (marcação de trabalho 0 ou 1)
    """
    # Inicializa contadores
    contDiurnos = 0
    contNoturnos = 0

    # Obtém número de linhas e colunas
    numLinhas = len(listaFuncionarios)
    numColunas = len(listaFuncionarios[0]) if numLinhas > 0 else 0

    # Número de funcionários
    numFuncionarios = numLinhas

    # Calcula quantos dias do mês existem no arquivo (total de colunas - 5 colunas fixas)
    numDiasMes = numColunas - 5  # Total - 5 = dias do mês
    numColunasMatriz = 4 + numDiasMes  # Tamanho da matriz de saída (4 dados + dias)

    # Cria matrizes temporárias para armazenar dados de cada turno
    matrizTemp_Diurnos = np.zeros((numFuncionarios, numColunasMatriz))
    matrizTemp_Noturnos = np.zeros((numFuncionarios, numColunasMatriz))

    # Percorre cada funcionário
    for cont in range(numLinhas):
        # Cargo: 1 para farmacêutico, 2 para auxiliar
        cargo = listaFuncionarios[cont][1].strip().lower()
        if cargo in ["farmacêutico", "farmaceutico"]:
            cargoNumerico = 1
        else:
            cargoNumerico = 2

        # Turno: 1 para diurno, 2 para noturno
        turno = listaFuncionarios[cont][2].strip().lower()

        # Inicio (coluna 4)
        inicio_str = listaFuncionarios[cont][3]
        try:
            inicio = float(inicio_str)
        except:
            inicio = 0

        # Fim (coluna 5)
        fim_str = listaFuncionarios[cont][4]
        try:
            fim = float(fim_str)
        except:
            fim = 0

        # Converte os dias do mês (colunas 6 em diante) para numérico
        diasDoMes = []
        for d in range(numDiasMes):
            valor_str = listaFuncionarios[cont][5 + d]
            try:
                valor = float(valor_str)
            except:
                valor = 0
            diasDoMes.append(valor)

        # Armazena dados na matriz correta de acordo com o turno
        if turno == "diurno":
            contDiurnos += 1
            matrizTemp_Diurnos[contDiurnos-1, 0] = cargoNumerico  # Cargo
            matrizTemp_Diurnos[contDiurnos-1, 1] = 1  # Turno diurno
            matrizTemp_Diurnos[contDiurnos-1, 2] = inicio  # Inicio
            matrizTemp_Diurnos[contDiurnos-1, 3] = fim  # Fim
            matrizTemp_Diurnos[contDiurnos-1, 4:] = diasDoMes  # Dias do mês
        else:
            contNoturnos += 1
            matrizTemp_Noturnos[contNoturnos-1, 0] = cargoNumerico  # Cargo
            matrizTemp_Noturnos[contNoturnos-1, 1] = 2  # Turno noturno
            matrizTemp_Noturnos[contNoturnos-1, 2] = inicio  # Inicio
            matrizTemp_Noturnos[contNoturnos-1, 3] = fim  # Fim
            matrizTemp_Noturnos[contNoturnos-1, 4:] = diasDoMes  # Dias do mês

    # Remove linhas vazias (zeros) das matrizes
    funcionariosDiurnos = matrizTemp_Diurnos[:contDiurnos, :]
    funcionariosNoturnos = matrizTemp_Noturnos[:contNoturnos, :]

    return funcionariosDiurnos, funcionariosNoturnos, numDiasMes
