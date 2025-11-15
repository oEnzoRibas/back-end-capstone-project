from sqlalchemy import Column, Integer, String
from extensions import db

"""
=================================================================
2. TABELA DE PRODUTOS (produtos)
=================================================================
"""
class Produto(db.Model):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(256), nullable=False)
    descricao = Column(String(256))
    preco = Column(db.Numeric(10,2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Produto {self.nome} - Preço: {self.preco} - Estoque: {self.estoque}>'
    
    def tem_estoque(self, quantidade):
        """Verifica se há estoque suficiente para a quantidade solicitada"""
        return self.estoque >= quantidade