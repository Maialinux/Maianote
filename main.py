from tkinter import PhotoImage, filedialog, Menu, LEFT, SEL_FIRST, SEL_LAST, INSERT, SEL, END, font, ttk, colorchooser, TclError
from customtkinter import CTk, CTkFrame, CTkTextbox, CTkButton, CTkToplevel, CTkLabel, CTkEntry, CTkFont, StringVar, BooleanVar, CTkCheckBox,set_appearance_mode,set_default_color_theme 
from tkinter import messagebox
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
        # PyInstaller cria um diretório temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def Modo_Claro():
   # print("Modo Claro")
    menubar.configure(background=tema_claro["branco_1"], foreground=tema_claro["preto_1"])
    menuArquivo.configure(bg=tema_claro["branco_1"], fg=tema_claro["preto_1"])
    menuEditar.configure(bg=tema_claro["branco_1"], fg=tema_claro["preto_1"])
    menuPesquisar.configure(bg=tema_claro["branco_1"], fg=tema_claro["preto_1"])
    menuEstilizar.configure(bg=tema_claro["branco_1"], fg=tema_claro["preto_1"])
    submenuEstilizar.configure(bg=tema_claro["branco_1"], fg=tema_claro["preto_1"])
    caixa_de_texto.configure(fg_color=tema_claro["branco_3"], text_color=tema_claro["preto_1"], border_color=tema_claro["branco_2"])
    caixa_numeros.configure(fg_color=tema_claro["branco_3"], text_color=tema_claro["preto_1"], border_color=tema_claro["branco_1"])
    main_frame.configure(fg_color=tema_claro["branco_1"])
    text_frame.configure(fg_color=tema_claro["branco_1"])
    set_default_color_theme("blue")
    set_appearance_mode("light")

def Modo_Escuro():
    #print("Modo Escuro")
    menubar.configure(background=tema_escuro["preto_3"], foreground=tema_escuro["branco_1"])
    menuArquivo.configure(bg=tema_escuro["preto_3"], fg=tema_escuro["branco_1"])
    menuEditar.configure(bg=tema_escuro["preto_3"], fg=tema_escuro["branco_1"])
    menuPesquisar.configure(bg=tema_escuro["preto_3"], fg=tema_escuro["branco_1"])
    menuEstilizar.configure(bg=tema_escuro["preto_3"], fg=tema_escuro["branco_1"])
    submenuEstilizar.configure(bg=tema_escuro["preto_3"], fg=tema_escuro["branco_1"])
    caixa_de_texto.configure(fg_color=tema_escuro["preto_2"], text_color=tema_escuro["branco_1"], border_color=tema_escuro["preto_2"])
    caixa_numeros.configure(fg_color=tema_escuro["preto_3"], text_color=tema_escuro["branco_1"], border_color=tema_escuro["preto_2"])
    main_frame.configure(fg_color=tema_escuro["preto_3"])
    text_frame.configure(fg_color=tema_escuro["preto_3"])
    set_default_color_theme("dark-blue")
    set_appearance_mode("dark")

   
    
undo_stack = []
max_undo = 20
redo_stack = []
root = CTk()
faviconTemp = resource_path("icones/favicon1.png")
favicon = PhotoImage(file=faviconTemp)
root.iconphoto(True, favicon)
root.title("Maianote")
root.geometry("1024x768")

# ICONES DO MENU ARQUIVO
iconeNovoTemp = resource_path("icones/novo1.png")
iconeAbrirTemp = resource_path("icones/abrir1.png")
iconeSalvarTemp = resource_path("icones/salvar1.png")
iconeSalvarComoTemp = resource_path("icones/salvar_como1.png")
iconeExportarPDFTemp = resource_path("icones/exportar_pdf1.png")
iconeSairTemp = resource_path("icones/sair1.png")
# ICONES DO MENU EDITAR
iconeDesfazerTemp = resource_path("icones/desfazer1.png")
iconeRefazerTemp = resource_path("icones/refazer1.png")
iconeRecortarTemp = resource_path("icones/recortar1.png")
iconeCopiarTemp = resource_path("icones/copiar3.png")
iconeColarTemp = resource_path("icones/colar1.png")
iconeSelecionarTudoTemp = resource_path("icones/selecionar_tudo1.png")
# ICONES DO MENU PESQUISAR
iconePesquisarTemp = resource_path("icones/pesquisar1.png")
# ICONES DO MENU ESTILIZAR
iconeFonteTemp = resource_path("icones/fonte1.png")
iconeCorTemp = resource_path("icones/cor1.png")
iconeTemaTemp = resource_path("icones/tema1.png")

