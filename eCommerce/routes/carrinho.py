# Rotas do carrinho de compras
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from extensions import db
from models.carrinho_model import Carrinho
from models.produto_model import Produto
from utils.carrinho_utils import (
    obter_carrinho_atual,
    adicionar_ao_carrinho,
    remover_do_carrinho,
    atualizar_quantidade_carrinho,
    calcular_total_carrinho,
    limpar_carrinho
)
from utils.auth_utils import get_cliente_autenticado, cliente_autenticado

carrinho_bp = Blueprint('carrinho', __name__, url_prefix='/carrinho')

@carrinho_bp.route('/')
def visualizar():
    """Rota para visualizar o carrinho"""

    items = obter_carrinho_atual()
    total = calcular_total_carrinho()
    
    return render_template('carrinho/visualizar.html', items=items, total=total)

@carrinho_bp.route('/adicionar/<int:produto_id>', methods=['POST'])
def adicionar(produto_id):
    """Rota para adicionar produto ao carrinho"""
    quantidade = request.form.get('quantidade', 1, type=int)
    if quantidade < 1:
        flash('A quantidade deve ser no mínimo 1.', 'danger')
        return redirect(url_for('produtos.listar'))
    
    sucesso, mensagem = adicionar_ao_carrinho(produto_id, quantidade)
    if sucesso:
        flash(mensagem, 'success')
    else:
        flash(mensagem, 'danger')
    
    referrer = request.referrer
    if referrer and 'produtos/' in referrer:
        return redirect(referrer)
        
    return redirect(url_for('produtos.listar'))

@carrinho_bp.route('/remover/<int:item_id>', methods=['POST'])
def remover(item_id):
    """Rota para remover item do carrinho"""
    
    obter_carrinho_atual()
    sucesso, mensagem = remover_do_carrinho(item_id)
    
    if sucesso:
        flash(mensagem, 'success')
    else:
        flash(mensagem, 'danger')
    
    return redirect(url_for('carrinho.visualizar'))

@carrinho_bp.route('/atualizar/<int:item_id>', methods=['POST'])
def atualizar(item_id):
    """Rota para atualizar quantidade no carrinho"""
    obter_carrinho_atual()
    
    quantidade = request.form.get('quantidade', 1, type=int)
    sucesso, mensagem = atualizar_quantidade_carrinho(item_id, quantidade)
    
    if sucesso:
        flash(mensagem, 'success')
    else:
        flash(mensagem, 'danger')
    
    return redirect(url_for('carrinho.visualizar'))

@carrinho_bp.route('/limpar', methods=['POST'])
def limpar():
    """Rota para limpar o carrinho"""
    if not cliente_autenticado():
        flash('Você precisa estar logado.', 'warning')
        return redirect(url_for('auth.login'))
    
    cliente = get_cliente_autenticado()
    limpar_carrinho(cliente.id)
    flash('Carrinho limpo com sucesso!', 'success')
    
    return redirect(url_for('carrinho.visualizar'))
