# Project Zomboid Modpack Manager

Este é um gerenciador de modpack para Project Zomboid, permitindo criar, atualizar e limpar modpacks facilmente.

## Dependências

- Python 3.6 ou superior

Este script utiliza apenas bibliotecas padrão do Python, então não há necessidade de instalar dependências adicionais.

## Instalação do Python

Se você ainda não tem o Python instalado, você pode baixá-lo do site oficial:

[Download Python](https://www.python.org/downloads/)

Certifique-se de marcar a opção "Add Python to PATH" durante a instalação no Windows.

## Configuração

Antes de usar o script, edite o arquivo `config.ini` para configurar os caminhos corretos para o seu sistema:


## Uso

O script suporta três comandos principais: `create`, `update`, e `clean`.

### Criar um novo modpack

```bash
python3 modpackmanager.py create [--source "SOURCE"] [--destination "DESTINATION"] [--name NAME]
```

Exemplo:
```bash
python3 modpackmanager.py create --source "/mnt/c/Program Files (x86)/Steam/steamapps/workshop/content/108600/" --destination "/mnt/c/Users/seu_usuario/Zomboid/Workshop/" --name MeuNovoModpack
```

### Atualizar um modpack existente

```bash
python3 modpackmanager.py update [--source "SOURCE"] [--destination "DESTINATION"] [--name NAME]
```

Exemplo:
```bash
python3 modpackmanager.py update --source "/mnt/c/Program Files (x86)/Steam/steamapps/workshop/content/108600/" --destination "/mnt/c/Users/seu_usuario/Zomboid/Workshop/" --name OneDayPack
```

### Limpar o diretório de destino do modpack

```bash
python3 modpackmanager.py clean [--destination "DESTINATION"] [--name NAME]
```

Exemplo:
```bash
python3 modpackmanager.py clean --destination "/mnt/c/Users/seu_usuario/Zomboid/Workshop/" --name MeuModpack
```

**AVISO**: O comando `clean` deve ser usado com cautela, pois irá remover todos os mods do pacote!

## Notas

- Se não forem fornecidos argumentos, o script usará os valores padrão do arquivo `config.ini`.
- Certifique-se de ter permissões de leitura e escrita nos diretórios de origem e destino.
- Os IDs dos mods devem ser adicionados na seção `[MODS]` do arquivo `config.ini`.

## Suporte

Este script foi testado em Windows (com e sem WSL), macOS e Linux. Se encontrar algum problema, por favor, abra uma issue no repositório do projeto.
