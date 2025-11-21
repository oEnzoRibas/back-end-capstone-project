import os
from flask import Flask, render_template, request
from config import Config
from extensions import db, login_manager
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    def configure_logs():
        """Configura o sistema de logs para gravar em arquivo rotativo"""
        if not os.path.exists('logs'):
            os.makedirs('logs')

        log_path = os.path.join('logs', 'ecommerce.log')

        # 20 MB, 5 arquivos de backup
        handler = RotatingFileHandler(
            log_path, 
            maxBytes=20 * 1024 * 1024, 
            backupCount=5,
            encoding='utf-8'
        )

        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s em %(module)s: %(message)s'
        )

        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Aplicação inicializada e logs configurados.')

    configure_logs()

    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Cliente.query.get(int(user_id))

    with app.app_context():
        from models.cliente_model import Cliente
        from models.produto_model import Produto
        from models.pedido_model import Pedido, ItemPedido
        from models.pagamento_model import Pagamento
        from models.carrinho_model import Carrinho

        db.create_all()

        admin = Cliente.query.filter_by(email="master@ecommerce.com").first()
        if not admin:
            admin = Cliente(
                nome="master",
                email="master@ecommerce.com",
                telefone="123456789",
                role = "admin"
            )
            admin.set_senha("elson")
            db.session.add(admin)
            db.session.commit()

        # ----------------------------------------------------------------------
        # 🚨 INSERÇÃO DE PRODUTOS INICIAIS (10 PRODUTOS) 🚨
        # ----------------------------------------------------------------------
        if Produto.query.count() == 0:
            produtos_iniciais = [
                {'nome': 'Notebook Ultra', 'descricao': 'Laptop de alta performance para trabalho e jogos.', 'preco': 3800.00, 'estoque': 15},
                {'nome': 'Smartphone X20', 'descricao': 'Câmera profissional e bateria de longa duração.', 'preco': 1500.00, 'estoque': 30},
                {'nome': 'Mouse Sem Fio', 'descricao': 'Ergonômico e preciso, ideal para designers.', 'preco': 120.50, 'estoque': 50},
                {'nome': 'Teclado Mecânico RGB', 'descricao': 'Switches táteis para digitação rápida e responsiva.', 'preco': 350.99, 'estoque': 20},
                {'nome': 'Monitor 4K 27"', 'descricao': 'Cores vibrantes e taxa de atualização de 144Hz.', 'preco': 2100.00, 'estoque': 10},
                {'nome': 'Webcam HD Pro', 'descricao': 'Resolução Full HD para streaming e videoconferências.', 'preco': 180.00, 'estoque': 40},
                {'nome': 'Headset Gamer', 'descricao': 'Áudio imersivo 7.1 e microfone com cancelamento de ruído.', 'preco': 450.00, 'estoque': 25},
                {'nome': 'HD Externo 2TB', 'descricao': 'Armazenamento confiável para backup e arquivos grandes.', 'preco': 550.00, 'estoque': 35},
                {'nome': 'Câmera Mirrorless', 'descricao': 'Equipamento leve e potente para fotografia profissional.', 'preco': 5200.00, 'estoque': 5},
                {'nome': 'Mochila Antifurto', 'descricao': 'Design elegante e compartimento seguro para laptop.', 'preco': 299.90, 'estoque': 60},
            ]

            for dados in produtos_iniciais:
                novo_produto = Produto(**dados)
                db.session.add(novo_produto)
            
            db.session.commit() # Commita todos os produtos
            print(f"Banco de dados inicializado com {len(produtos_iniciais)} produtos de exemplo.")
        # ----------------------------------------------------------------------

        from routes.auth import auth_bp
        from routes.produtos import produtos_bp
        from routes.carrinho import carrinho_bp
        from routes.pedidos import pedidos_bp
        from routes.index import index_bp
        from routes.cliente import cliente_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(produtos_bp)
        app.register_blueprint(carrinho_bp)
        app.register_blueprint(pedidos_bp)
        app.register_blueprint(cliente_bp)
        app.register_blueprint(index_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        app.logger.warning(f"404 - Rota não encontrada: {request.path}")
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error(f"500 - Erro interno do servidor: {error}")
        return render_template('500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='0.0.0.0')