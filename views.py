def menu_principal():
    print("\n===== MENU PRINCIPAL =====")
    print("1 - Gerenciar Escolas")
    print("2 - Gerenciar Unidades")
    print("3 - Gerenciar Turmas")
    print("4 - Gerenciar Usuários")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def mostrar_escolas(lista):
    print("\n--- Lista de Escolas ---")
    for escola in lista:
        print(escola)
