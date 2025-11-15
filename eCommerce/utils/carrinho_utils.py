# Funções auxiliares para carrinho de compras
from flask import session
from models.carrinho_model import Carrinho
from models.produto_model import Produto
from extensions import db

def obter_carrinho_sessao():
    """Obtém o carrinho armazenado na sessão"""
    return session.get('carrinho', [])

def salvar_carrinho_sessao(carrinho):
    """Salva o carrinho na sessão"""
    session['carrinho'] = carrinho
    session.modified = True

def adicionar_ao_carrinho(produto_id, quantidade, cliente_id=None):
    """Adiciona um produto ao carrinho"""
    produto = Produto.query.get(produto_id)
    
    if not produto:
        return False, 'Produto não encontrado'
    
    if not produto.tem_estoque(quantidade):
        return False, f'Estoque insuficiente. Disponível: {produto.estoque}'
    
    item_carrinho = Carrinho.query.filter_by(
        cliente_id=cliente_id,
        produto_id=produto_id
    ).first()
    
    if item_carrinho:
        item_carrinho.quantidade += quantidade
    else:
        item_carrinho = Carrinho(
            cliente_id=cliente_id,
            produto_id=produto_id,
            nome_produto=produto.nome,
            preco_unitario=produto.preco,
            quantidade=quantidade
        )
        db.session.add(item_carrinho)
    
    db.session.commit()
    return True, 'Produto adicionado ao carrinho'

def remover_do_carrinho(item_id, cliente_id=None):
    """Remove um item do carrinho"""
    item = Carrinho.query.filter_by(
        id=item_id,
        cliente_id=cliente_id
    ).first()
    
    if not item:
        return False, 'Item não encontrado no carrinho'
    
    db.session.delete(item)
    db.session.commit()
    return True, 'Item removido do carrinho'

def atualizar_quantidade_carrinho(item_id, quantidade, cliente_id=None):
    """Atualiza a quantidade de um item no carrinho"""
    if quantidade < 1:
        return remover_do_carrinho(item_id, cliente_id)
    
    item = Carrinho.query.filter_by(
        id=item_id,
        cliente_id=cliente_id
    ).first()
    
    if not item:
        return False, 'Item não encontrado no carrinho'
    
    produto = Produto.query.get(item.produto_id)
    if not produto.tem_estoque(quantidade):
        return False, f'Estoque insuficiente. Disponível: {produto.estoque}'
    
    item.quantidade = quantidade
    db.session.commit()
    return True, 'Quantidade atualizada'

def obter_carrinho_cliente(cliente_id):
    """Obtém todos os itens do carrinho de um cliente"""
    return Carrinho.query.filter_by(cliente_id=cliente_id).all()

def limpar_carrinho(cliente_id):
    """Limpa o carrinho de um cliente"""
    Carrinho.query.filter_by(cliente_id=cliente_id).delete()
    db.session.commit()

def calcular_total_carrinho(cliente_id):
    """Calcula o total do carrinho"""
    items = obter_carrinho_cliente(cliente_id)
    return sum(item.calcular_subtotal() for item in items)
