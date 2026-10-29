<?php
include '../conexao/conexao.php';

$cadastro = $_POST['cadastro'];

if ($cadastro == 1) {
    $codigo = $_POST['codigo'];
    $nome = $_POST['nome'];
    $categoria = $_POST['categoria'];
    $preco = $_POST['preco'] ?? '';
    $localizacao = $_POST['localizacao'] ?? '';

    $mysqli = $connection->query("INSERT INTO produto SET codigo='$codigo', nome='$nome', id_categoria='$categoria', preco='$preco', localizacao='$localizacao'");

    header("Location: ../../cadastros/produto.php");
} else if ($cadastro == 2) {
    $nome = $_POST['nome'];

    $mysqli = $connection->query("INSERT INTO categoria SET nome='$nome'");

    header("Location: ../../cadastros/categoria.php");
} else if ($cadastro == 3) {
    $produto = $_POST['produto'];
    $tipo = $_POST['tipo'];
    $quantidade = $_POST['quantidade'];

    $mysqli = $connection->query("INSERT INTO estoque SET produto_id='$produto', tipo_movimento='$tipo', quantidade='$quantidade', data_movimento=NOW()");

    header("Location: ../../estoque.php");
}
