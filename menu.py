import tkinter as tk
from tkinter import messagebox

# Função para adicionar um produto à lista de compras
def add_to_shopping_list(produto):
    # Adiciona o produto à lista de compras
    shopping_list_box.insert(tk.END, produto)
    
    # Exibe uma mensagem para o cliente
    messagebox.showinfo("Produto Adicionado", f"{produto} foi adicionado à lista de compras!")

# Configuração da tela principal do sistema
root_main = tk.Tk()
root_main.title("Sistema de Compras")
root_main.geometry("800x600")

# Título da tela principal
label_title_main = tk.Label(root_main, text="Bem-vindo ao Sistema de Compras", font=("Helvetica", 20))
label_title_main.pack(pady=20)

# Lista de produtos do supermercado
label_produto = tk.Label(root_main, text="Lista de Produtos", font=("Helvetica", 16))
label_produto.pack()

produto = [
    "Arroz",
    "Feijão",
    "Macarrão",
    "Óleo de Soja",
    "Leite",
    "Café",
    "Açúcar",
    "Sal",
    "Farinha de Trigo",
    "Ovos",
    "Tomate",
    "Cebola",
    "Batata",
    "Banana",
    "Maçã",
    "Laranja"
]

for produto in produto:
    button_product = tk.Button(root_main, text=produto, command=lambda p=produto: add_to_shopping_list(p))
    button_product.pack(pady=5)

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
