# Rota da página inicial
from flask import Blueprint, render_template, request
from models.produto_model import Produto

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    """Rota para a página inicial com catálogo de produtos"""
    page = request.args.get('page', 1, type=int)
    produtos = Produto.query.paginate(page=page, per_page=12)
    return render_template('index.html', produtos=produtos)
