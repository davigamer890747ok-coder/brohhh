#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pacote Steam + de Mil 100 Jogos - Davizin_Script TM
Interface Desktop Moderna com suporte a Steam Tools e Lua Tools
Autor: Davizin_Script TM

Requisitos:
    pip install customtkinter packaging

Uso:
    python steam_gui.py
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import subprocess
import threading
from datetime import datetime
from pathlib import Path

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GameLibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Pacote Steam + de Mil 100 Jogos - Davizin_Script TM")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Dados dos jogos
        self.games_data = []
        self.installed_games = set()
        self.categories = {
            "Todos os Jogos": [],
            "Ação": [],
            "Aventura": [],
            "RPG": [],
            "Estratégia": [],
            "Corrida": [],
            "Esportes": [],
            "Simulação": [],
            "Terror": [],
            "Indie": [],
            "Multiplayer": [],
            "Outros": []
        }
        
        # Carregar dados
        self.load_games_data()
        
        # Configurar layout
        self.setup_ui()
        
    def load_games_data(self):
        """Carrega dados dos jogos (simulado + manifests reais)"""
        # Jogos populares com capas
        popular_games = [
            {"id": 271590, "name": "GTA V", "genre": "Ação", "size": "94 GB", "category": "Ação", "icon": "🎮"},
            {"id": 1174180, "name": "Red Dead Redemption 2", "genre": "Aventura", "size": "150 GB", "category": "Aventura", "icon": "🤠"},
            {"id": 292030, "name": "The Witcher 3", "genre": "RPG", "size": "50 GB", "category": "RPG", "icon": "⚔️"},
            {"id": 1091500, "name": "Cyberpunk 2077", "genre": "RPG", "size": "70 GB", "category": "RPG", "icon": "🦾"},
            {"id": 1245620, "name": "Elden Ring", "genre": "RPG", "size": "60 GB", "category": "RPG", "icon": "👑"},
            {"id": 1593500, "name": "God of War", "genre": "Ação", "size": "70 GB", "category": "Ação", "icon": "🪓"},
            {"id": 1145360, "name": "Hades", "genre": "Ação", "size": "15 GB", "category": "Ação", "icon": "🔥"},
            {"id": 367520, "name": "Hollow Knight", "genre": "Aventura", "size": "9 GB", "category": "Indie", "icon": "🐛"},
            {"id": 814380, "name": "Sekiro", "genre": "Ação", "size": "25 GB", "category": "Ação", "icon": "🗡️"},
            {"id": 1551360, "name": "Forza Horizon 5", "genre": "Corrida", "size": "110 GB", "category": "Corrida", "icon": "🏎️"},
            {"id": 4000, "name": "Garry's Mod", "genre": "Simulação", "size": "5 GB", "category": "Simulação", "icon": "🔧", "dlcs": [223090, 489830, 489831, 489832, 489833, 489834, 489835]},
            {"id": 105600, "name": "Terraria", "genre": "Aventura", "size": "1 GB", "category": "Aventura", "icon": "⛏️"},
            {"id": 413150, "name": "Stardew Valley", "genre": "Simulação", "size": "1 GB", "category": "Simulação", "icon": "🌾"},
            {"id": 1086940, "name": "Baldur's Gate 3", "genre": "RPG", "size": "150 GB", "category": "RPG", "icon": "🐉"},
            {"id": 1172470, "name": "Apex Legends", "genre": "Ação", "size": "56 GB", "category": "Multiplayer", "icon": "🔫"},
            {"id": 730, "name": "Counter-Strike 2", "genre": "Ação", "size": "35 GB", "category": "Multiplayer", "icon": "💣"},
            {"id": 570, "name": "Dota 2", "genre": "Estratégia", "size": "60 GB", "category": "Multiplayer", "icon": "🏰"},
            {"id": 440, "name": "Team Fortress 2", "genre": "Ação", "size": "15 GB", "category": "Multiplayer", "icon": "🎩"},
            {"id": 1091500, "name": "Cyberpunk 2077", "genre": "RPG", "size": "70 GB", "category": "RPG", "icon": "🌃"},
            {"id": 1245620, "name": "ELDEN RING", "genre": "RPG", "size": "60 GB", "category": "RPG", "icon": "🌳"},
        ]
        
        # Adicionar jogos populares
        self.games_data.extend(popular_games)
        
        # Gerar mais jogos automaticamente para chegar a 1107
        genres = ["Ação", "Aventura", "RPG", "Estratégia", "Corrida", "Esportes", "Simulação", "Terror", "Indie"]
        categories_map = {
            "Ação": "Ação", "Aventura": "Aventura", "RPG": "RPG", 
            "Estratégia": "Estratégia", "Corrida": "Corrida", "Esportes": "Esportes",
            "Simulação": "Simulação", "Terror": "Terror", "Indie": "Indie"
        }
        
        base_names = [
            "Warfare", "Quest", "Legends", "Simulator", "Racing Pro", "Sports Championship",
            "Horror Nights", "Indie Adventure", "Battle Arena", "Space Explorer",
            "Fantasy World", "Modern Combat", "Medieval Times", "Future Tech",
            "Zombie Survival", "City Builder", "Farm Life", "Ocean Adventure",
            "Mountain Climbing", "Desert Storm", "Arctic Mission", "Jungle Expedition"
        ]
        
        for i in range(len(self.games_data), 1107):
            genre = genres[i % len(genres)]
            name = f"{base_names[i % len(base_names)]} {i+1}"
            size = f"{(i % 100) + 5} GB"
            
            game = {
                "id": 100000 + i,
                "name": name,
                "genre": genre,
                "size": size,
                "category": categories_map.get(genre, "Outros"),
                "icon": "🎮"
            }
            self.games_data.append(game)
        
        # Organizar por categorias
        for game in self.games_data:
            cat = game.get("category", "Outros")
            if cat in self.categories:
                self.categories[cat].append(game)
            else:
                self.categories["Outros"].append(game)
        
        # Adicionar "Todos os Jogos"
        self.categories["Todos os Jogos"] = self.games_data.copy()
        
        # Carregar jogos instalados (simulado)
        self.load_installed_games()
        
    def load_installed_games(self):
        """Carrega lista de jogos instalados"""
        installed_file = Path("installed_games.json")
        if installed_file.exists():
            try:
                with open(installed_file, 'r') as f:
                    data = json.load(f)
                    self.installed_games = set(data.get('games', []))
            except:
                self.installed_games = set()
        else:
            # Simular alguns jogos instalados
            self.installed_games = {730, 570, 440}  # CS2, Dota 2, TF2
            
    def save_installed_games(self):
        """Salva lista de jogos instalados"""
        installed_file = Path("installed_games.json")
        with open(installed_file, 'w') as f:
            json.dump({'games': list(self.installed_games), 'date': str(datetime.now())}, f, indent=2)
    
    def setup_ui(self):
        """Configura a interface principal"""
        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Main content
        self.grid_rowconfigure(2, weight=0)  # Footer
        
        # Criar header
        self.create_header()
        
        # Criar conteúdo principal (sidebar + lista de jogos)
        self.create_main_content()
        
        # Criar footer
        self.create_footer()
        
    def create_header(self):
        """Cria o cabeçalho"""
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a2e")
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame, 
            text="PACOTE STEAM + DE MIL 100 JOGOS",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        title_label.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="DAVIZIN_SCRIPT TM",
            font=ctk.CTkFont(size=14),
            text_color="#00ff88"
        )
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")
        
        # Box com informações à direita
        info_frame = ctk.CTkFrame(header_frame, fg_color="#16213e", corner_radius=10)
        info_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=15, sticky="e")
        
        # Texto DAVIZIN_SCRIPT TM
        brand_label = ctk.CTkLabel(
            info_frame,
            text="DAVIZIN_SCRIPT TM",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#00ff88"
        )
        brand_label.pack(pady=(10, 5))
        
        # Indicador total de jogos
        total_label = ctk.CTkLabel(
            info_frame,
            text=f"TOTAL DE JOGOS: {len(self.games_data)}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00ff88"
        )
        total_label.pack(pady=(5, 10))
        
    def create_main_content(self):
        """Cria o conteúdo principal com sidebar e lista de jogos"""
        main_frame = ctk.CTkFrame(self, fg_color="#0f0f1a")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Criar sidebar
        self.create_sidebar(main_frame)
        
        # Criar área de lista de jogos
        self.create_game_list_area(main_frame)
        
    def create_sidebar(self, parent):
        """Cria a barra lateral esquerda"""
        sidebar = ctk.CTkFrame(parent, width=280, corner_radius=0, fg_color="#1a1a2e")
        sidebar.grid(row=0, column=0, sticky="ns", padx=0, pady=0)
        sidebar.grid_rowconfigure(2, weight=1)
        
        # Ícone estilo Steam no topo
        icon_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        icon_frame.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        
        # Círculo com braço mecânico estilizado (emoji como placeholder)
        steam_icon = ctk.CTkLabel(
            icon_frame,
            text="⚙️",
            font=ctk.CTkFont(size=48),
            text_color="#00ff88"
        )
        steam_icon.pack()
        
        steam_label = ctk.CTkLabel(
            icon_frame,
            text="STEAM TOOLS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffffff"
        )
        steam_label.pack(pady=(5, 0))
        
        lua_label = ctk.CTkLabel(
            icon_frame,
            text="LUA TOOLS",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#00ccff"
        )
        lua_label.pack(pady=(2, 0))
        
        # Seção CATEGORIAS
        cat_label = ctk.CTkLabel(
            sidebar,
            text="CATEGORIAS",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#888888"
        )
        cat_label.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Lista de categorias
        self.category_buttons = {}
        categories_list = [
            "Todos os Jogos", "Ação", "Aventura", "RPG", "Estratégia",
            "Corrida", "Esportes", "Simulação", "Terror", "Indie",
            "Multiplayer", "Outros"
        ]
        
        for idx, cat in enumerate(categories_list):
            count = len(self.categories.get(cat, []))
            btn = ctk.CTkButton(
                sidebar,
                text=f"{cat} ({count})",
                font=ctk.CTkFont(size=12),
                height=35,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#2a2a4e",
                text_color="#cccccc",
                anchor="w",
                command=lambda c=cat: self.filter_by_category(c)
            )
            btn.grid(row=2, column=0, padx=20, pady=2, sticky="ew")
            self.category_buttons[cat] = btn
            
            if idx == 0:  # Destacar "Todos os Jogos"
                btn.configure(fg_color="#0066cc", text_color="#ffffff")
        
        # Seção OPÇÕES
        opt_label = ctk.CTkLabel(
            sidebar,
            text="OPÇÕES",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#888888"
        )
        opt_label.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Botão INSTALAR SELECIONADO (verde)
        install_btn = ctk.CTkButton(
            sidebar,
            text="INSTALAR SELECIONADO",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color="#00cc66",
            hover_color="#00aa55",
            text_color="#ffffff",
            command=self.install_selected
        )
        install_btn.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        
        # Botão VER INFORMAÇÕES (cinza)
        info_btn = ctk.CTkButton(
            sidebar,
            text="VER INFORMAÇÕES",
            font=ctk.CTkFont(size=12),
            height=40,
            corner_radius=8,
            fg_color="#444444",
            hover_color="#555555",
            text_color="#ffffff",
            command=self.show_info
        )
        info_btn.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        
        # Botão REMOVER JOGO (vermelho)
        remove_btn = ctk.CTkButton(
            sidebar,
            text="REMOVER JOGO",
            font=ctk.CTkFont(size=12),
            height=40,
            corner_radius=8,
            fg_color="#cc3333",
            hover_color="#aa2222",
            text_color="#ffffff",
            command=self.remove_game
        )
        remove_btn.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        
        # Seção FILTROS
        filter_label = ctk.CTkLabel(
            sidebar,
            text="FILTROS",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#888888"
        )
        filter_label.grid(row=7, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Campo de busca
        self.search_entry = ctk.CTkEntry(
            sidebar,
            placeholder_text="Pesquisar jogo...",
            font=ctk.CTkFont(size=12),
            height=40,
            corner_radius=8,
            fg_color="#2a2a4e",
            border_color="#444444",
            text_color="#ffffff"
        )
        self.search_entry.grid(row=8, column=0, padx=20, pady=5, sticky="ew")
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_games())
        
        # Checkbox "Mostrar apenas instalados"
        self.installed_only_var = ctk.BooleanVar(value=False)
        installed_checkbox = ctk.CTkCheckBox(
            sidebar,
            text="Mostrar apenas instalados",
            variable=self.installed_only_var,
            font=ctk.CTkFont(size=12),
            checkbox_width=18,
            checkbox_height=18,
            fg_color="#0066cc",
            hover_color="#0055aa",
            text_color="#cccccc",
            command=self.filter_installed
        )
        installed_checkbox.grid(row=9, column=0, padx=20, pady=10, sticky="w")
        
        # Informações Steam Tools e Lua Tools
        tools_frame = ctk.CTkFrame(sidebar, fg_color="#16213e", corner_radius=10)
        tools_frame.grid(row=10, column=0, padx=20, pady=20, sticky="ew")
        
        steam_tools_label = ctk.CTkLabel(
            tools_frame,
            text="✓ Steam Tools",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#00ff88"
        )
        steam_tools_label.pack(pady=5)
        
        lua_tools_label = ctk.CTkLabel(
            tools_frame,
            text="✓ Lua Tools",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#00ccff"
        )
        lua_tools_label.pack(pady=5)
        
        auto_label = ctk.CTkLabel(
            tools_frame,
            text="Instalação Automática",
            font=ctk.CTkFont(size=10),
            text_color="#888888"
        )
        auto_label.pack(pady=5)
        
    def create_game_list_area(self, parent):
        """Cria a área principal com a lista de jogos"""
        list_frame = ctk.CTkFrame(parent, corner_radius=0, fg_color="#0f0f1a")
        list_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Criar tabela com Treeview
        style = ttk.Style()
        style.theme_use("default")
        
        # Configurar cores do Treeview
        style.configure("Treeview",
            background="#1a1a2e",
            foreground="#ffffff",
            fieldbackground="#1a1a2e",
            rowheight=50,
            font=("Arial", 11)
        )
        
        style.configure("Treeview.Heading",
            background="#16213e",
            foreground="#00ff88",
            font=("Arial", 12, "bold")
        )
        
        style.map("Treeview",
            background=[('selected', '#0066cc')],
            foreground=[('selected', '#ffffff')]
        )
        
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        
        # Scrollbar horizontal
        scrollbar_x = ttk.Scrollbar(list_frame, orient="horizontal")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Treeview
        columns = ("num", "game", "genre", "size", "status")
        self.game_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        self.game_tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        
        scrollbar_y.config(command=self.game_tree.yview)
        scrollbar_x.config(command=self.game_tree.xview)
        
        # Configurar colunas
        self.game_tree.heading("num", text="#")
        self.game_tree.heading("game", text="JOGO")
        self.game_tree.heading("genre", text="GÊNERO")
        self.game_tree.heading("size", text="TAMANHO")
        self.game_tree.heading("status", text="STATUS")
        
        self.game_tree.column("num", width=50, anchor="center")
        self.game_tree.column("game", width=400, minwidth=300)
        self.game_tree.column("genre", width=150, anchor="center")
        self.game_tree.column("size", width=100, anchor="center")
        self.game_tree.column("status", width=150, anchor="center")
        
        # Preencher com dados iniciais
        self.populate_game_list(self.games_data)
        
    def populate_game_list(self, games):
        """Preenche a lista de jogos"""
        # Limpar lista atual
        for item in self.game_tree.get_children():
            self.game_tree.delete(item)
        
        # Adicionar jogos
        for idx, game in enumerate(games, 1):
            status = "Instalado" if game['id'] in self.installed_games else "Não instalado"
            status_color = "#00ff88" if status == "Instalado" else "#888888"
            
            # Ícone + nome do jogo
            game_name = f"{game.get('icon', '🎮')} {game['name']}"
            
            # Verificar se tem DLCs
            if 'dlcs' in game:
                game_name += f" (+{len(game['dlcs'])} DLCs)"
            
            self.game_tree.insert("", "end", values=(
                idx,
                game_name,
                game['genre'],
                game['size'],
                status
            ), tags=(status,))
            
        # Configurar tags de cor para status
        self.game_tree.tag_configure("Instalado", foreground="#00ff88")
        self.game_tree.tag_configure("Não instalado", foreground="#888888")
        
    def filter_by_category(self, category):
        """Filtra jogos por categoria"""
        # Resetar cores dos botões
        for btn in self.category_buttons.values():
            btn.configure(fg_color="transparent", text_color="#cccccc")
        
        # Destacar botão selecionado
        self.category_buttons[category].configure(fg_color="#0066cc", text_color="#ffffff")
        
        # Filtrar jogos
        games = self.categories.get(category, [])
        
        # Aplicar filtro de instalados se necessário
        if self.installed_only_var.get():
            games = [g for g in games if g['id'] in self.installed_games]
        
        self.populate_game_list(games)
        
    def search_games(self):
        """Busca jogos pelo nome"""
        query = self.search_entry.get().lower()
        
        if not query:
            self.filter_by_category("Todos os Jogos")
            return
        
        # Buscar em todos os jogos ou na categoria atual
        current_category = None
        for cat, btn in self.category_buttons.items():
            if btn.cget("fg_color") == "#0066cc":
                current_category = cat
                break
        
        if current_category:
            games = self.categories.get(current_category, [])
        else:
            games = self.games_data
        
        # Filtrar por nome
        filtered = [g for g in games if query in g['name'].lower()]
        
        # Aplicar filtro de instalados se necessário
        if self.installed_only_var.get():
            filtered = [g for g in filtered if g['id'] in self.installed_games]
        
        self.populate_game_list(filtered)
        
    def filter_installed(self):
        """Filtra para mostrar apenas jogos instalados"""
        # Obter categoria atual
        current_category = None
        for cat, btn in self.category_buttons.items():
            if btn.cget("fg_color") == "#0066cc":
                current_category = cat
                break
        
        if not current_category:
            current_category = "Todos os Jogos"
        
        games = self.categories.get(current_category, [])
        
        if self.installed_only_var.get():
            games = [g for g in games if g['id'] in self.installed_games]
        
        self.populate_game_list(games)
        
    def install_selected(self):
        """Instala jogo(s) selecionado(s) com Steam Tools e Lua Tools"""
        selected_items = self.game_tree.selection()
        
        if not selected_items:
            messagebox.showwarning("Atenção", "Selecione pelo menos um jogo para instalar!")
            return
        
        # Obter IDs dos jogos selecionados
        games_to_install = []
        for item in selected_items:
            values = self.game_tree.item(item, 'values')
            game_name = values[1].split(' ', 1)[1] if ' ' in values[1] else values[1]
            # Encontrar jogo correspondente
            for game in self.games_data:
                if game['name'] in game_name or game_name in game['name']:
                    games_to_install.append(game)
                    break
        
        if not games_to_install:
            messagebox.showerror("Erro", "Não foi possível identificar os jogos selecionados!")
            return
        
        # Confirmar instalação
        confirm = messagebox.askyesno(
            "Confirmar Instalação",
            f"Deseja instalar {len(games_to_install)} jogo(s)?\n\n"
            f"Incluirá:\n"
            f"• SteamCMD (jogos)\n"
            f"• LuaRocks (ferramentas Lua)\n"
            f"• DLCs associadas (se houver)\n\n"
            f"Isso pode levar muito tempo dependendo do tamanho dos jogos."
        )
        
        if not confirm:
            return
        
        # Executar instalação em thread separada
        def install_thread():
            try:
                from manifest_installer import ManifestInstaller
                installer = ManifestInstaller()
                
                for game in games_to_install:
                    # Instalar jogo via SteamCMD
                    self.update_status(f"Instalando {game['name']}...")
                    
                    # Criar manifest temporário
                    temp_manifest = {
                        "name": f"temp_{game['id']}",
                        "description": f"Instalação de {game['name']}",
                        "apps": [game['id']],
                        "tools": ["luajit", "lfs"],
                        "dlcs": game.get('dlcs', [])
                    }
                    
                    # Salvar manifest temporário
                    with open(f"temp_manifest_{game['id']}.json", 'w') as f:
                        json.dump(temp_manifest, f, indent=2)
                    
                    # Instalar
                    installer.install_manifest(f"temp_manifest_{game['id']}.json", auto_confirm=True)
                    
                    # Atualizar lista de instalados
                    self.installed_games.add(game['id'])
                    
                    # Limpar arquivo temporário
                    os.remove(f"temp_manifest_{game['id']}.json")
                
                # Salvar jogos instalados
                self.save_installed_games()
                
                # Atualizar interface
                self.after(0, lambda: self.populate_game_list(self.games_data))
                self.after(0, lambda: messagebox.showinfo("Sucesso", f"{len(games_to_install)} jogo(s) instalado(s) com sucesso!"))
                
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Erro", f"Erro na instalação: {str(e)}"))
            finally:
                self.after(0, lambda: self.status_label.configure(text="Pronto"))
        
        # Iniciar thread
        threading.Thread(target=install_thread, daemon=True).start()
        
        # Mostrar status
        self.status_label.configure(text="Instalando...")
        
    def show_info(self):
        """Mostra informações sobre o jogo selecionado"""
        selected_items = self.game_tree.selection()
        
        if not selected_items:
            messagebox.showinfo("Informações", "Selecione um jogo para ver informações detalhadas.")
            return
        
        item = selected_items[0]
        values = self.game_tree.item(item, 'values')
        
        # Encontrar jogo correspondente
        game_name = values[1].split(' ', 1)[1] if ' ' in values[1] else values[1]
        game = None
        for g in self.games_data:
            if g['name'] in game_name or game_name in g['name']:
                game = g
                break
        
        if game:
            info_text = f"""
            Nome: {game['name']}
            ID: {game['id']}
            Gênero: {game['genre']}
            Tamanho: {game['size']}
            Categoria: {game.get('category', 'N/A')}
            Status: {'Instalado' if game['id'] in self.installed_games else 'Não instalado'}
            
            Steam Tools: ✓ Suportado
            Lua Tools: ✓ Suportado
            
            """
            
            if 'dlcs' in game:
                info_text += f"\nDLCs incluídas: {len(game['dlcs'])}\n"
                info_text += f"IDs das DLCs: {', '.join(map(str, game['dlcs']))}"
            
            messagebox.showinfo(f"Informações - {game['name']}", info_text)
        else:
            messagebox.showinfo("Informações", "Jogo não encontrado na base de dados.")
            
    def remove_game(self):
        """Remove jogo(s) selecionado(s)"""
        selected_items = self.game_tree.selection()
        
        if not selected_items:
            messagebox.showwarning("Atenção", "Selecione pelo menos um jogo para remover!")
            return
        
        confirm = messagebox.askyesno(
            "Confirmar Remoção",
            "Deseja realmente remover o(s) jogo(s) selecionado(s)?\n\n"
            "Isso irá desinstalar os jogos do seu sistema."
        )
        
        if not confirm:
            return
        
        # Obter IDs dos jogos
        games_to_remove = []
        for item in selected_items:
            values = self.game_tree.item(item, 'values')
            game_name = values[1].split(' ', 1)[1] if ' ' in values[1] else values[1]
            
            for game in self.games_data:
                if game['name'] in game_name or game_name in game['name']:
                    games_to_remove.append(game)
                    break
        
        # Remover da lista de instalados
        for game in games_to_remove:
            self.installed_games.discard(game['id'])
        
        # Salvar alterações
        self.save_installed_games()
        
        # Atualizar interface
        self.populate_game_list(self.games_data)
        
        messagebox.showinfo("Sucesso", f"{len(games_to_remove)} jogo(s) removido(s) da lista de instalados!")
        
    def update_list(self):
        """Atualiza a lista de jogos"""
        self.load_games_data()
        
        # Resetar para "Todos os Jogos"
        self.filter_by_category("Todos os Jogos")
        
        messagebox.showinfo("Atualizado", "Lista de jogos atualizada com sucesso!")
        
    def export_list(self):
        """Exporta lista de jogos para JSON"""
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Exportar lista de jogos"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        'total_games': len(self.games_data),
                        'export_date': str(datetime.now()),
                        'games': self.games_data,
                        'installed': list(self.installed_games)
                    }, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Sucesso", f"Lista exportada com sucesso!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
                
    def create_footer(self):
        """Cria o rodapé"""
        footer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a2e", height=60)
        footer_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        footer_frame.grid_propagate(False)
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # Texto de copyright
        copyright_label = ctk.CTkLabel(
            footer_frame,
            text="DAVIZIN_SCRIPT TM - Todos os direitos reservados.",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        )
        copyright_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Botões à direita
        buttons_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, padx=20, pady=10, sticky="e")
        
        # Botão ATUALIZAR LISTA
        update_btn = ctk.CTkButton(
            buttons_frame,
            text="ATUALIZAR LISTA",
            font=ctk.CTkFont(size=11),
            height=35,
            corner_radius=6,
            fg_color="#444444",
            hover_color="#555555",
            text_color="#ffffff",
            command=self.update_list
        )
        update_btn.pack(side="left", padx=5)
        
        # Botão EXPORTAR LISTA
        export_btn = ctk.CTkButton(
            buttons_frame,
            text="EXPORTAR LISTA",
            font=ctk.CTkFont(size=11),
            height=35,
            corner_radius=6,
            fg_color="#0066cc",
            hover_color="#0055aa",
            text_color="#ffffff",
            command=self.export_list
        )
        export_btn.pack(side="left", padx=5)
        
        # Botão SAIR
        exit_btn = ctk.CTkButton(
            buttons_frame,
            text="SAIR",
            font=ctk.CTkFont(size=11, weight="bold"),
            height=35,
            corner_radius=6,
            fg_color="#cc3333",
            hover_color="#aa2222",
            text_color="#ffffff",
            command=self.quit
        )
        exit_btn.pack(side="left", padx=5)
        
        # Label de status
        self.status_label = ctk.CTkLabel(
            footer_frame,
            text="Pronto",
            font=ctk.CTkFont(size=10),
            text_color="#00ff88"
        )
        self.status_label.grid(row=0, column=0, padx=20, pady=10, sticky="e")


def main():
    app = GameLibraryApp()
    app.mainloop()


if __name__ == "__main__":
    main()
