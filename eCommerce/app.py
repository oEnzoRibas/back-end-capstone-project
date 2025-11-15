import os
from flask import Flask
from config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='0.0.0.0')