import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
import threading
import random
import time
import os
from PIL import Image, ImageDraw, ImageFont
import io

# --- CONFIGURAÇÕES GERAIS ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Paleta de Cores Oficial Steam Modernizada
COLORS = {
    "bg_main": "#121212",          # Fundo principal (quase preto)
    "bg_sidebar": "#1b2838",       # Azul clássico Steam
    "bg_card": "#2a475e",          # Fundo do card
    "bg_card_hover": "#3d6a8f",    # Hover do card
    "accent_blue": "#66c0f4",      # Texto destaque
    "btn_green": "#5c7e10",        # Botão Instalar
    "btn_green_hover": "#4c6b22",
    "text_main": "#ffffff",
    "text_dim": "#8f98a0",
    "badge_rpg": "#8e44ad",
    "badge_action": "#c0392b",
    "badge_strategy": "#27ae60",
    "badge_sim": "#d35400"
}

class GameDatabase:
    """Gerencia a base de dados de 100.000 jogos sem travar a memória"""
    
    GENRES = ["Ação", "Aventura", "RPG", "Estratégia", "Simulação", "Corrida", "Esportes", "Indie", "Terror"]
    BASE_GAMES = [
        "Counter-Strike", "Dota", "Half-Life", "Portal", "Left 4 Dead", "Team Fortress", 
        "Garry's Mod", "Rust", "ARK", "DayZ", "Fallout", "The Elder Scrolls", "Skyrim", 
        "Oblivion", "Morrowind", "Grand Theft Auto", "Red Dead", "Cyberpunk", "Witcher", 
        "Assassin's Creed", "Far Cry", "Watch Dogs", "Rainbow Six", "Ghost Recon", 
        "Call of Duty", "Battlefield", "Titanfall", "Apex Legends", "Mass Effect", 
        "Dragon Age", "FIFA", "NBA 2K", "F1", "Forza", "Halo", "Gears of War", 
        "Sea of Thieves", "State of Decay", "Grounded", "Microsoft Flight Simulator",
        "Stardew Valley", "Terraria", "Minecraft", "Roblox", "Among Us", "Fall Guys",
        "Valheim", "V Rising", "Project Zomboid", "Phasmophobia", "Lethal Company"
    ]

    def __init__(self, total_games=100000):
        self.total_games = total_games
        self.cache = {} # Cache simples para não regenerar tudo se filtrar
        
    def get_game(self, index):
        """Gera dados do jogo sob demanda (Lazy Generation)"""
        if index in self.cache:
            return self.cache[index]

        # Lógica para gerar nomes únicos mas realistas
        base_name = random.choice(self.BASE_GAMES)
        suffix = ""
        
        if index < 20:
            # Primeiros 20 são jogos famosos reais
            famous = [
                ("Counter-Strike 2", "Ação", 730), ("Dota 2", "MOBA", 570), 
                ("GTA V", "Aventura", 271590), ("RDR 2", "Aventura", 1174180),
                ("The Witcher 3", "RPG", 292030), ("Cyberpunk 2077", "RPG", 1091500),
                ("Elden Ring", "RPG", 1245620), ("God of War", "Ação", 1593500),
                ("Hades", "Indie", 1145360), ("Hollow Knight", "Indie", 367520),
                ("Sekiro", "Ação", 814380), ("Forza Horizon 5", "Corrida", 1551360),
                ("Baldur's Gate 3", "RPG", 1086940), ("Stardew Valley", "Simulação", 413150),
                ("Terraria", "Aventura", 105600), ("Dark Souls III", "RPG", 374320),
                ("Monster Hunter", "Ação", 582010), ("Resident Evil 4", "Terror", 2050650),
                ("Spider-Man", "Ação", 1817070), ("Horizon Zero Dawn", "RPG", 1151640)
            ]
            if index < len(famous):
                name, genre, appid = famous[index]
                return self._create_entry(index, name, genre, appid)

        # Geração procedural para os outros 99.980 jogos
        suffixes = ["Remastered", "Ultimate Edition", "Gold Edition", "II", "III", "IV", "Online", "VR", "Director's Cut", "Anniversary"]
        if random.random() > 0.7:
            suffix = f" {random.choice(suffixes)}"
        
        genre = random.choice(self.GENRES)
        appid = 100000 + index # AppIDs fictícios acima de 100k
        
        full_name = f"{base_name}{suffix} #{index}"
        return self._create_entry(index, full_name, genre, appid)

    def _create_entry(self, idx, name, genre, appid):
        # Determinar tamanho aleatório
        size = f"{random.randint(1, 150)} GB" if random.random() > 0.3 else f"{random.randint(500, 9000)} MB"
        
        entry = {
            "id": idx,
            "name": name,
            "genre": genre,
            "size": size,
            "appid": str(appid),
            "installed": False,
            "description": f"Uma experiência incrível em {genre}. Junte-se a milhões de jogadores nesta aventura épica."
        }
        
        # Cache apenas dos últimos acessados para economizar RAM
        if len(self.cache) > 500:
            self.cache.pop(next(iter(self.cache)))
        self.cache[idx] = entry
        return entry

    def search(self, query):
        """Retorna índices dos jogos que correspondem à busca"""
        # Nota: Em 100k, uma busca linear é rápida o suficiente se feita em thread, 
        # mas aqui faremos uma amostragem inteligente para a UI não travar ao digitar
        matches = []
        query = query.lower()
        
        # Otimização: Varre apenas se necessário. 
        # Para demo, vamos varrer um subset ou usar gerador
        count = 0
        for i in range(self.total_games):
            game = self.get_game(i)
            if query in game['name'].lower() or query in game['genre'].lower():
                matches.append(i)
                count += 1
                if count > 1000: break # Limita resultados para não travar a UI inicial
                
        return matches