iconeNovo = PhotoImage(file=iconeNovoTemp)
iconeAbrir = PhotoImage(file=iconeAbrirTemp)
iconeSalvar = PhotoImage(file=iconeSalvarTemp)
iconeSalvarComo = PhotoImage(file=iconeSalvarComoTemp)
iconeExportarPDF = PhotoImage(file=iconeExportarPDFTemp)
iconeSair = PhotoImage(file=iconeSairTemp)
# ICONES DO MENU EDITAR
iconeDesfazer = PhotoImage(file=iconeDesfazerTemp)
iconeRefazer = PhotoImage(file=iconeRefazerTemp)
iconeRecortar = PhotoImage(file=iconeRecortarTemp)
iconeCopiar = PhotoImage(file=iconeCopiarTemp)
iconeColar = PhotoImage(file=iconeColarTemp)
iconeSelecionarTudo = PhotoImage(file=iconeSelecionarTudoTemp)
# ICONES DO MENU PESQUISAR
iconePesquisar = PhotoImage(file=iconePesquisarTemp)
# ICONES DO MENU ESTILIZAR
iconeFonte = PhotoImage(file=iconeFonteTemp)
iconeCor = PhotoImage(file=iconeCorTemp)
iconeTema = PhotoImage(file=iconeTemaTemp)


