from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

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
    role = Column(String(50), default='cliente')
    
    
    def __repr__(self):
        """
        Representação em string do objeto Cliente
        """
        return f'<Cliente {self.nome} - Email: {self.email}> - Telefone: {self.telefone}'
    
    def to_dict(self):
        """
        Converte o objeto para dicionário
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
        }
    
    def set_senha(self, senha):
        """
        Define a senha do cliente, armazenando o hash.
        """
        self.senha_hash = generate_password_hash(password=senha, salt_length=8)

    def verificar_senha(self, senha):
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.
        """
        return check_password_hash(self.senha_hash, senha)