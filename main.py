from tkinter import *
from customtkinter import *
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

undo_stack=[]
max_undo=20
redo_stack=[]

root=CTk(fg_color="#e4e4e4")
favicon = PhotoImage(file="icones/favicon1.png")
root.iconphoto(True,favicon)
root.title("Maianote")
root.geometry("1024x768")

# ICONES DO MENU ARQUIVO
iconeNovo = PhotoImage(file="icones/novo.png")
iconeAbrir = PhotoImage(file="icones/abrir.png")
iconeSalvar = PhotoImage(file="icones/salvar.png")
iconeSalvarComo = PhotoImage(file="icones/salvar_como.png")
iconeExportarPDF = PhotoImage(file="icones/pdf.png")
iconeSair = PhotoImage(file="icones/fechar.png")
# ICONES DO MENU EDITAR
iconeDesfazer = PhotoImage(file="icones/desfazer.png")
iconeRefazer = PhotoImage(file="icones/refazer.png")
iconeRecortar = PhotoImage(file="icones/recortar.png")
iconeCopiar = PhotoImage(file="icones/copiar.png")
iconeColar = PhotoImage(file="icones/colar.png")
iconeSelecionarTudo = PhotoImage(file="icones/select_all.png")


def MenuPrincipal():
    # Barra de Menu Principal
    menubar = Menu(root, border=0, borderwidth=0,relief="solid",  bg="#d4d4d4", fg="#000000", activebackground="#36006e",activeforeground="#e7e7e7")
    # Menu Arquivo
    menuArquivo = Menu(menubar, tearoff=0, border=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000", activebackground="#36006e",activeforeground="#e7e7e7")
    menuArquivo.add_command(label="Novo",command=Novo,image=iconeNovo, compound=LEFT, accelerator="Ctrl+N")
    menuArquivo.add_command(label="Abrir",command=Abrir,image=iconeAbrir, compound=LEFT, accelerator="Ctrl+O")
    menuArquivo.add_command(label="Salvar",command=Salvar,image=iconeSalvar, compound=LEFT, accelerator="Ctrl+S")
    menuArquivo.add_command(label="Salvar Como",command=Salvar_Como,image=iconeSalvarComo, compound=LEFT, accelerator="Shift+Ctrl+S")
    menuArquivo.add_command(label="Exportar para PDF",command=Exportar_PDF,image=iconeExportarPDF, compound=LEFT, accelerator="Ctrl+E")
    menuArquivo.add_command(label="Sair",command=Sair,image=iconeSair, compound=LEFT, accelerator="Ctrl+Q")
    menubar.add_cascade(label="Arquivo", menu=menuArquivo)
    # Menu Editar
    menuEditar = Menu(menubar, tearoff=0, border=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000", activebackground="#36006e",activeforeground="#e7e7e7")
    menuEditar.add_command(label="Desfazer",command=Desfazer,image=iconeDesfazer, compound=LEFT, accelerator="Ctrl+Z")
    menuEditar.add_command(label="Refazer",command=Refazer,image=iconeRefazer, compound=LEFT, accelerator="Ctrl+Y")
    menuEditar.add_command(label="Recortar",command=Recortar,image=iconeRecortar, compound=LEFT, accelerator="Ctrl+R")
    menuEditar.add_command(label="Copiar",command=Copiar,image=iconeCopiar, compound=LEFT, accelerator="Ctrl+C")
    menuEditar.add_command(label="Colar",command=Colar,image=iconeColar, compound=LEFT, accelerator="Ctrl+V")
    menuEditar.add_command(label="Selecionar Tudo",command=Selecionar_Tudo,image=iconeSelecionarTudo, compound=LEFT, accelerator="Ctrl+A")
    menubar.add_cascade(label="Editar", menu=menuEditar)
    """# Pesquisar
    menuPesquisar = Menu(menubar, tearoff=0, border=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000", activebackground="#36006e",activeforeground="#e7e7e7")
    menuPesquisar.add_command(label="Localizar",command=None,image=None, compound=LEFT, accelerator="")
    menuPesquisar.add_command(label="Localizar e Substituir",command=None,image=None, compound=LEFT, accelerator="")
    menubar.add_cascade(label="Pesquisar", menu=menuPesquisar)
    # Visualizar
    menuVisualizar = Menu(menubar, tearoff=0, border=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000", activebackground="#36006e",activeforeground="#e7e7e7")
    menuVisualizar.add_command(label="Selecionar Fonte",command=None,image=None, compound=LEFT, accelerator="")
    menuVisualizar.add_command(label="Números das linhas",command=None,image=None, compound=LEFT, accelerator="")
    menubar.add_cascade(label="Visualizar", menu=menuVisualizar)
     # Temas e Esquemas de cores
    menuTemas = Menu(menubar, tearoff=0, border=0, borderwidth=0, relief="solid", bg="#d4d4d4", fg="#000000", activebackground="#36006e",activeforeground="#e7e7e7")
    menuTemas.add_command(label="Tema 1",command=None,image=None, compound=LEFT, accelerator="")
    menuTemas.add_command(label="Tema 2",command=None,image=None, compound=LEFT, accelerator="")
    menubar.add_cascade(label="Temas", menu=menuTemas)
"""

    root.config(menu=menubar)


current_file_path = None

def Atualiza_numeros(event=None):    
    caixa_numeros.delete("1.0", "end")
    numero_linhas = int(caixa_de_texto.index("end-1c").split(".")[0])
    for i in range(1, numero_linhas + 1):
        caixa_numeros.insert("end", f"{i}\n")
    save_state()  # Salva o estado após atualizar os números de linha

# Salvar estado inicial
def save_state():
    """Salva o estado atual do Text widget no histórico."""
    content = caixa_de_texto.get("1.0", "end-1c")  # Obtém todo o conteúdo do Text
    if undo_stack and undo_stack[-1] == content:
        return  # Não salvar se o conteúdo for igual ao último estado
    undo_stack.append(content)
    if len(undo_stack) > max_undo:
        undo_stack.pop(0)  # Remove o estado mais antigo se exceder o limite
    redo_stack.clear()  # Limpa o redo quando um novo estado é salvo
    root.clipboard_clear()

#def Visualizador_de_numeros(main_frame):
#    global caixa_numeros
    # Widget para exibir os números de linha
#    caixa_numeros = CTkTextbox(main_frame, width=30, bg_color="transparent", border_width=1, border_color="#d4d4d4")
#    caixa_numeros.pack(side="left", fill="both")

def Set_editor_de_texto():
    # Frame principal para organizar os widgets
    main_frame = CTkFrame(root)
    main_frame.pack(pady=0, padx=0, fill="both", expand=True)

    #Visualizador_de_numeros(main_frame=main_frame)
    global caixa_numeros
    # Widget para exibir os números de linha
    caixa_numeros = CTkTextbox(main_frame, width=30, bg_color="transparent", border_width=1, border_color="#d4d4d4")
    caixa_numeros.pack(side="left", fill="both")
  
    # Frame para a caixa de texto e a barra de rolagem
    text_frame = CTkFrame(main_frame)
    text_frame.pack(side="left", fill="both", expand=True)

    global caixa_de_texto 
    # Cria a caixa de texto
    caixa_de_texto = CTkTextbox(text_frame, wrap="word", width=400, height=200,undo=True)
    caixa_de_texto.pack(side="left", fill="both", expand=True)
    caixa_de_texto.focus()
    caixa_de_texto.bind("<KeyRelease>",lambda e:Atualiza_numeros(e))
    caixa_de_texto.bind("<MouseWheel>", lambda e: Atualiza_numeros(e)) 
    save_state()

########## FUNÇÕES DO MENU ARQUIVOS #############################
def Novo():
    linha = float(caixa_de_texto.index("end-1c"))  

    if current_file_path == None and linha >=1.1 :
        resposta = messagebox.askyesno("Atenção","Deseja salvar este documento?")
        if resposta == True:
            Salvar()
        else:       
            caixa_numeros.delete("1.0","end")
            caixa_de_texto.delete("1.0","end")
            caixa_de_texto.focus()

def Novo_key(event=None):
    linha = float(caixa_de_texto.index("end-1c"))  

    if current_file_path == None and linha >=1.1 :
        resposta = messagebox.askyesno("Atenção","Deseja salvar este documento?")
        if resposta == True:
            Salvar()
        else:       
            caixa_numeros.delete("1.0","end")
            caixa_de_texto.delete("1.0","end")
            caixa_de_texto.focus()


def Abrir():
    """Função para abrir um arquivo."""
    global current_file_path  
    file_path = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        initialdir="/home"
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            caixa_de_texto.delete("1.0","end")
            caixa_de_texto.insert("end",file.read())
            Atualiza_numeros()
            current_file_path = file_path
           

def Abrir_key(event=None):
    """Função para abrir um arquivo."""
    global current_file_path  
    file_path = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        initialdir="/home"
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            caixa_de_texto.delete("1.0","end")
            caixa_de_texto.insert("end",file.read())
            Atualiza_numeros()
            current_file_path = file_path

def Salvar():
    """Função para salvar o conteúdo em um arquivo."""
    global current_file_path
    if current_file_path:  # Se já existe um arquivo aberto/salvo
        with open(current_file_path, "w", encoding="utf-8") as file:
            file.write(caixa_de_texto.get("1.0","end"))
    else:  # Se nenhum arquivo foi aberto anteriormente, pede ao usuário para escolher um local
        Salvar_Como()    
        

def Salvar_key(event=None):
    """Função para salvar o conteúdo em um arquivo."""
    global current_file_path
    if current_file_path:  # Se já existe um arquivo aberto/salvo
        with open(current_file_path, "w", encoding="utf-8") as file:
            file.write(caixa_de_texto.get("1.0","end"))
    else:  # Se nenhum arquivo foi aberto anteriormente, pede ao usuário para escolher um local
        Salvar_Como()    


def Salvar_Como():
    """Função para salvar como um novo arquivo."""
    global current_file_path
    file_path = filedialog.asksaveasfilename(
        title="Salvar arquivo",
        defaultextension=".txt",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        initialdir="/home"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(caixa_de_texto.get("1.0","end"))
            current_file_path = file_path  # Atualiza o caminho do arquivo salvo
            messagebox.showinfo("Documento Salvo","Documento Salvo com Sucesso")

def Salvar_Como_key(event=None):
    """Função para salvar como um novo arquivo."""
    global current_file_path
    file_path = filedialog.asksaveasfilename(
        title="Salvar arquivo",
        defaultextension=".txt",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        initialdir="/home"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(caixa_de_texto.get("1.0","end"))
            current_file_path = file_path  # Atualiza o caminho do arquivo salvo
            messagebox.showinfo("Documento Salvo","Documento Salvo com Sucesso")
          
def Exportar_PDF():
 # Obter o texto da caixa de entrada
    texto = caixa_de_texto.get("1.0", "end-1c")  # Pega todo o texto da caixa de texto
    
    if not texto.strip():  # Verifica se o texto não está vazio
        messagebox.showwarning("Aviso","Erro: O texto está vazio!")
        return
    
    # Abrir diálogo para salvar o arquivo PDF
    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
    )
    
    if not caminho_arquivo:  # Se o usuário cancelar a seleção do arquivo
        messagebox.showerror("Erro","Exportação cancelada")
        return
    
    try:
        # Criar o PDF usando ReportLab
        pdf = SimpleDocTemplate(caminho_arquivo, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Converter o texto para um formato aceito pelo ReportLab (UTF-8)
        paragrafo = Paragraph(texto, style=styles["Normal"])
        
        # Adicionar o conteúdo ao PDF
        conteudo = [paragrafo]
        pdf.build(conteudo)
        messagebox.showinfo("PDF Exportado",f"PDF exportado com sucesso para:\n{caminho_arquivo}")
    except Exception as e:
        messagebox.showerror("Erro ao Exportar",f"Erro ao exportar PDF: {str(e)}")
    pass

def Exportar_PDF_key(event=None):
 # Obter o texto da caixa de entrada
    texto = caixa_de_texto.get("1.0", "end-1c")  # Pega todo o texto da caixa de texto
    
    if not texto.strip():  # Verifica se o texto não está vazio
        messagebox.showwarning("Aviso","Erro: O texto está vazio!")
        return
    
    # Abrir diálogo para salvar o arquivo PDF
    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
    )
    
    if not caminho_arquivo:  # Se o usuário cancelar a seleção do arquivo
        messagebox.showerror("Erro","Exportação cancelada")
        return
    
    try:
        # Criar o PDF usando ReportLab
        pdf = SimpleDocTemplate(caminho_arquivo, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Converter o texto para um formato aceito pelo ReportLab (UTF-8)
        paragrafo = Paragraph(texto, style=styles["Normal"])
        
        # Adicionar o conteúdo ao PDF
        conteudo = [paragrafo]
        pdf.build(conteudo)
        messagebox.showinfo("PDF Exportado",f"PDF exportado com sucesso para:\n{caminho_arquivo}")
    except Exception as e:
        messagebox.showerror("Erro ao Exportar",f"Erro ao exportar PDF: {str(e)}")
    pass

def Sair():
    linha = float(caixa_de_texto.index("end-1c"))  
   
    if current_file_path != None:
        print("Pegunta se quer salvar")
        resposta = messagebox.askyesno("Atenção","Deseja salvar este documento?")
        if resposta == True:
            Salvar()
            quit()
        else:
            quit()

    if current_file_path == None and linha >=1.1 :
        resposta = messagebox.askyesno("Atenção","Deseja salvar este documento?")
        if resposta == True:
            Salvar()
        else:
            quit()
    
    if current_file_path == None:
        quit()
   
def Sair_key(event=None):
    linha = float(caixa_de_texto.index("end-1c"))  
   
    if current_file_path != None:
        print("Pegunta se quer salvar")
        resposta = messagebox.askyesno("Atenção","Deseja salvar este documento?")
        if resposta == True:
            Salvar()
            quit()
        else:
            quit()

    if current_file_path == None and linha >=1.1 :
        resposta = messagebox.askyesno("Atenção","Deseja salvar este documento?")
        if resposta == True:
            Salvar()
        else:
            quit()
    
    if current_file_path == None:
        quit()

########## FUNÇÕES DO MENU EDITAR #############################

def Desfazer():
   if len(undo_stack) > 1:
        current_state = undo_stack.pop()
        redo_stack.append(current_state)
        previous_state = undo_stack[-1]
        caixa_de_texto.delete("1.0", "end")
        caixa_de_texto.insert("1.0", previous_state)
        Atualiza_numeros()

def Refazer():
    if redo_stack:
        redo_state = redo_stack.pop()
        undo_stack.append(redo_state)
        caixa_de_texto.delete("1.0", "end")
        caixa_de_texto.insert("1.0", redo_state)
        Atualiza_numeros()
       

def Recortar():
    try:
        global texto_selecionado
        texto_selecionado = caixa_de_texto.selection_get()
        caixa_de_texto.delete(SEL_FIRST,SEL_LAST)
        caixa_de_texto.clipboard_clear()
        print("Texto recortado: "+str(texto_selecionado))
    except:
        pass

def Copiar():
    try:
        global texto_selecionado
        texto_selecionado = caixa_de_texto.selection_get()
        caixa_de_texto.clipboard_clear()
        print("Texto copiado: "+str(texto_selecionado))
    except:
        pass

def Colar():
    try:
        global posicao
        global texto_selecionado
        posicao = caixa_de_texto.index(INSERT)
        caixa_de_texto.insert(posicao,texto_selecionado)
        print("Texto colado: "+str(texto_selecionado))
    except:
        pass

def Recortar_key(event=None):
    try:
        global selecionado
        selecionado = caixa_de_texto.clipboard_get()
        caixa_de_texto.clipboard_clear()
        print(selecionado + " - Recortado")
        
    except:
        pass

def Copiar_key(event=None):
    try:
        global selecionado
        selecionado = caixa_de_texto.clipboard_get()
        caixa_de_texto.clipboard_clear()
        print(selecionado + " - Copiado")
       
    except:
        pass
    
   
def Colar_key(event=None):
    try:
        global posicao
        posicao = caixa_de_texto.index(INSERT)
        caixa_de_texto.insert(posicao,selecionado)
        print(selecionado + " - colado")
        
    except:
        pass
   
def Selecionar_Tudo():
    try:
        print("Menu selecionar tudo")
        caixa_de_texto.tag_add(SEL,"1.0",END)
    except:
        pass

def Selecionar_Tudo_key(event=None):
    try:
        print("Atalho selecionar tudo")
        caixa_de_texto.tag_add(SEL,"1.0",END)
    except:
        pass


def AtalhoDoTeclado(event=None):
    # Atalhos e Evento de Tecla do Menu Arquivos
    root.bind("<Control-n>",Novo_key)
    root.bind("<Control-N>",Novo_key)
    root.bind("<Control-o>",Abrir_key)
    root.bind("<Control-O>",Abrir_key)
    root.bind("<Control-s>",Salvar_key)
    root.bind("<Control-S>",Salvar_key)
    root.bind("<Shift-Control-s>",Salvar_Como_key)
    root.bind("<Shift-Control-S>",Salvar_Como_key)
    root.bind("<Control-e>",Exportar_PDF_key)
    root.bind("<Control-E>",Exportar_PDF_key)
    root.bind("<Control-q>",Sair_key)
    root.bind("<Control-Q>",Sair_key)
    # Atalhos e Evento de Tecla do Menu Editar
    root.bind("<Control-z>",lambda e: Desfazer())
    root.bind("<Control-Z>",lambda e: Desfazer())
    root.bind("<Control-y>",lambda e: Refazer())
    root.bind("<Control-Y>",lambda e: Refazer())
    root.bind("<Control-x>",Recortar_key)
    root.bind("<Control-X>",Recortar_key)
    root.bind("<Control-c>",Copiar_key)
    root.bind("<Control-C>",Copiar_key)
    root.bind("<Control-v>",Colar_key)
    root.bind("<Control-V>",Colar_key)
    root.bind("<Control-a>",Selecionar_Tudo_key)
    root.bind("<Control-A>",Selecionar_Tudo_key)
    pass
   


if __name__=="__main__":
    MenuPrincipal()
    Set_editor_de_texto()
    AtalhoDoTeclado()
    root.mainloop()

