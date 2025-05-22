# explorer_terminal

Um script Python simples para navegar em pastas diretamente pelo terminal.

## Descrição

Este projeto oferece uma maneira fácil e rápida de explorar diretórios, visualizar arquivos e gerenciar operações básicas como cópia e exclusão, tudo usando comandos simples no terminal. Ideal para quem quer navegar pela estrutura de pastas sem sair do console.

## Funcionalidades

- Listar conteúdo de diretórios
- Navegar entre pastas (`cd`)
- Exibir o caminho atual
- Visualizar o conteúdo de arquivos de texto
- Excluir arquivos e pastas
- Copiar arquivos e pastas para outro local, com navegação até o destino antes de colar
- Registrar em um banco de dados SQLite todas as operações de cópia e exclusão realizadas

## Log de Operações

O script mantém um log automático das operações de cópia e exclusão em um banco de dados SQLite chamado `file_log.db`. Cada registro inclui o nome do arquivo ou pasta, o tipo de operação (`copy` ou `delete`), o caminho de origem, o caminho de destino (quando aplicável) e a data/hora da ação.

> **Atenção:** Para evitar que o arquivo de log seja versionado pelo Git, o nome `file_log.db` já está incluído no `.gitignore`.

## Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/explorer_terminal.git