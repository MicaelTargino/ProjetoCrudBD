SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;

CREATE DATABASE IF NOT EXISTS supermercado_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE supermercado_db;

ALTER DATABASE supermercado_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS produtos (
    codigo INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    quantidade_estoque INT NOT NULL DEFAULT 0,
    categoria VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    fornecedor VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    INDEX idx_nome (nome),
    INDEX idx_categoria (categoria),
    INDEX idx_fornecedor (fornecedor)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS clientes (
    codigo INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    email VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    telefone VARCHAR(20),
    endereco VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nome (nome),
    INDEX idx_cpf (cpf)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS vendas (
    codigo INT AUTO_INCREMENT PRIMARY KEY,
    codigo_cliente INT,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    forma_pagamento VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    desconto_total DECIMAL(5, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pendente',
    FOREIGN KEY (codigo_cliente) REFERENCES clientes(codigo) ON DELETE SET NULL,
    INDEX idx_data_venda (data_venda),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS itens_venda (
    codigo INT AUTO_INCREMENT PRIMARY KEY,
    codigo_venda INT NOT NULL,
    codigo_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (codigo_venda) REFERENCES vendas(codigo) ON DELETE CASCADE,
    FOREIGN KEY (codigo_produto) REFERENCES produtos(codigo) ON DELETE RESTRICT,
    INDEX idx_venda (codigo_venda),
    INDEX idx_produto (codigo_produto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
DELETE FROM produtos;
INSERT INTO produtos (nome, preco, quantidade_estoque, categoria, fornecedor) VALUES
('Arroz Branco 5kg', 25.90, 100, 'Alimentos', 'Fornecedor ABC'),
('Feijão Preto 1kg', 8.50, 150, 'Alimentos', 'Fornecedor ABC'),
('Óleo de Soja 900ml', 6.90, 200, 'Alimentos', 'Indústria XYZ'),
('Açúcar Cristal 1kg', 4.50, 180, 'Alimentos', 'Usina Doce'),
('Café em Pó 500g', 18.90, 80, 'Bebidas', 'Torrefadora Sul'),
('Leite Integral 1L', 5.90, 120, 'Laticínios', 'Fazenda Feliz'),
('Macarrão Espaguete 500g', 3.90, 250, 'Alimentos', 'Massas Brasil'),
('Molho de Tomate 340g', 2.50, 300, 'Alimentos', 'Indústria XYZ'),
('Sabonete em Barra', 2.20, 400, 'Higiene', 'Clean Corp'),
('Detergente Líquido 500ml', 2.90, 350, 'Limpeza', 'Clean Corp'),
('Papel Higiênico 4 rolos', 12.90, 150, 'Higiene', 'Paper Plus'),
('Água Mineral 1,5L', 3.50, 200, 'Bebidas', 'Fonte Natural'),
('Biscoito Recheado 140g', 3.20, 180, 'Alimentos', 'Biscoitos Top'),
('Refrigerante 2L', 7.90, 100, 'Bebidas', 'Bebidas Sul'),
('Creme Dental 90g', 5.50, 250, 'Higiene', 'Clean Corp');
DELETE FROM clientes;
INSERT INTO clientes (nome, cpf, email, telefone, endereco) VALUES
('João Silva', '123.456.789-01', 'joao@email.com', '(11) 98765-4321', 'Rua A, 123'),
('Maria Santos', '987.654.321-02', 'maria@email.com', '(11) 91234-5678', 'Av. B, 456'),
('Pedro Oliveira', '456.789.123-03', 'pedro@email.com', '(11) 95555-5555', 'Rua C, 789'),
('Ana Costa', '789.123.456-04', 'ana@email.com', '(11) 96666-6666', 'Av. D, 321'),
('Carlos Lima', '321.654.987-05', 'carlos@email.com', '(11) 97777-7777', 'Rua E, 654');