# Rotas de cliente
from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from models.cliente_model import Cliente
from forms.auth_forms import AtualizarPerfilForm
from utils.auth_utils import requer_autenticacao, get_cliente_autenticado

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')

@cliente_bp.route('/perfil')
@requer_autenticacao
def perfil():
    """Rota para visualizar perfil do cliente"""
    cliente = get_cliente_autenticado()
    return render_template('cliente/perfil.html', cliente=cliente)

@cliente_bp.route('/perfil/editar', methods=['GET', 'POST'])
@requer_autenticacao
def editar_perfil():
    """Rota para editar perfil do cliente"""
    cliente = get_cliente_autenticado()
    form = AtualizarPerfilForm()
    
    if form.validate_on_submit():
        cliente.nome = form.nome.data
        cliente.email = form.email.data
        cliente.telefone = form.telefone.data
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('cliente.perfil'))
    elif request.method == 'GET':
        form.nome.data = cliente.nome
        form.email.data = cliente.email
        form.telefone.data = cliente.telefone
    
    return render_template('cliente/editar_perfil.html', form=form, cliente=cliente)
