import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.lista_contas = []

    def realizar_transacao(self, conta_selecionada, operacao):
        operacao.registrar(conta_selecionada)

    def adicionar_conta(self, nova_conta):
        self.lista_contas.append(nova_conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        cliente.adicionar_conta(self)

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
        elif valor <= 0:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
        else:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        return False

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False
        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        total_saques = len([
            t for t in self.historico.transacoes if t["tipo"] == Saque.__name__
        ])

        if valor > self._limite:
            print("\n@@@ Operação falhou! Valor excede limite do saque. @@@")
        elif total_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Limite de saques atingido. @@@")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
    opcoes = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo cliente
    [q]\tSair
    => """
    return input(textwrap.dedent(opcoes))


def buscar_cliente_por_cpf(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)


def selecionar_conta(cliente):
    if not cliente.lista_contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.lista_contas[0]


def operacao_deposito(clientes):
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Valor do depósito: "))
    conta = selecionar_conta(cliente)
    if conta:
        cliente.realizar_transacao(conta, Deposito(valor))


def operacao_saque(clientes):
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Valor do saque: "))
    conta = selecionar_conta(cliente)
    if conta:
        cliente.realizar_transacao(conta, Saque(valor))


def mostrar_extrato(clientes):
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = selecionar_conta(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}")
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def cadastrar_cliente(clientes):
    cpf = input("CPF (somente números): ")
    if buscar_cliente_por_cpf(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ")

    novo_cliente = PessoaFisica(nome, nascimento, cpf, endereco)
    clientes.append(novo_cliente)
    print("\n=== Cliente criado com sucesso! ===")


def criar_nova_conta(numero_conta, clientes, contas):
    cpf = input("CPF do cliente: ")
    cliente = buscar_cliente_por_cpf(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    nova_conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(nova_conta)
    print("\n=== Conta criada com sucesso! ===")


def listar_todas_as_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            operacao_deposito(clientes)
        elif opcao == "s":
            operacao_saque(clientes)
        elif opcao == "e":
            mostrar_extrato(clientes)
        elif opcao == "nu":
            cadastrar_cliente(clientes)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_nova_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_todas_as_contas(contas)
        elif opcao == "q":
            break
        else:
            print("\n@@@ Opção inválida. Tente novamente. @@@")

main()
