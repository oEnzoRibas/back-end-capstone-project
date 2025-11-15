# Rotas do carrinho de compras
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from extensions import db
from models.carrinho_model import Carrinho
from models.produto_model import Produto
from utils.carrinho_utils import (
    adicionar_ao_carrinho, remover_do_carrinho, 
    atualizar_quantidade_carrinho, obter_carrinho_cliente,
    calcular_total_carrinho, limpar_carrinho
)
from utils.auth_utils import get_cliente_autenticado, cliente_autenticado

carrinho_bp = Blueprint('carrinho', __name__, url_prefix='/carrinho')

@carrinho_bp.route('/')
def visualizar():
    """Rota para visualizar o carrinho"""
    if cliente_autenticado():
        cliente = get_cliente_autenticado()
        items = obter_carrinho_cliente(cliente.id)
        total = calcular_total_carrinho(cliente.id)
        
        flash(f'Total do carrinho: R$ {total:.2f}', 'info')
    else:
        flash(f'Carrinho vazio ou usuário não autenticado.', 'info')
        items = []
        total = 0
    
    return render_template('carrinho/visualizar.html', items=items, total=total)

@carrinho_bp.route('/adicionar/<int:produto_id>', methods=['POST'])
def adicionar(produto_id):
    """Rota para adicionar produto ao carrinho"""
    quantidade = request.form.get('quantidade', 1, type=int)
    
    if cliente_autenticado():
        cliente = get_cliente_autenticado()
        sucesso, mensagem = adicionar_ao_carrinho(produto_id, quantidade, cliente.id)
    else:
        sucesso, mensagem = adicionar_ao_carrinho(produto_id, quantidade, cliente_id=None)
    
    if sucesso:
        flash(mensagem, 'success')
    else:
        flash(mensagem, 'danger')
    
    referrer = request.referrer
    if referrer and 'produtos/detalhes' in referrer:
        return redirect(referrer)
    return redirect(url_for('produtos.listar'))

@carrinho_bp.route('/remover/<int:item_id>', methods=['POST'])
def remover(item_id):
    """Rota para remover item do carrinho"""
    if not cliente_autenticado():
        flash('Você precisa estar logado.', 'warning')
        return redirect(url_for('auth.login'))
    
    cliente = get_cliente_autenticado()
    sucesso, mensagem = remover_do_carrinho(item_id, cliente.id)
    
    if sucesso:
        flash(mensagem, 'success')
    else:
        flash(mensagem, 'danger')
    
    return redirect(url_for('carrinho.visualizar'))

@carrinho_bp.route('/atualizar/<int:item_id>', methods=['POST'])
def atualizar(item_id):
    """Rota para atualizar quantidade no carrinho"""
    if not cliente_autenticado():
        flash('Você precisa estar logado.', 'warning')
        return redirect(url_for('auth.login'))
    
    quantidade = request.form.get('quantidade', 1, type=int)
    cliente = get_cliente_autenticado()
    sucesso, mensagem = atualizar_quantidade_carrinho(item_id, quantidade, cliente.id)
    
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
