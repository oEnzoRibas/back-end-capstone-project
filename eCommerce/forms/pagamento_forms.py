from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

"""
Formulário para pagamento
"""
class PagamentoForm(FlaskForm):
    tipo_pagamento = SelectField(
        'Tipo de Pagamento', 
        choices=[
            ('cartao', 'Cartão de Crédito'),
            ('pix', 'PIX'),
            ('boleto', 'Boleto Bancário')
    ], 
    validators=[
        DataRequired(message='Selecione um tipo de pagamento')
        ]
    )
    
    submit = SubmitField('Confirmar Pagamento')

