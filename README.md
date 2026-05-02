# Steam Tools 🎮

Uma coleção completa de ferramentas úteis para usuários da Steam.

## ✨ Funcionalidades

### Principais Recursos
- 🔍 **Buscar jogos** por nome com resultados ilimitados
- 📋 **Ver detalhes completos** de um jogo (por App ID)
- 👥 **Ver jogadores atuais** em tempo real
- 👤 **Informações de usuário** Steam
- 💰 **Verificar descontos** e histórico de preços
- 🔥 **Top jogos populares** baseado em jogadores ativos
- 🆕 **Atualizações recentes** de jogos
- ⚖️ **Comparar múltiplos jogos** lado a lado
- 💾 **Exportar dados** para JSON

### Informações Detalhadas dos Jogos
- Nome, tipo e descrição
- Preço atual e descontos ativos
- Plataformas suportadas (Windows, Mac, Linux)
- Categorias e gêneros
- Data de lançamento
- Pontuação Metacritic
- Número de recomendações

## 📦 Instalação

### Requisitos
- Python 3.6+
- Biblioteca `requests`

```bash
pip install requests
```

## 🚀 Uso

### Modo Interativo
```bash
python steam_tools.py
```
ou
```bash
python steam_tools.py --interactive
```

### Linha de Comando

**Buscar jogos:**
```bash
python steam_tools.py --search "Counter"
python steam_tools.py --search "Half-Life" --limit 20
```

**Ver detalhes de um jogo:**
```bash
python steam_tools.py --app 730
python steam_tools.py --app 1091500  # Cyberpunk 2077
```

**Ver jogadores atuais:**
```bash
python steam_tools.py --players 730
python steam_tools.py --players 570  # Dota 2
```

**Informações de usuário:**
```bash
python steam_tools.py --user "SEU_STEAM_ID"
```

**Verificar descontos:**
```bash
python steam_tools.py --deals 730
```

**Top jogos populares:**
```bash
python steam_tools.py --top
python steam_tools.py --top 5  # Mostrar apenas top 5
```

**Atualizações recentes:**
```bash
python steam_tools.py --updates
```

**Comparar jogos:**
```bash
python steam_tools.py --compare 730,570,440
python steam_tools.py --compare 1091500,1245620,1086940
```

**Exportar dados para JSON:**
```bash
python steam_tools.py --export 730
python steam_tools.py --export 730 --output cs2_details.json
```

**Ajuda:**
```bash
python steam_tools.py --help
```

## 📊 Exemplos Práticos

### Counter-Strike 2 (App ID: 730)
```bash
# Ver detalhes completos
python steam_tools.py --app 730

# Ver jogadores atuais
python steam_tools.py --players 730

# Verificar descontos
python steam_tools.py --deals 730

# Exportar dados
python steam_tools.py --export 730 --output cs2.json
```

### Buscar jogos específicos
```bash
# Buscar jogos com "Half-Life"
python steam_tools.py --search "Half-Life"

# Buscar jogos com "Elden" (limitado a 5 resultados)
python steam_tools.py --search "Elden" --limit 5
```

### Comparar múltiplos jogos
```bash
# Comparar CS2, Dota 2 e Team Fortress 2
python steam_tools.py --compare 730,570,440

# Comparar jogos AAA modernos
python steam_tools.py --compare 1091500,1245620,1086940
```

## 🎯 Menu Interativo

No modo interativo, você terá acesso a:

1. 🔍 Buscar jogos por nome
2. 📋 Ver detalhes de um jogo (por App ID)
3. 👥 Ver jogadores atuais
4. 👤 Informações de usuário Steam
5. 💰 Verificar descontos
6. 🔥 Top jogos populares
7. 🆕 Atualizações recentes
8. ⚖️ Comparar jogos
9. 💾 Exportar dados para JSON
10. 🚪 Sair

## 🔗 Links Úteis

- [Steam Web API](https://steamcommunity.com/dev)
- [SteamDB](https://steamdb.info/)
- [IsThereAnyDeal](https://isthereanydeal.com/)
- [Steam Calculator](https://steamcalculator.com/)
- [Lista de App IDs](https://steamdb.info/apps/)

## 🎮 App IDs Populares

| Jogo | App ID |
|------|--------|
| Counter-Strike 2 | 730 |
| Dota 2 | 570 |
| Team Fortress 2 | 440 |
| Grand Theft Auto V | 271590 |
| Cyberpunk 2077 | 1091500 |
| Elden Ring | 1245620 |
| Baldur's Gate 3 | 1086940 |
| Apex Legends | 1172470 |
| PUBG: BATTLEGROUNDS | 578080 |
| Rust | 252490 |

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
/workspace/
├── steam_tools.py    # Script principal
├── README.md         # Este arquivo
└── *.json            # Arquivos exportados (opcional)
```

### Adicionando Novas Funcionalidades

Para adicionar novas funcionalidades, estenda a classe `SteamTools`:

```python
class SteamTools:
    def __init__(self):
        # ...
    
    def nova_funcionalidade(self, params):
        # Sua implementação aqui
        pass
```

## 📝 Licença

MIT License - Sinta-se livre para usar, modificar e distribuir!

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## ⚠️ Avisos

- Algumas funcionalidades requerem conexão com a internet
- A API da Steam pode ter limitações de taxa (rate limiting)
- Para informações completas de perfil de usuário, é necessária uma API Key da Steam
- Dados de jogadores podem não estar disponíveis para todos os jogos

---

Criado com ❤️ para a comunidade Steam

**Versão:** 2.0  
**Última atualização:** 2024
