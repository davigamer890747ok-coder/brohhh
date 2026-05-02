import PyInstaller.__main__
import os
import shutil

# Nome do arquivo principal da interface
MAIN_SCRIPT = "steam_gui.py"
APP_NAME = "PacoteSteam_DavizinScript"

def build_exe():
    print(f"🚀 Iniciando compilação de {APP_NAME}...")
    
    # Limpar pastas antigas se existirem
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        
    PyInstaller.__main__.run([
        MAIN_SCRIPT,
        "--name=" + APP_NAME,
        "--onefile",  # Cria um único arquivo .exe
        "--noconsole",  # Não mostra janela de console (ideal para apps GUI)
        "--windowed",  # Modo janela
        "--clean",  # Limpa cache antes de compilar
        "--add-data=assets;assets" if os.path.exists("assets") else None,  # Inclui pasta de assets se existir
        "--hidden-import=customtkinter",
        "--hidden-import=PIL",
        "--hidden-import=requests",
        "--icon=NONE",  # Se tiver um ícone .ico, coloque o caminho aqui ex: "--icon=logo.ico"
    ])

    print("\n✅ Compilação concluída!")
    print(f"📦 Seu executável está em: dist/{APP_NAME}.exe")
    print("\n💡 Dica: Você pode copiar este arquivo .exe para qualquer computador com Windows e ele funcionará sem precisar instalar Python.")

if __name__ == "__main__":
    build_exe()
