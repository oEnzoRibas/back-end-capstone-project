# Rotas de pedidos
from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from models.pedido_model import Pedido, ItemPedido
from models.pagamento_model import Pagamento
from models.produto_model import Produto
from forms.pagamento_forms import PagamentoForm
from utils.auth_utils import requer_autenticacao, get_cliente_autenticado
from utils.carrinho_utils import obter_carrinho_cliente, calcular_total_carrinho, limpar_carrinho
from datetime import datetime

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@pedidos_bp.route('/')
@requer_autenticacao
def listar():
    """Rota para listar pedidos do cliente"""
    cliente = get_cliente_autenticado()
    page = request.args.get('page', 1, type=int)
    pedidos = Pedido.query.filter_by(cliente_id=cliente.id).paginate(page=page, per_page=10)
    return render_template('pedidos/listar.html', pedidos=pedidos)

@pedidos_bp.route('/<int:pedido_id>')
@requer_autenticacao
def detalhes(pedido_id):
    """Rota para visualizar detalhes de um pedido"""
    cliente = get_cliente_autenticado()
    pedido = Pedido.query.get_or_404(pedido_id)
    
    # Verifica se o pedido pertence ao cliente
    if pedido.cliente_id != cliente.id:
        flash('Você não tem permissão para acessar este pedido.', 'danger')
        return redirect(url_for('pedidos.listar'))
    
    return render_template('pedidos/detalhes.html', pedido=pedido)

@pedidos_bp.route('/criar', methods=['GET', 'POST'])
@requer_autenticacao
def criar():
    """Rota para criar novo pedido a partir do carrinho"""
    cliente = get_cliente_autenticado()
    items_carrinho = obter_carrinho_cliente(cliente.id)
    
    if not items_carrinho:
        flash('Seu carrinho está vazio.', 'warning')
        return redirect(url_for('carrinho.visualizar'))
    
    form = PagamentoForm()
    
    if form.validate_on_submit():
        try:
            # Cria novo pedido
            pedido = Pedido(cliente_id=cliente.id)
            db.session.add(pedido)
            db.session.flush()  # Para obter o ID do pedido
            
            # Adiciona itens ao pedido e atualiza estoque
            total_pedido = 0
            for item_carrinho in items_carrinho:
                produto = Produto.query.get(item_carrinho.produto_id)
                
                # Verifica estoque novamente
                if not produto.tem_estoque(item_carrinho.quantidade):
                    db.session.rollback()
                    flash(f'Estoque insuficiente para {produto.nome}', 'danger')
                    return redirect(url_for('carrinho.visualizar'))
                
                # Cria item do pedido
                item_pedido = ItemPedido(
                    pedido_id=pedido.id,
                    produto_id=produto.id,
                    quantidade=item_carrinho.quantidade,
                    preco_unitario=item_carrinho.preco_unitario
                )
                db.session.add(item_pedido)
                
                # Reduz estoque
                produto.reduzir_estoque(item_carrinho.quantidade)
                
                total_pedido += item_pedido.calcular_subtotal()
            
            # Cria pagamento
            pagamento = Pagamento(
                pedido_id=pedido.id,
                tipo=form.tipo_pagamento.data,
                valor=total_pedido
            )
            db.session.add(pagamento)
            
            # Limpa carrinho
            limpar_carrinho(cliente.id)
            
            # Confirma transação
            db.session.commit()
            
            flash('Pedido criado com sucesso! Aguardando confirmação de pagamento.', 'success')
            return redirect(url_for('pedidos.detalhes', pedido_id=pedido.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar pedido: {str(e)}', 'danger')
            return redirect(url_for('carrinho.visualizar'))
    
    total = calcular_total_carrinho(cliente.id)
    return render_template('pedidos/criar.html', form=form, items=items_carrinho, total=total)

@pedidos_bp.route('/<int:pedido_id>/confirmar-pagamento', methods=['POST'])
@requer_autenticacao
def confirmar_pagamento(pedido_id):
    """Rota para confirmar pagamento de um pedido"""
    cliente = get_cliente_autenticado()
    pedido = Pedido.query.get_or_404(pedido_id)
    
    # Verifica se o pedido pertence ao cliente
    if pedido.cliente_id != cliente.id:
        flash('Você não tem permissão para acessar este pedido.', 'danger')
        return redirect(url_for('pedidos.listar'))
    
    if pedido.pagamento:
        pedido.pagamento.confirmar_pagamento()
        pedido.atualizar_status('confirmado')
        db.session.commit()
        flash('Pagamento confirmado com sucesso!', 'success')
    
    return redirect(url_for('pedidos.detalhes', pedido_id=pedido.id))

@pedidos_bp.route('/<int:pedido_id>/cancelar', methods=['POST'])
@requer_autenticacao
def cancelar(pedido_id):
    """Rota para cancelar um pedido"""
    cliente = get_cliente_autenticado()
    pedido = Pedido.query.get_or_404(pedido_id)
    
    # Verifica se o pedido pertence ao cliente
    if pedido.cliente_id != cliente.id:
        flash('Você não tem permissão para acessar este pedido.', 'danger')
        return redirect(url_for('pedidos.listar'))
    
    # Verifica se o pedido pode ser cancelado
    if pedido.status not in ['pendente', 'confirmado']:
        flash('Este pedido não pode ser cancelado.', 'danger')
        return redirect(url_for('pedidos.detalhes', pedido_id=pedido.id))
    
    # Restaura estoque
    for item in pedido.itens:
        produto = Produto.query.get(item.produto_id)
        produto.aumentar_estoque(item.quantidade)
    
    # Atualiza status
    pedido.atualizar_status('cancelado')
    if pedido.pagamento:
        pedido.pagamento.cancelar_pagamento()
    
    db.session.commit()
    flash('Pedido cancelado com sucesso!', 'success')
    
    return redirect(url_for('pedidos.listar'))
