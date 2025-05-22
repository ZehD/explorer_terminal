import os
import shutil

def list_directory(path):
    print(f"\nDiretório: {path}\n")
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
    copy_mode = False
    copy_source = None
    copy_source_name = None

    while True:
        items = list_directory(current_path)

        if copy_mode:
            print("\n📋 MODO CÓPIA ATIVO - Item selecionado: " + copy_source_name)
            print("\nOpções:")
            print(" - Digite o número do Folder para navegar")
            print(" - '..' para voltar")
            print(" - 'paste' para colar aqui")
            print(" - 'cancel' para cancelar a cópia")
        else:
            print("\nOpções:")
            print(" - Digite o número do Folder/Arquivo para abrir")
            print(" - '..' para voltar")
            print(" - 'del <número>' para deletar")
            print(" - 'cp <número>' para iniciar cópia")
            print(" - 'exit' para sair")

        choice = input("Insira a sua escolha: ")

        if choice == "exit" and not copy_mode:
            break
        elif choice == "cancel" and copy_mode:
            copy_mode = False
            copy_source = None
            copy_source_name = None
            print("Operação de cópia cancelada.")
        elif choice == "paste" and copy_mode:
            try:
                dest_path = os.path.join(current_path, copy_source_name)
                if os.path.isdir(copy_source):
                    shutil.copytree(copy_source, dest_path)
                    print(f"Pasta '{copy_source_name}' copiada para o diretório atual.")
                else:
                    shutil.copy2(copy_source, dest_path)
                    print(f"Arquivo '{copy_source_name}' copiado para o diretório atual.")
                copy_mode = False
                copy_source = None
                copy_source_name = None
            except Exception as e:
                print(f"Erro ao colar: {e}")
        elif choice == "..":
            current_path = os.path.dirname(current_path)
        elif choice.startswith("del ") and not copy_mode:
            _, idx = choice.split(maxsplit=1)
            if idx.isdigit() and int(idx) < len(items):
                selected = items[int(idx)]
                selected_path = os.path.join(current_path, selected)
                try:
                    if os.path.isdir(selected_path):
                        shutil.rmtree(selected_path)
                        print(f"Pasta '{selected}' deletada.")
                    else:
                        os.remove(selected_path)
                        print(f"Arquivo '{selected}' deletado.")
                except Exception as e:
                    print(f"Erro ao deletar: {e}")
            else:
                print("Índice inválido para deletar.")
        elif choice.startswith("cp ") and not copy_mode:
            _, idx = choice.split(maxsplit=1)
            if idx.isdigit() and int(idx) < len(items):
                selected = items[int(idx)]
                selected_path = os.path.join(current_path, selected)
                copy_source = selected_path
                copy_source_name = selected
                copy_mode = True
                print(f"Item '{selected}' selecionado para cópia. Navegue até o destino e digite 'paste'.")
            else:
                print("Índice inválido para copiar.")
        elif choice.isdigit() and int(choice) < len(items):
            selected = items[int(choice)]
            selected_path = os.path.join(current_path, selected)
            if os.path.isdir(selected_path):
                current_path = selected_path
            elif not copy_mode:  # Only allow file viewing when not in copy mode
                try:
                    with open(selected_path, 'r', encoding='utf-8') as f:
                        print(f"\n📄 Conteúdo de {selected}:\n")
                        print(f.read())
                except Exception as e:
                    print(f"Erro ao abrir arquivo: {e}")
        else:
            print("Escolha inválida.")

if __name__ == "__main__":
    main()