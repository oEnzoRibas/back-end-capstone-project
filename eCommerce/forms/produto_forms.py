from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

"""
Formulario para gerenciar produtos
"""
class ProdutoForm(FlaskForm):
    """Formulário para criar/editar produtos"""
    nome = StringField(
        'Nome do Produto', validators=[
            DataRequired(message='Nome é obrigatório'),
            Length(min=3, max=255, message='Nome deve ter entre 3 e 255 caracteres')
        ]
    )
    
    descricao = TextAreaField(
        'Descrição', validators=[
            Optional(),
            Length(max=1000, message='Descrição deve ter no máximo 1000 caracteres')
        ]
    )
    
    preco = FloatField(
        'Preço', validators=[
            DataRequired(message='Preço é obrigatório'),
            NumberRange(min=0.01, message='Preço deve ser maior que 0')
        ]
    )
    
    estoque = IntegerField(
        'Estoque', validators=[
            DataRequired(message='Estoque é obrigatório'),
            NumberRange(min=0, message='Estoque não pode ser negativo')
        ]
    )
    
    submit = SubmitField('Salvar Produto')


"""
Formulário para adicionar produto ao carrinho
"""
class AdicionarCarrinhoForm(FlaskForm):
    quantidade = IntegerField(
        'Quantidade', 
        validators=[
            DataRequired(message='Quantidade é obrigatória'),
            NumberRange(min=1, message='Quantidade deve ser no mínimo 1')
        ]
    )
    
    submit = SubmitField('Adicionar ao Carrinho')

"""
Formulário para atualizar quantidade no carrinho
"""
class AtualizarCarrinhoForm(FlaskForm):
    quantidade = IntegerField(
        'Quantidade', 
        validators=[
            DataRequired(message='Quantidade é obrigatória'),
            NumberRange(min=1, message='Quantidade deve ser no mínimo 1')
        ]
    )
    
    submit = SubmitField('Atualizar')
