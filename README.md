## Disclaimer

This project was created solely for academic purposes to explore and understand file management concepts in an operating system. It is not intended for production use or real-world deployment. Use at your own risk.  

Este projeto foi criado unicamente para fins acadêmicos, com o objetivo de explorar e compreender conceitos de gerenciamento de arquivos em um sistema operacional. Não é destinado para uso em produção ou em ambientes reais. Use por sua conta e risco.


# explorer_terminal

Um explorador de arquivos simples em Python, com opções de uso via terminal ou interface gráfica (GUI).

##  Descrição

Este projeto oferece uma maneira prática de navegar por diretórios, visualizar arquivos de texto e realizar operações básicas como cópia, exclusão e renomeação. Você pode escolher entre utilizar a versão **terminal**, com comandos simples, ou a versão **gráfica (GUI)**, construída com Tkinter.

Ideal para quem deseja uma ferramenta leve de exploração de arquivos, com registro de operações em banco de dados.

##  Funcionalidades

### Terminal (`explorer_terminal.py`)
- Listar conteúdo de diretórios
- Navegar entre pastas (`cd`)
- Visualizar conteúdo de arquivos de texto
- Excluir arquivos e pastas
- Copiar arquivos e pastas com opção de colar em outro local
- Registro de operações (cópia e exclusão) em SQLite

### Interface Gráfica (`explorer_gui.py`)
- Navegação por pastas com botões
- Voltar para diretório anterior
- Visualizar arquivos
- Copiar, renomear e excluir arquivos/pastas
- Interface amigável com Tkinter
- Log das operações igual ao modo terminal

##  Log de Operações

Todas as operações de **cópia** e **exclusão** são registradas automaticamente em um banco de dados SQLite chamado `file_log.db`.

Cada registro inclui:
- Nome do arquivo/pasta
- Tipo da operação (`copy` ou `delete`)
- Caminho de origem
- Caminho de destino (quando aplicável)
- Data e hora da operação

>  O arquivo `file_log.db` está listado no `.gitignore` para evitar versionamento.

## ▶️ Como Usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/explorer_terminal.git
   cd explorer_terminal


https://www.canva.com/design/DAGqGoJqcWE/cRHqzast53wNj2fvFIlssg/edit?utm_content=DAGqGoJqcWE&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton