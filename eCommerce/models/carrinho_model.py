from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey 
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from extensions import db

"""
=================================================================
6. TABELA DE CARRINHO (carrinhos)
=================================================================
"""
class Carrinho(db.Model):
    __tablename__ = 'carrinhos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    session_id = db.Column(db.String(36), nullable=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=True)
    produto_id = Column(Integer)
    nome_produto = Column(String(256))
    preco_unitario = Column(db.Numeric(10,2))
    quantidade = Column(Integer, nullable=False)
    criado_em = Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<Carrinho {self.id} - Cliente {self.cliente_id} - Produto {self.nome_produto} - Quantidade {self.quantidade}>'
    
    def calcular_subtotal(self):
        """Calcula o total do item no carrinho"""
        return self.preco_unitario * self.quantidade