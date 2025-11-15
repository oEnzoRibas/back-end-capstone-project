from sqlalchemy import Column, Integer, String, ForeignKey
from extensions import db

"""
=================================================================
5. TABELA DE PAGAMENTOS (pagamentos)
=================================================================
"""
class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    tipo = Column(String(256))
    valor = Column(db.Numeric(10,2), nullable=False)
    status = Column(String(256), default="aguardando")

    def __repr__(self):
        return f'<Pagamento {self.id} - Pedido {self.pedido_id} - Valor {self.valor} - Status {self.status}>'