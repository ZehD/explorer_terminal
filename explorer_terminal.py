import os

def list_directory(path):
    print(f"\n Diretório: {path}\n")
    items = os.listdir(path)
    for idx, item in enumerate(items):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            print(f"{idx}. [DIR]  {item}")
        else:
            print(f"{idx}.       {item}")
    return items

def main():
    current_path = os.getcwd()

    while True:
        items = list_directory(current_path)
        print("\Opções:")
        print(" - Digite o númerodo Folder")
        print(" - '..' para voltar")
        print(" - 'exit' para sair")

        choice = input("Insira a sua escolha: ")

        if choice == "exit":
            break
        elif choice == "..":
            current_path = os.path.dirname(current_path)
        elif choice.isdigit() and int(choice) < len(items):
            selected = items[int(choice)]
            selected_path = os.path.join(current_path, selected)

            if os.path.isdir(selected_path):
                current_path = selected_path
            else:
                try:
                    with open(selected_path, 'r', encoding='utf-8') as f:
                        print(f"\n📄 Conteudo  de  {selected}:\n")
                        print(f.read())
                except Exception as e:
                    print(f"Erro ao abrir arquivo: {e}")
        else:
            print("Escolha inválida.")

if __name__ == "__main__":
    main()
