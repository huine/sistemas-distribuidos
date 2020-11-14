def calcular_cpf(cpf):
    """Calcula os digitos de um cpf."""
    r1 = range(10, 1, -1)
    r2 = range(11, 1, -1)

    v1 = 11 - (sum(item[0] * item[1] for item in zip(cpf, r1)) % 11)
    if v1 >= 10:
        v1 = 0

    cpf.append(v1)

    v2 = 11 - (sum(item[0] * item[1] for item in zip(cpf, r2)) % 11)
    if v2 >= 10:
        v2 = 0
    cpf.append(v2)

    tmp = ''.join([str(i) for i in cpf])

    return '%s-%s%s\n' % (tmp[:-2], tmp[-2], tmp[-1])


def calcular_cnpj(cnpj):
    """Calcula os digitos de um cnpj."""
    seq = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    v1 = 11 - (sum(item[0] * item[1] for item in zip(cnpj, seq[1:])) % 11)
    if v1 >= 10:
        v1 = 0

    cnpj.append(v1)

    v2 = 11 - (sum(item[0] * item[1] for item in zip(cnpj, seq)) % 11)
    if v2 >= 10:
        v2 = 0
    cnpj.append(v2)

    tmp = ''.join([str(i) for i in cnpj])

    return '%s-%s%s\n' % (tmp[:-2], tmp[-2], tmp[-1])
