from tkinter import PhotoImage, filedialog, Menu, LEFT, SEL_FIRST, SEL_LAST, INSERT, SEL, END, font, ttk, colorchooser, TclError
from customtkinter import CTk, CTkFrame, CTkTextbox, CTkButton, CTkToplevel, CTkLabel, CTkEntry, CTkFont, StringVar, BooleanVar, CTkCheckBox, CTkImage, set_appearance_mode, set_default_color_theme
from tkinter import messagebox
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import urllib.parse
import json
import sys
import os
from temas.temas import tema_escuro, tema_claro

def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso, funciona tanto para desenvolvimento quanto para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MaiaNoteApp(CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Maianote")
        self.geometry("1024x768")
        
        self.current_file_path = None
        self.undo_stack = []
        self.redo_stack = []
        self.max_undo = 25
        self.current_font = CTkFont(family="Arial", size=13)
        self.typing_timer = None
        
        self.init_icons()
        self.setup_ui()
        self.setup_bindings()
        self.modo_claro()  # Modo claro inicial padrão
        self.save_state()  # Estado inicial
        self.after(200, self.set_favicon)

    def set_favicon(self):
        try:
            ico_path = resource_path("icones/favicon1.ico")
            png_path = resource_path("icones/favicon1.png")
            if os.path.exists(ico_path):
                self.iconbitmap(ico_path)
            if os.path.exists(png_path):
                self.favicon = PhotoImage(file=png_path)
                self.iconphoto(False, self.favicon)
                self.iconphoto(True, self.favicon)
        except Exception:
            pass

    def init_icons(self):
        # Favicon
        self.set_favicon()

        icon_names = [
            "novo", "abrir", "salvar", "salvar_como", "exportar_pdf", "sair",
            "desfazer", "refazer", "recortar", "copiar", "colar", "selecionar_tudo",
            "pesquisar", "fonte", "cor", "tema"
        ]
        
        self.icones_light = {}
        self.icones_dark = {}
        self.ctk_icones = {}

        for name in icon_names:
            path_light = resource_path(f"icones/{name}1.png")
            path_dark = resource_path(f"icones/{name}2.png")
            
            # PhotoImage para menus nativos do Tkinter
            self.icones_light[name] = PhotoImage(file=path_light)
            if os.path.exists(path_dark):
                self.icones_dark[name] = PhotoImage(file=path_dark)
            else:
                self.icones_dark[name] = self.icones_light[name]
                
            # CTkImage para botões CustomTkinter (toolbar)
            img_light = Image.open(path_light)
            img_dark = Image.open(path_dark if os.path.exists(path_dark) else path_light)
            self.ctk_icones[name] = CTkImage(light_image=img_light, dark_image=img_dark, size=(16, 16))

    def setup_ui(self):
        self.create_menu()
        self.create_toolbar()
        self.create_editor()
        self.create_statusbar()

    def create_menu(self):
        self.menubar = Menu(self, border=0, borderwidth=0, relief="solid")
        
        # Menu Arquivo
        self.menuArquivo = Menu(self.menubar, tearoff=0, border=0, borderwidth=0, relief="solid")
        self.menuArquivo.add_command(label="Novo", command=self.novo, image=self.icones_light["novo"], compound=LEFT, accelerator="Ctrl+N")
        self.menuArquivo.add_command(label="Abrir", command=self.abrir, image=self.icones_light["abrir"], compound=LEFT, accelerator="Ctrl+O")
        self.menuArquivo.add_command(label="Salvar", command=self.salvar, image=self.icones_light["salvar"], compound=LEFT, accelerator="Ctrl+S")
        self.menuArquivo.add_command(label="Salvar Como", command=self.salvar_como, image=self.icones_light["salvar_como"], compound=LEFT, accelerator="Shift+Ctrl+S")
        self.menuArquivo.add_separator()
        self.menuArquivo.add_command(label="Exportar para PDF", command=self.exportar_pdf, image=self.icones_light["exportar_pdf"], compound=LEFT, accelerator="Ctrl+E")
        self.menuArquivo.add_separator()
        self.menuArquivo.add_command(label="Sair", command=self.sair, image=self.icones_light["sair"], compound=LEFT, accelerator="Ctrl+Q")
        self.menubar.add_cascade(label="Arquivo", menu=self.menuArquivo)

        # Menu Editar
        self.menuEditar = Menu(self.menubar, tearoff=0, border=0, borderwidth=0, relief="solid")
        self.menuEditar.add_command(label="Desfazer", command=self.desfazer, image=self.icones_light["desfazer"], compound=LEFT, accelerator="Ctrl+Z")
        self.menuEditar.add_command(label="Refazer", command=self.refazer, image=self.icones_light["refazer"], compound=LEFT, accelerator="Ctrl+Y")
        self.menuEditar.add_separator()
        self.menuEditar.add_command(label="Recortar", command=self.recortar, image=self.icones_light["recortar"], compound=LEFT, accelerator="Ctrl+X")
        self.menuEditar.add_command(label="Copiar", command=self.copiar, image=self.icones_light["copiar"], compound=LEFT, accelerator="Ctrl+C")
        self.menuEditar.add_command(label="Colar", command=self.colar, image=self.icones_light["colar"], compound=LEFT, accelerator="Ctrl+V")
        self.menuEditar.add_separator()
        self.menuEditar.add_command(label="Selecionar Tudo", command=self.selecionar_tudo, image=self.icones_light["selecionar_tudo"], compound=LEFT, accelerator="Ctrl+A")
        self.menubar.add_cascade(label="Editar", menu=self.menuEditar)

        # Menu Pesquisar
        self.menuPesquisar = Menu(self.menubar, tearoff=0, border=0, borderwidth=0, relief="solid")
        self.menuPesquisar.add_command(label="Localizar e Substituir", command=self.localizar, image=self.icones_light["pesquisar"], compound=LEFT, accelerator="Ctrl+F")
        self.menubar.add_cascade(label="Pesquisar", menu=self.menuPesquisar)

        # Menu Estilizar
        self.menuEstilizar = Menu(self.menubar, tearoff=0, border=0, borderwidth=0, relief="solid")
        self.menuEstilizar.add_command(label="Fontes e Tamanho", command=self.open_font_dialog, image=self.icones_light["fonte"], compound=LEFT)
        self.menuEstilizar.add_command(label="Mudar Cor Texto", command=self.change_text_color, image=self.icones_light["cor"], compound=LEFT, accelerator="Ctrl+K")
        
        self.submenuEstilizar = Menu(self.menuEstilizar, tearoff=0, borderwidth=0, relief="solid")
        self.submenuEstilizar.add_command(label="Claro", command=self.modo_claro)
        self.submenuEstilizar.add_command(label="Escuro", command=self.modo_escuro)
        self.menuEstilizar.add_cascade(label="Temas", menu=self.submenuEstilizar, image=self.icones_light["tema"], compound=LEFT)
        
        self.menubar.add_cascade(label="Estilizar", menu=self.menuEstilizar)
        self.config(menu=self.menubar)

    def create_toolbar(self):
        self.toolbar = CTkFrame(self, height=40, corner_radius=0)
        self.toolbar.pack(side="top", fill="x", padx=0, pady=0)
        
        def make_btn(text, icon_name, command):
            btn = CTkButton(
                self.toolbar, 
                text="", 
                image=self.ctk_icones[icon_name], 
                width=32, 
                height=32, 
                fg_color="transparent",
                hover_color=("#d1d5db", "#374151"),
                command=command
            )
            btn.pack(side="left", padx=3, pady=4)
            return btn

        make_btn("Novo", "novo", self.novo)
        make_btn("Abrir", "abrir", self.abrir)
        make_btn("Salvar", "salvar", self.salvar)
        
        sep1 = CTkFrame(self.toolbar, width=2, height=24, fg_color=("#cbd5e1", "#475569"))
        sep1.pack(side="left", padx=6, pady=8)
        
        make_btn("Desfazer", "desfazer", self.desfazer)
        make_btn("Refazer", "refazer", self.refazer)
        make_btn("Localizar", "pesquisar", self.localizar)
        
        sep2 = CTkFrame(self.toolbar, width=2, height=24, fg_color=("#cbd5e1", "#475569"))
        sep2.pack(side="left", padx=6, pady=8)
        
        make_btn("Fonte", "fonte", self.open_font_dialog)
        make_btn("Cor", "cor", self.change_text_color)
        
        self.btn_tema = CTkButton(
            self.toolbar, 
            text=" Alternar Tema", 
            image=self.ctk_icones["tema"], 
            height=32, 
            fg_color="transparent",
            hover_color=("#d1d5db", "#374151"),
            command=self.toggle_tema
        )
        self.btn_tema.pack(side="right", padx=8, pady=4)

    def create_editor(self):
        self.main_frame = CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        self.caixa_numeros = CTkTextbox(
            self.main_frame,
            width=48,
            border_width=0,
            border_spacing=5,
            bg_color="transparent",
            font=CTkFont(family="Arial", size=13, weight="bold"),
            corner_radius=0,
            activate_scrollbars=False,
            state="disabled"
        )
        self.caixa_numeros.pack(side="left", fill="y")

        self.text_frame = CTkFrame(self.main_frame, fg_color="transparent", corner_radius=0)
        self.text_frame.pack(side="left", fill="both", expand=True)

        self.caixa_de_texto = CTkTextbox(
            self.text_frame,
            wrap="word",
            undo=True,
            corner_radius=0
        )
        self.caixa_de_texto.pack(side="left", fill="both", expand=True)

        self.caixa_de_texto.configure(font=self.current_font)
        self.caixa_numeros.configure(font=self.current_font)

        self.caixa_de_texto._textbox.configure(yscrollcommand=self.sync_scroll_from_textbox)

    def create_statusbar(self):
        self.statusbar = CTkFrame(self, height=26, corner_radius=0)
        self.statusbar.pack(side="bottom", fill="x")
        
        self.lbl_pos = CTkLabel(self.statusbar, text="Lin 1, Col 1", font=CTkFont(size=11))
        self.lbl_pos.pack(side="left", padx=12, pady=2)

        self.lbl_stats = CTkLabel(self.statusbar, text="0 palavras | 0 caracteres", font=CTkFont(size=11))
        self.lbl_stats.pack(side="right", padx=12, pady=2)

        self.lbl_encoding = CTkLabel(self.statusbar, text="UTF-8", font=CTkFont(size=11))
        self.lbl_encoding.pack(side="right", padx=12, pady=2)

    def sync_scroll_from_textbox(self, *args):
        try:
            self.caixa_de_texto._v_scrollbar.set(*args)
        except Exception:
            pass
        try:
            self.caixa_numeros._textbox.yview_moveto(args[0])
        except Exception:
            pass

    def setup_bindings(self):
        self.caixa_de_texto.bind("<KeyRelease>", self.on_key_release)
        self.caixa_de_texto.bind("<ButtonRelease-1>", self.update_cursor_status)

        self.bind("<Control-n>", lambda e: self.novo())
        self.bind("<Control-N>", lambda e: self.novo())
        self.bind("<Control-o>", lambda e: self.abrir())
        self.bind("<Control-O>", lambda e: self.abrir())
        self.bind("<Control-s>", lambda e: self.salvar())
        self.bind("<Control-S>", lambda e: self.salvar())
        self.bind("<Shift-Control-s>", lambda e: self.salvar_como())
        self.bind("<Shift-Control-S>", lambda e: self.salvar_como())
        self.bind("<Control-e>", lambda e: self.exportar_pdf())
        self.bind("<Control-E>", lambda e: self.exportar_pdf())
        self.bind("<Control-q>", lambda e: self.sair())
        self.bind("<Control-Q>", lambda e: self.sair())

        self.bind("<Control-z>", lambda e: self.desfazer())
        self.bind("<Control-Z>", lambda e: self.desfazer())
        self.bind("<Control-y>", lambda e: self.refazer())
        self.bind("<Control-Y>", lambda e: self.refazer())
        self.bind("<Control-x>", lambda e: self.recortar())
        self.bind("<Control-X>", lambda e: self.recortar())
        self.bind("<Control-c>", lambda e: self.copiar())
        self.bind("<Control-C>", lambda e: self.copiar())
        self.bind("<Control-v>", lambda e: self.colar())
        self.bind("<Control-V>", lambda e: self.colar())
        self.bind("<Control-a>", lambda e: self.selecionar_tudo())
        self.bind("<Control-A>", lambda e: self.selecionar_tudo())
        self.bind("<Control-f>", lambda e: self.localizar())
        self.bind("<Control-F>", lambda e: self.localizar())
        self.bind("<Control-k>", lambda e: self.change_text_color())
        self.bind("<Control-K>", lambda e: self.change_text_color())

        self.protocol("WM_DELETE_WINDOW", self.sair)

    def on_key_release(self, event=None):
        self.atualiza_numeros()
        self.update_cursor_status()
        
        if self.typing_timer is not None:
            self.after_cancel(self.typing_timer)
        self.typing_timer = self.after(600, self.save_state)

    def update_cursor_status(self, event=None):
        try:
            index = self.caixa_de_texto.index(INSERT)
            lin, col = index.split('.')
            self.lbl_pos.configure(text=f"Lin {lin}, Col {int(col) + 1}")
            
            texto = self.caixa_de_texto.get("1.0", "end-1c")
            palavras = len(texto.split())
            caracteres = len(texto)
            self.lbl_stats.configure(text=f"{palavras} palavras | {caracteres} caracteres")
        except Exception:
            pass

    def atualiza_numeros(self):
        self.caixa_numeros.configure(state="normal")
        self.caixa_numeros.delete("1.0", "end")
        linhas = int(self.caixa_de_texto.index("end-1c").split(".")[0])
        num_str = "\n".join(str(i) for i in range(1, linhas + 1)) + "\n"
        self.caixa_numeros.insert("1.0", num_str)
        self.caixa_numeros.configure(state="disabled")

    def toggle_tema(self):
        if self._appearance_mode == "dark":
            self.modo_claro()
        else:
            self.modo_escuro()

    def update_menu_icons(self, theme_dict):
        try:
            # Menu Arquivo
            self.menuArquivo.entryconfigure("Novo", image=theme_dict["novo"])
            self.menuArquivo.entryconfigure("Abrir", image=theme_dict["abrir"])
            self.menuArquivo.entryconfigure("Salvar", image=theme_dict["salvar"])
            self.menuArquivo.entryconfigure("Salvar Como", image=theme_dict["salvar_como"])
            self.menuArquivo.entryconfigure("Exportar para PDF", image=theme_dict["exportar_pdf"])
            self.menuArquivo.entryconfigure("Sair", image=theme_dict["sair"])

            # Menu Editar
            self.menuEditar.entryconfigure("Desfazer", image=theme_dict["desfazer"])
            self.menuEditar.entryconfigure("Refazer", image=theme_dict["refazer"])
            self.menuEditar.entryconfigure("Recortar", image=theme_dict["recortar"])
            self.menuEditar.entryconfigure("Copiar", image=theme_dict["copiar"])
            self.menuEditar.entryconfigure("Colar", image=theme_dict["colar"])
            self.menuEditar.entryconfigure("Selecionar Tudo", image=theme_dict["selecionar_tudo"])

            # Menu Pesquisar
            self.menuPesquisar.entryconfigure("Localizar e Substituir", image=theme_dict["pesquisar"])

            # Menu Estilizar
            self.menuEstilizar.entryconfigure("Fontes e Tamanho", image=theme_dict["fonte"])
            self.menuEstilizar.entryconfigure("Mudar Cor Texto", image=theme_dict["cor"])
            self.menuEstilizar.entryconfigure("Temas", image=theme_dict["tema"])
        except Exception:
            pass

    def modo_claro(self):
        self._appearance_mode = "light"
        set_default_color_theme("blue")
        set_appearance_mode("light")

        self.menubar.configure(background=tema_claro["preto_3"], foreground=tema_claro["preto_1"])
        self.menuArquivo.configure(bg=tema_claro["branco_3"], fg=tema_claro["preto_1"], activebackground=tema_claro["branco_2"], activeforeground=tema_claro["preto_1"])
        self.menuEditar.configure(bg=tema_claro["branco_3"], fg=tema_claro["preto_1"], activebackground=tema_claro["branco_2"], activeforeground=tema_claro["preto_1"])
        self.menuPesquisar.configure(bg=tema_claro["branco_3"], fg=tema_claro["preto_1"], activebackground=tema_claro["branco_2"], activeforeground=tema_claro["preto_1"])
        self.menuEstilizar.configure(bg=tema_claro["branco_3"], fg=tema_claro["preto_1"], activebackground=tema_claro["branco_2"], activeforeground=tema_claro["preto_1"])
        self.submenuEstilizar.configure(bg=tema_claro["branco_3"], fg=tema_claro["preto_1"], activebackground=tema_claro["branco_2"], activeforeground=tema_claro["preto_1"])

        self.toolbar.configure(fg_color=tema_claro["branco_1"])
        self.main_frame.configure(fg_color=tema_claro["branco_1"])
        self.text_frame.configure(fg_color=tema_claro["branco_1"])
        self.statusbar.configure(fg_color=tema_claro["branco_2"])
        
        self.caixa_de_texto.configure(fg_color=tema_claro["branco_3"], text_color=tema_claro["preto_1"], border_color=tema_claro["branco_2"])
        self.caixa_numeros.configure(fg_color=tema_claro["branco_1"], text_color=tema_claro["preto_2"], border_color=tema_claro["branco_1"])
        self.lbl_pos.configure(text_color=tema_claro["preto_1"])
        self.lbl_stats.configure(text_color=tema_claro["preto_1"])
        self.lbl_encoding.configure(text_color=tema_claro["preto_1"])

        self.update_menu_icons(self.icones_light)
        self.after(50, self.set_favicon)

    def modo_escuro(self):
        self._appearance_mode = "dark"
        set_default_color_theme("dark-blue")
        set_appearance_mode("dark")

        self.menubar.configure(background=tema_escuro["preto_3"], foreground=tema_escuro["branco_1"])
        self.menuArquivo.configure(bg=tema_escuro["preto_3"], fg=tema_escuro["branco_1"], activebackground=tema_escuro["branco_2"], activeforeground=tema_escuro["preto_1"])
        self.menuEditar.configure(bg=tema_escuro["preto_3"], fg=tema_escuro["branco_1"], activebackground=tema_escuro["branco_2"], activeforeground=tema_escuro["preto_1"])
        self.menuPesquisar.configure(bg=tema_escuro["preto_3"], fg=tema_escuro["branco_1"], activebackground=tema_escuro["branco_2"], activeforeground=tema_escuro["preto_1"])
        self.menuEstilizar.configure(bg=tema_escuro["preto_3"], fg=tema_escuro["branco_1"], activebackground=tema_escuro["branco_2"], activeforeground=tema_escuro["preto_1"])
        self.submenuEstilizar.configure(bg=tema_escuro["preto_3"], fg=tema_escuro["branco_1"], activebackground=tema_escuro["branco_2"], activeforeground=tema_escuro["preto_1"])

        self.toolbar.configure(fg_color=tema_escuro["preto_3"])
        self.main_frame.configure(fg_color=tema_escuro["preto_3"])
        self.text_frame.configure(fg_color=tema_escuro["preto_3"])
        self.statusbar.configure(fg_color=tema_escuro["branco_3"])

        self.caixa_de_texto.configure(fg_color=tema_escuro["preto_2"], text_color=tema_escuro["branco_1"], border_color=tema_escuro["preto_2"])
        self.caixa_numeros.configure(fg_color=tema_escuro["preto_3"], text_color=tema_escuro["branco_2"], border_color=tema_escuro["preto_3"])
        self.lbl_pos.configure(text_color=tema_escuro["branco_1"])
        self.lbl_stats.configure(text_color=tema_escuro["branco_1"])
        self.lbl_encoding.configure(text_color=tema_escuro["branco_1"])

        self.update_menu_icons(self.icones_dark)
        self.after(50, self.set_favicon)

    def get_text_and_tags(self):
        text_widget = self.caixa_de_texto._textbox
        content = self.caixa_de_texto.get("1.0", "end-1c")
        
        all_tag_ranges = []
        for tag in text_widget.tag_names():
            if tag in ('sel', 'found'):
                continue
            ranges = text_widget.tag_ranges(tag)
            if ranges:
                tag_list = [(str(ranges[i]), str(ranges[i+1])) for i in range(0, len(ranges), 2)]
                config = {}
                font_config = text_widget.tag_cget(tag, "font")
                if font_config:
                    if isinstance(font_config, font.Font):
                        family = font_config.actual('family')
                        if not family or family == "TkDefaultFont":
                            family = "Arial"
                        config['font'] = {
                            'family': family,
                            'size': font_config.actual('size'),
                            'weight': font_config.actual('weight'),
                            'slant': font_config.actual('slant'),
                            'underline': bool(font_config.actual('underline')),
                            'overstrike': bool(font_config.actual('overstrike'))
                        }
                    else:
                        config['font'] = {'family': str(font_config), 'size': 13}
                foreground = text_widget.tag_cget(tag, "foreground")
                if foreground:
                    config['foreground'] = foreground
                if config:
                    all_tag_ranges.append({'tag': tag, 'ranges': tag_list, 'config': config})
        
        return content, all_tag_ranges

    def apply_tags_to_text(self, text, tag_data):
        self.caixa_de_texto.delete("1.0", "end")
        self.caixa_de_texto.insert("1.0", text)
        
        text_widget = self.caixa_de_texto._textbox
        for item in tag_data:
            tag_name = item['tag']
            config = item['config']
            ranges = item['ranges']
            
            tag_config = {}
            if 'font' in config:
                f = config['font']
                try:
                    family = f.get('family', 'Arial')
                    size = f.get('size', 13)
                    weight = f.get('weight', 'normal')
                    slant = f.get('slant', 'roman')
                    underline = f.get('underline', False)
                    overstrike = f.get('overstrike', False)
                    
                    if not family or family == "TkDefaultFont":
                        family = "Arial"
                    
                    tk_font = font.Font(
                        family=family,
                        size=size,
                        weight=weight,
                        slant=slant,
                        underline=underline,
                        overstrike=overstrike
                    )
                    tag_config['font'] = tk_font
                except Exception:
                    try:
                        tk_font = font.Font(family="Arial", size=size, weight=weight, slant=slant, underline=underline, overstrike=overstrike)
                        tag_config['font'] = tk_font
                    except Exception:
                        tag_config['font'] = font.Font(size=size)
                    
            if 'foreground' in config:
                tag_config['foreground'] = config['foreground']
                
            text_widget.tag_configure(tag_name, **tag_config)
            for start, end in ranges:
                text_widget.tag_add(tag_name, start, end)

    def save_state(self):
        content, tag_data = self.get_text_and_tags()
        state = {'text': content, 'tags': tag_data}
        if self.undo_stack:
            last_state = self.undo_stack[-1]
            if (last_state['text'] == content and 
                len(last_state['tags']) == len(tag_data) and
                all(tag in last_state['tags'] for tag in tag_data)):
                return
        self.undo_stack.append(state)
        if len(self.undo_stack) > self.max_undo:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def novo(self):
        linha = float(self.caixa_de_texto.index("end-1c"))
        if self.current_file_path is None and linha >= 1.0:
            resposta = messagebox.askyesno("Atenção", "Deseja salvar este documento?")
            if resposta:
                self.salvar()
            else:
                self.caixa_de_texto.delete("1.0", "end")
                self.atualiza_numeros()
                self.update_cursor_status()
                self.save_state()

    def abrir(self):
        file_path = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=(
                ("Maianote files", "*.mnote"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ),
            initialdir=os.path.expanduser("~")
        )
        if file_path:
            self.caixa_de_texto.delete("1.0", "end")
            if file_path.endswith('.mnote'):
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        self.apply_tags_to_text(data['text'], data['tags'])
                        self.atualiza_numeros()
                        self.update_cursor_status()
                        self.current_file_path = file_path
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")
            else:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        self.caixa_de_texto.insert("end", file.read())
                        self.atualiza_numeros()
                        self.update_cursor_status()
                        self.current_file_path = file_path
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")

    def salvar(self):
        if self.current_file_path:
            if self.current_file_path.endswith('.mnote'):
                self.salvar_com_formatacao(self.current_file_path)
            else:
                with open(self.current_file_path, "w", encoding="utf-8") as file:
                    file.write(self.caixa_de_texto.get("1.0", "end-1c"))
        else:
            self.salvar_como()

    def salvar_como(self):
        file_path = filedialog.asksaveasfilename(
            title="Salvar arquivo",
            defaultextension=".mnote",
            filetypes=(
                ("Maianote files", "*.mnote"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ),
            initialdir=os.path.expanduser("~")
        )
        if file_path:
            self.current_file_path = file_path
            if file_path.endswith('.mnote'):
                self.salvar_com_formatacao(file_path)
                messagebox.showinfo("Documento Salvo", "Documento salvo com formatação!")
            else:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.caixa_de_texto.get("1.0", "end-1c"))
                messagebox.showinfo("Documento Salvo", "Documento salvo como texto puro!")

    def salvar_com_formatacao(self, file_path):
        try:
            content, tag_data = self.get_text_and_tags()
            data = {'text': content, 'tags': tag_data}
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erro ao salvar", f"Erro ao salvar arquivo: {str(e)}")

    def exportar_pdf(self):
        texto = self.caixa_de_texto.get("1.0", "end-1c")
        if not texto.strip():
            messagebox.showwarning("Aviso", "Erro: O texto está vazio!")
            return

        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
        if not caminho_arquivo:
            return

        try:
            pdf = SimpleDocTemplate(caminho_arquivo, pagesize=letter)
            styles = getSampleStyleSheet()
            paragrafo = Paragraph(texto, style=styles["Normal"])
            conteudo = [paragrafo]
            pdf.build(conteudo)
            messagebox.showinfo("PDF Exportado", f"PDF exportado com sucesso para:\n{caminho_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro ao Exportar", f"Erro ao exportar PDF: {str(e)}")

    def sair(self):
        linha = float(self.caixa_de_texto.index("end-1c"))
        if self.current_file_path is not None or linha >= 1.1:
            resposta = messagebox.askyesno("Atenção", "Deseja salvar este documento antes de sair?")
            if resposta:
                self.salvar()
        self.destroy()

    def desfazer(self):
        if len(self.undo_stack) > 1:
            current_state = self.undo_stack.pop()
            self.redo_stack.append(current_state)
            previous_state = self.undo_stack[-1]
            self.apply_tags_to_text(previous_state['text'], previous_state['tags'])
            self.atualiza_numeros()
            self.update_cursor_status()

    def refazer(self):
        if self.redo_stack:
            redo_state = self.redo_stack.pop()
            self.undo_stack.append(redo_state)
            self.apply_tags_to_text(redo_state['text'], redo_state['tags'])
            self.atualiza_numeros()
            self.update_cursor_status()

    def recortar(self):
        try:
            texto_selecionado = self.caixa_de_texto.selection_get()
            self.caixa_de_texto.delete(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(texto_selecionado)
            self.save_state()
            self.atualiza_numeros()
            self.update_cursor_status()
        except Exception:
            pass

    def copiar(self):
        try:
            texto_selecionado = self.caixa_de_texto.selection_get()
            self.clipboard_clear()
            self.clipboard_append(texto_selecionado)
        except Exception:
            pass

    def colar(self):
        try:
            texto_selecionado = self.clipboard_get()
            posicao = self.caixa_de_texto.index(INSERT)
            self.caixa_de_texto.insert(posicao, texto_selecionado)
            self.save_state()
            self.atualiza_numeros()
            self.update_cursor_status()
        except Exception:
            pass

    def selecionar_tudo(self):
        self.caixa_de_texto.tag_add(SEL, "1.0", END)
        self.caixa_de_texto.mark_set(INSERT, "1.0")

    def localizar(self):
        if hasattr(self, 'find_replace_window') and self.find_replace_window.winfo_exists():
            self.find_replace_window.lift()
            return

        find_replace_window = CTkToplevel(self)
        find_replace_window.title("Localizar e Substituir")
        find_replace_window.geometry("360x200")
        find_replace_window.resizable(False, False)
        self.find_replace_window = find_replace_window

        find_label = CTkLabel(find_replace_window, text="Localizar:")
        find_label.pack(pady=(12, 0))
        find_entry = CTkEntry(find_replace_window, width=310)
        find_entry.pack(pady=4)

        replace_label = CTkLabel(find_replace_window, text="Substituir por:")
        replace_label.pack()
        replace_entry = CTkEntry(find_replace_window, width=310)
        replace_entry.pack(pady=4)

        def find_text():
            term = find_entry.get()
            if not term:
                return
            self.caixa_de_texto.tag_remove(SEL, "1.0", END)
            start = self.caixa_de_texto.index(INSERT)
            pos = self.caixa_de_texto.search(term, start, nocase=True, stopindex=END)
            if not pos:
                pos = self.caixa_de_texto.search(term, "1.0", nocase=True, stopindex=END)
            if pos:
                end = f"{pos}+{len(term)}c"
                self.caixa_de_texto.tag_add(SEL, pos, end)
                self.caixa_de_texto.mark_set(INSERT, end)
                self.caixa_de_texto.see(INSERT)
            else:
                messagebox.showinfo("Não encontrado", f"'{term}' não foi encontrado.")

        def replace_text():
            term = find_entry.get()
            replacement = replace_entry.get()
            if not term:
                return
            try:
                sel_start = self.caixa_de_texto.index(SEL_FIRST)
                sel_end = self.caixa_de_texto.index(SEL_LAST)
                selected_text = self.caixa_de_texto.get(sel_start, sel_end)
                if selected_text.lower() == term.lower():
                    self.caixa_de_texto.delete(sel_start, sel_end)
                    self.caixa_de_texto.insert(sel_start, replacement)
                    new_end = f"{sel_start}+{len(replacement)}c"
                    self.caixa_de_texto.tag_add(SEL, sel_start, new_end)
                    self.caixa_de_texto.mark_set(INSERT, new_end)
                    self.save_state()
                    self.atualiza_numeros()
                    self.update_cursor_status()
            except Exception:
                find_text()

        def replace_all():
            term = find_entry.get()
            replacement = replace_entry.get()
            if not term:
                return
            content = self.caixa_de_texto.get("1.0", "end-1c")
            new_content = content.replace(term, replacement)
            self.caixa_de_texto.delete("1.0", "end")
            self.caixa_de_texto.insert("1.0", new_content)
            self.atualiza_numeros()
            self.update_cursor_status()
            self.save_state()

        btn_frame = CTkFrame(find_replace_window, fg_color="transparent")
        btn_frame.pack(pady=12)
        CTkButton(btn_frame, width=80, text="Localizar", command=find_text).pack(side="left", padx=4)
        CTkButton(btn_frame, width=80, text="Substituir", command=replace_text).pack(side="left", padx=4)
        CTkButton(btn_frame, width=95, text="Substituir Tudo", command=replace_all).pack(side="left", padx=4)
        find_entry.focus_set()

    def open_font_dialog(self):
        try:
            sel_start = self.caixa_de_texto.index(SEL_FIRST)
            sel_end = self.caixa_de_texto.index(SEL_LAST)
        except Exception:
            messagebox.showinfo("Aviso", "Selecione um trecho de texto para aplicar a formatação de fonte.")
            return

        dialog = FontDialog(self)
        self.wait_window(dialog.top)
        if not dialog.result:
            return

        family, size, bold, italic, underline, overstrike = dialog.result

        try:
            if not family or family == "TkDefaultFont":
                family = "Arial"
            tk_font = font.Font(
                family=family,
                size=size,
                weight="bold" if bold else "normal",
                slant="italic" if italic else "roman",
                underline=underline,
                overstrike=overstrike
            )
        except Exception:
            try:
                tk_font = font.Font(family="Arial", size=size)
            except Exception:
                tk_font = font.Font(size=size)

        safe_family = urllib.parse.quote(family.replace(' ', '_'), safe='')
        weight_str = "bold" if bold else "normal"
        slant_str = "italic" if italic else "roman"
        underline_str = "1" if underline else "0"
        overstrike_str = "1" if overstrike else "0"
        tag_name = f"font_{safe_family}_{size}_{weight_str}_{slant_str}_{underline_str}_{overstrike_str}"
        
        self.caixa_de_texto._textbox.tag_configure(tag_name, font=tk_font)
        self.caixa_de_texto._textbox.tag_add(tag_name, sel_start, sel_end)
        self.save_state()

    def change_text_color(self):
        try:
            start = self.caixa_de_texto.index("sel.first")
            end = self.caixa_de_texto.index("sel.last")
        except TclError:
            messagebox.showwarning("Aviso", "Selecione um trecho do texto primeiro.")
            return

        color = colorchooser.askcolor(title="Escolha a cor do texto")
        if color[1] is None:
            return

        tag_name = f"color_{color[1].replace('#', '')}"
        self.caixa_de_texto._textbox.tag_configure(tag_name, foreground=color[1])
        self.caixa_de_texto._textbox.tag_add(tag_name, start, end)   
        self.save_state()


class FontDialog:
    def __init__(self, parent):
        self.top = CTkToplevel(parent)
        self.top.title("Selecionar Fonte")
        self.top.geometry("380x280")
        self.top.resizable(False, False)
        self.parent = parent
        self.result = None

        families = list(font.families())
        families.sort()

        default_family = "Arial"
        default_size = 13
        default_weight = "normal"
        default_slant = "roman"
        default_underline = False
        default_overstrike = False

        self.family_var = StringVar(value=default_family)
        self.size_var = StringVar(value=str(default_size))
        self.bold_var = BooleanVar(value=(default_weight == "bold"))
        self.italic_var = BooleanVar(value=(default_slant == "italic"))
        self.underline_var = BooleanVar(value=default_underline)
        self.overstrike_var = BooleanVar(value=default_overstrike)

        CTkLabel(self.top, text="Família:").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.family_combo = ttk.Combobox(self.top, textvariable=self.family_var, values=families, state="readonly", width=28)
        self.family_combo.grid(row=0, column=1, padx=15, pady=10, sticky="w")

        CTkLabel(self.top, text="Tamanho:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        size_entry = CTkEntry(self.top, textvariable=self.size_var, width=90)
        size_entry.grid(row=1, column=1, padx=15, pady=5, sticky="w")

        CTkCheckBox(self.top, text="Negrito", variable=self.bold_var).grid(row=2, column=0, sticky="w", padx=15, pady=5)
        CTkCheckBox(self.top, text="Itálico", variable=self.italic_var).grid(row=2, column=1, sticky="w", padx=15, pady=5)
        CTkCheckBox(self.top, text="Sublinhado", variable=self.underline_var).grid(row=3, column=0, sticky="w", padx=15, pady=5)
        CTkCheckBox(self.top, text="Rasurado", variable=self.overstrike_var).grid(row=3, column=1, sticky="w", padx=15, pady=5)

        btn_frame = CTkFrame(self.top, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        CTkButton(btn_frame, text="OK", width=90, command=self.ok).pack(side="left", padx=8)
        CTkButton(btn_frame, text="Cancelar", width=90, fg_color="transparent", border_width=1, command=self.cancel).pack(side="left", padx=8)

    def ok(self):
        try:
            size = int(self.size_var.get())
        except ValueError:
            size = 13
            
        family_str = self.family_var.get()
        self.result = (
            family_str,
            size,
            self.bold_var.get(),
            self.italic_var.get(),
            self.underline_var.get(),
            self.overstrike_var.get()
        )
        self.top.destroy()
        self.parent.caixa_numeros.configure(font=(family_str, size))
        self.parent.caixa_de_texto.configure(font=(family_str, size))

    def cancel(self):
        self.result = None
        self.top.destroy()


if __name__ == "__main__":
    app = MaiaNoteApp()
    app.mainloop()