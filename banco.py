saldo= 0 
depositos= 0
extrato= ""
saques_diarios= 0
QTD_MAX_SAQUES= 3

while True:
    menu= input( '''
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair 

=> ''')
    
    if menu=="d":
        print("Depósito")
        valor= float(input("Insira o valor do depósito: "))
        
        if valor>0:
            saldo+=valor
            extrato= f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Valor inválido.")

    elif menu=="s":
        valor= float(input("Insira o valor para saque: "))
        if saques_diarios>QTD_MAX_SAQUES:
            print("Número de saques máximos atingido.")
        elif valor>saldo:
            print("Saldo Insuficiente.")
        elif valor > 500:
            print("Valor de saque maior que o permitido.")
        elif valor>0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            saques_diarios += 1
        else:
            print("Valor inválido para saque.")

    elif menu== "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif menu== "q":
        print("Sair")
        break
    else: 
        print("Operação Inválida")