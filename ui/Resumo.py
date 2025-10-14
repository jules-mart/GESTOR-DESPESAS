# resumo.py

import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AbaResumo(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Configura o grid da aba para dividir o espaço entre o gráfico e os detalhes
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- DADOS DE EXEMPLO (substitua pela sua lógica real) ---
        renda_mensal = 5000.00
        despesas_totais = 3250.50
        saldo_restante = renda_mensal - despesas_totais

        # Frame para o Gráfico
        chart_frame = ctk.CTkFrame(self, fg_color="transparent")
        chart_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # --- Criação do Gráfico Circular (Donut Chart) ---
        figura = Figure(figsize=(4, 4), dpi=100)
        figura.patch.set_facecolor("#242424")  # Cor de fundo do TabView
        ax = figura.add_subplot(111)

        valores = [despesas_totais, saldo_restante]
        legendas = ['Despesas', 'Saldo']
        # Vermelho para despesa, verde para saldo
        cores = ['#e63946', '#2a9d8f']

        ax.pie(valores, labels=None, colors=cores, autopct=None, startangle=90,
               wedgeprops=dict(width=0.4, edgecolor='#242424'))

        porcentagem_gasta = (despesas_totais / renda_mensal) * 100
        ax.text(0, 0, f'{porcentagem_gasta:.1f}%\nGasto', ha='center', va='center',
                fontsize=24, color='white', weight='bold')

        canvas = FigureCanvasTkAgg(figura, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

        # --- Frame para os Detalhes em Texto ---
        details_frame = ctk.CTkFrame(self, fg_color="transparent")
        details_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        label_titulo_detalhes = ctk.CTkLabel(
            details_frame, text="Resumo do Mês", font=ctk.CTkFont(size=22, weight="bold"))
        label_titulo_detalhes.pack(pady=(20, 20), anchor="w")

        label_renda = ctk.CTkLabel(
            details_frame, text=f"Renda Mensal: R$ {renda_mensal:,.2f}", font=ctk.CTkFont(size=16))
        label_renda.pack(pady=10, anchor="w")

        label_despesas = ctk.CTkLabel(
            details_frame, text=f"Total de Despesas: R$ {despesas_totais:,.2f}", font=ctk.CTkFont(size=16))
        label_despesas.pack(pady=10, anchor="w")

        label_saldo = ctk.CTkLabel(details_frame, text=f"Saldo Restante: R$ {saldo_restante:,.2f}", font=ctk.CTkFont(
            size=18, weight="bold"), text_color="#2a9d8f")
        label_saldo.pack(pady=20, anchor="w")
