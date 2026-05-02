# 🚀 Guia de Compilação - Pacote Steam Davizin Script

Este guia explica como transformar o código Python em um arquivo `.exe` fácil de usar.

## 📋 Pré-requisitos

Você precisa ter o Python instalado e as seguintes bibliotecas:

```bash
pip install pyinstaller customtkinter packaging pillow
```

## 🔨 Como Criar o Executável (.exe)

### Opção 1: Automática (Recomendada)

Basta executar o script de build que criamos:

```bash
python build_exe.py
```

O script fará todo o trabalho automaticamente:
1. Verificará as dependências
2. Compilará o código
3. Gerará o arquivo `.exe` na pasta `dist`

### Opção 2: Manual

Se preferir fazer manualmente, use este comando:

```bash
pyinstaller --onefile --windowed --name "PacoteSteam_DavizinScript" steam_gui.py
```

## 📂 Onde encontrar o .exe?

Após a compilação, seu executável estará em:
```
/dist/PacoteSteam_DavizinScript.exe
```

## ✨ Vantagens do .exe

- **Portátil**: Não precisa instalar Python no PC do usuário
- **Profissional**: Ícone próprio e nome amigável
- **Fácil de distribuir**: Basta enviar um único arquivo
- **Seguro**: O código fonte fica oculto dentro do executável

## ⚙️ Opções Avançadas

Se quiser personalizar ainda mais, adicione estes parâmetros ao PyInstaller:

- `--icon=meu_icone.ico`: Adiciona um ícone personalizado
- `--add-data "assets;assets"`: Inclui pastas com imagens/recursos
- `--hidden-import modulo`: Garante que módulos específicos sejam incluídos

## 🐛 Solução de Problemas

**Erro: "ModuleNotFoundError"**
- Instale todas as dependências: `pip install -r requirements.txt`

**Erro: "File not found"**
- Certifique-se de estar na mesma pasta onde está o `steam_gui.py`

**Executável muito grande?**
- É normal. O .exe inclui o interpretador Python inteiro (~50-100MB).
- Use UPX para comprimir: `--upx-dir=/caminho/para/upx`

## 📤 Distribuição

Para distribuir para seus usuários:
1. Pegue o arquivo `PacoteSteam_DavizinScript.exe` da pasta `dist`
2. Envie por download direto, Google Drive, Mega, etc.
3. O usuário só precisa clicar duas vezes para abrir!

---
**Davizin_Script TM** - Todos os direitos reservados.
