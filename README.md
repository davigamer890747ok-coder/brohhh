# 🎮 Pacote Steam + de Mil 100 Jogos - Davizin_Script TM

Interface desktop moderna com tema escuro para gerenciamento e instalação automática de jogos Steam e ferramentas Lua.

## ✨ Funcionalidades

- **Interface Moderna**: Tema escuro profissional inspirado em gerenciadores de biblioteca de jogos
- **1107+ Jogos**: Catálogo completo com jogos populares e DLCs
- **Steam Tools**: Instalação automática via SteamCMD
- **Lua Tools**: Gerenciamento de ferramentas Lua via LuaRocks
- **Categorias**: Filtragem por gênero (Ação, RPG, Aventura, etc.)
- **Busca**: Pesquisa rápida de jogos
- **Status**: Acompanhamento de jogos instalados
- **Exportação**: Exporta lista de jogos para JSON
- **Automático**: Instalação totalmente automatizada

## 📋 Requisitos

### Sistema Operacional
- Windows 10/11
- Linux (Ubuntu, Debian, Fedora)
- macOS

### Dependências Python
```bash
pip install customtkinter packaging
```

### Dependências do Sistema
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk tk wget

# Fedora
sudo dnf install python3-tkinter wget

# Windows
# Python já inclui tkinter
```

## 🚀 Instalação

### 1. Clonar Repositório
```bash
git clone <seu-repositorio>
cd <diretorio-do-projeto>
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar Interface
```bash
python steam_gui.py
```

## 🎯 Uso da Interface

### Barra Lateral Esquerda

**Categorias:**
- Todos os Jogos (1107)
- Ação, Aventura, RPG, Estratégia
- Corrida, Esportes, Simulação
- Terror, Indie, Multiplayer, Outros

**Opções:**
- 🟢 **INSTALAR SELECIONADO**: Instala jogos selecionados
- ⚫ **VER INFORMAÇÕES**: Detalhes do jogo
- 🔴 **REMOVER JOGO**: Remove da lista de instalados

**Filtros:**
- Campo de busca: "Pesquisar jogo..."
- Checkbox: "Mostrar apenas instalados"

### Área Principal

**Tabela de Jogos:**
- **#**: Número do jogo
- **JOGO**: Nome com ícone
- **GÊNERO**: Categoria do jogo
- **TAMANHO**: Espaço necessário
- **STATUS**: Instalado (verde) / Não instalado (cinza)

### Cabeçalho
- Título: "PACOTE STEAM + DE MIL 100 JOGOS"
- Subtítulo: "DAVIZIN_SCRIPT TM"
- Total de jogos: Contador em tempo real

### Rodapé
- Copyright: "DAVIZIN_SCRIPT TM - Todos os direitos reservados."
- Botões: ATUALIZAR LISTA | EXPORTAR LISTA | SAIR

## 🔧 Linha de Comando

### Instalar Manifest
```bash
python manifest_installer.py --install nome_do_manifest
```

### Listar Manifests
```bash
python manifest_installer.py --list
```

### Gerar Manifest em Massa
```bash
python manifest_installer.py --generate-bulk 1 100000 steam_100k
```

### Modo Automático
```bash
python manifest_installer.py --install meu_pacote --auto
```

### Ver Histórico
```bash
python manifest_installer.py --installed
```

## 📦 Estrutura de Arquivos

```
/workspace/
├── steam_gui.py              # Interface gráfica principal
├── manifest_installer.py     # Instalador de manifests
├── manifests/                # Diretório de manifests JSON
│   ├── essential_games.json
│   ├── dev_tools.json
│   └── steam_100k.json
├── steamcmd/                 # SteamCMD (instalado automaticamente)
├── installed_games.json      # Registro de jogos instalados
└── installation_history.json # Histórico de instalações
```

## 🎮 Exemplo de Manifest JSON

```json
{
  "name": "garrys_mod_complete",
  "description": "Garry's Mod com todos os DLCs",
  "apps": [4000],
  "dlcs": [223090, 489830, 489831, 489832, 489833, 489834, 489835],
  "tools": ["luajit", "lfs"]
}
```

## 🛠️ Recursos Técnicos

### Steam Tools
- **SteamCMD**: Download e instalação de jogos
- **Suporte a DLCs**: Instalação automática de DLCs associadas
- **Login Anônimo**: Para jogos free-to-play e demos

### Lua Tools
- **LuaRocks**: Gerenciador de pacotes Lua
- **Ferramentas Incluídas**:
  - LuaJIT (Just-In-Time compiler)
  - LuaFileSystem (LFS)
  - LPeg (Parsing Expression Grammar)
  - LuaSocket (Rede)
  - LuaSec (SSL/TLS)

## 📸 Screenshots

A interface apresenta:
- Tema escuro (#0f0f1a, #1a1a2e, #16213e)
- Cores de destaque: Verde (#00ff88), Azul (#0066cc)
- Ícones emoji para jogos
- Status colorido (verde = instalado, cinza = não instalado)

## 🔐 Segurança

- SteamCMD baixado oficialmente da Valve
- LuaRocks da fonte oficial
- Sem armazenamento de credenciais
- Instalação em diretório local

## 📝 Licença

**DAVIZIN_SCRIPT TM** - Todos os direitos reservados.

## 👤 Autor

**Davizin_Script TM**

## 🆘 Suporte

Para problemas ou sugestões, abra uma issue no repositório.

---

**Divirta-se jogando! 🎮**
