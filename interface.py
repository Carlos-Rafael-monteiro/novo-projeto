import tkinter as tk
from tkinter import messagebox, ttk

from estacionamento import Estacionamento


class TelaLogin:
    """Tela inicial de autenticação do sistema."""

    def __init__(self, parent: tk.Tk, callback) -> None:
        self.parent = parent
        self.root = parent
        self.callback = callback

        # Garante que a janela principal esteja visível e preparada para receber os widgets.
        self.parent.deiconify()
        self.parent.update_idletasks()
        self.parent.title("Login")
        self.parent.geometry("360x260")
        self.parent.resizable(False, False)
        self.parent.configure(bg="#0f172a")
        self.parent.protocol("WM_DELETE_WINDOW", self.parent.destroy)
        self.parent.attributes("-fullscreen", False)

        # Remove qualquer conteúdo antigo para evitar resíduos visuais ao trocar de tela.
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Cria o cartão visual da tela de login.
        card = tk.Frame(self.parent, bg="#111827", bd=0)
        card.place(relx=0.5, rely=0.5, anchor="center", width=320, height=220)

        tk.Label(card, text="Acesso ao sistema", fg="#f8fafc", bg="#111827", font=("Segoe UI", 15, "bold")).pack(pady=(18, 8))
        tk.Label(card, text="Entre com suas credenciais", fg="#94a3b8", bg="#111827", font=("Segoe UI", 10)).pack()

        tk.Label(card, text="Usuário:", fg="#e2e8f0", bg="#111827", anchor="w").pack(anchor="w", padx=24, pady=(12, 2))
        self.usuario_var = tk.StringVar()
        tk.Entry(card, textvariable=self.usuario_var, bg="#1f2937", fg="#f9fafb", insertbackground="#f9fafb", bd=0, relief="flat").pack(padx=24, fill="x")

        tk.Label(card, text="Senha:", fg="#e2e8f0", bg="#111827", anchor="w").pack(anchor="w", padx=24, pady=(8, 2))
        self.senha_var = tk.StringVar()
        tk.Entry(card, textvariable=self.senha_var, show="*", bg="#1f2937", fg="#f9fafb", insertbackground="#f9fafb", bd=0, relief="flat").pack(padx=24, fill="x")

        tk.Button(card, text="Entrar", command=self.entrar, bg="#2563eb", fg="white", bd=0, relief="flat", padx=14, pady=6, font=("Segoe UI", 10, "bold")).pack(pady=(16, 0))
        tk.Button(card, text="Tela cheia", command=self.alternar_tela_cheia, bg="#0f766e", fg="white", bd=0, relief="flat", padx=10, pady=5, font=("Segoe UI", 9, "bold")).pack(pady=(8, 0))
        # Atalhos de teclado para facilitar o uso do operador.
        self.parent.bind("<Return>", lambda _event: self.entrar())
        self.parent.bind("<F11>", lambda _event: self.alternar_tela_cheia())

    def alternar_tela_cheia(self) -> None:
        estado = self.parent.attributes("-fullscreen")
        self.parent.attributes("-fullscreen", not estado)

    def entrar(self) -> None:
        """Valida as credenciais do usuário e, se estiverem corretas, entra no sistema."""
        usuario = self.usuario_var.get().strip()
        senha = self.senha_var.get().strip()
        if self.callback(usuario, senha):
            for widget in self.parent.winfo_children():
                widget.destroy()
            InterfaceEstacionamento(self.parent, usuario=usuario)


