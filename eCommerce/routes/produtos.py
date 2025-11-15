# Rotas de produtos
from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from models.produto_model import Produto
from forms.produto_forms import ProdutoForm, AdicionarCarrinhoForm
from utils.auth_utils import requer_autenticacao, get_cliente_autenticado, requer_admin

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@produtos_bp.route('/')
def listar():
    """Rota para listar todos os produtos"""
    page = request.args.get('page', 1, type=int)
    produtos = Produto.query.paginate(page=page, per_page=10)
    return render_template('produtos/listar.html', produtos=produtos)

@produtos_bp.route('/<int:produto_id>')
def detalhes(produto_id):
    """Rota para visualizar detalhes de um produto"""
    produto = Produto.query.get_or_404(produto_id)
    form = AdicionarCarrinhoForm()
    return render_template('produtos/detalhes.html', produto=produto, form=form)

@produtos_bp.route('/criar', methods=['GET', 'POST'])
@requer_autenticacao
@requer_admin
def criar():
    """Rota para criar novo produto (apenas admin)"""
    cliente = get_cliente_autenticado()
    if not cliente or cliente.role != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('produtos.listar'))
    
    form = ProdutoForm()
    if form.validate_on_submit():
        produto = Produto(
            nome=form.nome.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            estoque=form.estoque.data
        )
        db.session.add(produto)
        db.session.commit()
        
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('produtos.detalhes', produto_id=produto.id))
    
    return render_template('produtos/criar.html', form=form)

@produtos_bp.route('/<int:produto_id>/editar', methods=['GET', 'POST'])
@requer_autenticacao
def editar(produto_id):
    """Rota para editar um produto (apenas admin)"""
    cliente = get_cliente_autenticado()
    if not cliente or cliente.role != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('produtos.listar'))
    
    produto = Produto.query.get_or_404(produto_id)
    form = ProdutoForm()
    
    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.descricao = form.descricao.data
        produto.preco = form.preco.data
        produto.estoque = form.estoque.data
        
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produtos.detalhes', produto_id=produto.id))
    elif request.method == 'GET':
        form.nome.data = produto.nome
        form.descricao.data = produto.descricao
        form.preco.data = produto.preco
        form.estoque.data = produto.estoque
    
    return render_template('produtos/editar.html', form=form, produto=produto)

@produtos_bp.route('/<int:produto_id>/deletar', methods=['POST'])
@requer_autenticacao
def deletar(produto_id):
    """Rota para deletar um produto (apenas admin)"""
    cliente = get_cliente_autenticado()
    if not cliente or cliente.role != 'admin':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('produtos.listar'))
    
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('produtos.listar'))
