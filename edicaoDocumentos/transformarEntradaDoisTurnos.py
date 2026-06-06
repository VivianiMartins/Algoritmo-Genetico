import numpy as np
from edicaoDocumentos.validarValorInteiro import validarValorInteiro

def transformarEntradaDoisTurnos(lista_funcionarios):
    """
    Transforma a lista de funcionários em matrizes separadas por turno
    ESTRUTURA DA LISTA DO CSV (SEM CABEÇALHO): Nome | Cargo | Turno | Inicio | Fim | Dias do mês
    """
    cont_diurnos = 0
    cont_noturnos = 0

    num_linhas = len(lista_funcionarios)
    num_colunas = len(lista_funcionarios[0]) if num_linhas > 0 else 0

    num_funcionarios = num_linhas
    num_dias_mes = num_colunas - 5
    num_colunas_matriz = 4 + num_dias_mes
    farmaceuticos_diurnos = 0
    farmaceuticos_noturnos = 0
    auxiliares_diurnos = 0
    auxiliares_noturnos = 0

    matriz_temp_diurnos = np.zeros((num_funcionarios, num_colunas_matriz))
    matriz_temp_noturnos = np.zeros((num_funcionarios, num_colunas_matriz))

    nomes_diurnos = []
    nomes_noturnos = []

    for cont in range(num_linhas):
        nome = lista_funcionarios[cont][0].strip()  # Nome do funcionário
        cargo = lista_funcionarios[cont][1].strip().lower()
        cargo_numerico = 1 if cargo in ["farmacêutico", "farmaceutico"] else 2
        ultimo_dia_mes = lista_funcionarios[cont][-1]

        turno = lista_funcionarios[cont][2].strip().lower()

        inicio = validarValorInteiro(lista_funcionarios[cont][3], "inicio", cont)
        fim = validarValorInteiro(lista_funcionarios[cont][4], "fim", cont)

        dias_raw = lista_funcionarios[cont][5:5 + num_dias_mes]
        dias_do_mes = [validarValorInteiro(d, "dia", d_idx + 1) for d_idx, d in enumerate(dias_raw)]

        if turno == "diurno":
            if cargo_numerico == 1:
                farmaceuticos_diurnos += 1
            else:
                auxiliares_diurnos += 1

            matriz_temp_diurnos[cont_diurnos, 0] = cargo_numerico
            matriz_temp_diurnos[cont_diurnos, 1] = 1
            matriz_temp_diurnos[cont_diurnos, 2] = inicio
            matriz_temp_diurnos[cont_diurnos, 3] = fim
            matriz_temp_diurnos[cont_diurnos, 4:] = dias_do_mes
            nomes_diurnos.append((nome, cargo_numerico, ultimo_dia_mes, inicio, fim))
            cont_diurnos += 1
        else:
            if cargo_numerico == 1:
                farmaceuticos_noturnos += 1
            else:
                auxiliares_noturnos += 1

            matriz_temp_noturnos[cont_noturnos, 0] = cargo_numerico
            matriz_temp_noturnos[cont_noturnos, 1] = 2
            matriz_temp_noturnos[cont_noturnos, 2] = inicio
            matriz_temp_noturnos[cont_noturnos, 3] = fim
            matriz_temp_noturnos[cont_noturnos, 4:] = dias_do_mes
            nomes_noturnos.append((nome, cargo_numerico, ultimo_dia_mes, inicio, fim))
            cont_noturnos += 1

    funcionarios_diurnos = matriz_temp_diurnos[:cont_diurnos, :]
    funcionarios_noturnos = matriz_temp_noturnos[:cont_noturnos, :]

    return funcionarios_diurnos, funcionarios_noturnos, num_dias_mes, nomes_diurnos, nomes_noturnos, farmaceuticos_diurnos, farmaceuticos_noturnos, auxiliares_diurnos, auxiliares_noturnos