import tkinter as tk
from tkinter import messagebox
import time
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações do email
EMAIL = "renantaynaerik2@gmail.com"  
SENHA_EMAIL = "wpku yqbm vyba qorc"

# Função para enviar email
def enviar_email(assunto, corpo):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = EMAIL
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain'))

    try:
        servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        servidor_smtp.starttls()
        servidor_smtp.login(EMAIL, SENHA_EMAIL)
        texto = msg.as_string()
        servidor_smtp.sendmail(EMAIL, EMAIL, texto)
        servidor_smtp.quit()
    except Exception as e:
        print(f"Falha ao enviar email: {e}")

# Função para registrar acessos e erros
def registrar_evento(nome_usuario, evento):
    ip = "127.0.0.1"  # Aqui você pode adicionar lógica para obter o IP real
    entrada_log = {
        "nome": nome_usuario,
        "evento": evento,
        "data/hora": time.strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip
    }
    with open("access_log.json", "a") as arquivo_log:
        arquivo_log.write(json.dumps(entrada_log) + "\n")  # Escreve a entrada JSON no arquivo seguido por uma nova linha

# Carregar dados de usuários do arquivo
def carregar_usuarios():
    try:
        with open("usuarios.json", "r") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

# Salvar dados de usuários no arquivo
def salvar_usuarios(usuarios):
    with open("usuarios.json", "w") as arquivo:
        json.dump(usuarios, arquivo)

# Definição das Estratégias de Autenticação
class EstrategiaAutenticacao:
    def __init__(self, usuarios):
        self.usuarios = usuarios

    def autenticar(self, nome_usuario: str, senha: str) -> bool:
        return nome_usuario in self.usuarios and self.usuarios[nome_usuario] == senha

# Sujeito Observável
class AssuntoAutenticacao:
    def __init__(self):
        self.observadores = []

    def anexar(self, observador):
        self.observadores.append(observador)

    def notificar(self, evento):
        for observador in self.observadores:
            observador.atualizar(evento)

# Observador
class ObservadorAutenticacao:
    def __init__(self, assunto):
        self.assunto = assunto
        self.assunto.anexar(self)

    def atualizar(self, evento):
        if evento == "login_sucesso":
            messagebox.showinfo("Login", "Login bem-sucedido!")
        elif evento == "login_falhou":
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos.")
        elif evento == "registro_sucesso":
            messagebox.showinfo("Sucesso", "Registro bem-sucedido! Você pode fazer login agora.")
        elif evento == "registro_falhou":
            messagebox.showerror("Erro", "O nome de usuário já existe. Escolha um nome de usuário diferente.")

# Variáveis globais
usuarios = carregar_usuarios()
estrategia_autenticacao = EstrategiaAutenticacao(usuarios)
tentativas = 0
max_tentativas = 3
duracao_bloqueio = 30  # segundos
bloqueado_ate = 0

# Sujeito Observável de Autenticação
assunto_autenticacao = AssuntoAutenticacao()
observador_autenticacao = ObservadorAutenticacao(assunto_autenticacao)

# Funções da Interface do Usuário (Tkinter)
def fazer_login():
    global tentativas
    global bloqueado_ate

    hora_atual = time.time()
    if hora_atual < bloqueado_ate:
        tempo_restante = int(bloqueado_ate - hora_atual)
        messagebox.showwarning("Bloqueado", f"Tente novamente em {tempo_restante} segundos.")
        return

    nome_usuario = entrada_nome_usuario.get()
    senha = entrada_senha.get()

    if estrategia_autenticacao.autenticar(nome_usuario, senha):
        tentativas = 0
        assunto_autenticacao.notificar("login_sucesso")
        registrar_evento(nome_usuario, "sucesso_login")
        enviar_email("Login bem-sucedido", f"Login bem-sucedido para o usuário: {nome_usuario}")

    else:
        tentativas += 1
        registrar_evento(nome_usuario, "falha_login")
        enviar_email("Tentativa de login falhou", f"Tentativa de login falhou para o usuário: {nome_usuario}")
        
        if tentativas >= max_tentativas:
            bloqueado_ate = hora_atual + duracao_bloqueio
            messagebox.showerror("Bloqueado", f"Muitas tentativas de login falhadas. Tente novamente em {duracao_bloqueio} segundos.")
            enviar_email("Conta bloqueada", f"A conta do usuário {nome_usuario} foi bloqueada por {duracao_bloqueio} segundos devido a muitas tentativas falhadas.")
        else:
            tentativas_restantes = max_tentativas - tentativas
            messagebox.showerror("Erro", f"Nome de usuário ou senha incorretos. Você tem {tentativas_restantes} tentativas restantes.")
            assunto_autenticacao.notificar("login_falhou")

def fazer_registro():
    novo_nome_usuario = entrada_novo_nome_usuario.get()
    nova_senha = entrada_nova_senha.get()
    
    if novo_nome_usuario in usuarios:
        assunto_autenticacao.notificar("registro_falhou")
        registrar_evento(novo_nome_usuario, "falha_registro")
    else:
        usuarios[novo_nome_usuario] = nova_senha
        salvar_usuarios(usuarios)
        assunto_autenticacao.notificar("registro_sucesso")
        registrar_evento(novo_nome_usuario, "sucesso_registro")
        enviar_email("Novo usuário registrado", f"Um novo usuário foi registrado: {novo_nome_usuario}")

def mostrar_janela_registro():
    global entrada_novo_nome_usuario, entrada_nova_senha, janela_registro
    janela_registro = tk.Toplevel(raiz)  # Cria uma nova janela (Toplevel)
    janela_registro.title("Registrar")  # Define o título da nova janela
    janela_registro.geometry("300x200")  # Define o tamanho da nova janela

    # Cria e posiciona o rótulo e a entrada para o novo nome de usuário
    rotulo_novo_nome_usuario = tk.Label(janela_registro, text="Novo Usuário")
    rotulo_novo_nome_usuario.pack(pady=5)

    entrada_novo_nome_usuario = tk.Entry(janela_registro)
    entrada_novo_nome_usuario.pack(pady=5)

    # Cria e posiciona o rótulo e a entrada para a nova senha
    rotulo_nova_senha = tk.Label(janela_registro, text="Nova Senha")
    rotulo_nova_senha.pack(pady=5)

    entrada_nova_senha = tk.Entry(janela_registro, show="*")
    entrada_nova_senha.pack(pady=5)

    # Cria e posiciona o botão de registro que chama a função fazer_registro
    botao_registro = tk.Button(janela_registro, text="Registrar", command=fazer_registro)
    botao_registro.pack(pady=20)
    
    # Configura a janela de registro para ser modal
    janela_registro.grab_set()

# Configuração da janela principal
raiz = tk.Tk()
raiz.title("Tela de Login")
raiz.geometry("300x200")

# Widgets da tela de login
rotulo_nome_usuario = tk.Label(raiz, text="Nome de Usuário")
rotulo_nome_usuario.pack(pady=5)

entrada_nome_usuario = tk.Entry(raiz)
entrada_nome_usuario.pack(pady=5)

rotulo_senha = tk.Label(raiz, text="Senha")
rotulo_senha.pack(pady=5)

entrada_senha = tk.Entry(raiz, show="*")
entrada_senha.pack(pady=5)

botao_login = tk.Button(raiz, text="Entrar", command=fazer_login)
botao_login.pack(pady=5)

botao_registro = tk.Button(raiz, text="Registrar", command=mostrar_janela_registro)
botao_registro.pack(pady=5)

# Iniciar a aplicação
raiz.mainloop()
