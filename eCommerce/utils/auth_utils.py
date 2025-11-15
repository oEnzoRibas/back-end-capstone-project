# Funções auxiliares de autenticação
from flask import session, redirect, url_for
from functools import wraps
from models.cliente_model import Cliente

def login_cliente(cliente_id):
    """Faz login de um cliente na sessão"""
    session['cliente_id'] = cliente_id
    session['cliente_autenticado'] = True
    session['cliente_role'] = Cliente.query.get(cliente_id).role

def logout_cliente():
    """Faz logout do cliente"""
    session.pop('cliente_id', None)
    session.pop('cliente_autenticado', None)
    session.pop('cliente_role', None)

def get_cliente_autenticado():
    """Retorna o cliente autenticado ou None"""
    cliente_id = session.get('cliente_id')
    if cliente_id:
        return Cliente.query.get(cliente_id)
    return None

def cliente_autenticado():
    """Verifica se há um cliente autenticado"""
    return session.get('cliente_autenticado', False)

def requer_autenticacao(f):
    """Decorator para rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not cliente_autenticado():
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def requer_admin(f):
    """Decorator para rotas que requerem acesso de admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        cliente = get_cliente_autenticado()
        if not cliente or cliente.role != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
