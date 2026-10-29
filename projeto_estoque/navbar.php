<nav class="navbar lg:navbar-expand bg-1 fg-2">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Estoque Empresa</a>
        <button class="btn-icon navbar-toggler" type="button" data-bs-toggle="drawer" data-bs-target="#navbarDrawer" aria-controls="navbarDrawer" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon" aria-hidden="true"></span>
        </button>
        <dialog class="drawer drawer-end" tabindex="-1" id="navbarDrawer" aria-labelledby="navbarDrawerLabel">
            <div class="drawer-header">
                <h5 class="drawer-title" id="navbarDrawerLabel">Menu</h5>
                <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
            </div>
            <div class="drawer-body mb-2 md:mb-0">
                <ul class="nav navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="http://localhost/projeto_estoque/index.php">Home</a>
                    </li>
                    <li class="nav-item">
                        <button class="nav-link" type="button" data-bs-toggle="menu" aria-expanded="false">
                            Cadastros
                        </button>
                        <div class="menu">
                            <a class="menu-item" href="http://localhost/projeto_estoque/cadastros/produto.php">Cadastrar Produto</a>
                            <a class="menu-item" href="http://localhost/projeto_estoque/cadastros/categoria.php">Cadastrar Categoria</a>
                        </div>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" aria-current="page" href="http://localhost/projeto_estoque/estoque.php">Estoque</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" aria-current="page" href="http://localhost/projeto_estoque/movimentacao.php">Relatório movimentação</a>
                    </li>
                </ul>
            </div>
        </dialog>
    </div>
</nav>