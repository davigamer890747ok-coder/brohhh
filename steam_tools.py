#!/usr/bin/env python3
"""
Steam Tools - Uma coleção de ferramentas úteis para usuários da Steam
"""

import requests
import json
import argparse
import sys
from datetime import datetime

class SteamTools:
    def __init__(self):
        self.base_url = "https://api.steampowered.com"
        self.steam_store_url = "https://store.steampowered.com"
        
    def get_app_details(self, app_id):
        """Obter detalhes de um jogo/app na Steam"""
        try:
            url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if str(app_id) in data and data[str(app_id)]['success']:
                app_data = data[str(app_id)]['data']
                print(f"\n{'='*50}")
                print(f"🎮 {app_data.get('name', 'N/A')}")
                print(f"{'='*50}")
                print(f"Tipo: {app_data.get('type', 'N/A')}")
                print(f"Descrição: {app_data.get('short_description', 'N/A')[:200]}...")
                
                if 'price_overview' in app_data:
                    price = app_data['price_overview']
                    print(f"Preço: {price.get('final_formatted', 'Grátis')}")
                
                if 'platforms' in app_data:
                    platforms = app_data['platforms']
                    print(f"Plataformas: ", end="")
                    plat_list = []
                    if platforms.get('windows'): plat_list.append("Windows")
                    if platforms.get('mac'): plat_list.append("Mac")
                    if platforms.get('linux'): plat_list.append("Linux")
                    print(", ".join(plat_list))
                
                if 'categories' in app_data:
                    categories = [cat['description'] for cat in app_data['categories'][:5]]
                    print(f"Categorias: {', '.join(categories)}")
                    
                print(f"{'='*50}\n")
                return app_data
            else:
                print(f"❌ App ID {app_id} não encontrado ou indisponível.")
                return None
        except Exception as e:
            print(f"❌ Erro ao obter detalhes: {e}")
            return None
    
    def search_games(self, query, limit=5):
        """Buscar jogos por nome"""
        try:
            # Usar endpoint alternativo da Steam
            url = "https://api.steampowered.com/ISteamApps/GetAppList/v0002/"
            params = {"format": "json"}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"ℹ️  Busca offline - mostrando exemplos conhecidos")
                # Lista de exemplo para demonstração
                examples = [
                    {"appid": 70, "name": "Half-Life"},
                    {"appid": 220, "name": "Half-Life 2"},
                    {"appid": 380, "name": "Half-Life 2: Episode One"},
                    {"appid": 420, "name": "Half-Life 2: Episode Two"},
                    {"appid": 546560, "name": "Half-Life 2: Update"},
                ]
                results = [ex for ex in examples if query.lower() in ex['name'].lower()]
                if results:
                    print(f"\n🔍 Resultados para '{query}':\n")
                    for i, app in enumerate(results, 1):
                        print(f"{i}. {app['name']} (ID: {app['appid']})")
                    print()
                return results
            
            data = response.json()
            apps = data.get('applist', {}).get('apps', [])
            results = []
            
            for app in apps:
                name = app.get('name', '')
                if name and query.lower() in name.lower():
                    results.append(app)
                    if len(results) >= limit:
                        break
            
            if results:
                print(f"\n🔍 Resultados para '{query}':\n")
                for i, app in enumerate(results, 1):
                    print(f"{i}. {app.get('name')} (ID: {app.get('appid')})")
                print()
                return results
            else:
                print(f"❌ Nenhum jogo encontrado para '{query}'")
                return []
        except requests.exceptions.JSONDecodeError:
            print("❌ Erro ao processar resposta da API. Tente novamente.")
            return []
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            return []
    
    def get_player_count(self, app_id):
        """Obter número de jogadores atuais"""
        try:
            url = f"{self.base_url}/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('response', {}).get('result') == 1:
                count = data['response'].get('player_count', 0)
                print(f"\n👥 Jogadores atuais em {app_id}: {count:,}")
                return count
            else:
                print(f"❌ Não foi possível obter dados de jogadores para {app_id}")
                return None
        except Exception as e:
            print(f"❌ Erro ao obter jogadores: {e}")
            return None
    
    def get_user_games(self, steam_id):
        """Obter jogos de um usuário (requer API key para dados completos)"""
        print(f"\nℹ️  Perfil Steam: {steam_id}")
        print(f"URL do perfil: https://steamcommunity.com/profiles/{steam_id}")
        print("Nota: Para ver a lista completa de jogos, é necessária uma API Key da Steam.")
        print()
    
    def check_deals(self, app_id):
        """Verificar histórico de preços e descontos"""
        try:
            url = f"https://isThereAnyDeal.com/api/prices/historical/"
            print(f"\n💰 Para verificar descontos históricos, visite:")
            print(f"https://isthereanydeal.com/game/{app_id}/info/")
            print(f"https://steamdb.info/app/{app_id}/charts/")
            print()
        except Exception as e:
            print(f"Erro: {e}")
    
    def show_menu(self):
        """Mostrar menu interativo"""
        while True:
            print("\n" + "="*50)
            print("🎮 STEAM TOOLS 🎮")
            print("="*50)
            print("1. 🔍 Buscar jogos por nome")
            print("2. 📋 Ver detalhes de um jogo (por App ID)")
            print("3. 👥 Ver jogadores atuais")
            print("4. 👤 Informações de usuário Steam")
            print("5. 💰 Verificar descontos")
            print("6. 🚪 Sair")
            print("="*50)
            
            choice = input("\nEscolha uma opção (1-6): ").strip()
            
            if choice == '1':
                query = input("Digite o nome do jogo: ").strip()
                if query:
                    self.search_games(query)
            elif choice == '2':
                app_id = input("Digite o App ID: ").strip()
                if app_id.isdigit():
                    self.get_app_details(int(app_id))
            elif choice == '3':
                app_id = input("Digite o App ID: ").strip()
                if app_id.isdigit():
                    self.get_player_count(int(app_id))
            elif choice == '4':
                steam_id = input("Digite o Steam ID: ").strip()
                if steam_id:
                    self.get_user_games(steam_id)
            elif choice == '5':
                app_id = input("Digite o App ID: ").strip()
                if app_id.isdigit():
                    self.check_deals(int(app_id))
            elif choice == '6':
                print("\nObrigado por usar Steam Tools! 🎮")
                break
            else:
                print("Opção inválida!")

def main():
    parser = argparse.ArgumentParser(description='Steam Tools - Ferramentas para Steam')
    parser.add_argument('--search', type=str, help='Buscar jogos por nome')
    parser.add_argument('--app', type=int, help='Obter detalhes do App ID')
    parser.add_argument('--players', type=int, help='Ver jogadores atuais do App ID')
    parser.add_argument('--user', type=str, help='Informações do usuário Steam')
    parser.add_argument('--deals', type=int, help='Verificar descontos do App ID')
    parser.add_argument('--interactive', action='store_true', help='Modo interativo')
    
    args = parser.parse_args()
    steam = SteamTools()
    
    if args.search:
        steam.search_games(args.search)
    elif args.app:
        steam.get_app_details(args.app)
    elif args.players:
        steam.get_player_count(args.players)
    elif args.user:
        steam.get_user_games(args.user)
    elif args.deals:
        steam.check_deals(args.deals)
    elif args.interactive or len(sys.argv) == 1:
        steam.show_menu()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
