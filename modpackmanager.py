import shutil
import os
import argparse
import configparser
import sys


def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def get_mod_ids(config):
    return config['MODS']['mod_ids'].split(',')

def get_modpack_name(config, args_name):
    return args_name or config['DEFAULT'].get('name', 'default_modpack')

def get_full_destination(destination, name):
    """Retorna o caminho completo do destino incluindo o nome do modpack e a estrutura de pastas."""
    return os.path.join(destination, name, "Contents", "mods")

def create(source, destination, name):
    """Cria a estrutura completa do modpack."""
    modpack_path = os.path.join(destination, name)
    if os.path.exists(modpack_path):
        print(f"Erro: Um modpack com o nome '{name}' já existe em {modpack_path}")
        print("Por favor, escolha um nome diferente ou use o comando 'update' "
              "para atualizar o modpack existente.")
        sys.exit(0)

    print(f"Criando a estrutura do modpack '{name}'...")
    full_destination = get_full_destination(destination, name)
    os.makedirs(full_destination, exist_ok=True)
    
    # Criar o arquivo mod.info
    mod_info_file_path = os.path.join(modpack_path, "mod.info")
    mod_info_content = """name=Mod Template
id=ModTemplate
description=This is an example mod containing two maps.
poster=poster.png"""
    with open(mod_info_file_path, 'w') as mod_info_file:
        mod_info_file.write(mod_info_content)
    print(f"Arquivo mod.info criado em {mod_info_file_path}")

    copy_mods_for_creation(source, destination, name)

def clean(destination, name):
    """Remove todo o conteúdo do diretório de destino se o modpack existir."""
    modpack_path = os.path.join(destination, name)
    
    if not os.path.exists(modpack_path):
        print(f"Erro: O modpack '{name}' não existe em {destination}")
        print("Por favor, verifique o nome do modpack e tente novamente.")
        sys.exit(0)

    full_destination = get_full_destination(destination, name)
    print(f"Limpando o diretório de destino: {full_destination}")
    if os.path.exists(full_destination):
        for item in os.listdir(full_destination):
            item_path = os.path.join(full_destination, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        print(f"O diretório {full_destination} foi limpo com sucesso.")
    else:
        print(f"O diretório {full_destination} não existe. Nada para limpar.")

def update(source, destination, name):
    """Executa a limpeza e depois copia os arquivos novos."""
    modpack_path = os.path.join(destination, name)
    
    if not os.path.exists(modpack_path):
        print(f"Erro: O modpack '{name}' não existe em {destination}")
        print("Por favor, verifique o nome do modpack e tente novamente.")
        sys.exit(0)

    full_destination = get_full_destination(destination, name)
    clean(destination, name)
    print("Atualizando os mods...")
    config = load_config()
    mod_ids = get_mod_ids(config)
    error_occurred = False
    for mod_id in mod_ids:
        src_path = os.path.join(source, mod_id.strip(), "mods")
        if not os.path.exists(src_path):
            print(f"Erro: Pasta 'mods' não encontrada para o mod com ID {mod_id} em {src_path}")
            error_occurred = True
            continue
        print(f"Copiando conteúdo da pasta 'mods' do mod com ID: {mod_id}")
        for item in os.listdir(src_path):
            s = os.path.join(src_path, item)
            d = os.path.join(full_destination, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
    if not error_occurred:
        print("Mods atualizados com sucesso!")
    else:
        print("Atualização concluída com erros. Verifique as mensagens acima.")

def copy_mods_for_creation(source, destination, name):
    """Copia os mods para o novo modpack."""
    full_destination = get_full_destination(destination, name)
    print("Copiando mods para o novo modpack...")
    config = load_config()
    mod_ids = get_mod_ids(config)
    error_occurred = False
    for mod_id in mod_ids:
        src_path = os.path.join(source, mod_id.strip(), "mods")
        if not os.path.exists(src_path):
            print(f"Erro: Pasta 'mods' não encontrada para o mod com ID {mod_id} em {src_path}")
            error_occurred = True
            continue
        print(f"Copiando conteúdo da pasta 'mods' do mod com ID: {mod_id}")
        for item in os.listdir(src_path):
            s = os.path.join(src_path, item)
            d = os.path.join(full_destination, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy2(s, d)
    if not error_occurred:
        print("Modpack criado com sucesso!")
    else:
        print("Criação do modpack concluída com erros. Verifique as mensagens acima.")

def main():
    config = load_config()
    parser = argparse.ArgumentParser(description="Gerenciador de Modpack para Project Zomboid")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando create
    create_parser = subparsers.add_parser("create", help="Cria um novo modpack")
    create_parser.add_argument("--source", help="Diretório fonte dos mods")
    create_parser.add_argument("--destination", help="Diretório de destino para o modpack")
    create_parser.add_argument("--name", help="Nome do modpack")

    # Comando update
    update_parser = subparsers.add_parser("update", help="Atualiza um modpack existente")
    update_parser.add_argument("--source", help="Diretório fonte dos mods")
    update_parser.add_argument("--destination", help="Diretório de destino do modpack")
    update_parser.add_argument("--name", help="Nome do modpack")

    # Comando clean
    clean_parser = subparsers.add_parser(
        "clean",
        help="Limpa o diretório de destino do modpack. WARNING: Deve ser usado com cautela, "
             "pois irá remover todos os mods do pacote!"
    )
    clean_parser.add_argument("--destination", help="Diretório de destino do modpack")
    clean_parser.add_argument("--name", help="Nome do modpack")

    args = parser.parse_args()

    if args.command == "create":
        source = args.source or config['DEFAULT'].get('source')
        destination = args.destination or config['DEFAULT'].get('destination')
        name = get_modpack_name(config, args.name)
        if not source or not destination:
            create_parser.print_help()
            return
        create(source, destination, name)
    elif args.command == "update":
        source = args.source or config['DEFAULT'].get('source')
        destination = args.destination or config['DEFAULT'].get('destination')
        name = get_modpack_name(config, args.name)
        if not source or not destination:
            update_parser.print_help()
            return
        update(source, destination, name)
    elif args.command == "clean":
        destination = args.destination or config['DEFAULT'].get('destination')
        name = get_modpack_name(config, args.name)
        if not destination:
            clean_parser.print_help()
            return
        clean(destination, name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
