# Steam Tools 🎮

Uma coleção de ferramentas úteis para usuários da Steam.

## Funcionalidades

- 🔍 **Buscar jogos** por nome
- 📋 **Ver detalhes** de um jogo (por App ID)
- 👥 **Ver jogadores atuais** em um jogo
- 👤 **Informações de usuário** Steam
- 💰 **Verificar descontos** e histórico de preços

## Instalação

### Requisitos
- Python 3.6+
- Biblioteca `requests`

```bash
pip install requests
```

## Uso

### Modo Interativo
```bash
python steam_tools.py
```

### Linha de Comando

**Buscar jogos:**
```bash
python steam_tools.py --search "Counter"
```

**Ver detalhes de um jogo:**
```bash
python steam_tools.py --app 730
```

**Ver jogadores atuais:**
```bash
python steam_tools.py --players 730
```

**Informações de usuário:**
```bash
python steam_tools.py --user "SEU_STEAM_ID"
```

**Verificar descontos:**
```bash
python steam_tools.py --deals 730
```

## Exemplos

### Counter-Strike 2 (App ID: 730)
```bash
python steam_tools.py --app 730
```

### Buscar jogos com "Half-Life"
```bash
python steam_tools.py --search "Half-Life"
```

## Links Úteis

- [Steam Web API](https://steamcommunity.com/dev)
- [SteamDB](https://steamdb.info/)
- [IsThereAnyDeal](https://isthereanydeal.com/)

## Licença

MIT License - Sinta-se livre para usar e modificar!

---
Criado com ❤️ para a comunidade Steam
