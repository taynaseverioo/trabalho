import tkinter as tk
from tkinter import messagebox
import time
import json

# Carregar dados de usuários do arquivo
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Salvar dados de usuários no arquivo
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)

# Definição das Estratégias de Autenticação
class AuthStrategy:
    def __init__(self, users):
        self.users = users

    def authenticate(self, username: str, password: str) -> bool:
        return username in self.users and self.users[username] == password

# Sujeito Observável
class AuthSubject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, event):
        for observer in self.observers:
            observer.update(event)

# Observador
class AuthObserver:
    def __init__(self, subject):
        self.subject = subject
        self.subject.attach(self)

    def update(self, event):
        if event == "login_success":
            messagebox.showinfo("Login", "Login bem-sucedido!")
        elif event == "login_failed":
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        elif event == "registration_success":
            messagebox.showinfo("Sucesso", "Registro bem-sucedido! Você pode agora fazer login.")
        elif event == "registration_failed":
            messagebox.showerror("Erro", "Usuário já existe. Escolha um nome de usuário diferente.")

# Variáveis globais
users = load_users()
auth_strategy = AuthStrategy(users)
attempts = 0
max_attempts = 3
block_duration = 30  # segundos
blocked_until = 0

# Sujeito Observável de Autenticação
auth_subject = AuthSubject()
auth_observer = AuthObserver(auth_subject)

# Funções da Interface do Usuário (Tkinter)
def login():
    global attempts
    global blocked_until

    current_time = time.time()
    if current_time < blocked_until:
        remaining_time = int(blocked_until - current_time)
        messagebox.showwarning("Bloqueado", f"Tente novamente em {remaining_time} segundos.")
        return

    username = entry_username.get()
    password = entry_password.get()

    if auth_strategy.authenticate(username, password):
        attempts = 0
        auth_subject.notify("login_success")
    else:
        attempts += 1
        if attempts >= max_attempts:
            blocked_until = current_time + block_duration
            messagebox.showerror("Bloqueado", f"Muitas tentativas falhadas. Tente novamente em {block_duration} segundos.")
        else:
            remaining_attempts = max_attempts - attempts
            messagebox.showerror("Erro", f"Usuário ou senha incorretos. Você tem {remaining_attempts} tentativas restantes.")
            auth_subject.notify("login_failed")

# Função para abrir a tela principal após o login
def open_main_screen():
    # Fechar a janela de login
    root.destroy()
    
    # Abrir a tela principal do sistema
    root_main = tk.Tk()
    root_main.title("Tela Principal")
    root_main.geometry("300x200")

def register():
    new_username = entry_new_username.get()
    new_password = entry_new_password.get()
    
    if new_username in users:
        auth_subject.notify("registration_failed")
    else:
        users[new_username] = new_password
        save_users(users)
        auth_subject.notify("registration_success")

def show_register_window():
    global entry_new_username, entry_new_password, register_window
    register_window = tk.Toplevel(root)  # Cria uma nova janela (Toplevel)
    register_window.title("Registrar")  # Define o título da nova janela
    register_window.geometry("300x200")  # Define o tamanho da nova janela

    # Cria e posiciona o rótulo e a entrada para o novo nome de usuário
    label_new_username = tk.Label(register_window, text="Novo Usuário")
    label_new_username.pack(pady=5)

    entry_new_username = tk.Entry(register_window)
    entry_new_username.pack(pady=5)

    # Cria e posiciona o rótulo e a entrada para a nova senha
    label_new_password = tk.Label(register_window, text="Nova Senha")
    label_new_password.pack(pady=5)

    entry_new_password = tk.Entry(register_window, show="*")
    entry_new_password.pack(pady=5)

    # Cria e posiciona o botão de registro que chama a função register
    button_register = tk.Button(register_window, text="Registrar", command=register)
    button_register.pack(pady=20)
    
    # Configura a janela de registro para ser modal
    register_window.grab_set()

# Configuração da janela principal
root = tk.Tk()
root.title("Tela de Login")
root.geometry("300x200")

# Widgets da tela de login
label_username = tk.Label(root, text="Usuário")
label_username.pack(pady=5)

entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="Senha")
label_password.pack(pady=5)

entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

button_login = tk.Button(root, text="Entrar", command=login)
button_login.pack(pady=5)

button_register = tk.Button(root, text="Registrar", command=show_register_window)
button_register.pack(pady=5)

# Iniciar a aplicação
root.mainloop()
