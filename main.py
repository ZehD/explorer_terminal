from file_logger import create_table
from explorer_terminal import terminal_flow
from explorer_gui import start_gui

def main():
    create_table()

    print("Escolha o modo de execução:")
    print("1. Terminal")
    print("2. Interface Gráfica (GUI)")

    choice = input("Digite 1 ou 2: ").strip()

    if choice == "1":
        terminal_flow()
    elif choice == "2":
        start_gui()
    else:
        print("Opção inválida. Encerrando.")

if __name__ == "__main__":
    main()