def MenuPrincipal():
    global menubar,menuArquivo, menuEditar, menuPesquisar, menuEstilizar,submenuEstilizar

    menubar = Menu(root, border=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000",
                   activebackground="#131313", activeforeground="#e7e7e7")
    menuArquivo = Menu(menubar, tearoff=0, border=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000",
                       activebackground="#131313", activeforeground="#e7e7e7")
    menuArquivo.add_command(label="Novo", command=Novo_key, image=iconeNovo, compound=LEFT, accelerator="Ctrl+N")
    menuArquivo.add_command(label="Abrir", command=Abrir, image=iconeAbrir, compound=LEFT, accelerator="Ctrl+O")
    menuArquivo.add_command(label="Salvar", command=Salvar, image=iconeSalvar, compound=LEFT, accelerator="Ctrl+S")
    menuArquivo.add_command(label="Salvar Como", command=Salvar_Como, image=iconeSalvarComo, compound=LEFT,
                            accelerator="Shift+Ctrl+S")
    menuArquivo.add_command(label="Exportar para PDF", command=Exportar_PDF, image=iconeExportarPDF, compound=LEFT,
                            accelerator="Ctrl+E")
    menuArquivo.add_command(label="Sair", command=Sair, image=iconeSair, compound=LEFT, accelerator="Ctrl+Q")
    menubar.add_cascade(label="Arquivo", menu=menuArquivo)

    menuEditar = Menu(menubar, tearoff=0, border=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000",
                    activebackground="#131313", activeforeground="#e7e7e7")
    menuEditar.add_command(label="Desfazer", command=Desfazer, image=iconeDesfazer, compound=LEFT, accelerator="Ctrl+Z")
    menuEditar.add_command(label="Refazer", command=Refazer, image=iconeRefazer, compound=LEFT, accelerator="Ctrl+Y")
    menuEditar.add_command(label="Recortar", command=Recortar, image=iconeRecortar, compound=LEFT, accelerator="Ctrl+X")
    menuEditar.add_command(label="Copiar", command=Copiar, image=iconeCopiar, compound=LEFT, accelerator="Ctrl+C")
    menuEditar.add_command(label="Colar", command=Colar, image=iconeColar, compound=LEFT, accelerator="Ctrl+V")
    menuEditar.add_command(label="Selecionar Tudo", command=Selecionar_Tudo, image=iconeSelecionarTudo, compound=LEFT,
                        accelerator="Ctrl+A")
    menubar.add_cascade(label="Editar", menu=menuEditar)

    ##############  MENU PESQUISAR ###############
    menuPesquisar = Menu(menubar, tearoff=0, border=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000",activebackground="#131313", activeforeground="#e7e7e7")
    menuPesquisar.add_command(label="Localizar e Substituir", command=Localizar, image=iconePesquisar, compound=LEFT,accelerator="Ctrl+F")
    menubar.add_cascade(label="Pesquisar", menu=menuPesquisar)

    ##############  MENU ESTILIZAR ###############
    menuEstilizar = Menu(menubar, tearoff=0, border=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000",activebackground="#131313", activeforeground="#e7e7e7")
    menuEstilizar.add_command(label="Fontes e Tamanho", command=Open_font_dialog, image=iconeFonte, compound=LEFT,accelerator=None)
    menuEstilizar.add_command(label="Mudar Cor Texto", command=Change_text_color, image=iconeCor, compound=LEFT,accelerator=None)
    menubar.add_cascade(label="Estilizar", menu=menuEstilizar)
    
    submenuEstilizar = Menu(menuEstilizar, tearoff=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000",activebackground="#131313", activeforeground="#e7e7e7")
    submenuEstilizar.add_command(label="Claro", command=Modo_Claro, image=None, compound=LEFT,accelerator=None)
    submenuEstilizar.add_command(label="Escuro", command=Modo_Escuro, image=None, compound=LEFT,accelerator=None)
    menuEstilizar.add_cascade(label="Temas", menu=submenuEstilizar , image=iconeTema, compound=LEFT)
    root.config(menu=menubar)
    

current_file_path = None

# Fonte padrão do editor (não será alterada após inicialização)
current_font = CTkFont(family="Arial", size=13)

def Atualiza_numeros(event=None):
    caixa_numeros.configure(state="normal")
    caixa_numeros.delete("1.0", "end")
    linhas = int(caixa_de_texto.index("end-1c").split(".")[0])
    for i in range(1, linhas + 1):
        caixa_numeros.insert("end-1c", f"{i}\n")
    caixa_numeros.configure(state="disabled")

def get_text_and_tags():
    """Obtém o texto e todas as tags aplicadas com suas configurações"""
    text_widget = caixa_de_texto._textbox
    content = caixa_de_texto.get("1.0", "end-1c")
    
    # Coleta todas as tags aplicadas (exceto as especiais)
    all_tag_ranges = []
    for tag in text_widget.tag_names():
        if tag in ('sel', 'found'):
            continue
        ranges = text_widget.tag_ranges(tag)
        if ranges:
            # Converte para lista de tuplas (start, end)
            tag_list = [(str(ranges[i]), str(ranges[i+1])) for i in range(0, len(ranges), 2)]
            # Obtém as configurações da tag
            config = {}
            font_config = text_widget.tag_cget(tag, "font")
            if font_config:
                if isinstance(font_config, font.Font):
                    # Extrai a família da fonte de forma segura
                    family = font_config.actual('family')
                    # Verifica se a família é válida
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
                    # Caso seja uma string (nome da fonte)
                    config['font'] = {'family': str(font_config), 'size': 13}
            foreground = text_widget.tag_cget(tag, "foreground")
            if foreground:
                config['foreground'] = foreground
            if config:
                all_tag_ranges.append({'tag': tag, 'ranges': tag_list, 'config': config})
    
    return content, all_tag_ranges


def apply_tags_to_text(text, tag_data):
    """Aplica as tags salvas ao texto recém-inserido"""
    caixa_de_texto.delete("1.0", "end")
    caixa_de_texto.insert("1.0", text)
    
    text_widget = caixa_de_texto._textbox
    for item in tag_data:
        tag_name = item['tag']
        config = item['config']
        ranges = item['ranges']
        
        # Configura a tag
        tag_config = {}
        if 'font' in config:
            f = config['font']
            try:
                # Garante valores padrão e trata a família da fonte corretamente
                family = f.get('family', 'Arial')
                size = f.get('size', 13)
                weight = f.get('weight', 'normal')
                slant = f.get('slant', 'roman')
                underline = f.get('underline', False)
                overstrike = f.get('overstrike', False)
                
                # Verifica se a família da fonte é válida
                if not family or family == "TkDefaultFont":
                    family = "Arial"
                
                # Tenta criar a fonte com a família exata
                tk_font = font.Font(
                    family=family,
                    size=size,
                    weight=weight,
                    slant=slant,
                    underline=underline,
                    overstrike=overstrike
                )
                tag_config['font'] = tk_font
            except Exception as e:
                #print(f"Erro ao criar fonte '{family}': {e}")
                # Tenta com fontes alternativas
                try:
                    # Primeiro tenta Arial como fallback
                    tk_font = font.Font(
                        family="Arial",
                        size=size,
                        weight=weight,
                        slant=slant,
                        underline=underline,
                        overstrike=overstrike
                    )
                    tag_config['font'] = tk_font
                except:
                    # Último fallback: fonte padrão
                    tk_font = font.Font(size=size)
                    tag_config['font'] = tk_font
                
        if 'foreground' in config:
            tag_config['foreground'] = config['foreground']
            
        # Aplica a configuração da tag
        text_widget.tag_configure(tag_name, **tag_config)
        
        # Aplica a tag aos intervalos
        for start, end in ranges:
            text_widget.tag_add(tag_name, start, end)


def save_state():
    """Salva o estado atual (texto + formatação) no undo stack"""
    content, tag_data = get_text_and_tags()
    state = {
        'text': content,
        'tags': tag_data
    }
    # Comparação mais robusta para evitar erros
    if undo_stack:
        last_state = undo_stack[-1]
        if (last_state['text'] == content and 
            len(last_state['tags']) == len(tag_data) and
            all(tag in last_state['tags'] for tag in tag_data)):
            return
    undo_stack.append(state)
    if len(undo_stack) > max_undo:
        undo_stack.pop(0)
    redo_stack.clear()


def Set_editor_de_texto():
    global main_frame, text_frame
    main_frame = CTkFrame(root)
    main_frame.pack(pady=0, padx=0, fill="both", expand=True)
    global caixa_numeros

    caixa_numeros = CTkTextbox(
        main_frame,
        width=45,
        border_width=1,
        border_spacing=5,
        fg_color="#f4f4f4",
        bg_color="transparent",
        text_color="#666",
        font=CTkFont(weight="bold"),
        corner_radius=0,
        activate_scrollbars=False,
        state="disabled"
    )
    caixa_numeros.pack(side="left", fill="y")

    text_frame = CTkFrame(main_frame, fg_color="transparent")
    text_frame.pack(side="left", fill="both", expand=True)

    global caixa_de_texto
    caixa_de_texto = CTkTextbox(
        text_frame,
        wrap="word",
        undo=True
    )
    caixa_de_texto.pack(side="left", fill="both", expand=True)

    # === SINCRONIZAÇÃO DE ROLAGEM ===
    def sync_scroll():
        try:
            frac = caixa_de_texto._textbox.yview()[0]
            caixa_numeros._textbox.yview_moveto(frac)           
        except Exception:
            pass
        root.after(15, sync_scroll)
        

    sync_scroll()

    caixa_de_texto.bind("<KeyRelease>", lambda e: root.after(10, lambda: [Atualiza_numeros(), save_state()]))
    Atualiza_numeros()
    caixa_de_texto.configure(font=current_font)
    caixa_numeros.configure(font=current_font)
    save_state()  # Estado inicial
    

########## FUNÇÕES DO MENU ARQUIVO #############################
def Novo():
    linha = float(caixa_de_texto.index("end-1c"))
    if current_file_path is None and linha >= 1.0:
        resposta = messagebox.askyesno("Atenção", "Deseja salvar este documento?")
        if resposta:
            Salvar()
        else:
            caixa_de_texto.delete("1.0", "end")
            Atualiza_numeros()
            save_state()


def Novo_key(event=None):
    Novo()


def Abrir():
    global current_file_path
    file_path = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=(
            ("Maianote files", "*.mnote"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ),
        initialdir="/home"
    )
    if file_path:
        caixa_de_texto.delete("1.0", "end")
        if file_path.endswith('.mnote'):
            # Carrega arquivo com formatação
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    apply_tags_to_text(data['text'], data['tags'])
                    Atualiza_numeros()
                    current_file_path = file_path
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")
        else:
            # Carrega arquivo de texto puro
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    caixa_de_texto.insert("end", file.read())
                    Atualiza_numeros()
                    current_file_path = file_path
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")


def Abrir_key(event=None):
    Abrir()


def Salvar():
    global current_file_path
    if current_file_path:
        # Determina o tipo de arquivo baseado na extensão
        if current_file_path.endswith('.mnote'):
            salvar_com_formatacao(current_file_path)
        else:
            # Salva como texto puro (APENAS texto, sem formatação)
            with open(current_file_path, "w", encoding="utf-8") as file:
                file.write(caixa_de_texto.get("1.0", "end-1c"))
    else:
        Salvar_Como()


def Salvar_key(event=None):
    Salvar()


def Salvar_Como():
    global current_file_path
    file_path = filedialog.asksaveasfilename(
        title="Salvar arquivo",
        defaultextension=".mnote",
        filetypes=(
            ("Maianote files", "*.mnote"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ),
        initialdir="/home"
    )
    if file_path:
        current_file_path = file_path
        if file_path.endswith('.mnote'):
            salvar_com_formatacao(file_path)
            messagebox.showinfo("Documento Salvo", "Documento salvo com formatação!")
        else:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(caixa_de_texto.get("1.0", "end-1c"))
            messagebox.showinfo("Documento Salvo", "Documento salvo como texto puro!")


def salvar_com_formatacao(file_path):
    """Salva o documento com todas as formatações em formato JSON"""
    try:
        content, tag_data = get_text_and_tags()
        data = {
            'text': content,
            'tags': tag_data
        }
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Erro ao salvar", f"Erro ao salvar arquivo: {str(e)}")


def Salvar_Como_key(event=None):
    Salvar_Como()


def Exportar_PDF():
    texto = caixa_de_texto.get("1.0", "end-1c")
    if not texto.strip():
        messagebox.showwarning("Aviso", "Erro: O texto está vazio!")
        return

    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
    )
    if not caminho_arquivo:
        messagebox.showerror("Erro", "Exportação cancelada")
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


def Exportar_PDF_key(event=None):
    Exportar_PDF()


def Sair():
    linha = float(caixa_de_texto.index("end-1c"))
    if current_file_path is not None:
        resposta = messagebox.askyesno("Atenção", "Deseja salvar este documento?")
        if resposta:
            Salvar()
        quit()
    elif linha >= 1.1:
        resposta = messagebox.askyesno("Atenção", "Deseja salvar este documento?")
        if resposta:
            Salvar()
        quit()
    else:
        quit()


def Sair_key(event=None):
    Sair()


########## FUNÇÕES DO MENU EDITAR #############################
def Desfazer():
    if len(undo_stack) > 1:
        current_state = undo_stack.pop()
        redo_stack.append(current_state)
        previous_state = undo_stack[-1]
        apply_tags_to_text(previous_state['text'], previous_state['tags'])
        Atualiza_numeros()


def Refazer():
    if redo_stack:
        redo_state = redo_stack.pop()
        undo_stack.append(redo_state)
        apply_tags_to_text(redo_state['text'], redo_state['tags'])
        Atualiza_numeros()


def Recortar():
    try:
        texto_selecionado = caixa_de_texto.selection_get()
        caixa_de_texto.delete(SEL_FIRST, SEL_LAST)
        root.clipboard_clear()
        root.clipboard_append(texto_selecionado)
        save_state()  # Salva estado após recortar
    except:
        pass


def Copiar():
    try:
        texto_selecionado = caixa_de_texto.selection_get()
        root.clipboard_clear()
        root.clipboard_append(texto_selecionado)
    except:
        pass


def Colar():
    try:
        texto_selecionado = root.clipboard_get()
        posicao = caixa_de_texto.index(INSERT)
        caixa_de_texto.insert(posicao, texto_selecionado)
        save_state()  # Salva estado após colar
    except:
        pass


def Selecionar_Tudo():
    caixa_de_texto.tag_add(SEL, "1.0", END)
    caixa_de_texto.mark_set(INSERT, "1.0")


def Selecionar_Tudo_key(event=None):
    Selecionar_Tudo()


########## FUNÇÕES DO MENU PESQUISAR #############################
def Localizar():
    if hasattr(Localizar, 'find_replace_window') and Localizar.find_replace_window.winfo_exists():
        Localizar.find_replace_window.lift()
        return

    find_replace_window = CTkToplevel(root)
    find_replace_window.title("Localizar e Substituir")
    find_replace_window.geometry("350x180")
    find_replace_window.resizable(False, False)
    Localizar.find_replace_window = find_replace_window

    find_label = CTkLabel(find_replace_window, text="Localizar:")
    find_label.pack(pady=(10, 0))
    find_entry = CTkEntry(find_replace_window, width=300)
    find_entry.pack(pady=5)

    replace_label = CTkLabel(find_replace_window, text="Substituir por:")
    replace_label.pack()
    replace_entry = CTkEntry(find_replace_window, width=300)
    replace_entry.pack(pady=5)

    def find_text():
        term = find_entry.get()
        if not term:
            return
        caixa_de_texto.tag_remove(SEL, "1.0", END)
        start = caixa_de_texto.index(INSERT)
        pos = caixa_de_texto.search(term, start, nocase=True, stopindex=END)
        if not pos:
            pos = caixa_de_texto.search(term, "1.0", nocase=True, stopindex=END)
        if pos:
            end = f"{pos}+{len(term)}c"
            caixa_de_texto.tag_add(SEL, pos, end)
            caixa_de_texto.mark_set(INSERT, end)
            caixa_de_texto.see(INSERT)
        else:
            messagebox.showinfo("Não encontrado", f"'{term}' não foi encontrado.")

    def replace_text():
        term = find_entry.get()
        replacement = replace_entry.get()
        if not term:
            return
        try:
            sel_start = caixa_de_texto.index(SEL_FIRST)
            sel_end = caixa_de_texto.index(SEL_LAST)
            selected_text = caixa_de_texto.get(sel_start, sel_end)
            if selected_text.lower() == term.lower():
                caixa_de_texto.delete(sel_start, sel_end)
                caixa_de_texto.insert(sel_start, replacement)
                new_end = f"{sel_start}+{len(replacement)}c"
                caixa_de_texto.tag_add(SEL, sel_start, new_end)
                caixa_de_texto.mark_set(INSERT, new_end)
                save_state()  # Salva estado após substituir
        except:
            find_text()

    def replace_all():
        term = find_entry.get()
        replacement = replace_entry.get()
        if not term:
            return
        content = caixa_de_texto.get("1.0", "end-1c")
        new_content = content.replace(term, replacement)
        caixa_de_texto.delete("1.0", "end")
        caixa_de_texto.insert("1.0", new_content)
        Atualiza_numeros()
        save_state()  # Salva estado após substituir tudo

    btn_frame = CTkFrame(find_replace_window)
    btn_frame.pack(pady=10)
    CTkButton(btn_frame, width=50, text="Localizar", command=find_text).pack(side="left", padx=5)
    CTkButton(btn_frame, width=50, text="Substituir", command=replace_text).pack(side="left", padx=5)
    CTkButton(btn_frame, width=50, text="Substituir Tudo", command=replace_all).pack(side="left", padx=5)
    find_entry.focus_set()


########## MENU ESTILIZAR #############################
def Open_font_dialog():
    # Verifica se há texto selecionado
    try:
        sel_start = caixa_de_texto.index(SEL_FIRST)
        sel_end = caixa_de_texto.index(SEL_LAST)
    except:
        messagebox.showinfo("Aviso", "Selecione um trecho de texto para aplicar a formatação de fonte.")
        return

    dialog = FontDialog(root, None)
    root.wait_window(dialog.top)
    if not dialog.result:
        return

    family, size, bold, italic, underline, overstrike = dialog.result

    # Cria uma fonte Tkinter (necessária para tags)
    try:
        # Garante que a família da fonte seja tratada corretamente
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
    except:
        # Fallback caso a fonte não exista
        try:
            tk_font = font.Font(family="Arial", size=size)
        except:
            tk_font = font.Font(size=size)

    # Gera um nome de tag consistente baseado nas propriedades
    # Usa urllib.parse.quote para lidar com espaços e caracteres especiais no nome da fonte
    safe_family = urllib.parse.quote(family.replace(' ', '_'), safe='')
    weight_str = "bold" if bold else "normal"
    slant_str = "italic" if italic else "roman"
    underline_str = "1" if underline else "0"
    overstrike_str = "1" if overstrike else "0"
    tag_name = f"font_{safe_family}_{size}_{weight_str}_{slant_str}_{underline_str}_{overstrike_str}"
    
    # Aplica a tag ao Text subjacente
    caixa_de_texto._textbox.tag_configure(tag_name, font=tk_font)
    caixa_de_texto._textbox.tag_add(tag_name, sel_start, sel_end)
    save_state()  # Salva estado após aplicar formatação


class FontDialog:
    def __init__(self, parent, current_font=None):
        self.top = CTkToplevel(parent)
        self.top.title("Selecionar Fonte")
        self.result = None

        families = list(font.families())
        families.sort()

        # Valores padrão
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

        CTkLabel(self.top, text="Família:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.family_combo = ttk.Combobox(self.top, textvariable=self.family_var, values=families, state="readonly", width=30)
        self.family_combo.grid(row=0, column=1, padx=10, pady=5)

        CTkLabel(self.top, text="Tamanho:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        size_entry = CTkEntry(self.top, textvariable=self.size_var, width=80)
        size_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        CTkCheckBox(self.top, text="Negrito", variable=self.bold_var).grid(row=2, column=0, sticky="w", padx=10, pady=2)
        CTkCheckBox(self.top, text="Itálico", variable=self.italic_var).grid(row=2, column=1, sticky="w", padx=10, pady=2)
        CTkCheckBox(self.top, text="Sublinhado", variable=self.underline_var).grid(row=3, column=0, sticky="w", padx=10, pady=2)
        CTkCheckBox(self.top, text="Rasurado", variable=self.overstrike_var).grid(row=3, column=1, sticky="w", padx=10, pady=2)

        btn_frame = CTkFrame(self.top, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        CTkButton(btn_frame, text="OK", command=self.ok).pack(side="left", padx=5)
        CTkButton(btn_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        

    def ok(self):
        try:
            size = int(self.size_var.get())
            
        except ValueError:
            size = 13
        self.result = (
            self.family_var.get(),
            size,
            self.bold_var.get(),
            self.italic_var.get(),
            self.underline_var.get(),
            self.overstrike_var.get()
        )
        self.top.destroy()
        caixa_numeros.configure(font=(self.family_var,size))
        caixa_de_texto.configure(font=(self.family_var,size))
    def cancel(self):
        self.result = None
        self.top.destroy()


def Change_text_color():
    try:
        # Obtém a seleção atual
        start = caixa_de_texto.index("sel.first")
        end = caixa_de_texto.index("sel.last")
    except TclError:
        messagebox.showwarning("Aviso", "Selecione um trecho do texto primeiro.")
        return

    # Abre o seletor de cor
    color = colorchooser.askcolor(title="Escolha a cor do texto")
    if color[1] is None:  # Usuário cancelou
        return

    # Cria uma tag única para essa cor
    tag_name = f"color_{color[1].replace('#', '')}"
    
    # Aplica a tag ao widget Text subjacente (via _textbox)
    caixa_de_texto._textbox.tag_configure(tag_name, foreground=color[1])
    caixa_de_texto._textbox.tag_add(tag_name, start, end)   
    save_state()  # Salva estado após aplicar cor


def AtalhoDoTeclado():
    caixa_de_texto.bind("<Control-n>", Novo_key)
    caixa_de_texto.bind("<Control-N>", Novo_key)
    root.bind("<Control-o>", Abrir_key)
    root.bind("<Control-O>", Abrir_key)
    root.bind("<Control-s>", Salvar_key)
    root.bind("<Control-S>", Salvar_key)
    root.bind("<Shift-Control-s>", Salvar_Como_key)
    root.bind("<Shift-Control-S>", Salvar_Como_key)
    root.bind("<Control-e>", Exportar_PDF_key)
    root.bind("<Control-E>", Exportar_PDF_key)
    root.bind("<Control-q>", Sair_key)
    root.bind("<Control-Q>", Sair_key)

    root.bind("<Control-z>", lambda e: Desfazer())
    root.bind("<Control-Z>", lambda e: Desfazer())
    root.bind("<Control-y>", lambda e: Refazer())
    root.bind("<Control-Y>", lambda e: Refazer())
    root.bind("<Control-x>", lambda e: Recortar())
    root.bind("<Control-X>", lambda e: Recortar())
    root.bind("<Control-c>", lambda e: Copiar())
    root.bind("<Control-C>", lambda e: Copiar())
    root.bind("<Control-v>", lambda e: Colar())
    root.bind("<Control-V>", lambda e: Colar())
    root.bind("<Control-a>", Selecionar_Tudo_key)
    root.bind("<Control-f>", lambda e: Localizar())
    root.bind("<Control-t>", lambda e: Open_font_dialog())
    root.bind("<Control-k>", lambda e: Change_text_color())  # Novo atalho para cor
    # Vincula clique ao texto para atualizar números


if __name__ == "__main__":
    MenuPrincipal()
    Set_editor_de_texto()
    AtalhoDoTeclado()
    root.mainloop()