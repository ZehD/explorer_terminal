import os
import sys
import shutil
from file_logger import log_operation

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

def terminal_flow():
    current_path = os.getcwd()
    copy_mode = False
    copy_source = None
    copy_source_name = None

    print("Bem-vindo ao Explorador de Arquivos do Terminal!")
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
            print(" - 'open <número>' para abrir o arquivo com programa padrão")
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
                    print(f"Pasta '{copy_source_name}' copiada.")
                else:
                    shutil.copy2(copy_source, dest_path)
                    print(f"Arquivo '{copy_source_name}' copiado.")
                log_operation(copy_source_name, 'copy', copy_source, dest_path)
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
                    else:
                        os.remove(selected_path)
                    print(f"'{selected}' deletado.")
                    log_operation(selected, 'delete', selected_path)
                except Exception as e:
                    print(f"Erro ao deletar: {e}")
            else:
                print("Índice inválido.")
        elif choice.startswith("cp ") and not copy_mode:
            _, idx = choice.split(maxsplit=1)
            if idx.isdigit() and int(idx) < len(items):
                selected = items[int(idx)]
                copy_source = os.path.join(current_path, selected)
                copy_source_name = selected
                copy_mode = True
                print(f"Item '{selected}' pronto para cópia. Navegue até o destino e digite 'paste'.")
            else:
                print("Índice inválido.")
        elif choice.startswith("open ") and not copy_mode:
            _, idx = choice.split(maxsplit=1)
            if idx.isdigit() and int(idx) < len(items):
                selected = items[int(idx)]
                selected_path = os.path.join(current_path, selected)
                if os.path.isfile(selected_path):
                    try:
                        if os.name == 'nt':  # Windows
                            os.system(f'start "" "{selected_path}"')
                        elif sys.platform == 'darwin':  # macOS
                            os.system(f'open "{selected_path}"')
                        else:  # Linux 
                            os.system(f'xdg-open "{selected_path}"')

                        log_operation(selected, 'open', selected_path)
                    except Exception as e:
                        print(f"Erro ao abrir arquivo: {e}")
                else:
                    print("Você só pode abrir arquivos, não diretórios.")
            else:
                print("Índice inválido.")
        elif choice.isdigit() and int(choice) < len(items):
            selected = items[int(choice)]
            selected_path = os.path.join(current_path, selected)
            if os.path.isdir(selected_path):
                current_path = selected_path
            elif not copy_mode:
                try:
                    with open(selected_path, 'r', encoding='utf-8') as f:
                        print(f"\n Conteúdo de {selected}:\n")
                        print(f.read())
                    log_operation(selected, 'open', selected_path) 
                except Exception as e:
                    print(f"Erro ao abrir arquivo: {e}")
        else:
            print("Escolha inválida.")
