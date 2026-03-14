from datetime import datetime
from typing import Optional

class Produto:
    def __init__(self, codigo: Optional[int] = None, nome: str = "", preco: float = 0.0, 
                 quantidade_estoque: int = 0, categoria: str = "", fornecedor: str = ""):
        self.codigo = codigo
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.categoria = categoria
        self.fornecedor = fornecedor
    
    def calcular_valor_total_estoque(self) -> float:
        return self.preco * self.quantidade_estoque
    
    def verificar_disponibilidade(self, quantidade_desejada: int) -> bool:
        return self.quantidade_estoque >= quantidade_desejada
    
    def atualizar_estoque(self, quantidade: int, operacao: str = "adicionar"):
        if operacao == "adicionar":
            self.quantidade_estoque += quantidade
        elif operacao == "remover":
            if self.verificar_disponibilidade(quantidade):
                self.quantidade_estoque -= quantidade
                return True
            return False
    
    def aplicar_desconto(self, percentual: float) -> float:
        return self.preco * (1 - percentual / 100)
    
    def formatar_preco(self) -> str:
        return f"R$ {self.preco:.2f}"
    
    def to_dict(self) -> dict:
        return {
            'codigo': self.codigo,
            'nome': self.nome,
            'preco': self.preco,
            'quantidade_estoque': self.quantidade_estoque,
            'categoria': self.categoria,
            'fornecedor': self.fornecedor
        }


class Cliente:
    def __init__(self, codigo: Optional[int] = None, nome: str = "", cpf: str = "", 
                 email: str = "", telefone: str = "", endereco: str = ""):
        self.codigo = codigo
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.endereco = endereco
        self.data_cadastro = datetime.now()
    
    
    def obter_primeiro_nome(self) -> str:
        return self.nome.split()[0] if self.nome else ""
    
    def to_dict(self) -> dict:
        return {
            'codigo': self.codigo,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco
        }


class ItemVenda:
    def __init__(self, produto: Produto, quantidade: int, preco_unitario: float):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
    
    def calcular_subtotal(self) -> float:
        return self.quantidade * self.preco_unitario
    
    def aplicar_desconto_item(self, percentual: float) -> float:
        subtotal = self.calcular_subtotal()
        return subtotal * (1 - percentual / 100)


class Venda:
    def __init__(self, codigo: Optional[int] = None, cliente: Optional[Cliente] = None):
        self.codigo = codigo
        self.cliente = cliente
        self.itens = []
        self.data_venda = datetime.now()
        self.forma_pagamento = ""
        self.desconto_total = 0.0
        self.status = "pendente"
    
    def adicionar_item(self, produto: Produto, quantidade: int, preco_unitario: Optional[float] = None):
        if preco_unitario is None:
            preco_unitario = produto.preco
        
        if produto.verificar_disponibilidade(quantidade):
            item = ItemVenda(produto, quantidade, preco_unitario)
            self.itens.append(item)
            return True
        return False
    
    def remover_item(self, indice: int):
        if 0 <= indice < len(self.itens):
            self.itens.pop(indice)
            return True
        return False
    
    def calcular_total(self) -> float:
        total = sum(item.calcular_subtotal() for item in self.itens)
        return total * (1 - self.desconto_total / 100)
    
    def calcular_total_itens(self) -> int:
        return sum(item.quantidade for item in self.itens)
    
    def aplicar_desconto_geral(self, percentual: float):
        self.desconto_total = percentual
    
    def finalizar_venda(self, forma_pagamento: str) -> bool:
        if not self.itens:
            return False
        
        for item in self.itens:
            if not item.produto.atualizar_estoque(item.quantidade, "remover"):
                return False
        
        self.forma_pagamento = forma_pagamento
        self.status = "concluida"
        return True
    
    def cancelar_venda(self):
        if self.status == "concluida":
            for item in self.itens:
                item.produto.atualizar_estoque(item.quantidade, "adicionar")
        
        self.status = "cancelada"
    
    def obter_resumo(self) -> dict:
        return {
            'codigo': self.codigo,
            'cliente': self.cliente.nome if self.cliente else "Cliente não identificado",
            'data': self.data_venda.strftime('%d/%m/%Y %H:%M'),
            'total_itens': self.calcular_total_itens(),
            'valor_total': self.calcular_total(),
            'forma_pagamento': self.forma_pagamento,
            'status': self.status
        }