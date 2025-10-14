# TelaPrincipal.py

import customtkinter as ctk


class TelaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Painel Financeiro Principal")
        self.geometry("800x600")
        self.resizable(True, True)

        # Configura o grid para que o TabView ocupe todo o espaço
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Cria o sistema de Abas (TabView) ---
        self.tab_view = ctk.CTkTabview(self, fg_color="#1e1e2f")
        self.tab_view.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # --- Adiciona as abas ---
        self.tab_view.add("Resumo")
        self.tab_view.add("Limites")
        self.tab_view.add("Metas")
        self.tab_view.add("Despesas")

        # Define a aba inicial que será exibida
        self.tab_view.set("Resumo")

        # --- Adiciona conteúdo de exemplo em cada aba ---
        self.criar_conteudo_abas()

    def criar_conteudo_abas(self):
        # Aba de Resumo
        frame_resumo = self.tab_view.tab("Resumo")
        label_resumo = ctk.CTkLabel(
            frame_resumo,
            text="Aqui ficará o resumo financeiro.",
            font=ctk.CTkFont(size=20)
        )
        label_resumo.pack(padx=20, pady=20, expand=True)

        # Aba de Limites
        frame_limites = self.tab_view.tab("Limites")
        label_limites = ctk.CTkLabel(
            frame_limites,
            text="Aqui ficarão os controles de limites de gastos.",
            font=ctk.CTkFont(size=20)
        )
        label_limites.pack(padx=20, pady=20, expand=True)

        # Aba de Metas
        frame_metas = self.tab_view.tab("Metas")
        label_metas = ctk.CTkLabel(
            frame_metas,
            text="Aqui ficará o acompanhamento de metas.",
            font=ctk.CTkFont(size=20)
        )
        label_metas.pack(padx=20, pady=20, expand=True)

        # Aba de Despesas
        frame_despesas = self.tab_view.tab("Despesas")
        label_despesas = ctk.CTkLabel(
            frame_despesas,
            text="Aqui será o local para lançamento de despesas.",
            font=ctk.CTkFont(size=20)
        )
        label_despesas.pack(padx=20, pady=20, expand=True)
