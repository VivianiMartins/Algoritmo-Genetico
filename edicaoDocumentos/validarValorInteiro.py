def validarValorInteiro(valor, nome, indice=None):
    """
    Valida e converte um valor para inteiro, com tratamento robusto de tipos.
    Valor convertido ou 0 em caso de erro
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
