# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey 
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

"""
=================================================================
1. TABELA DE CLIENTES (clientes)
=================================================================
"""
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(256), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    senha_hash = Column(String(256), nullable=False)
    telefone = Column(String(256))
    
    def __repr__(self):
        return f'<Cliente {self.nome} - Email: {self.email}> - Telefone: {self.telefone}'


class Produto(db.Model):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(256), nullable=False)
    descricao = Column(String(256))
    preco = Column(db.Numeric(10,2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Produto {self.nome} - Preço: {self.preco} - Estoque: {self.estoque}>'

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    data = Column(db.Datatime, datetime.datetime.now)
    status = Column(String(256), default="pendente")

    def __repr__(self):
        return f'<Pedido {self.id} - Cliente {self.client_id} - Status {self.status}>'

class ItemPedido(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    tipo = Column(String(256))
    valor = Column(db.Numeric(10,2), nullable=False)
    status = Column(String(256), default="aguardando")

    def __repr__(self):
        return f'<ItemPedido {self.id} - Pedido {self.pedido_id} - Tipo {self.tipo} - Valor {self.valor}>'
    

class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    tipo = Column(String(256))
    valor = Column(db.Numeric(10,2), nullable=False)
    status = Column(String(256), default="aguardando")
    
    def __repr__(self):
        return f'<Pagamento {self.id} - Pedido {self.pedido_id} - Valor {self.valor} - Status {self.status}>'

class Carrinho(db.Model):
    __tablename__ = 'carrinhos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=True)
    produto_id = Column(Integer)
    nome_produto = Column(String(256))
    preco_unitario = Column(db.Numeric(10,2))
    quantidade = Column(Integer, nullable=False)
    criado_em = Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<Carrinho {self.id} - Cliente {self.cliente_id} - Produto {self.nome_produto} - Quantidade {self.quantidade}>'