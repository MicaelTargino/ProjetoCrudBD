from typing import List, Optional, Dict, Any
from conexao_bd import ConexaoBD
from modelos import Produto, Cliente, Venda, ItemVenda
from datetime import datetime

class GerenciadorProdutos:
    def __init__(self, conexao: ConexaoBD):
        self.conexao = conexao
    
    def inserir(self, produto: Produto) -> Optional[int]:
        query = """
            INSERT INTO produtos (nome, preco, quantidade_estoque, categoria, fornecedor)
            VALUES (%s, %s, %s, %s, %s)
        """
        parametros = (
            produto.nome,
            produto.preco,
            produto.quantidade_estoque,
            produto.categoria,
            produto.fornecedor
        )
        
        codigo = self.conexao.executar_insert(query, parametros)
        if codigo:
            produto.codigo = codigo
        return codigo
    
    def alterar(self, produto: Produto) -> bool:
        query = """
            UPDATE produtos
            SET nome = %s, preco = %s, quantidade_estoque = %s, 
                categoria = %s, fornecedor = %s
            WHERE codigo = %s
        """
        parametros = (
            produto.nome,
            produto.preco,
            produto.quantidade_estoque,
            produto.categoria,
            produto.fornecedor,
            produto.codigo
        )
        
        linhas_afetadas = self.conexao.executar_update(query, parametros)
        return linhas_afetadas > 0
    
    def pesquisar_por_nome(self, nome: str) -> List[Produto]:
        query = "SELECT * FROM produtos WHERE nome LIKE %s"
        parametros = (f"%{nome}%",)
        
        resultados = self.conexao.executar_query(query, parametros)
        return self._converter_para_produtos(resultados)
    
    def remover(self, codigo: int) -> bool:
        query = "DELETE FROM produtos WHERE codigo = %s"
        parametros = (codigo,)
        
        linhas_afetadas = self.conexao.executar_delete(query, parametros)
        return linhas_afetadas > 0
    
    def listar_todos(self) -> List[Produto]:
        query = "SELECT * FROM produtos ORDER BY nome"
        
        resultados = self.conexao.executar_query(query)
        return self._converter_para_produtos(resultados)
    
    def exibir_um(self, codigo: int) -> Optional[Produto]:
        query = "SELECT * FROM produtos WHERE codigo = %s"
        parametros = (codigo,)
        
        resultados = self.conexao.executar_query(query, parametros)
        produtos = self._converter_para_produtos(resultados)
        return produtos[0] if produtos else None
    
    def buscar_por_categoria(self, categoria: str) -> List[Produto]:
        query = "SELECT * FROM produtos WHERE categoria = %s ORDER BY nome"
        parametros = (categoria,)
        
        resultados = self.conexao.executar_query(query, parametros)
        return self._converter_para_produtos(resultados)
    
    def buscar_por_fornecedor(self, fornecedor: str) -> List[Produto]:
        query = "SELECT * FROM produtos WHERE fornecedor LIKE %s ORDER BY nome"
        parametros = (f"%{fornecedor}%",)
        
        resultados = self.conexao.executar_query(query, parametros)
        return self._converter_para_produtos(resultados)
    
    def atualizar_estoque(self, codigo: int, quantidade: int, operacao: str = "adicionar") -> bool:
        produto = self.exibir_um(codigo)
        if not produto:
            return False
        
        if operacao == "adicionar":
            nova_quantidade = produto.quantidade_estoque + quantidade
        elif operacao == "remover":
            if produto.quantidade_estoque < quantidade:
                return False
            nova_quantidade = produto.quantidade_estoque - quantidade
        else:
            return False
        
        query = "UPDATE produtos SET quantidade_estoque = %s WHERE codigo = %s"
        parametros = (nova_quantidade, codigo)
        
        linhas_afetadas = self.conexao.executar_update(query, parametros)
        return linhas_afetadas > 0
    
    def obter_produtos_em_falta(self, quantidade_minima: int = 10) -> List[Produto]:
        query = "SELECT * FROM produtos WHERE quantidade_estoque < %s ORDER BY quantidade_estoque"
        parametros = (quantidade_minima,)
        
        resultados = self.conexao.executar_query(query, parametros)
        return self._converter_para_produtos(resultados)
    
    def _converter_para_produtos(self, resultados: List[Dict]) -> List[Produto]:
        produtos = []
        if resultados:
            for resultado in resultados:
                produto = Produto(
                    codigo=resultado['codigo'],
                    nome=resultado['nome'],
                    preco=float(resultado['preco']),
                    quantidade_estoque=resultado['quantidade_estoque'],
                    categoria=resultado['categoria'],
                    fornecedor=resultado['fornecedor']
                )
                produtos.append(produto)
        return produtos


