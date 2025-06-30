import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tVer Extrato
    [nc]\tCriar nova conta
    [lc]\tListar contas
    [nu]\tCadastrar novo usuário
    [q]\tSair do sistema
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo_atual, valor, historico_transacoes, /):
    if valor > 0:
        saldo_atual += valor
        historico_transacoes += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito efetuado com sucesso! ===")
    else:
        print("\n@@@ Falha! Valor de depósito inválido. @@@")

    return saldo_atual, historico_transacoes


def sacar(*, saldo_atual, valor, historico_transacoes, limite_saque, qtd_saques_realizados, limite_saques):
    saldo_insuficiente = valor > saldo_atual
    excede_limite = valor > limite_saque
    ultrapassa_saques = qtd_saques_realizados >= limite_saques

    if saldo_insuficiente:
        print("\n@@@ Saldo insuficiente para realizar o saque. @@@")

    elif excede_limite:
        print("\n@@@ O valor excede o limite permitido por saque. @@@")

    elif ultrapassa_saques:
        print("\n@@@ Limite diário de saques atingido. @@@")

    elif valor > 0:
        saldo_atual -= valor
        historico_transacoes += f"Saque:\t\tR$ {valor:.2f}\n"
        qtd_saques_realizados += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Valor inválido. Informe um valor positivo. @@@")

    return saldo_atual, historico_transacoes, qtd_saques_realizados


def exibir_extrato(saldo_atual, /, *, historico_transacoes):
    print("\n================ EXTRATO ================")
    print("Nenhuma movimentação encontrada." if not historico_transacoes else historico_transacoes)
    print(f"\nSaldo disponível:\tR$ {saldo_atual:.2f}")
    print("==========================================")


def criar_usuario(lista_usuarios):
    cpf = input("Digite o CPF (apenas números): ")
    usuario = buscar_usuario(cpf, lista_usuarios)

    if usuario:
        print("\n@@@ Já existe um usuário com esse CPF. @@@")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, número - bairro - cidade/UF): ")

    lista_usuarios.append({
        "nome": nome,
        "data_nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("\n=== Usuário cadastrado com sucesso! ===")


def buscar_usuario(cpf, lista_usuarios):
    filtrados = [usuario for usuario in lista_usuarios if usuario["cpf"] == cpf]
    return filtrados[0] if filtrados else None


def criar_conta(agencia, numero_conta, lista_usuarios):
    cpf = input("Digite o CPF do titular: ")
    usuario = buscar_usuario(cpf, lista_usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ CPF não encontrado. Cadastro da conta cancelado. @@@")
    return None


def listar_contas(lista_contas):
    for conta in lista_contas:
        dados = f"""\n
        Agência:\t{conta['agencia']}
        Conta:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(dados))


def main():
    LIMITE_SAQUES_DIARIO = 3
    NUM_AGENCIA = "0001"

    saldo_atual = 0
    limite_saque = 500
    historico_transacoes = ""
    qtd_saques_realizados = 0
    lista_usuarios = []
    lista_contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor a depositar: "))
            saldo_atual, historico_transacoes = depositar(saldo_atual, valor, historico_transacoes)

        elif opcao == "s":
            valor = float(input("Informe o valor para saque: "))
            saldo_atual, historico_transacoes, qtd_saques_realizados = sacar(
                saldo_atual=saldo_atual,
                valor=valor,
                historico_transacoes=historico_transacoes,
                limite_saque=limite_saque,
                qtd_saques_realizados=qtd_saques_realizados,
                limite_saques=LIMITE_SAQUES_DIARIO,
            )

        elif opcao == "e":
            exibir_extrato(saldo_atual, historico_transacoes=historico_transacoes)

        elif opcao == "nu":
            criar_usuario(lista_usuarios)

        elif opcao == "nc":
            numero_conta = len(lista_contas) + 1
            conta = criar_conta(NUM_AGENCIA, numero_conta, lista_usuarios)

            if conta:
                lista_contas.append(conta)

        elif opcao == "lc":
            listar_contas(lista_contas)

        elif opcao == "q":
            print("\n=== Saindo... Obrigado por utilizar nosso sistema bancário! ===")
            break

        else:
            print("\n@@@ Opção inválida. Escolha novamente. @@@")

main()
