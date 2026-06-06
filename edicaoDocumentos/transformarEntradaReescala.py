from edicaoDocumentos.encontrarFuncionario import encontrarFuncionario

def transformarEntradaReescala(lista_funcionarios, dia_reescala, funcionario):
    """
    Transforma a lista de funcionários em matrizes separadas uma com a escala original até a data da troca, e outra com os dias que tem que haver a troca.
    """
    num_linhas = len(lista_funcionarios)
    num_colunas = len(lista_funcionarios[0]) if num_linhas > 0 else 0

    num_dias_mes = num_colunas - 5
    dias_ok = num_colunas - (num_dias_mes - dia_reescala) - 1
    dias_reescala = dia_reescala - 2 #vai pegar um dia antes para comparar
    reescala = []
    cargos_ok = []
    matriz_para_reescalar = []
    matriz_nao_reescalar = []

    funcionarios_troca, ids_troca, cargo_troca = encontrarFuncionario(lista_funcionarios, funcionario, num_linhas)

    if cargo_troca == 1:
        for linha in lista_funcionarios:
            if str(linha[1]).strip().lower() in ["farmacêutico", "farmaceutico"]:
                reescala.append(linha)
            else:
                cargos_ok.append(linha)
    elif cargo_troca == 2:
        for linha in lista_funcionarios:
            if str(linha[1]).strip().lower() == "auxiliar":
                reescala.append(linha)
            else:
                cargos_ok.append(linha)

    for linha in reescala:
        matriz_nao_reescalar.append(linha[:dias_ok])
        matriz_para_reescalar.append(linha[dias_reescala:])

    return  cargos_ok, matriz_para_reescalar, matriz_nao_reescalar, funcionarios_troca, ids_troca, num_dias_mes, cargo_troca