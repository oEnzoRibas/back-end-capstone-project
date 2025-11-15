from sqlalchemy import Column, Integer, String, ForeignKey 
import datetime
from extensions import db

"""
=================================================================
3. TABELA DE PEDIDOS (pedidos)
=================================================================
"""
class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    data = Column(db.DateTime, default=datetime.datetime.now)
    status = Column(String(256), default="pendente")
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade='all, delete-orphan')
    pagamentos = db.relationship('Pagamento', backref='pedido', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Pedido {self.id} - Cliente {self.client_id} - Status {self.status}>'
    
    def atualizar_status(self, novo_status):
        """Atualiza o status do pedido."""
        self.status = novo_status

    def calcular_total(self):
        """Calcula o valor total do pedido somando os subtotais dos itens."""
        return sum(item.calcular_subtotal() for item in self.itens)
    
    
    
"""
4. TABELA DE ITENS DE PEDIDO (itens_pedido)
=================================================================
"""
class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10,2), nullable=False)
    produto = db.relationship('Produto', primaryjoin='ItemPedido.produto_id == Produto.id') 
    
    def __repr__(self):
        return f'<ItemPedido {self.id} - Pedido {self.pedido_id} - Produto {self.produto_id}>'
    
    def calcular_subtotal(self):
        """Calcula o valor total deste item."""
        return float(self.preco_unitario) * self.quantidade
    
