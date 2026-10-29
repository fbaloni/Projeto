<?php
include 'assets/conexao/conexao.php';
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
    <?php include 'navbar.php'; ?>
    <div class="container">
        <div class="row my-5">
            <div class="col-md-12 text-center">
                <h3>Estoque Entrada / Saída</h3>
                <p>Movimentação de estoque</p>
            </div>
        </div>

        <div class="row">
            <div class="col-md-12">
                <form class="form-horizontal" method="post" id="insert" action="assets/insert/insert.php">
                    <input type="text" name="cadastro" value="3" hidden>
                    <div class="row">
                        <div class="col-md-12">
                            <label for="produto" class="form-label">Produto</label>
                            <select class="form-control" id="produto" name="produto" aria-label="Produto" required>
                                <option>Escolha um produto</option>
                                <?php
                                $nome_prod = $connection->query("SELECT id, nome  FROM produto");
                                while ($row = $nome_prod->fetch_object()) {
                                    $id = $row->id;
                                    $nome = $row->nome;
                                    echo "<option value='$id'>$nome</option>";
                                };
                                ?>
                            </select>
                        </div>
                        <div class="md:col-6">
                            <label for="tipo" class="form-label">Tipo</label>
                            <select class="form-control" id="tipo" name="tipo" aria-label="Tipo" required>
                                <option>Escolha um tipo</option>
                                <option value="entrada">Entrada</option>
                                <option value="saida">Saída</option>
                            </select>
                        </div>
                        <div class="md:col-6">
                            <label for="quantidade" class="form-label">Quantidade</label>
                            <input class="form-control" type="number" id="quantidade" name="quantidade" placeholder="Quantidade do produto" aria-label="Quantidade do produto" required>
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
                <h4>Lista de Entradas e Saídas</h4>
            </div>
        </div>

        <div class="row">
            <div class="col-md-12">
                <table id="table" class="table text-center" cellspacing="1" data-order='[[ 2, "asc" ]]' data-page-length='25'>
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Categoria</th>
                            <th>Quantidade</th>
                            <th>Movimento</th>
                            <th>Data</th>
                            <th>Deletar</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        $tabela = $connection->query("SELECT p.nome, c.nome as categoria, e.quantidade, e.data_movimento, e.tipo_movimento FROM estoque e JOIN produto p ON e.produto_id = p.id JOIN categoria c ON p.id_categoria = c.id");

                        // Joga os dados em uma Tabela
                        while ($row = $tabela->fetch_object()) {
                            $nome = $row->nome;
                            $categoria = $row->categoria;
                            $quantidade = $row->quantidade;
                            $data_movimento = $row->data_movimento;
                            $tipo_movimento = $row->tipo_movimento;

                            $data = date('d/m/Y H:m', strtotime($data_movimento));

                            echo "<tr>
                            <td>$nome</td>                            
                            <td>$categoria</td>
                            <td>$quantidade</td>
                            <td class='text-uppercase'>$tipo_movimento</td>
                            <td>$data</td>
                            <td class='align-middle'><a class='btn btn-sm btn-danger center-block font-weight-bold' href='assets/delete/delete.php?id=" . $id . "&cadastro=3' onclick=\"return confirm('Tem certeza que deseja DELETAR este registro?'); return false;\"><i class='fa-solid fa-trash' aria-hidden='true'></i> Deletar</a></td>                            
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