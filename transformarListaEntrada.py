import numpy as np

def validar_valor_inteiro(valor, nome, indice=None):
    """
    Valida e converte um valor para inteiro, com tratamento robusto de tipos.

    Args:
        valor: Valor a ser validado (int, float, str)
        nome: Nome do campo para mensagens de erro (ex: "inicio", "fim", "dia")
        indice: Índice opcional para dias (ex: 1 para dia 1)

    Returns:
        int: Valor convertido ou 0 em caso de erro
    """
    try:
        if isinstance(valor, int):
            return valor
        elif isinstance(valor, float):
            if valor == int(valor):
                return int(valor)
            else:
                raise ValueError(f"{nome} deve ser inteiro, recebido float: {valor}")
        elif isinstance(valor, str):
            return int(float(valor))
        else:
            raise ValueError(f"Tipo inválido para {nome}: {type(valor)}")
    except (ValueError, TypeError) as e:
        msg = f"ERRO ao processar {nome}"
        if indice is not None:
            msg += f" {indice}"
        print(f"{msg}: {e}")
        return 0


def transformarListaEntrada(listaFuncionarios):
    """
    Transforma a lista de funcionários em matrizes separadas por turno
    ESTRUTURA DA LISTA DO CSV (SEM CABEÇALHO): Nome | Cargo | Turno | Inicio | Fim | Dias do mês
    ESTRUTURA DA LISTA DE SAÍDA: Cargo (1=Farmacêutico ou 2=Auxiliar) | Turno (1=Diurno ou 2=Noturno) | Inicio (inteiro) | Fim (inteiro) | Dias do mês (0 ou 1)

    Retorna:
      funcionariosDiurnos: matriz [funcionários x colunas_dados]
      funcionariosNoturnos: matriz [funcionários x colunas_dados]
      numDiasMes: número de dias do mês
      nomesDiurnos: lista de tuplas (nome, cargo_numerico) para diurnos
      nomesNoturnos: lista de tuplas (nome, cargo_numerico) para noturnos
    """
    contDiurnos = 0
    contNoturnos = 0

    numLinhas = len(listaFuncionarios)
    numColunas = len(listaFuncionarios[0]) if numLinhas > 0 else 0

    numFuncionarios = numLinhas
    numDiasMes = numColunas - 5
    numColunasMatriz = 4 + numDiasMes

    matrizTemp_Diurnos = np.zeros((numFuncionarios, numColunasMatriz))
    matrizTemp_Noturnos = np.zeros((numFuncionarios, numColunasMatriz))

    nomesDiurnos = []
    nomesNoturnos = []

    for cont in range(numLinhas):
        nome = listaFuncionarios[cont][0].strip()  # Nome do funcionário
        cargo = listaFuncionarios[cont][1].strip().lower()
        cargoNumerico = 1 if cargo in ["farmacêutico", "farmaceutico"] else 2

        turno = listaFuncionarios[cont][2].strip().lower()

        inicio = validar_valor_inteiro(listaFuncionarios[cont][3], "inicio", cont)
        fim = validar_valor_inteiro(listaFuncionarios[cont][4], "fim", cont)

        dias_raw = listaFuncionarios[cont][5:5 + numDiasMes]
        diasDoMes = [validar_valor_inteiro(d, "dia", d_idx + 1) for d_idx, d in enumerate(dias_raw)]

        if turno == "diurno":
            matrizTemp_Diurnos[contDiurnos, 0] = cargoNumerico
            matrizTemp_Diurnos[contDiurnos, 1] = 1
            matrizTemp_Diurnos[contDiurnos, 2] = inicio
            matrizTemp_Diurnos[contDiurnos, 3] = fim
            matrizTemp_Diurnos[contDiurnos, 4:] = diasDoMes
            nomesDiurnos.append((nome, cargoNumerico))
            contDiurnos += 1
        else:
            matrizTemp_Noturnos[contNoturnos, 0] = cargoNumerico
            matrizTemp_Noturnos[contNoturnos, 1] = 2
            matrizTemp_Noturnos[contNoturnos, 2] = inicio
            matrizTemp_Noturnos[contNoturnos, 3] = fim
            matrizTemp_Noturnos[contNoturnos, 4:] = diasDoMes
            nomesNoturnos.append((nome, cargoNumerico))
            contNoturnos += 1

    funcionariosDiurnos = matrizTemp_Diurnos[:contDiurnos, :]
    funcionariosNoturnos = matrizTemp_Noturnos[:contNoturnos, :]

    return funcionariosDiurnos, funcionariosNoturnos, numDiasMes, nomesDiurnos, nomesNoturnos