class CadastroWindow(tk.Toplevel):
    """Janela responsável pelo cadastro e manutenção de clientes do estacionamento."""

    def __init__(self, parent: tk.Tk, app: "InterfaceEstacionamento") -> None:
        super().__init__(parent)
        self.app = app
        self.estacionamento = app.estacionamento
        self.title("Cadastro de clientes")
        self.geometry("900x560")
        self.resizable(False, False)
        self.configure(bg="#0f172a")
        self.transient(parent)

        # Formulário para inserir os dados do cliente.
        frame_form = tk.LabelFrame(self, text="Cadastro de clientes", bg="#111827", fg="#f8fafc", padx=12, pady=12, font=("Segoe UI", 12, "bold"))
        frame_form.pack(fill="x", padx=18, pady=(16, 10))

        tk.Label(frame_form, text="Tipo:", fg="#e2e8f0", bg="#111827").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.tipo_var = tk.StringVar(value="mensalista")
        ttk.Combobox(frame_form, textvariable=self.tipo_var, values=["mensalista", "credenciado", "avulso"], state="readonly", width=20).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nome:", fg="#e2e8f0", bg="#111827").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.nome_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.nome_var, width=25, bg="#1f2937", fg="#f9fafb", insertbackground="#f9fafb").grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Placa:", fg="#e2e8f0", bg="#111827").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.placa_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.placa_var, width=25, bg="#1f2937", fg="#f9fafb", insertbackground="#f9fafb").grid(row=2, column=1, padx=5, pady=5)
        tk.Label(frame_form, text="Ex.: ABC1234 ou ABC1D23", fg="#94a3b8", bg="#111827", font=("Segoe UI", 9)).grid(row=2, column=2, sticky="w", padx=5)

        tk.Label(frame_form, text="Telefone:", fg="#e2e8f0", bg="#111827").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.telefone_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.telefone_var, width=25, bg="#1f2937", fg="#f9fafb", insertbackground="#f9fafb").grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Valor mensal:", fg="#e2e8f0", bg="#111827").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.valor_mensal_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.valor_mensal_var, width=25, bg="#1f2937", fg="#f9fafb", insertbackground="#f9fafb").grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Código de acesso:", fg="#e2e8f0", bg="#111827").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.codigo_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.codigo_var, width=25, bg="#1f2937", fg="#f9fafb", insertbackground="#f9fafb").grid(row=5, column=1, padx=5, pady=5)

        tk.Button(frame_form, text="Salvar", command=self.salvar_cliente, width=18, bg="#2563eb", fg="white", bd=0, relief="flat", pady=4).grid(row=6, column=0, padx=5, pady=10)
        tk.Button(frame_form, text="Remover", command=self.remover_cliente, width=18, bg="#ef4444", fg="white", bd=0, relief="flat", pady=4).grid(row=6, column=1, padx=5, pady=10)

        # Lista visual dos clientes já cadastrados para consulta rápida.
        frame_lista = tk.LabelFrame(self, text="Clientes cadastrados", bg="#111827", fg="#f8fafc", padx=10, pady=10, font=("Segoe UI", 11, "bold"))
        frame_lista.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.tabela = ttk.Treeview(frame_lista, columns=("tipo", "nome", "placa", "telefone", "valor_mensal", "codigo_acesso", "valor_hora"), show="headings")
        self.tabela.heading("tipo", text="Tipo")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("placa", text="Placa")
        self.tabela.heading("telefone", text="Telefone")
        self.tabela.heading("valor_mensal", text="Valor Mensal")
        self.tabela.heading("codigo_acesso", text="Código")
        self.tabela.heading("valor_hora", text="Valor/Hora")
        self.tabela.pack(fill="both", expand=True)
        self.atualizar_tabela()

    def salvar_cliente(self) -> None:
        """Salva um novo cliente após validar os campos obrigatórios."""
        try:
            tipo = self.tipo_var.get()
            nome = self.nome_var.get().strip()
            placa = self.estacionamento.normalizar_placa(self.placa_var.get().strip())
            self.placa_var.set(placa)
            telefone = self.telefone_var.get().strip()
            valor_mensal = float(self.valor_mensal_var.get()) if self.valor_mensal_var.get() else None
            codigo_acesso = self.codigo_var.get().strip()

            if not nome or not placa or not telefone:
                raise ValueError("Nome, placa e telefone são obrigatórios")

            self.estacionamento.cadastrar_cliente(
                tipo=tipo,
                nome=nome,
                placa=placa,
                telefone=telefone,
                valor_mensal=valor_mensal,
                codigo_acesso=codigo_acesso,
            )
            self.estacionamento.salvar()
            self.limpar_campos()
            self.atualizar_tabela()
            self.app.atualizar_janelas()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso")
        except ValueError as err:
            messagebox.showerror("Erro", str(err))
        except Exception as err:  # pragma: no cover - depende do ambiente
            messagebox.showerror("Erro", f"Não foi possível salvar: {err}")

    def remover_cliente(self) -> None:
        """Remove um cliente selecionado da lista e persiste a alteração."""
        selecionado = self.tabela.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente na lista")
            return

        item = self.tabela.item(selecionado[0])
        placa = item["values"][2]
        if self.estacionamento.remover_cliente(placa):
            self.estacionamento.salvar()
            self.atualizar_tabela()
            self.app.atualizar_janelas()
            messagebox.showinfo("Sucesso", "Cliente removido")

    def limpar_campos(self) -> None:
        """Limpa os campos do formulário após o cadastro."""
        self.nome_var.set("")
        self.placa_var.set("")
        self.telefone_var.set("")
        self.valor_mensal_var.set("")
        self.codigo_var.set("")

    def atualizar_tabela(self) -> None:
        """Recarrega a grade de clientes com os dados mais recentes."""
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for cliente in self.estacionamento.listar_clientes():
            self.tabela.insert(
                "",
                "end",
                values=(
                    cliente.get("tipo", ""),
                    cliente.get("nome", ""),
                    cliente.get("placa", ""),
                    cliente.get("telefone", ""),
                    cliente.get("valor_mensal", ""),
                    cliente.get("codigo_acesso", ""),
                    cliente.get("valor_hora", ""),
                ),
            )


