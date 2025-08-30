from flask import Flask
from Extras.db import db
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from Routes.user_routes import user_bp
from Routes.stock_routes import stock_bp
from Routes.watchlist_routes import watchlist_bp
from Routes.simulator_routes import simulator_bp

app.register_blueprint(user_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(watchlist_bp)
app.register_blueprint(simulator_bp)

db.init_app(app)

from flask_cors import CORS
CORS(app)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
