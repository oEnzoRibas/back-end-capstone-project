# Funções auxiliares para carrinho de compras (Finalizadas)

from flask import session
from models.carrinho_model import Carrinho
from models.produto_model import Produto
from extensions import db 
from flask_login import current_user 
import uuid

SESSION_CART_KEY = 'temp_cart_id'


def get_cart_identifier():
    """
    Retorna o identificador do carrinho: cliente_id (logado) OU session_id (visitante).
    """
    if current_user.is_authenticated:
        return {'cliente_id': current_user.id, 'session_id': None}

    if SESSION_CART_KEY not in session:
        session[SESSION_CART_KEY] = str(uuid.uuid4())
        session.modified = True

    return {'cliente_id': None, 'session_id': session[SESSION_CART_KEY]}


def obter_carrinho_atual():
    """Obtém todos os itens do carrinho atual (logado ou visitante)"""
    ids = get_cart_identifier()
    
    if ids['cliente_id'] is not None:
        # Logado: filtra por cliente_id
        return Carrinho.query.filter_by(cliente_id=ids['cliente_id']).all()
    else:
        # Deslogado: filtra por session_id
        return Carrinho.query.filter_by(session_id=ids['session_id']).all()

def adicionar_ao_carrinho(produto_id, quantidade):
    """Adiciona um produto ao carrinho (suporta logado e deslogado)"""
    
    ids = get_cart_identifier()
    
    produto = Produto.query.get(produto_id)
    if not produto:
        return False, 'Produto não encontrado'
    if not produto.tem_estoque(quantidade):
        return False, f'Estoque insuficiente. Disponível: {produto.estoque}'
    
    query_base = Carrinho.query.filter_by(produto_id=produto_id)
    
    if ids['cliente_id'] is not None:
        item_carrinho = query_base.filter_by(cliente_id=ids['cliente_id']).first()
    else:
        item_carrinho = query_base.filter_by(session_id=ids['session_id']).first()
        
    if item_carrinho:
        item_carrinho.quantidade += quantidade
    else:
        item_carrinho = Carrinho(
            cliente_id=ids['cliente_id'],
            session_id=ids['session_id'],
            produto_id=produto_id,
            nome_produto=produto.nome,
            preco_unitario=produto.preco,
            quantidade=quantidade
        )
        db.session.add(item_carrinho)
    
    db.session.commit()
    return True, 'Produto adicionado ao carrinho'

def remover_do_carrinho(item_id):
    """Remove um item do carrinho, verificando a posse (logado ou visitante)"""
    ids = get_cart_identifier()
    
    item_query = Carrinho.query.filter_by(id=item_id)
    
    if ids['cliente_id'] is not None:
        item = item_query.filter_by(cliente_id=ids['cliente_id']).first()
    else:
        item = item_query.filter_by(session_id=ids['session_id']).first()

    if not item:
        return False, 'Item não encontrado no carrinho'
    
    db.session.delete(item)
    db.session.commit()
    return True, 'Item removido do carrinho'

def atualizar_quantidade_carrinho(item_id, quantidade):
    """
    Atualiza a quantidade de um item no carrinho.
    """
    if quantidade < 1:
        # Chama remover_do_carrinho sem passar cliente_id
        return remover_do_carrinho(item_id) 
    
    ids = get_cart_identifier()
    item_query = Carrinho.query.filter_by(id=item_id)

    if ids['cliente_id'] is not None:
        item = item_query.filter_by(cliente_id=ids['cliente_id']).first()
    else:
        item = item_query.filter_by(session_id=ids['session_id']).first()
    
    if not item:
        return False, 'Item não encontrado no carrinho'
    
    produto = Produto.query.get(item.produto_id)
    if not produto.tem_estoque(quantidade):
        return False, f'Estoque insuficiente. Disponível: {produto.estoque}'
    
    item.quantidade = quantidade
    db.session.commit()
    return True, 'Quantidade atualizada'

def limpar_carrinho():
    """
    Limpa o carrinho atual (logado ou visitante).
    """
    ids = get_cart_identifier()

    if ids['cliente_id'] is not None:
        Carrinho.query.filter_by(cliente_id=ids['cliente_id']).delete()
    else:
        Carrinho.query.filter_by(session_id=ids['session_id']).delete()

    db.session.commit()
    return True, 'Carrinho limpo com sucesso'


def calcular_total_carrinho():
    """
    Calcula o total do carrinho atual (logado ou visitante).
    """
    items = obter_carrinho_atual()
    # Assume que o modelo Carrinho tem o método calcular_subtotal()
    return sum(item.calcular_subtotal() for item in items)


def migrar_carrinho_visitante(cliente_id):
    """
    Move todos os itens do carrinho temporário (session_id) para o cliente recém-logado.
    Isto ocorre logo após um visitante fazer login com sucesso.
    """
    temp_session_id = session.get(SESSION_CART_KEY)

    if temp_session_id:
        itens_temporarios = Carrinho.query.filter_by(session_id=temp_session_id).all()
        
        for item in itens_temporarios:
            item_existente = Carrinho.query.filter_by(
                cliente_id=cliente_id,
                produto_id=item.produto_id
            ).first()
            
            if item_existente:
                item_existente.quantidade += item.quantidade
                db.session.delete(item)
            else:
                item.cliente_id = cliente_id
                item.session_id = None
        
        db.session.commit()
        
        session.pop(SESSION_CART_KEY, None)
        session.modified = True
        return True
    return False