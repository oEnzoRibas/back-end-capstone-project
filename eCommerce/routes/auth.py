from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from extensions import db
from models.cliente_model import Cliente
from forms.auth_forms import RegistroForm, LoginForm, AtualizarPerfilForm
from utils.auth_utils import login_cliente, logout_cliente, get_cliente_autenticado, cliente_autenticado, requer_autenticacao

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """Rota para registro de novo cliente"""
    if cliente_autenticado():
        return redirect(url_for('produtos.listar'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        try:
            cliente = Cliente(
                nome=form.nome.data,
                email=form.email.data,
                telefone=form.telefone.data,
                role=form.role.data or 'cliente'
            )
            cliente.set_senha(form.senha.data)
            
            db.session.add(cliente)
            db.session.commit()
            
            flash('Registro realizado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro inesperado: {e}', 'danger')
            return render_template('auth/registrar.html', form=form)
        
    elif request.method == 'POST':
        flash('Por favor, corrija os erros no formulário.', 'danger')
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Erro em {field}: {error}', 'danger')
    
    return render_template('auth/registrar.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Rota para login de cliente"""
    if cliente_autenticado():
        return redirect(url_for('produtos.listar'))
    
    form = LoginForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(email=form.email.data).first()
        
        if cliente and cliente.verificar_senha(form.senha.data):
            login_cliente(cliente.id)
            flash(f'Bem-vindo, {cliente.nome}!', 'success')
            return redirect(url_for('produtos.listar'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    """Rota para logout"""
    logout_cliente()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/perfil')
@requer_autenticacao
def perfil():
    """Rota para visualizar perfil do cliente"""
    cliente = get_cliente_autenticado()
    return render_template('auth/perfil.html', cliente=cliente)

@auth_bp.route('/perfil/editar', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.perfil'))
    elif request.method == 'GET':
        form.nome.data = cliente.nome
        form.email.data = cliente.email
        form.telefone.data = cliente.telefone
    
    return render_template('auth/editar_perfil.html', form=form, cliente=cliente)
