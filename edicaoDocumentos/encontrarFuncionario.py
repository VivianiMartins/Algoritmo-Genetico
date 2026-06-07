def encontrarFuncionario(lista_funcionarios, funcionario):
    """
    Procura 'funcionario' na primeira coluna de cada linha de 'lista_funcionarios'.
    """
    funcionario_proc = funcionario.strip().lower()

    match = next(((idx, linha) for idx, linha in enumerate(lista_funcionarios) if str(linha[0]).strip().lower() == funcionario_proc), None)

    if match is None:
        print(f"\n>> Funcionário não encontrado para reescala <<")
        return [], 0, 0

    id_troca = match[0]
    funcionario_troca = match[1]
    cargo_nome = str(funcionario_troca[1]).strip().lower()
    cargo_troca = 1 if cargo_nome in ["farmacêutico", "farmaceutico"] else 2

    return funcionario_troca, id_troca, cargo_troca