"""
Script de Build para criar o Executável (.exe)
Pacote Steam + de Mil 100 Jogos - Davizin_Script TM

Este script utiliza o PyInstaller para compilar o projeto em um único arquivo .exe
portátil, sem necessidade de instalar Python no computador do usuário final.

Requisitos:
pip install pyinstaller customtkinter packaging

Uso:
python build_exe.py
"""

import os
import sys
import subprocess
import shutil

def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas."""
    print("🔍 Verificando dependências...")
    try:
        import customtkinter
        import PyInstaller
        print("✅ Dependências encontradas.")
    except ImportError as e:
        print(f"❌ Erro: Dependência faltando ({e}).")
        print("Instale com: pip install pyinstaller customtkinter packaging")
        sys.exit(1)

def build_executable():
    """Executa o PyInstaller com as configurações otimizadas."""
    
    # Nome do script principal da interface
    main_script = "steam_gui.py"
    
    if not os.path.exists(main_script):
        print(f"❌ Erro: O arquivo '{main_script}' não foi encontrado na pasta atual.")
        print("Certifique-se de estar na raiz do projeto.")
        return

    print(f"🔨 Compilando '{main_script}' em executável...")
    print("⏳ Isso pode levar alguns minutos...")

    # Comandos do PyInstaller
    # --onefile: Cria um único arquivo .exe
    # --windowed: Não abre a janela de console preta (ideal para GUI)
    # --icon: Adiciona o ícone (se existir)
    # --name: Nome do arquivo final
    # --hidden-import: Garante que módulos internos sejam incluídos
    
    command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "PacoteSteam_DavizinScript",
        "--clean",  # Limpa cache anterior
        "--noconfirm",
        # Imports ocultos necessários para customtkinter e subprocessos
        "--hidden-import", "customtkinter",
        "--hidden-import", "PIL",
        "--hidden-import", "json",
        "--hidden-import", "subprocess",
        "--hidden-import", "threading",
        main_script
    ]

    # Tenta adicionar ícone se existir
    icon_path = "icon.ico"
    if os.path.exists(icon_path):
        command.extend(["--icon", icon_path])
        print(f"🎨 Ícone '{icon_path}' detectado e adicionado.")
    else:
        print("⚠️ Nenhum ícone 'icon.ico' encontrado. Usando ícone padrão do Windows.")

    try:
        subprocess.run(command, check=True)
        
        print("\n" + "="*50)
        print("✅ COMPILAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*50)
        
        # Caminhos de saída
        dist_folder = os.path.join(os.getcwd(), "dist")
        exe_path = os.path.join(dist_folder, "PacoteSteam_DavizinScript.exe")
        
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📦 Arquivo gerado: {exe_path}")
            print(f"💾 Tamanho aproximado: {size_mb:.2f} MB")
            print("\n📂 O executável está na pasta 'dist'.")
            print("💡 Dica: Você pode copiar este arquivo .exe para qualquer lugar e ele funcionará!")
        else:
            print("❌ Erro: O arquivo .exe não foi gerado mesmo sem erros de compilação.")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro durante a compilação: {e}")
        print("Verifique se há erros de sintaxe no seu código Python.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

def cleanup():
    """Limpa arquivos temporários gerados pelo PyInstaller (opcional)."""
    folders_to_clean = ["build", "__pycache__"]
    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                # shutil.rmtree(folder) # Descomente se quiser deletar automaticamente
                print(f"🧹 Pasta temporária '{folder}' pode ser removida manualmente se desejar.")
            except Exception:
                pass

if __name__ == "__main__":
    print("🚀 Iniciando processo de criação do Executável...")
    print("Projeto: Pacote Steam + de Mil 100 Jogos - Davizin_Script TM\n")
    
    check_dependencies()
    build_executable()
    cleanup()
    
    print("\n🎉 Processo finalizado!")
