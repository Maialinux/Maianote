import customtkinter as ctk
import tkinter as tk

# Configurando o tema do CustomTkinter
ctk.set_appearance_mode("dark")  # Modo escuro
ctk.set_default_color_theme("blue")  # Tema azul

# Criando a janela principal
root = ctk.CTk()
root.title("Menu com Checkbox no CustomTkinter")
root.geometry("400x300")

# Variável para armazenar o estado do checkbox
var_checkbox = tk.BooleanVar(value=False)

# Função para alternar o modo de aparência
def alternar_modo():
    if var_checkbox.get():
        ctk.set_appearance_mode("light")  # Modo claro
    else:
        ctk.set_appearance_mode("dark")   # Modo escuro

# Criando o menu principal
menu_principal = tk.Menu(root)
root.configure(menu=menu_principal)

# Criando um menu "Configurações" com checkbox
menu_configuracoes = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Configurações", menu=menu_configuracoes)

# Adicionando um checkbox ao menu
menu_configuracoes.add_checkbutton(
    label="Modo Claro",
    variable=var_checkbox,
    command=alternar_modo
)

# Executando a aplicação
root.mainloop()