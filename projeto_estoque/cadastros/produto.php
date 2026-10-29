<?php
include '../assets/conexao/conexao.php';
?>

<!DOCTYPE html>
<html lang="pt-br">

<head>
    <title></title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="css/style.css" rel="stylesheet">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@6.0.0-alpha.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-B/GM4XqrwHnWXNOWMbloTmrYXZg10cakYGmpfsR/bbzQ6JAJI4ihuyADKLnBgrCe" crossorigin="anonymous">
    <link href="https://cdn.datatables.net/v/bs5/dt-3.1.4/b-4.1.2/cc-2.1.2/date-2.1.2/datatables.min.css" rel="stylesheet" integrity="sha384-Opeaz2OZx+MFPau91bDMruHN/VB/WEnCSNaojnGS2ay4Rx3r5JtxklIp30uw4Yek" crossorigin="anonymous">
</head>

<body>
    <?php include '../navbar.php'; ?>
    <div class="container">
        <div class="row my-5">
            <div class="col-md-12 text-center">
                <h3>Cadastrar Produto</h3>
            </div>
        </div>

        <div class="row">
            <div class="col-md-12">
                <form class="form-horizontal" method="post" id="insert" action="../assets/insert/insert.php">
                    <input type="text" name="cadastro" value="1" hidden>
                    <div class="row">
                        <div class="md:col-6">
                            <label for="codigo" class="form-label">Código</label>
                            <input class="form-control" type="text" id="codigo" name="codigo" placeholder="Código do produto" aria-label="Código do produto" required>
                        </div>
                        <div class="md:col-6">
                            <label for="categoria" class="form-label">Categoria</label>
                            <select class="form-control" id="categoria" name="categoria" aria-label="Categoria do produto" required>
                                <option>Escolha uma categoria</option>
                                <?php
                                $nome_cat = $connection->query("SELECT id, nome  FROM categoria");
                                while ($row = $nome_cat->fetch_object()) {
                                    $id = $row->id;
                                    $nome = $row->nome;
                                    echo "<option value='$id'>$nome</option>";
                                };
                                ?>
                            </select>
                        </div>
                        <div class="col-md-12">
                            <label for="nome" class="form-label">Nome</label>
                            <input class="form-control" type="text" id="nome" name="nome" placeholder="Nome do produto" aria-label="Nome do produto" required>
                        </div>
                        <div class="md:col-6">
                            <label for="preco" class="form-label">Preço</label>
                            <input class="form-control" type="number" id="preco" name="preco" placeholder="Preço do produto" aria-label="Preço do produto" step="0.01">
                        </div>
                        <div class="md:col-6">
                            <label for="localizacao" class="form-label">Localização</label>
                            <input class="form-control" type="text" id="localizacao" name="localizacao" placeholder="Localização do produto" aria-label="Localização do produto">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12 my-5 text-center">
                            <button type="submit" class="btn-solid theme-primary">Cadastrar</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <div class="row my-5">
            <div class="col-md-12 text-center">
                <h4>Lista de Produtos</h4>
            </div>
        </div>

        <div class="row">
            <div class="col-md-12">
                <table id="table" class="table" cellspacing="1" data-order='[[ 2, "asc" ]]' data-page-length='25'>
                    <thead>
                        <tr>
                            <th>Código</th>
                            <th>Nome</th>
                            <th>Categoria</th>
                            <th>Preço Uni.</th>
                            <th>Localização</th>
                            <th>Deletar</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        $mysqli = $connection->query("SELECT p.id, p.codigo, p.nome, c.nome as categoria, p.preco, p.localizacao FROM produto p JOIN categoria c ON p.id_categoria = c.id");

                        // Joga os dados em uma Tabela
                        while ($row = $mysqli->fetch_object()) {
                            $id = $row->id;
                            $codigo = $row->codigo;
                            $nome = $row->nome;
                            $categoria = $row->categoria;
                            $preco = $row->preco;
                            $localizacao = $row->localizacao;

                            echo "<tr>
                            <td>$codigo</td>
                            <td>$nome</td>
                            <td>$categoria</td>
                            <td>$preco</td>
                            <td>$localizacao</td>
                            <td class='align-middle'><a class='btn btn-sm btn-danger center-block font-weight-bold' href='../assets/delete/delete.php?id=" . $id . "&cadastro=1' onclick=\"return confirm('Tem certeza que deseja DELETAR este registro?'); return false;\"><i class='fa-solid fa-trash' aria-hidden='true'></i> Deletar</a></td>
                            </tr>";
                        };
                        ?>
                    </tbody>
                </table>
            </div>
        </div>

        <script type="module" src="https://cdn.jsdelivr.net/npm/bootstrap@6.0.0-alpha.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-1a/pXj49ZQ1aHEmrJ+gMw1otqoVsYwlEnlD8mIfY2TV03r20Y0CN7uqx1tQogjPL" crossorigin="anonymous"></script>
        <script src="https://cdn.datatables.net/v/bs5/dt-3.1.4/b-4.1.2/cc-2.1.2/date-2.1.2/datatables.min.js" integrity="sha384-FcK6T4Qgydapgv5zFxhA+oVhE5yO1cQm3xB6KE+jsAheVYD3MQmrz8vEJkTqutgx" crossorigin="anonymous"></script>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                new DataTable('#table', {
                    language: {
                        url: 'https://cdn.datatables.net/plug-ins/3.1.4/i18n/pt-BR.json'
                    },
                    autoWidth: false,
                    scrollX: true
                });
            });
        </script>

</body>

</html>