#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manifest Installer - Steam Tools & Lua Tools
Instalação automática de jogos e ferramentas Lua
Autor: Davizin_Script TM
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class ManifestInstaller:
    def __init__(self):
        self.install_dir = Path(__file__).parent
        self.manifests_dir = self.install_dir / "manifests"
        self.history_file = self.install_dir / "installation_history.json"
        self.installed_games_file = self.install_dir / "installed_games.json"
        
        # Criar diretórios necessários
        self.manifests_dir.mkdir(exist_ok=True)
        
        # Carregar histórico
        self.installation_history = self.load_history()
        
    def load_history(self):
        """Carrega histórico de instalações"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return {"installations": [], "total_installed": 0}
        return {"installations": [], "total_installed": 0}
    
    def save_history(self):
        """Salva histórico de instalações"""
        with open(self.history_file, 'w') as f:
            json.dump(self.installation_history, f, indent=2)
    
    def check_steamcmd(self):
        """Verifica se SteamCMD está instalado"""
        steamcmd_path = self.install_dir / "steamcmd" / "steamcmd.exe" if sys.platform == "win32" else self.install_dir / "steamcmd" / "steamcmd.sh"
        return steamcmd_path.exists()
    
    def install_steamcmd(self):
        """Instala SteamCMD"""
        print("📦 Instalando SteamCMD...")
        steamcmd_dir = self.install_dir / "steamcmd"
        steamcmd_dir.mkdir(exist_ok=True)
        
        try:
            if sys.platform == "win32":
                # Windows
                subprocess.run([
                    "powershell", "-Command",
                    f"Invoke-WebRequest -Uri https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip -OutFile {steamcmd_dir}/steamcmd.zip"
                ], check=True)
                subprocess.run(["powershell", "-Command", f"Expand-Archive -Path {steamcmd_dir}/steamcmd.zip -DestinationPath {steamcmd_dir}"], check=True)
                os.remove(steamcmd_dir / "steamcmd.zip")
            else:
                # Linux
                subprocess.run(["wget", "-q", "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz", "-O", str(steamcmd_dir / "steamcmd.tar.gz")], check=True)
                subprocess.run(["tar", "-xzf", str(steamcmd_dir / "steamcmd.tar.gz"), "-C", str(steamcmd_dir)], check=True)
                os.remove(steamcmd_dir / "steamcmd.tar.gz")
            
            print("✅ SteamCMD instalado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao instalar SteamCMD: {e}")
            return False
    
    def check_luarocks(self):
        """Verifica se LuaRocks está instalado"""
        try:
            result = subprocess.run(["luarocks", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def install_luarocks(self):
        """Instala LuaRocks (se necessário)"""
        print("📦 Verificando LuaRocks...")
        if self.check_luarocks():
            print("✅ LuaRocks já está instalado!")
            return True
        
        print("⚠️ LuaRocks não encontrado. Por favor, instale manualmente:")
        print("   Ubuntu/Debian: sudo apt-get install luarocks")
        print("   Windows: baixe em https://luarocks.github.io/luarocks/")
        return False
    
    def install_lua_tool(self, tool_name):
        """Instala ferramenta Lua via LuaRocks"""
        print(f"🔧 Instalando {tool_name}...")
        try:
            subprocess.run(["luarocks", "install", tool_name], check=True)
            print(f"✅ {tool_name} instalado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao instalar {tool_name}: {e}")
            return False
    
    def install_game(self, app_id, auto_confirm=False):
        """Instala jogo via SteamCMD"""
        if not self.check_steamcmd():
            if not self.install_steamcmd():
                return False
        
        print(f"🎮 Instalando jogo {app_id}...")
        
        steamcmd_path = self.install_dir / "steamcmd" / ("steamcmd.exe" if sys.platform == "win32" else "steamcmd.sh")
        
        try:
            # Comando SteamCMD
            if sys.platform == "win32":
                cmd = [str(steamcmd_path), "+login", "anonymous", f"+app_update", str(app_id), "+quit"]
            else:
                cmd = ["bash", str(steamcmd_path), "+login", "anonymous", f"+app_update", str(app_id), "+quit"]
            
            subprocess.run(cmd, check=True)
            print(f"✅ Jogo {app_id} instalado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao instalar jogo {app_id}: {e}")
            return False
    
    def install_manifest(self, manifest_path, auto_confirm=False):
        """Instala todos os itens de um manifest"""
        if not os.path.exists(manifest_path):
            print(f"❌ Manifest não encontrado: {manifest_path}")
            return False
        
        # Carregar manifest
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        manifest_name = manifest.get('name', 'unknown')
        description = manifest.get('description', 'Sem descrição')
        apps = manifest.get('apps', [])
        dlcs = manifest.get('dlcs', [])
        tools = manifest.get('tools', [])
        
        print(f"\n{'='*60}")
        print(f"📦 MANIFEST: {manifest_name}")
        print(f"📝 Descrição: {description}")
        print(f"🎮 Jogos: {len(apps)}")
        print(f"📥 DLCs: {len(dlcs)}")
        print(f"🔧 Ferramentas Lua: {len(tools)}")
        print(f"{'='*60}\n")
        
        if not auto_confirm:
            confirm = input("Deseja continuar com a instalação? (s/n): ")
            if confirm.lower() != 's':
                print("❌ Instalação cancelada.")
                return False
        
        total_installed = 0
        total_items = len(apps) + len(dlcs) + len(tools)
        
        # Instalar jogos
        for app_id in apps:
            print(f"\n[{total_installed+1}/{total_items}] Instalando jogo {app_id}...")
            if self.install_game(app_id, auto_confirm):
                total_installed += 1
        
        # Instalar DLCs
        for dlc_id in dlcs:
            print(f"\n[{total_installed+1}/{total_items}] Instalando DLC {dlc_id}...")
            if self.install_game(dlc_id, auto_confirm):
                total_installed += 1
        
        # Instalar ferramentas Lua
        for tool in tools:
            print(f"\n[{total_installed+1}/{total_items}] Instalando ferramenta Lua: {tool}")
            if self.install_lua_tool(tool):
                total_installed += 1
        
        # Atualizar histórico
        self.installation_history["installations"].append({
            "manifest": manifest_name,
            "date": str(datetime.now()),
            "items_installed": total_installed,
            "total_items": total_items
        })
        self.installation_history["total_installed"] += total_installed
        self.save_history()
        
        print(f"\n{'='*60}")
        print(f"✅ Instalação concluída! {total_installed}/{total_items} itens instalados.")
        print(f"{'='*60}\n")
        
        return True
    
    def generate_bulk_manifest(self, start_id, end_id, name="bulk_manifest"):
        """Gera manifest em massa com faixa de AppIDs"""
        print(f"🚀 Gerando manifest em massa de {start_id} a {end_id}...")
        
        apps = list(range(start_id, end_id + 1))
        
        manifest = {
            "name": name,
            "description": f"Manifest gerado automaticamente com {len(apps)} jogos",
            "type": "bulk",
            "generated_date": str(datetime.now()),
            "apps": apps,
            "dlcs": [],
            "tools": ["luajit", "lfs"]
        }
        
        manifest_path = self.manifests_dir / f"{name}.json"
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        file_size = os.path.getsize(manifest_path) / (1024 * 1024)  # MB
        
        print(f"✅ Manifest gerado: {manifest_path}")
        print(f"📊 Tamanho do arquivo: {file_size:.2f} MB")
        print(f"📦 Total de jogos: {len(apps)}")
        
        return manifest_path
    
    def list_manifests(self):
        """Lista todos os manifests disponíveis"""
        print("\n📦 MANIFESTS DISPONÍVEIS:\n")
        
        if not self.manifests_dir.exists():
            print("Nenhum manifest encontrado.")
            return
        
        manifests = list(self.manifests_dir.glob("*.json"))
        
        if not manifests:
            print("Nenhum manifest encontrado.")
            return
        
        for manifest_path in manifests:
            try:
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                
                name = manifest.get('name', manifest_path.stem)
                apps = len(manifest.get('apps', []))
                dlcs = len(manifest.get('dlcs', []))
                tools = len(manifest.get('tools', []))
                
                print(f"  • {name}")
                print(f"    Jogos: {apps} | DLCs: {dlcs} | Ferramentas: {tools}")
                print()
            except Exception as e:
                print(f"  • {manifest_path.stem} (erro ao ler)")
    
    def show_installed(self):
        """Mostra histórico de instalações"""
        print("\n📋 HISTÓRICO DE INSTALAÇÕES:\n")
        
        if not self.installation_history["installations"]:
            print("Nenhuma instalação registrada.")
            return
        
        for install in self.installation_history["installations"]:
            print(f"  • {install['manifest']}")
            print(f"    Data: {install['date']}")
            print(f"    Itens: {install['items_installed']}/{install['total_items']}")
            print()
        
        print(f"Total geral: {self.installation_history['total_installed']} itens instalados")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Manifest Installer - Steam Tools & Lua Tools")
    parser.add_argument("--install", type=str, help="Instalar manifest específico")
    parser.add_argument("--list", action="store_true", help="Listar manifests disponíveis")
    parser.add_argument("--installed", action="store_true", help="Mostrar histórico de instalações")
    parser.add_argument("--generate-bulk", type=str, nargs=3, metavar=("START", "END", "NAME"), help="Gerar manifest em massa")
    parser.add_argument("--auto", action="store_true", help="Modo automático (sem confirmações)")
    
    args = parser.parse_args()
    
    installer = ManifestInstaller()
    
    if args.list:
        installer.list_manifests()
    elif args.installed:
        installer.show_installed()
    elif args.generate_bulk:
        start, end, name = args.generate_bulk
        installer.generate_bulk_manifest(int(start), int(end), name)
    elif args.install:
        manifest_path = args.install
        if not manifest_path.endswith(".json"):
            manifest_path = str(installer.manifests_dir / f"{manifest_path}.json")
        installer.install_manifest(manifest_path, auto_confirm=args.auto)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
