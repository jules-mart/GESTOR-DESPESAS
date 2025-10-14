import customtkinter as ctk
from tkinter import messagebox


class TelaCadastro(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Usuário")
        self.geometry("500x650")
        self.resizable(False, False)
        self.grab_set()

        # O frame principal ainda usa .pack para preencher a janela
        self.frame = ctk.CTkFrame(self, fg_color="#1e1e2f")
        self.frame.pack(padx=30, pady=30, fill="both", expand=True)

        # --- CONFIGURANDO O LAYOUT GRID ---
        # Faz a coluna 0 (a única que usaremos) se expandir para preencher o frame
        self.frame.grid_columnconfigure(0, weight=1)

        # Título
        self.label_titulo = ctk.CTkLabel(
            self.frame,
            text="🧾 Cadastro de Usuário",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff"
        )
        # sticky="ew" faz o widget se esticar horizontalmente (leste-oeste)
        self.label_titulo.grid(row=0, column=0, padx=30, pady=(15, 5))

        # Subtítulo
        self.label_subtitulo = ctk.CTkLabel(
            self.frame,
            text="Preencha seus dados pessoais e financeiros",
            font=ctk.CTkFont(size=13),
            text_color="#a5a5a5"
        )
        self.label_subtitulo.grid(row=1, column=0, padx=30, pady=(0, 15))

        # --- Campos de Dados Pessoais ---
        self.entry_nome = ctk.CTkEntry(
            self.frame, placeholder_text="Nome completo",
            fg_color="#2c2c3c", text_color="#ffffff", placeholder_text_color="#aaaaaa"
        )
        self.entry_nome.grid(row=2, column=0, padx=30, pady=8, sticky="ew")

        self.entry_data_nasc = ctk.CTkEntry(
            self.frame, placeholder_text="Data de nascimento (DD/MM/AAAA)",
            fg_color="#2c2c3c", text_color="#ffffff", placeholder_text_color="#aaaaaa"
        )
        self.entry_data_nasc.grid(
            row=3, column=0, padx=30, pady=8, sticky="ew")

        self.entry_cpf = ctk.CTkEntry(
            self.frame, placeholder_text="CPF (somente números)",
            fg_color="#2c2c3c", text_color="#ffffff", placeholder_text_color="#aaaaaa"
        )
        self.entry_cpf.grid(row=4, column=0, padx=30, pady=8, sticky="ew")

        self.entry_profissao = ctk.CTkEntry(
            self.frame, placeholder_text="Profissão",
            fg_color="#2c2c3c", text_color="#ffffff", placeholder_text_color="#aaaaaa"
        )
        self.entry_profissao.grid(
            row=5, column=0, padx=30, pady=8, sticky="ew")

        self.entry_renda = ctk.CTkEntry(
            self.frame, placeholder_text="Renda mensal (R$)",
            fg_color="#2c2c3c", text_color="#ffffff", placeholder_text_color="#aaaaaa"
        )
        self.entry_renda.grid(row=6, column=0, padx=30, pady=8, sticky="ew")

        # --- Campos de Dados de Acesso ---
        self.label_login = ctk.CTkLabel(
            self.frame, text="Dados de Acesso", font=ctk.CTkFont(size=14, weight="bold"), text_color="#ffffff"
        )
        self.label_login.grid(row=7, column=0, padx=30, pady=(20, 5))

        self.entry_usuario = ctk.CTkEntry(
            self.frame, placeholder_text="Usuário",
            fg_color="#2c2c3c", text_color="#ffffff", placeholder_text_color="#aaaaaa"
        )
        self.entry_usuario.grid(row=8, column=0, padx=30, pady=8, sticky="ew")

        self.entry_senha = ctk.CTkEntry(
            self.frame, placeholder_text="Senha", show="*",
            fg_color="#2c2c3c", text_color="#ffffff", placeholder_text_color="#aaaaaa"
        )
        self.entry_senha.grid(row=9, column=0, padx=30, pady=8, sticky="ew")

        self.entry_confirmar = ctk.CTkEntry(
            self.frame, placeholder_text="Confirmar senha", show="*",
            fg_color="#2c2c3c", text_color="#ffffff", placeholder_text_color="#aaaaaa"
        )
        self.entry_confirmar.grid(
            row=10, column=0, padx=30, pady=8, sticky="ew")

        # --- BOTÃO DE CADASTRO ---
        self.btn_cadastrar = ctk.CTkButton(
            self.frame,
            text="Cadastrar",
            command=self.cadastrar_usuario,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#16a34a",
            hover_color="#15803d",
            text_color="white"
        )
        self.btn_cadastrar.grid(
            row=11, column=0, padx=30, pady=20, sticky="ew")

    def cadastrar_usuario(self):
        senha = self.entry_senha.get()
        confirmar_senha = self.entry_confirmar.get()

        if senha != confirmar_senha:
            messagebox.showerror("Erro de Cadastro",
                                 "As senhas não coincidem!", parent=self)
            return

        campos = [
            self.entry_nome.get(), self.entry_data_nasc.get(), self.entry_cpf.get(),
            self.entry_profissao.get(), self.entry_renda.get(), self.entry_usuario.get(),
            self.entry_senha.get()
        ]

        if any(campo == "" for campo in campos):
            messagebox.showwarning(
                "Atenção", "Por favor, preencha todos os campos.", parent=self)
            return

        messagebox.showinfo(
            "Sucesso", "Usuário cadastrado com sucesso!", parent=self)
        self.destroy()
