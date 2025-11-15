from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TelField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from wtforms.validators import Email
from models.cliente_model import Cliente

class LoginForm(FlaskForm):
    nome = StringField('nome', validators=[DataRequired(), Length(min=3, max=256)])
    senha = StringField('senha', validators=[DataRequired(), Length(min=3, max=256)])


"""
Formulário de registro de novo cliente
"""
class RegistroForm(FlaskForm):
    
    nome = StringField(
        'Nome', 
        validators=[
            DataRequired(message='Nome é obrigatório'),
            Length(min=3, max=255, message='Nome deve ter entre 3 e 255 caracteres')
        ]
    )
    
    email = StringField(
        'Email', 
        validators=[
            DataRequired(message='Email é obrigatório'),
            Email(message='Email inválido')
        ]
    )
    
    telefone = TelField(
        'Telefone', 
        validators=[
            Length(max=20, message='Telefone deve ter no máximo 20 caracteres')
        ]
    )
    
    role = SelectField(
        'Role', 
        default="cliente", 
        choices=[('cliente', 'Cliente'), ('admin', 'Administrador')],
        validators=[
            Optional()
        ]
    )

    senha = PasswordField(
        'Senha', validators=[
            DataRequired(message='Senha é obrigatória'),
            Length(min=6, message='Senha deve ter no mínimo 6 caracteres')
        ]
    )
    
    confirmar_senha = PasswordField(
        'Confirmar Senha', 
        validators=[
            DataRequired(message='Confirmação de senha é obrigatória'),
            EqualTo('senha', message='As senhas não correspondem')
        ]
    )

    
    submit = SubmitField('Registrar')


"""
Formulário de login
"""
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        Email(message='Email inválido')
    ])
    
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])
    
    submit = SubmitField('Entrar')

"""
Formulário para atualizar perfil do cliente
"""
class AtualizarPerfilForm(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=255, message='Nome deve ter entre 3 e 255 caracteres')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    
    telefone = TelField('Telefone', validators=[
        Length(max=20, message='Telefone deve ter no máximo 20 caracteres')
    ])
    
    submit = SubmitField('Atualizar')
    
    def validate_email(self, field):
        """Valida se o email já existe (exceto o do usuário atual)"""
        cliente = Cliente.query.filter_by(email=field.data).first()
        if cliente and cliente.id != self.cliente_id:
            raise ValidationError('Este email já está cadastrado')
