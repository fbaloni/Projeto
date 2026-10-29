create database estoque_empresa;

use estoque_empresa;

create table categoria (
    id int primary key auto_increment,
    nome varchar(50) not null
);

create table produto (
    id int primary key auto_increment,
    codigo varchar(50) not null,
    id_categoria int not null,
    nome varchar(100) not null,
    quantidade int not null,
    preco decimal(10, 2),
    localizacao varchar(100),
    foreign key (id_categoria) references categoria(id)
);

create table estoque(
    id int primary key auto_increment,
    produto_id int not null,
    quantidade int not null,
    data_movimento datetime not null,
    tipo_movimento enum('entrada', 'saida') not null,
    foreign key (produto_id) references produto(id)
);