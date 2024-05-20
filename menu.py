import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Função para adicionar um produto à lista de compras
def add_to_shopping_list(product):
    # Adiciona o produto à lista de compras
    shopping_list_box.insert(tk.END, product)
    
    # Exibe uma mensagem para o cliente
    messagebox.showinfo("Produto Adicionado", f"{product} foi adicionado à lista de compras!")

# Configuração da tela principal do sistema
root_main = tk.Tk()
root_main.title("Sistema de Compras")
root_main.geometry("800x600")

# Título da tela principal
label_title_main = tk.Label(root_main, text="Bem-vindo ao Sistema de Compras", font=("Helvetica", 20))
label_title_main.pack(pady=20)

# Lista de produtos do supermercado
label_products = tk.Label(root_main, text="Lista de Produtos", font=("Helvetica", 16))
label_products.pack()

# Carrega imagens dos produtos
image_arroz = Image.open("arroz.png")  # Substitua "arroz.png" pelo nome da sua imagem de arroz
image_feijao = Image.open("feijao.png")  # Substitua "feijao.png" pelo nome da sua imagem de feijão
image_macarrao = Image.open("macarrao.png")  # Substitua "macarrao.png" pelo nome da sua imagem de macarrão

# Redimensiona as imagens para caber nos botões
image_arroz = image_arroz.resize((100, 100), Image.ANTIALIAS)
image_feijao = image_feijao.resize((100, 100), Image.ANTIALIAS)
image_macarrao = image_macarrao.resize((100, 100), Image.ANTIALIAS)

# Converte as imagens para o formato Tkinter
photo_arroz = ImageTk.PhotoImage(image_arroz)
photo_feijao = ImageTk.PhotoImage(image_feijao)
photo_macarrao = ImageTk.PhotoImage(image_macarrao)

# Botões com imagens
button_arroz = tk.Button(root_main, image=photo_arroz, command=lambda: add_to_shopping_list("Arroz"))
button_arroz.pack(pady=5)

button_feijao = tk.Button(root_main, image=photo_feijao, command=lambda: add_to_shopping_list("Feijão"))
button_feijao.pack(pady=5)

button_macarrao = tk.Button(root_main, image=photo_macarrao, command=lambda: add_to_shopping_list("Macarrão"))
button_macarrao.pack(pady=5)

# Lista de compras
label_shopping_list = tk.Label(root_main, text="Lista de Compras", font=("Helvetica", 16))
label_shopping_list.pack()

shopping_list_box = tk.Listbox(root_main, width=50, height=10)
shopping_list_box.pack()

# Botão para sair do sistema
button_exit_main = tk.Button(root_main, text="Sair", font=("Helvetica", 12), command=root_main.quit)
button_exit_main.pack(pady=20)

# Iniciar a aplicação
root_main.mainloop()