class ControleWindow(tk.Toplevel):
    """Janela principal de operação do estacionamento para entrada e saída de veículos."""

    def __init__(self, parent: tk.Tk, app: "InterfaceEstacionamento") -> None:
        super().__init__(parent)
        self.app = app
        self.estacionamento = app.estacionamento
        self.title("Registro de entrada/saída")
        self.geometry("900x560")
        self.resizable(False, False)
        self.configure(bg="#0f172a")
        self.transient(parent)

        # Exibe o estado geral do estacionamento, como ocupação e vagas disponíveis.
        painel_frame = tk.LabelFrame(self, text="Painel de ocupação", bg="#111827", fg="#f8fafc", padx=12, pady=10, font=("Segoe UI", 11, "bold"))
        painel_frame.pack(fill="x", padx=18, pady=(16, 10))
        self.painel_var = tk.StringVar()
        tk.Label(painel_frame, textvariable=self.painel_var, fg="#f8fafc", bg="#111827", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(painel_frame, text="Tarifas: carro R$15, moto R$8", fg="#cbd5e1", bg="#111827", font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        # Área de operação para registrar a entrada e a saída do veículo.
        frame_mov = tk.LabelFrame(self, text="Controle de entrada e saída", bg="#111827", fg="#f8fafc", padx=12, pady=8, font=("Segoe UI", 11, "bold"))
        frame_mov.pack(fill="x", padx=18, pady=(0, 10))
        tk.Label(frame_mov, text="Placa:", fg="#e2e8f0", bg="#111827").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.placa_mov_var = tk.StringVar()
        self.entrada_placa = tk.Entry(
            frame_mov,
            textvariable=self.placa_mov_var,
            width=20,
            bg="#1f2937",
            fg="#f9fafb",
            insertbackground="#f9fafb",
            highlightthickness=2,
            highlightcolor="#38bdf8",
            highlightbackground="#334155",
        )
        self.entrada_placa.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_mov, text="Ex.: ABC1234 ou ABC1D23", fg="#94a3b8", bg="#111827", font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w", padx=5)
        tk.Button(frame_mov, text="Registrar entrada", command=self.registrar_entrada, width=18, bg="#10b981", fg="white", bd=0, relief="flat", pady=4).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(frame_mov, text="Registrar saída", command=self.registrar_saida, width=18, bg="#f59e0b", fg="white", bd=0, relief="flat", pady=4).grid(row=0, column=3, padx=5, pady=5)
        self.entrada_placa.bind("<KeyRelease>", self.sugerir_placa)
        self.entrada_placa.bind("<Return>", self.confirmar_movimento)
        self.entrada_placa.bind("<Escape>", self.limpar_placa)

        tk.Label(frame_mov, text="Forma de pagamento:", fg="#e2e8f0", bg="#111827").grid(row=1, column=0, sticky="w", padx=5, pady=(6, 2))
        self.forma_pagamento_var = tk.StringVar(value="pix")
        self.forma_pagamento_combo = ttk.Combobox(frame_mov, textvariable=self.forma_pagamento_var, values=["credito", "debito", "pix", "dinheiro"], state="readonly", width=16)
        self.forma_pagamento_combo.grid(row=1, column=1, sticky="w", padx=5, pady=(6, 2))
        self.valor_var = tk.StringVar(value="R$ 0,00")
        self.label_valor = tk.Label(frame_mov, textvariable=self.valor_var, fg="#fbbf24", bg="#111827", font=("Segoe UI", 10, "bold"))
        self.label_valor.grid(row=1, column=2, columnspan=2, sticky="w", padx=5, pady=(6, 2))
        self.forma_pagamento_combo.bind("<Return>", self.confirmar_movimento)

        # Lista os veículos que ainda estão presentes no estacionamento.
        frame_patio = tk.LabelFrame(self, text="Veículos no pátio", bg="#111827", fg="#f8fafc", padx=10, pady=10, font=("Segoe UI", 11, "bold"))
        frame_patio.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        self.lista_patio = tk.Listbox(frame_patio, bg="#1f2937", fg="#f9fafb", height=10)
        self.lista_patio.pack(fill="both", expand=True)

        self.atualizar_painel()
        self.atualizar_patio()
        self.previsualizar_valor()

    def sugerir_placa(self, _event=None) -> None:
        """Mostra uma sugestão de valor conforme a placa digitada e o estado do movimento."""
        texto = self.placa_mov_var.get().strip()
        if not texto:
            self.valor_var.set("R$ 0,00")
            self.label_valor.configure(fg="#fbbf24")
            return

        placa = self.estacionamento.normalizar_placa(texto)
        if not placa:
            self.valor_var.set("R$ 0,00")
            self.label_valor.configure(fg="#fbbf24")
            return

        movimento_ativo = None
        for movimento in self.estacionamento.movimentacoes:
            if movimento.get("status") == "ativo" and self.estacionamento.normalizar_placa(str(movimento.get("placa", ""))) == placa:
                movimento_ativo = movimento
                break

        if movimento_ativo is None:
            self.valor_var.set("R$ 0,00")
            self.label_valor.configure(fg="#fbbf24")
            return

        cliente = self.estacionamento.buscar_por_placa(placa)
        tipo_cliente = "cadastrado" if cliente is not None else "avulso"
        valor = 0.0 if tipo_cliente == "cadastrado" else float(self.estacionamento.obter_tarifa("carro") or 0.0)
        self.valor_var.set(f"Valor estimado: R$ {valor:.2f} | {tipo_cliente}")
        self.label_valor.configure(fg="#f59e0b")

    def previsualizar_valor(self) -> None:
        self.sugerir_placa()

    def confirmar_movimento(self, _event=None) -> None:
        """Decide automaticamente se deve registrar entrada ou saída a partir da placa informada."""
        placa = self.estacionamento.normalizar_placa(self.placa_mov_var.get().strip())
        if not placa:
            messagebox.showwarning("Atenção", "Informe a placa")
            return

        self.placa_mov_var.set(placa)
        movimento_ativo = None
        for movimento in self.estacionamento.listar_movimentacoes_ativas():
            if self.estacionamento.normalizar_placa(str(movimento.get("placa", ""))) == placa:
                movimento_ativo = movimento
                break

        if movimento_ativo is None:
            self.registrar_entrada()
        else:
            self.registrar_saida()

    def registrar_entrada(self) -> None:
        """Registra a entrada de um veículo e prepara o campo para a próxima operação."""
        try:
            placa = self.estacionamento.normalizar_placa(self.placa_mov_var.get().strip())
            self.placa_mov_var.set(placa)
            self.estacionamento.registrar_entrada(placa)
            self.estacionamento.salvar()
            self.placa_mov_var.set("")
            self.atualizar_painel()
            self.atualizar_patio()
            self.app.atualizar_janelas()
            self.after(50, self._focar_placa)
            messagebox.showinfo("Sucesso", "Entrada registrada")
        except ValueError as err:
            messagebox.showerror("Erro", str(err))

    def registrar_saida(self) -> None:
        """Registra a saída de um veículo, calcula o valor e grava a forma de pagamento."""
        try:
            placa = self.estacionamento.normalizar_placa(self.placa_mov_var.get().strip())
            self.placa_mov_var.set(placa)
            forma_pagamento = self.forma_pagamento_var.get()
            movimento = self.estacionamento.registrar_saida(placa, forma_pagamento=forma_pagamento)
            self.estacionamento.salvar()
            self.placa_mov_var.set("")
            self.atualizar_painel()
            self.atualizar_patio()
            self.app.atualizar_janelas()
            self.after(50, self._focar_placa)

            cliente = self.estacionamento.buscar_por_placa(placa)
            tipo_cliente = "cadastrado" if cliente is not None else "avulso"
            valor_total = movimento.get("valor_total", 0.0)
            self.valor_var.set(f"Valor: R$ {float(valor_total):.2f} | Pagamento: {forma_pagamento}")
            self.label_valor.configure(fg="#10b981")
            messagebox.showinfo("Sucesso", f"Saída registrada para {tipo_cliente} - valor total R$ {float(valor_total):.2f}")
        except ValueError as err:
            messagebox.showerror("Erro", str(err))

    def limpar_placa(self, _event=None) -> None:
        """Limpa o campo de placa e o prepara para a próxima digitação."""
        self.placa_mov_var.set("")
        self.valor_var.set("R$ 0,00")
        self.label_valor.configure(fg="#fbbf24")
        self._destacar_placa_pronta()
        self._focar_placa()

    def _destacar_placa_pronta(self) -> None:
        """Destaca visualmente o campo quando ele estiver vazio e pronto para uma nova placa."""
        if self.winfo_exists():
            self.entrada_placa.configure(highlightbackground="#22c55e", highlightcolor="#22c55e")

    def _focar_placa(self) -> None:
        """Retorna o foco ao campo de placa e seleciona o texto para digitação imediata."""
        if self.winfo_exists():
            self.entrada_placa.focus_set()
            self.entrada_placa.selection_clear()
            self.entrada_placa.icursor(tk.END)
            self.entrada_placa.select_range(0, tk.END)
            self.entrada_placa.configure(highlightbackground="#38bdf8", highlightcolor="#38bdf8")

    def atualizar_painel(self) -> None:
        """Atualiza os valores do painel de ocupação na tela."""
        painel = self.estacionamento.obter_painel_ocupacao()
        self.painel_var.set(f"Ocupadas: {painel['ocupadas']} | Livres: {painel['livres']} | Ocupação: {painel['percentual']}%")

    def atualizar_patio(self) -> None:
        """Atualiza a lista de veículos que ainda permanecem no pátio."""
        self.lista_patio.delete(0, tk.END)
        for movimento in self.estacionamento.listar_movimentacoes_ativas():
            cliente = self.estacionamento.buscar_por_placa(movimento.get("placa", ""))
            tipo = "cadastrado" if cliente is not None else "avulso"
            self.lista_patio.insert(tk.END, f"Placa: {movimento.get('placa')} | Entrada: {movimento.get('entrada')} | Tipo: {tipo}")


class UsuariosWindow(tk.Toplevel):
    """Janela administrativa para criação e listagem de usuários."""

    def __init__(self, parent: tk.Tk, app: "InterfaceEstacionamento") -> None:
        super().__init__(parent)
        self.app = app
        self.estacionamento = app.estacionamento
        self.title("Usuários cadastrados")
        self.geometry("520x460")
        self.resizable(False, False)
        self.configure(bg="#0f172a")
        self.transient(parent)

        frame_form = tk.LabelFrame(self, text="Novo usuário", bg="#111827", fg="#f8fafc", padx=12, pady=12, font=("Segoe UI", 11, "bold"))
        frame_form.pack(fill="x", padx=18, pady=(18, 10))

        tk.Label(frame_form, text="Usuário:", fg="#e2e8f0", bg="#111827").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.usuario_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.usuario_var, width=25, bg="#1f2937", fg="#f9fafb", insertbackground="#f9fafb").grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Senha:", fg="#e2e8f0", bg="#111827").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.senha_var = tk.StringVar()
        tk.Entry(frame_form, textvariable=self.senha_var, show="*", width=25, bg="#1f2937", fg="#f9fafb", insertbackground="#f9fafb").grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Perfil:", fg="#e2e8f0", bg="#111827").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.perfil_var = tk.StringVar(value="operador")
        ttk.Combobox(frame_form, textvariable=self.perfil_var, values=["administrador", "operador"], state="readonly", width=22).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(frame_form, text="Criar usuário", command=self.salvar_usuario, bg="#2563eb", fg="white", bd=0, relief="flat", padx=12, pady=5).grid(row=3, column=0, columnspan=2, pady=8)

        frame = tk.LabelFrame(self, text="Usuários cadastrados", bg="#111827", fg="#f8fafc", padx=12, pady=12, font=("Segoe UI", 11, "bold"))
        frame.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.tabela = ttk.Treeview(frame, columns=("usuario", "perfil"), show="headings")
        self.tabela.heading("usuario", text="Usuário")
        self.tabela.heading("perfil", text="Perfil")
        self.tabela.pack(fill="both", expand=True)
        self.atualizar_tabela()

    def salvar_usuario(self) -> None:
        """Cria um usuário e atualiza a lista após persistir os dados."""
        try:
            self.estacionamento.cadastrar_usuario(
                usuario=self.usuario_var.get(),
                senha=self.senha_var.get(),
                perfil=self.perfil_var.get(),
            )
            self.estacionamento.salvar()
            self.usuario_var.set("")
            self.senha_var.set("")
            self.atualizar_tabela()
            messagebox.showinfo("Sucesso", "Usuário criado com sucesso")
        except ValueError as err:
            messagebox.showerror("Erro", str(err))

    def atualizar_tabela(self) -> None:
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        for usuario in self.app.estacionamento.listar_usuarios():
            self.tabela.insert("", "end", values=(usuario.get("usuario", ""), usuario.get("perfil", "")))


class InterfaceEstacionamento:
    """Classe principal da interface gráfica do sistema de estacionamento."""

    def __init__(self, root: tk.Tk, usuario: str = "admin") -> None:
        self.root = root
        self.root.title("Sistema de Estacionamento")
        self.root.geometry("760x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f172a")

        # Instancia o núcleo do sistema com persistência em JSON.
        self.estacionamento = Estacionamento(storage_type="json")
        self.estacionamento.carregar()
        self.estacionamento.definir_tarifa("carro", 15.0)
        self.estacionamento.definir_tarifa("moto", 8.0)

        self.usuario = usuario
        self.perfil = self.estacionamento.obter_perfil_usuario(usuario) or "administrador"
        self.cadastro_window = None
        self.controle_window = None
        self.usuarios_window = None
        self.criar_interface()
        self.root.bind("<F11>", lambda _event: self.alternar_tela_cheia())

    def criar_interface(self) -> None:
        """Monta a tela inicial com navegação para cadastro e controle."""
        menu_bar = tk.Menu(self.root)
        menu_sessao = tk.Menu(menu_bar, tearoff=0)
        menu_sessao.add_command(label="Sair e trocar usuário", command=self.sair_para_login)
        menu_sessao.add_separator()
        menu_sessao.add_command(label="Sair do sistema", command=self.root.destroy)
        menu_bar.add_cascade(label="Sessão", menu=menu_sessao)
        self.root.configure(menu=menu_bar)

        header = tk.Frame(self.root, bg="#111827")
        header.pack(fill="x")
        tk.Label(header, text="Sistema de Estacionamento", fg="#f8fafc", bg="#111827", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=16)
        tk.Button(header, text="Tela cheia", command=self.alternar_tela_cheia, bg="#0f766e", fg="white", bd=0, relief="flat", padx=10, pady=5, font=("Segoe UI", 9, "bold")).pack(anchor="e", padx=20, pady=(0, 16))

        nav = tk.Frame(self.root, bg="#0f172a")
        nav.pack(fill="x", padx=18, pady=(0, 10))
        if self.perfil == "administrador":
            tk.Button(nav, text="Cadastro de clientes", command=self.abrir_cadastro, bg="#2563eb", fg="white", bd=0, relief="flat", padx=12, pady=6).pack(side="left")
        tk.Button(nav, text="Registro de entrada/saída", command=self.abrir_controle, bg="#10b981", fg="white", bd=0, relief="flat", padx=12, pady=6).pack(side="left", padx=(8, 0))
        if self.perfil == "administrador":
            tk.Button(nav, text="Usuários", command=self.abrir_usuarios, bg="#7c3aed", fg="white", bd=0, relief="flat", padx=12, pady=6).pack(side="left", padx=(8, 0))

        texto = "Bem-vindo(a)! Utilize o controle de entrada/saída para operar o estacionamento." if self.perfil == "operador" else "Abra uma das janelas para cadastrar clientes ou controlar entradas e saídas."
        tk.Label(self.root, text=texto, fg="#cbd5e1", bg="#0f172a", font=("Segoe UI", 10)).pack(pady=12)

    def alternar_tela_cheia(self) -> None:
        estado = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not estado)

    def sair_para_login(self) -> None:
        """Encerra a sessão atual e retorna à tela de autenticação."""
        for janela in (self.cadastro_window, self.controle_window, self.usuarios_window):
            if janela is not None and janela.winfo_exists():
                janela.destroy()

        self.root.configure(menu="")
        for widget in self.root.winfo_children():
            widget.destroy()
        TelaLogin(self.root, lambda usuario, senha: autenticar(usuario, senha, self.root))

    def abrir_cadastro(self) -> None:
        """Abre a janela de cadastro de clientes, se ainda não estiver aberta."""
        if self.cadastro_window is not None and self.cadastro_window.winfo_exists():
            self.cadastro_window.focus_set()
            return
        self.cadastro_window = CadastroWindow(self.root, self)

    def abrir_controle(self) -> None:
        """Abre a janela de controle de entrada e saída de veículos."""
        if self.controle_window is not None and self.controle_window.winfo_exists():
            self.controle_window.focus_set()
            self.controle_window.after(50, self.controle_window._focar_placa)
            return
        self.controle_window = ControleWindow(self.root, self)
        self.controle_window.after(100, self.controle_window._focar_placa)

    def abrir_usuarios(self) -> None:
        """Abre a janela de usuários cadastrados."""
        if self.perfil != "administrador":
            messagebox.showwarning("Acesso negado", "Apenas administradores podem gerenciar usuários")
            return
        if self.usuarios_window is not None and self.usuarios_window.winfo_exists():
            self.usuarios_window.focus_set()
            return
        self.usuarios_window = UsuariosWindow(self.root, self)

    def atualizar_janelas(self) -> None:
        """Atualiza as janelas abertas após qualquer alteração no estado do estacionamento."""
        if self.cadastro_window is not None and self.cadastro_window.winfo_exists():
            self.cadastro_window.atualizar_tabela()
        if self.controle_window is not None and self.controle_window.winfo_exists():
            self.controle_window.atualizar_painel()
            self.controle_window.atualizar_patio()


def main() -> None:
    """Ponto de entrada da aplicação gráfica."""
    root = tk.Tk()
    TelaLogin(root, lambda usuario, senha: autenticar(usuario, senha, root))
    root.mainloop()


def autenticar(usuario: str, senha: str, root: tk.Tk) -> bool:
    """Autentica o operador usando as credenciais do estacionamento."""
    estacionamento = Estacionamento(storage_type="json")
    if estacionamento.autenticar_usuario(usuario, senha):
        return True
    messagebox.showerror("Erro", "Usuário ou senha inválidos")
    return False


if __name__ == "__main__":
    main()
