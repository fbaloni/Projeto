import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# Dados em memória: serão perdidos ao fechar o programa.
# Para manter os cadastros entre execuções, pode-se adicionar SQLite depois.
categorias = []
produtos = []       # [codigo, nome, categoria, quantidade]
movimentacoes = []  # [data_hora, codigo, nome, tipo, quantidade]


class SistemaEstoque:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Estoque")
        self.root.geometry("1000x650")
        self.root.minsize(820, 540)

        self.cor_menu = "#35205f"
        self.cor_destaque = "#6c45a3"
        self.cor_fundo = "#f4f2f8"
        self.root.configure(bg=self.cor_fundo)

        self._criar_estilos()
        self._criar_menu()
        self._criar_area_principal()
        self.mostrar_inicio()

    def _criar_estilos(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        estilo.configure("TLabel", font=("Segoe UI", 10))
        estilo.configure("TButton", font=("Segoe UI", 10), padding=6)
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 20, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 12, "bold"))

    def _criar_menu(self):
        menu_barra = tk.Menu(self.root)

        menu_cadastros = tk.Menu(menu_barra, tearoff=False)
        menu_cadastros.add_command(label="Categorias", command=self.tela_categorias)
        menu_cadastros.add_command(label="Produtos", command=self.tela_produtos)
        menu_barra.add_cascade(label="Cadastros", menu=menu_cadastros)

        menu_estoque = tk.Menu(menu_barra, tearoff=False)
        menu_estoque.add_command(label="Movimentar estoque", command=self.tela_movimentacao)
        menu_barra.add_cascade(label="Estoque", menu=menu_estoque)

        menu_consultas = tk.Menu(menu_barra, tearoff=False)
        menu_consultas.add_command(label="Consultar categorias", command=self.tela_categorias)
        menu_consultas.add_command(label="Consultar produtos", command=self.tela_produtos)
        menu_consultas.add_command(label="Relatório de movimentações", command=self.tela_relatorio)
        menu_barra.add_cascade(label="Consultas / Relatórios", menu=menu_consultas)

        menu_barra.add_command(label="Início", command=self.mostrar_inicio)
        menu_barra.add_command(label="Sair", command=self.root.destroy)
        self.root.config(menu=menu_barra)

    def _criar_area_principal(self):
        self.cabecalho = tk.Frame(self.root, bg=self.cor_menu, height=66)
        self.cabecalho.pack(fill="x")
        self.cabecalho.pack_propagate(False)
        tk.Label(
            self.cabecalho, text="📦  CONTROLE DE ESTOQUE",
            bg=self.cor_menu, fg="white", font=("Segoe UI", 17, "bold")
        ).pack(side="left", padx=22, pady=14)

        self.area = tk.Frame(self.root, bg=self.cor_fundo, padx=24, pady=22)
        self.area.pack(fill="both", expand=True)

        self.status = tk.StringVar(value="Sistema pronto")
        tk.Label(
            self.root, textvariable=self.status, anchor="w",
            bg="#e7e1ef", fg="#3b2a52", padx=12, pady=6
        ).pack(fill="x", side="bottom")

    def _limpar_area(self):
        for widget in self.area.winfo_children():
            widget.destroy()

    def _titulo(self, texto, descricao=None):
        ttk.Label(self.area, text=texto, style="Titulo.TLabel").pack(anchor="w", pady=(0, 5))
        if descricao:
            ttk.Label(self.area, text=descricao).pack(anchor="w", pady=(0, 18))

    def _botao(self, pai, texto, comando):
        return ttk.Button(pai, text=texto, command=comando)

    def mostrar_inicio(self):
        self._limpar_area()
        self._titulo("Bem-vindo!", "Selecione uma opção no menu superior ou nos atalhos abaixo.")
        atalhos = ttk.Frame(self.area)
        atalhos.pack(anchor="w", pady=18)

        opcoes = [
            ("Cadastrar categorias", self.tela_categorias),
            ("Cadastrar produtos", self.tela_produtos),
            ("Entrada / saída", self.tela_movimentacao),
            ("Relatório de movimentações", self.tela_relatorio),
        ]
        for i, (texto, comando) in enumerate(opcoes):
            botao = self._botao(atalhos, texto, comando)
            botao.grid(row=i // 2, column=i % 2, padx=(0, 12), pady=8, sticky="ew")
        atalhos.columnconfigure(0, weight=1)
        atalhos.columnconfigure(1, weight=1)

        resumo = ttk.LabelFrame(self.area, text="Resumo do estoque", padding=18)
        resumo.pack(fill="x", pady=20)
        total_itens = sum(p[3] for p in produtos)
        ttk.Label(resumo, text=f"Categorias cadastradas: {len(categorias)}").pack(anchor="w", pady=3)
        ttk.Label(resumo, text=f"Produtos cadastrados: {len(produtos)}").pack(anchor="w", pady=3)
        ttk.Label(resumo, text=f"Unidades em estoque: {total_itens}").pack(anchor="w", pady=3)
        self.status.set("Tela inicial")

    def tela_categorias(self):
        self._limpar_area()
        self._titulo("Cadastro de categorias", "Informe o nome de uma categoria e clique em Salvar.")
        formulario = ttk.LabelFrame(self.area, text="Nova categoria", padding=12)
        formulario.pack(fill="x", pady=(0, 16))

        ttk.Label(formulario, text="Nome da categoria:").grid(row=0, column=0, sticky="w", padx=(0, 8))
        nome_var = tk.StringVar()
        entrada = ttk.Entry(formulario, textvariable=nome_var, width=45)
        entrada.grid(row=0, column=1, sticky="ew", padx=4)
        formulario.columnconfigure(1, weight=1)

        tabela_frame = ttk.LabelFrame(self.area, text="Categorias cadastradas", padding=8)
        tabela_frame.pack(fill="both", expand=True)
        tabela = ttk.Treeview(tabela_frame, columns=("nome",), show="headings")
        tabela.heading("nome", text="Nome da categoria")
        tabela.column("nome", width=400)
        tabela.pack(fill="both", expand=True)

        def atualizar():
            tabela.delete(*tabela.get_children())
            for categoria in categorias:
                tabela.insert("", "end", values=(categoria,))

        def salvar():
            nome = nome_var.get().strip()
            if not nome:
                messagebox.showwarning("Campo obrigatório", "Digite o nome da categoria.")
                entrada.focus_set()
                return
            if any(c.casefold() == nome.casefold() for c in categorias):
                messagebox.showwarning("Categoria existente", "Essa categoria já está cadastrada.")
                return
            categorias.append(nome)
            nome_var.set("")
            atualizar()
            self.status.set(f"Categoria '{nome}' cadastrada")
            messagebox.showinfo("Sucesso", f"Categoria '{nome}' cadastrada.")
            entrada.focus_set()

        self._botao(formulario, "Salvar categoria", salvar).grid(row=0, column=2, padx=(8, 0))
        atualizar()
        entrada.focus_set()

    def tela_produtos(self):
        self._limpar_area()
        self._titulo("Cadastro de produtos", "Cadastre produtos vinculados a uma categoria existente.")
        formulario = ttk.LabelFrame(self.area, text="Dados do produto", padding=12)
        formulario.pack(fill="x", pady=(0, 16))

        codigo_var = tk.StringVar()
        nome_var = tk.StringVar()
        categoria_var = tk.StringVar()
        quantidade_var = tk.StringVar(value="0")

        campos = [
            ("Código:", codigo_var),
            ("Nome:", nome_var),
        ]
        for linha, (rotulo, variavel) in enumerate(campos):
            ttk.Label(formulario, text=rotulo).grid(row=linha, column=0, sticky="w", pady=5, padx=(0, 8))
            ttk.Entry(formulario, textvariable=variavel, width=32).grid(row=linha, column=1, sticky="ew", pady=5)

        ttk.Label(formulario, text="Categoria:").grid(row=0, column=2, sticky="w", padx=(18, 8))
        combo_categoria = ttk.Combobox(
            formulario, textvariable=categoria_var,
            values=categorias, state="readonly", width=28
        )
        combo_categoria.grid(row=0, column=3, sticky="ew", pady=5)

        ttk.Label(formulario, text="Quantidade inicial:").grid(row=1, column=2, sticky="w", padx=(18, 8))
        ttk.Entry(formulario, textvariable=quantidade_var, width=12).grid(row=1, column=3, sticky="w", pady=5)
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        tabela_frame = ttk.LabelFrame(self.area, text="Produtos cadastrados", padding=8)
        tabela_frame.pack(fill="both", expand=True)
        colunas = ("codigo", "nome", "categoria", "quantidade")
        tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")
        for col, titulo, largura in [
            ("codigo", "Código", 100), ("nome", "Produto", 330),
            ("categoria", "Categoria", 220), ("quantidade", "Estoque", 100)
        ]:
            tabela.heading(col, text=titulo)
            tabela.column(col, width=largura, anchor="w")
        tabela.pack(fill="both", expand=True)

        def atualizar():
            tabela.delete(*tabela.get_children())
            for p in produtos:
                tabela.insert("", "end", values=(p[0], p[1], p[2], p[3]))
            combo_categoria.configure(values=categorias)

        def salvar():
            codigo_texto = codigo_var.get().strip()
            nome = nome_var.get().strip()
            categoria = categoria_var.get().strip()
            try:
                codigo = int(codigo_texto)
                quantidade = int(quantidade_var.get().strip())
            except ValueError:
                messagebox.showwarning("Dados inválidos", "Código e quantidade devem ser números inteiros.")
                return
            if not nome or not categoria:
                messagebox.showwarning("Campos obrigatórios", "Preencha o nome e selecione uma categoria.")
                return
            if quantidade < 0:
                messagebox.showwarning("Quantidade inválida", "A quantidade inicial não pode ser negativa.")
                return
            if categoria not in categorias:
                messagebox.showwarning("Categoria não encontrada", "Cadastre a categoria antes do produto.")
                return
            if any(p[0] == codigo for p in produtos):
                messagebox.showwarning("Código existente", "Já existe um produto com esse código.")
                return

            produtos.append([codigo, nome, categoria, quantidade])
            if quantidade > 0:
                movimentacoes.append([
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    codigo, nome, "estoque inicial", quantidade
                ])
            codigo_var.set("")
            nome_var.set("")
            quantidade_var.set("0")
            categoria_var.set("")
            atualizar()
            self.status.set(f"Produto '{nome}' cadastrado")
            messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado.")

        self._botao(formulario, "Salvar produto", salvar).grid(row=2, column=3, sticky="e", pady=(8, 0))
        atualizar()

    def tela_movimentacao(self):
        self._limpar_area()
        self._titulo("Movimentação de estoque", "Registre entradas e saídas de produtos.")
        formulario = ttk.LabelFrame(self.area, text="Nova movimentação", padding=14)
        formulario.pack(fill="x", pady=(0, 16))

        produto_var = tk.StringVar()
        tipo_var = tk.StringVar(value="entrada")
        quantidade_var = tk.StringVar(value="1")

        ttk.Label(formulario, text="Produto:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        opcoes_produtos = [f"{p[0]} - {p[1]} (estoque: {p[3]})" for p in produtos]
        combo = ttk.Combobox(formulario, textvariable=produto_var, values=opcoes_produtos,
                             state="readonly", width=48)
        combo.grid(row=0, column=1, sticky="ew", pady=6)

        ttk.Label(formulario, text="Tipo:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Combobox(formulario, textvariable=tipo_var, values=("entrada", "saida"),
                     state="readonly", width=15).grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(formulario, text="Quantidade:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Entry(formulario, textvariable=quantidade_var, width=16).grid(row=2, column=1, sticky="w", pady=6)
        formulario.columnconfigure(1, weight=1)

        tabela_frame = ttk.LabelFrame(self.area, text="Estoque atual", padding=8)
        tabela_frame.pack(fill="both", expand=True)
        tabela = ttk.Treeview(tabela_frame, columns=("codigo", "nome", "estoque"), show="headings")
        for col, titulo, largura in [
            ("codigo", "Código", 100), ("nome", "Produto", 400), ("estoque", "Quantidade", 120)
        ]:
            tabela.heading(col, text=titulo)
            tabela.column(col, width=largura)
        tabela.pack(fill="both", expand=True)

        def atualizar():
            tabela.delete(*tabela.get_children())
            for p in produtos:
                tabela.insert("", "end", values=(p[0], p[1], p[3]))
            combo.configure(values=[f"{p[0]} - {p[1]} (estoque: {p[3]})" for p in produtos])

        def salvar_movimentacao():
            selecao = produto_var.get().strip()
            if not selecao:
                messagebox.showwarning("Produto obrigatório", "Cadastre e selecione um produto.")
                return
            try:
                quantidade = int(quantidade_var.get().strip())
            except ValueError:
                messagebox.showwarning("Quantidade inválida", "Informe uma quantidade inteira.")
                return
            if quantidade <= 0:
                messagebox.showwarning("Quantidade inválida", "A quantidade deve ser maior que zero.")
                return

            codigo = int(selecao.split(" - ", 1)[0])
            produto = next((p for p in produtos if p[0] == codigo), None)
            if produto is None:
                messagebox.showerror("Erro", "Produto não encontrado.")
                return

            tipo = tipo_var.get()
            if tipo == "saida" and produto[3] < quantidade:
                messagebox.showwarning(
                    "Estoque insuficiente",
                    f"Estoque disponível de {produto[1]}: {produto[3]} unidade(s)."
                )
                return

            if tipo == "entrada":
                produto[3] += quantidade
            else:
                produto[3] -= quantidade

            movimentacoes.append([
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                produto[0], produto[1], tipo, quantidade
            ])
            atualizar()
            produto_var.set("")
            quantidade_var.set("1")
            self.status.set(f"{tipo.capitalize()} de {quantidade} unidade(s): {produto[1]}")
            messagebox.showinfo("Movimentação registrada", f"{tipo.capitalize()} de {quantidade} unidade(s) registrada.")

        self._botao(formulario, "Registrar movimentação", salvar_movimentacao).grid(
            row=3, column=1, sticky="w", pady=(8, 0)
        )
        atualizar()

    def tela_relatorio(self):
        self._limpar_area()
        self._titulo("Relatório de movimentações", "Histórico de entradas, saídas e estoque inicial.")
        barra = ttk.Frame(self.area)
        barra.pack(fill="x", pady=(0, 10))
        ttk.Label(barra, text=f"Total de registros: {len(movimentacoes)}").pack(side="left")

        tabela_frame = ttk.Frame(self.area)
        tabela_frame.pack(fill="both", expand=True)
        colunas = ("data", "codigo", "nome", "tipo", "quantidade")
        tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")
        definicoes = [
            ("data", "Data e hora", 155), ("codigo", "Código", 85),
            ("nome", "Produto", 300), ("tipo", "Movimentação", 150),
            ("quantidade", "Quantidade", 100)
        ]
        for col, titulo, largura in definicoes:
            tabela.heading(col, text=titulo)
            tabela.column(col, width=largura)
        barra_scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=barra_scroll.set)
        tabela.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")

        for m in reversed(movimentacoes):
            tabela.insert("", "end", values=(m[0], m[1], m[2], m[3], m[4]))
        self.status.set("Relatório de movimentações")


def main():
    root = tk.Tk()
    SistemaEstoque(root)
    root.mainloop()


if __name__ == "__main__":
    main()
