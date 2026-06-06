def encontrarFuncionario(lista_funcionarios, funcionario, num_linhas):
    """
    Procura 'funcionario' na primeira coluna de cada linha de 'lista_funcionarios'.
    """
    funcionario_proc = funcionario.strip().lower()
    funcionarios_troca = []
    ids_troca = []
    cargo_troca = []

    for idx in range(num_linhas):
        nome = lista_funcionarios[idx]
        temp = str(nome).strip().lower()

        if funcionario_proc == temp:
            funcionarios_troca.append(lista_funcionarios[idx])
            ids_troca.append(idx)
            cargo = lista_funcionarios[idx][1].strip().lower()
            cargo_numerico = 1 if cargo in ["farmacêutico", "farmaceutico"] else 2
            cargo_troca.append(cargo_numerico)

    if len(funcionarios_troca) == 0: print(f"\n>> Funcionário não encontrado para reescala <<")

    return funcionarios_troca, ids_troca, cargo_troca