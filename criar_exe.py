import PyInstaller.__main__
import os
import sys

def build_exe():
    # Nome do seu script principal com a interface
    # VERIFIQUE se o nome do arquivo da interface é este mesmo (ex: steam_gui.py ou main.py)
    main_script = 'steam_gui.py' 
    
    if not os.path.exists(main_script):
        print(f"❌ ERRO: O arquivo '{main_script}' não foi encontrado na pasta atual.")
        print("Verifique se o nome do arquivo da interface está correto.")
        return

    print(f"🚀 Iniciando compilação de {main_script}...")
    print("⏳ Isso pode levar alguns minutos. Aguarde...")

    # Lista de argumentos segura (sem None)
    args = [
        main_script,
        '--name=PacoteSteam_DavizinScript',
        '--onefile',          # Cria um único arquivo .exe
        '--windowed',         # Não mostra a tela preta do console
        '--noconfirm',        # Não pede confirmação para sobrescrever
        '--clean',            # Limpa cache anterior antes de compilar
        '--hidden-import=customtkinter',
        '--hidden-import=PIL',
        '--hidden-import=requests',
        '--hidden-import=json',
        '--hidden-import=threading',
    ]

    # Adiciona ícone apenas se o arquivo existir
    icon_file = 'logo.ico' # Se tiver um ícone, coloque ele na pasta e mude o nome aqui
    if os.path.exists(icon_file):
        args.append(f'--icon={icon_file}')
    
    try:
        PyInstaller.__main__.run(args)
        print("\n✅ SUCESSO! Seu executável está na pasta 'dist'.")
        print(f"📦 Arquivo: dist\\PacoteSteam_DavizinScript.exe")
    except Exception as e:
        print(f"\n❌ ERRO NA COMPILAÇÃO: {e}")

if __name__ == '__main__':
    build_exe()