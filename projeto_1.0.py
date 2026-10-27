#estrutura
categorias = []
produtos = []
movimentacoes = []

#cadastro
def cadastro_categorias(nome):
    if nome in categorias:
        print("Categoria ja existe")
    else:
        categorias.append(nome)
        print(f"Categoria '{nome}' cadastrada")

def cadastro_produtos(codigo, nome, categoria, quantidade=0):
    if categoria not in categorias:
        print("Categoria nao encontrada")
        return
    
    for p in produtos:
        if p[0] == codigo:
            print("Produto ja cadastrado")
            return
    
    produtos.append([codigo, nome, categoria, quantidade])
    print(f"Produto '{nome}' cadastrado")

#consulta
def consulta_produtos():
    print("Consulta produtos")

    for p in produtos:
        print (f"Codigo: {p[0]} Nome: {p[1]} Categoria: {p[2]} Estoque: {p[3]}")

def consulta_categorias():
    print("Consulta Categorias")

    for c in categorias:
        print(f"Categorias: {c}")

#movimentacao
def movimentacao_produto(codigo, tipo, quantidade):
    for p in produtos:
        if p[0] == codigo:
            if tipo == "entrada":
                p[3] += quantidade
            elif tipo == "saida":
                if p[3] < quantidade:
                    print ("Quantidade insulficiente")
                    return
                p[3] -= quantidade
            else:
                print("Tipo errado utilize 'entrada' ou 'saida' .")
                return

            movimentacoes.append([p[1], tipo, quantidade])
            print(f"{tipo} de {quantidade} de {p[1]} adicionado.")
            return
    print("Produto nao encontrado")

#relatorio
def relatorio():
    print("Relatorio - Movimentacoes")
    for m in movimentacoes:
        print(f"{m[1]} - {m[0]} - {m[2]}")

cadastro_categorias("Carregadores")
cadastro_categorias("Fonte")
cadastro_produtos(1001, "Carregador Samsung 15W", "Carregadores", 10)
cadastro_produtos(2001, "Fonte Corsair 800W 80 Plus", "Fonte", 8)

consulta_categorias()
consulta_produtos()

movimentacao_produto(1001, "entrada", 2)
movimentacao_produto(2001, "saida", 2)

consulta_produtos()
relatorio()
