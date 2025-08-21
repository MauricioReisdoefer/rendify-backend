from Routes import user_route
from flask import Flask
from Extras import db
from Routes import user_route, stock_routes, watchlist_routes

app = Flask(__name__)
app.register_blueprint(user_route.user_bp, url_prefix='/user')
app.register_blueprint(stock_routes.stock_bp, url_prefix='/stock')
app.register_blueprint(watchlist_routes.watchlist_bp, url_prefix='/watch')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.db.init_app(app)

from flask_cors import CORS
CORS(app)


with app.app_context():
    db.db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
