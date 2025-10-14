# Login.py (Versão Atualizada)

import customtkinter as ctk
from tkinter import messagebox
from Cadastro import TelaCadastro
from TelaPrincipal import TelaPrincipal  # <-- IMPORTA A NOVA TELA

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login - Sistema Financeiro")
        self.geometry("400x350")
        self.resizable(False, False)

        # Frame principal
        self.frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e1e2f")
        self.frame.pack(padx=40, pady=40, fill="both", expand=True)

        # Título
        self.label_titulo = ctk.CTkLabel(
            self.frame,
            text="Acesso ao Sistema",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff"
        )
        self.label_titulo.pack(pady=(20, 10))

        # Campo usuário
        self.entry_usuario = ctk.CTkEntry(
            self.frame,
            placeholder_text="Usuário",
            fg_color="#2c2c3c",
            text_color="#ffffff",
            placeholder_text_color="#aaaaaa"
        )
        self.entry_usuario.pack(pady=10, padx=20, fill="x")

        # Campo senha
        self.entry_senha = ctk.CTkEntry(
            self.frame,
            placeholder_text="Senha",
            show="*",
            fg_color="#2c2c3c",
            text_color="#ffffff",
            placeholder_text_color="#aaaaaa"
        )
        self.entry_senha.pack(pady=10, padx=20, fill="x")

        # Botão Login
        self.btn_login = ctk.CTkButton(
            self.frame,
            text="Entrar",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white",
            command=self.verificar_login
        )
        self.btn_login.pack(pady=(25, 10), padx=20, fill="x")

        # Botão Cadastro
        self.btn_cadastro = ctk.CTkButton(
            self.frame,
            text="Cadastrar",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#16a34a",
            hover_color="#15803d",
            text_color="white",
            command=self.abrir_cadastro
        )
        self.btn_cadastro.pack(pady=(0, 10), padx=20, fill="x")

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if usuario == "admin" and senha == "1234":
            # --- MUDANÇA PRINCIPAL AQUI ---
            self.destroy()  # Fecha a janela de login
            tela_principal = TelaPrincipal()  # Cria a tela principal
            tela_principal.mainloop()  # Exibe a tela principal
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def abrir_cadastro(self):
        TelaCadastro(self)
