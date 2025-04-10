import customtkinter as ctk
import tkinter as tk
# Configurando o tema do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Criando a janela principal
root = ctk.CTk()
root.title("Menu Personalizado com Checkbox")
root.geometry("400x300")

# Variável para armazenar o estado do checkbox
var_checkbox = tk.BooleanVar(value=False)

# Função para alternar o modo de aparência
def alternar_modo():
    if var_checkbox.get():
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

# Criando um frame para o menu personalizado
menu_frame = ctk.CTkFrame(root, width=200, height=300, fg_color="gray15")
menu_frame.place(x=0, y=0)

# Adicionando um título ao menu
titulo = ctk.CTkLabel(menu_frame, text="Configurações", font=("Arial", 16))
titulo.pack(pady=10)

# Adicionando um checkbox ao menu
checkbox = ctk.CTkCheckBox(menu_frame, text="Modo Claro", variable=var_checkbox, command=alternar_modo)
checkbox.pack(pady=10)

# Executando a aplicação
root.mainloop()