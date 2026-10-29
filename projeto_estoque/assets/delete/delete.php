<?php
include '../conexao/conexao.php';

$cadastro = $_GET['cadastro'];

if ($cadastro == 1) {
    $id = $_GET['id'];

    $mysqli = $connection->query("DELETE FROM produto WHERE id='$id'");

    header("Location: ../../cadastros/produto.php");
} else if ($cadastro == 2) {
    $id = $_GET['id'];

    $mysqli = $connection->query("DELETE FROM categoria WHERE id='$id'");

    header("Location: ../../cadastros/categoria.php");
} else if ($cadastro == 3) {
    $id = $_GET['id'];

    $mysqli = $connection->query("DELETE FROM estoque WHERE id='$id'");

    header("Location: ../../estoque.php");
}