class HoverCard(ctk.CTkFrame):
    """Card de jogo com efeito de hover e imagem dinâmica"""
    def __init__(self, parent, game_data, install_callback, width=200, height=280):
        super().__init__(parent, fg_color=COLORS["bg_card"], corner_radius=10, width=width, height=height)
        self.game_data = game_data
        self.install_callback = install_callback
        self.width = width
        self.height = height
        self.img_label = None
        
        self._setup_ui()
        self._bind_hover()

    def _setup_ui(self):
        self.pack_propagate(False) # Mantém tamanho fixo
        
        # 1. Imagem (Placeholder inicial)
        self.img_frame = ctk.CTkFrame(self, fg_color="black", width=self.width, height=140)
        self.img_frame.pack(pady=(10, 5), padx=5, anchor="n")
        self.img_frame.pack_propagate(False)
        
        self.lbl_placeholder = ctk.CTkLabel(self.img_frame, text="Carregando...", text_color=COLORS["text_dim"])
        self.lbl_placeholder.place(relx=0.5, rely=0.5, anchor="center")
        
        # Iniciar download da imagem em background
        threading.Thread(target=self._load_image, daemon=True).start()

        # 2. Título
        self.title_lbl = ctk.CTkLabel(
            self, text=self.game_data['name'], 
            font=ctk.CTkFont(size=13, weight="bold"), 
            text_color=COLORS["text_main"], 
            wraplength=self.width - 20, justify="left"
        )
        self.title_lbl.pack(padx=10, pady=(5, 0), anchor="w")

        # 3. Gênero Badge
        genre_color = COLORS.get(f"badge_{self.game_data['genre'].lower()}", COLORS["text_dim"])
        self.genre_lbl = ctk.CTkLabel(
            self, text=self.game_data['genre'],
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#fff", bg_color=genre_color, corner_radius=4
        )
        self.genre_lbl.pack(padx=10, pady=(5, 0), anchor="w")

        # 4. Tamanho e Status
        info_txt = f"💾 {self.game_data['size']}"
        self.info_lbl = ctk.CTkLabel(self, text=info_txt, text_color=COLORS["text_dim"], font=ctk.CTkFont(size=10))
        self.info_lbl.pack(padx=10, pady=(5, 0), anchor="w")

        # 5. Botão
        btn_text = "INSTALAR" if not self.game_data['installed'] else "INSTALADO"
        btn_color = COLORS["btn_green"] if not self.game_data['installed'] else COLORS["text_dim"]
        
        self.btn = ctk.CTkButton(
            self, text=btn_text,
            fg_color=btn_color,
            hover_color=COLORS["btn_green_hover"] if not self.game_data['installed'] else COLORS["bg_card_hover"],
            font=ctk.CTkFont(size=11, weight="bold"),
            height=28,
            command=lambda: self.install_callback(self.game_data)
        )
        self.btn.pack(fill="x", padx=10, pady=10)

    def _load_image(self):
        appid = self.game_data['appid']
        url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"
        
        # Para jogos gerados (>100k), a steam pode não ter imagem. Usamos placeholder gerado.
        try:
            if int(appid) > 2000000: # Se for ID fake muito alto
                raise Exception("Fake ID")
                
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                img_data = resp.content
                img = Image.open(io.BytesIO(img_data))
                img = img.resize((self.width, 140), Image.Resampling.LANCZOS)
                self._update_img(img)
            else:
                raise Exception("404")
        except:
            # Gerar imagem procedural com as cores do gênero
            img = Image.new('RGB', (self.width, 140), color=(40, 40, 40))
            draw = ImageDraw.Draw(img)
            # Desenhar texto simples
            draw.text((10, 60), self.game_data['name'][:15], fill=(100, 100, 100))
            self._update_img(img)

    def _update_img(self, img):
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(self.width, 140))
        self.after(0, lambda: self._apply_img(ctk_img))

    def _apply_img(self, ctk_img):
        if self.img_label: self.img_label.destroy()
        self.img_label = ctk.CTkLabel(self.img_frame, text="", image=ctk_img)
        self.img_label.place(x=0, y=0)
        self.lbl_placeholder.destroy()

    def _bind_hover(self):
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        # Bind children também para o efeito funcionar ao passar sobre labels/botões
        for child in self.winfo_children():
            child.bind("<Enter>", self._on_enter)
            child.bind("<Leave>", self._on_leave)

    def _on_enter(self, event=None):
        self.configure(fg_color=COLORS["bg_card_hover"])

    def _on_leave(self, event=None):
        self.configure(fg_color=COLORS["bg_card"])

class SteamLibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Pacote Steam + 100 Mil Jogos - Davizin_Script TM")
        self.geometry("1400x900")
        
        # Banco de dados gigante
        self.db = GameDatabase(total_games=100000)
        self.current_indices = list(range(100)) # Carrega apenas os primeiros 100 inicialmente
        
        self._setup_ui()
        self._load_visible_games()

    def _setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=COLORS["bg_sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="ns")
        
        # Logo Area
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=100)
        logo_frame.pack(fill="x", padx=20, pady=20)
        
        lbl_title = ctk.CTkLabel(logo_frame, text="STEAM\nTOOLS", font=ctk.CTkFont(size=28, weight="bold"), text_color=COLORS["accent_blue"])
        lbl_title.pack(side="left")
        
        lbl_sub = ctk.CTkLabel(logo_frame, text="DAVIZIN\nSCRIPT TM", font=ctk.CTkFont(size=12), text_color=COLORS["text_dim"])
        lbl_sub.pack(side="right", pady=30)

        # Search
        self.search_entry = ctk.CTkEntry(self.sidebar, placeholder_text="🔍 Buscar entre 100k jogos...", height=40, border_width=0, fg_color="#152638")
        self.search_entry.pack(fill="x", padx=20, pady=10)
        self.search_entry.bind("<KeyRelease>", lambda e: self._trigger_search())

        # Stats
        stats_lbl = ctk.CTkLabel(self.sidebar, text=f"TOTAL: {self.db.total_games:,} JOGOS", text_color=COLORS["accent_blue"], font=ctk.CTkFont(weight="bold"))
        stats_lbl.pack(pady=10)

        # Categories Scroll
        cat_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        cat_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        cats = ["Todos", "Ação", "Aventura", "RPG", "Estratégia", "Corrida", "Simulação", "Terror", "Indie", "VR"]
        for cat in cats:
            btn = ctk.CTkButton(cat_frame, text=cat, anchor="w", fg_color="transparent", hover_color=COLORS["bg_card_hover"], text_color=COLORS["text_main"])
            btn.pack(fill="x", pady=2)

        # Actions
        act_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=150)
        act_frame.pack(fill="x", padx=20, pady=20)
        act_frame.pack_propagate(False)
        
        btn_install = ctk.CTkButton(act_frame, text="INSTALAR SELECIONADOS", fg_color=COLORS["btn_green"], height=45, font=ctk.CTkFont(weight="bold"))
        btn_install.pack(fill="x", pady=5)
        
        btn_tools = ctk.CTkButton(act_frame, text="GERENCIAR LUA TOOLS", fg_color="#3a4b5e", height=35)
        btn_tools.pack(fill="x", pady=5)

        # --- MAIN AREA ---
        self.main_area = ctk.CTkFrame(self, fg_color=COLORS["bg_main"])
        self.main_area.grid(row=0, column=1, sticky="nsew")
        
        # Header
        header = ctk.CTkFrame(self.main_area, fg_color="transparent", height=60)
        header.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(header, text="BIBLIOTECA DE JOGOS", font=ctk.CTkFont(size=24, weight="bold"), text_color=COLORS["text_main"]).pack(side="left")
        
        self.count_lbl = ctk.CTkLabel(header, text="Mostrando 100 jogos", text_color=COLORS["text_dim"])
        self.count_lbl.pack(side="right")

        # Grid de Jogos (Scrollable)
        # Usamos um frame scrollable normal. Para 100k reais, ideal seria virtualização, 
        # mas aqui carregamos em lotes (chunks) conforme o scroll.
        self.games_container = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        self.games_container.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Configurar grid columns responsivas
        for i in range(6): # 6 colunas
            self.games_container.grid_columnconfigure(i, weight=1)

        # Bind de scroll para carregar mais
        self.games_container.bind("<MouseWheel>", self._on_scroll)
        self.games_container.bind("<Button-4>", self._on_scroll)
        self.games_container.bind("<Button-5>", self._on_scroll)
        
        self.last_scroll = 0
        self.loading_lock = False

    def _load_visible_games(self, start=0, count=60):
        """Carrega um lote de jogos na grade"""
        end = min(start + count, self.db.total_games)
        
        # Limpar se for recarga total
        if start == 0:
            for widget in self.games_container.winfo_children():
                widget.destroy()
        
        row = 0
        col = 0
        max_cols = 6
        
        for i in range(start, end):
            game_data = self.db.get_game(i)
            
            card = HoverCard(self.games_container, game_data, self._install_game)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        self.count_lbl.configure(text=f"Mostrando {start}-{end} de {self.db.total_games:,}")

    def _on_scroll(self, event):
        """Detecta scroll para carregar mais jogos (Infinite Scroll)"""
        if self.loading_lock: return
        
        # Direção do scroll
        direction = event.delta if event.type == "MouseWheel" else (-1 if event.num == 4 else 1)
        
        # Pega posição atual
        current_scroll = self.games_container.yview()[1]
        
        # Se chegou perto do fim (90%)
        if current_scroll > 0.9 and direction < 0:
            self.loading_lock = True
            current_count = int(self.count_lbl.cget("text").split('-')[1].split()[0])
            
            # Carrega mais 60 em thread
            threading.Thread(target=lambda: self._load_more(current_count), daemon=True).start()

    def _load_more(self, current_start):
        time.sleep(0.1) # Pequeno delay
        self.after(0, lambda: self._load_visible_games(start=current_start, count=60))
        self.loading_lock = False

    def _trigger_search(self):
        query = self.search_entry.get()
        if len(query) < 3: return
        
        # Roda busca em thread
        def do_search():
            indices = self.db.search(query)
            self.after(0, lambda: self._show_search_results(indices))
        
        threading.Thread(target=do_search, daemon=True).start()

    def _show_search_results(self, indices):
        # Limpa e mostra resultados
        for widget in self.games_container.winfo_children():
            widget.destroy()
            
        row = 0
        col = 0
        for idx in indices[:100]: # Limita a 100 resultados na tela
            game = self.db.get_game(idx)
            card = HoverCard(self.games_container, game, self._install_game)
            card.grid(row=row, column=col, padx=15, pady=15)
            col += 1
            if col >= 6:
                col = 0
                row += 1
        
        self.count_lbl.configure(text=f"Resultados da busca: {len(indices)} encontrados")

    def _install_game(self, game_data):
        msg = f"Iniciando instalação automática via SteamCMD:\n\nJogo: {game_data['name']}\nID: {game_data['appid']}\nTamanho: {game_data['size']}\n\nBaixar ferramentas Lua necessárias?"
        if messagebox.askyesno("Confirmar Instalação", msg):
            # Aqui chamaria o script backend
            game_data['installed'] = True
            # Atualiza o botão visualmente (simplificado)
            messagebox.showinfo("Davizin Script", "Adicionado à fila de download! O SteamCMD iniciará em breve.")

if __name__ == "__main__":
    app = SteamLibraryApp()
    app.mainloop()
    