class GerenciadorClientes:
    def __init__(self, conexao: ConexaoBD):
        self.conexao = conexao
    
    def inserir(self, cliente: Cliente) -> Optional[int]:
        query = """
            INSERT INTO clientes (nome, cpf, email, telefone, endereco)
            VALUES (%s, %s, %s, %s, %s)
        """
        parametros = (
            cliente.nome,
            cliente.cpf,
            cliente.email,
            cliente.telefone,
            cliente.endereco
        )
        
        codigo = self.conexao.executar_insert(query, parametros)
        if codigo:
            cliente.codigo = codigo
        return codigo
    
    def alterar(self, cliente: Cliente) -> bool:
        query = """
            UPDATE clientes
            SET nome = %s, cpf = %s, email = %s, telefone = %s, endereco = %s
            WHERE codigo = %s
        """
        parametros = (
            cliente.nome,
            cliente.cpf,
            cliente.email,
            cliente.telefone,
            cliente.endereco,
            cliente.codigo
        )
        
        linhas_afetadas = self.conexao.executar_update(query, parametros)
        return linhas_afetadas > 0
    
    def pesquisar_por_nome(self, nome: str) -> List[Cliente]:
        query = "SELECT * FROM clientes WHERE nome LIKE %s"
        parametros = (f"%{nome}%",)
        
        resultados = self.conexao.executar_query(query, parametros)
        return self._converter_para_clientes(resultados)
    
    def remover(self, codigo: int) -> bool:
        query = "DELETE FROM clientes WHERE codigo = %s"
        parametros = (codigo,)
        
        linhas_afetadas = self.conexao.executar_delete(query, parametros)
        return linhas_afetadas > 0
    
    def listar_todos(self) -> List[Cliente]:
        query = "SELECT * FROM clientes ORDER BY nome"
        
        resultados = self.conexao.executar_query(query)
        return self._converter_para_clientes(resultados)
    
    def exibir_um(self, codigo: int) -> Optional[Cliente]:
        query = "SELECT * FROM clientes WHERE codigo = %s"
        parametros = (codigo,)
        
        resultados = self.conexao.executar_query(query, parametros)
        clientes = self._converter_para_clientes(resultados)
        return clientes[0] if clientes else None
    
    def buscar_por_cpf(self, cpf: str) -> Optional[Cliente]:
        query = "SELECT * FROM clientes WHERE cpf = %s"
        parametros = (cpf,)
        
        resultados = self.conexao.executar_query(query, parametros)
        clientes = self._converter_para_clientes(resultados)
        return clientes[0] if clientes else None
    
    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        query = "SELECT * FROM clientes WHERE email = %s"
        parametros = (email,)
        
        resultados = self.conexao.executar_query(query, parametros)
        clientes = self._converter_para_clientes(resultados)
        return clientes[0] if clientes else None
    
    def verificar_cpf_existe(self, cpf: str, excluir_codigo: Optional[int] = None) -> bool:
        if excluir_codigo:
            query = "SELECT COUNT(*) as total FROM clientes WHERE cpf = %s AND codigo != %s"
            parametros = (cpf, excluir_codigo)
        else:
            query = "SELECT COUNT(*) as total FROM clientes WHERE cpf = %s"
            parametros = (cpf,)
        
        resultado = self.conexao.executar_query(query, parametros)
        return resultado[0]['total'] > 0 if resultado else False
    
    def _converter_para_clientes(self, resultados: List[Dict]) -> List[Cliente]:
        clientes = []
        if resultados:
            for resultado in resultados:
                cliente = Cliente(
                    codigo=resultado['codigo'],
                    nome=resultado['nome'],
                    cpf=resultado['cpf'],
                    email=resultado['email'],
                    telefone=resultado['telefone'],
                    endereco=resultado['endereco']
                )
                clientes.append(cliente)
        return clientes


