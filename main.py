from views import menu_principal
from controllers import adicionar_escola

def main():
    while True:
        opcao = menu_principal()
        if opcao == "1":
            adicionar_escola()
        elif opcao == "0":
            print("👋 Encerrando...")
            break
        else:
            print("⚠ Opção inválida")

if __name__ == "__main__":
    main()