class GerenciadorVendas:
    def __init__(self, conexao: ConexaoBD):
        self.conexao = conexao
        self.gerenciador_produtos = GerenciadorProdutos(conexao)
        self.gerenciador_clientes = GerenciadorClientes(conexao)
    
    def inserir(self, venda: Venda) -> Optional[int]:
        try:
            self.conexao.iniciar_transacao()
            
            query_venda = """
                INSERT INTO vendas (codigo_cliente, data_venda, forma_pagamento, desconto_total, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            parametros_venda = (
                venda.cliente.codigo if venda.cliente else None,
                venda.data_venda,
                venda.forma_pagamento,
                venda.desconto_total,
                venda.status
            )
            
            codigo_venda = self.conexao.executar_insert(query_venda, parametros_venda)
            if not codigo_venda:
                self.conexao.reverter_transacao()
                return None
            
            venda.codigo = codigo_venda
            
            for item in venda.itens:
                query_item = """
                    INSERT INTO itens_venda (codigo_venda, codigo_produto, quantidade, preco_unitario)
                    VALUES (%s, %s, %s, %s)
                """
                parametros_item = (
                    codigo_venda,
                    item.produto.codigo,
                    item.quantidade,
                    item.preco_unitario
                )
                self.conexao.executar_insert(query_item, parametros_item)
                
                self.gerenciador_produtos.atualizar_estoque(
                    item.produto.codigo, 
                    item.quantidade, 
                    "remover"
                )
            
            self.conexao.confirmar_transacao()
            return codigo_venda
            
        except Exception as e:
            self.conexao.reverter_transacao()
            print(f"Erro ao inserir venda: {e}")
            return None
    
    def exibir_um(self, codigo: int) -> Optional[Dict]:
        query_venda = """
            SELECT v.*, c.nome as nome_cliente
            FROM vendas v
            LEFT JOIN clientes c ON v.codigo_cliente = c.codigo
            WHERE v.codigo = %s
        """
        parametros = (codigo,)
        
        resultado_venda = self.conexao.executar_query(query_venda, parametros)
        if not resultado_venda:
            return None
        
        venda_dict = resultado_venda[0]
        
        query_itens = """
            SELECT iv.*, p.nome as nome_produto
            FROM itens_venda iv
            JOIN produtos p ON iv.codigo_produto = p.codigo
            WHERE iv.codigo_venda = %s
        """
        
        itens = self.conexao.executar_query(query_itens, parametros)
        venda_dict['itens'] = itens
        
        return venda_dict
    
    def listar_todos(self) -> List[Dict]:
        query = """
            SELECT v.*, c.nome as nome_cliente,
                   (SELECT SUM(iv.quantidade * iv.preco_unitario)
                    FROM itens_venda iv
                    WHERE iv.codigo_venda = v.codigo) as total
            FROM vendas v
            LEFT JOIN clientes c ON v.codigo_cliente = c.codigo
            ORDER BY v.data_venda DESC
        """
        
        return self.conexao.executar_query(query)
    
    def buscar_por_cliente(self, codigo_cliente: int) -> List[Dict]:
        query = """
            SELECT v.*, 
                   (SELECT SUM(iv.quantidade * iv.preco_unitario)
                    FROM itens_venda iv
                    WHERE iv.codigo_venda = v.codigo) as total
            FROM vendas v
            WHERE v.codigo_cliente = %s
            ORDER BY v.data_venda DESC
        """
        parametros = (codigo_cliente,)
        
        return self.conexao.executar_query(query, parametros)
    
    def buscar_por_periodo(self, data_inicio: datetime, data_fim: datetime) -> List[Dict]:
        query = """
            SELECT v.*, c.nome as nome_cliente,
                   (SELECT SUM(iv.quantidade * iv.preco_unitario)
                    FROM itens_venda iv
                    WHERE iv.codigo_venda = v.codigo) as total
            FROM vendas v
            LEFT JOIN clientes c ON v.codigo_cliente = c.codigo
            WHERE v.data_venda BETWEEN %s AND %s
            ORDER BY v.data_venda DESC
        """
        parametros = (data_inicio, data_fim)
        
        return self.conexao.executar_query(query, parametros)
    
    def cancelar_venda(self, codigo: int) -> bool:
        try:
            self.conexao.iniciar_transacao()
            
            venda = self.exibir_um(codigo)
            if not venda or venda['status'] == 'cancelada':
                self.conexao.reverter_transacao()
                return False
            
            for item in venda['itens']:
                self.gerenciador_produtos.atualizar_estoque(
                    item['codigo_produto'],
                    item['quantidade'],
                    "adicionar"
                )
            
            query = "UPDATE vendas SET status = 'cancelada' WHERE codigo = %s"
            parametros = (codigo,)
            self.conexao.executar_update(query, parametros)
            
            self.conexao.confirmar_transacao()
            return True
            
        except Exception as e:
            self.conexao.reverter_transacao()
            print(f"Erro ao cancelar venda: {e}")
            return False
    
    def obter_total_vendas_dia(self, data: datetime) -> Dict[str, Any]:
        query = """
            SELECT COUNT(*) as quantidade_vendas,
                   COALESCE(SUM(
                       (SELECT SUM(iv.quantidade * iv.preco_unitario)
                        FROM itens_venda iv
                        WHERE iv.codigo_venda = v.codigo)
                   ), 0) as total_vendido
            FROM vendas v
            WHERE DATE(v.data_venda) = DATE(%s) AND v.status = 'concluida'
        """
        parametros = (data,)
        
        resultado = self.conexao.executar_query(query, parametros)
        return resultado[0] if resultado else {'quantidade_vendas': 0, 'total_vendido': 0}