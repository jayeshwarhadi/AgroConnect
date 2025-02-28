from flask import Flask , session
from routes.auth import auth
from routes.seller import seller_bp
from routes.public import public
from routes.admin import admin_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.secret_key = "admin123"

app.register_blueprint(auth)
app.register_blueprint(seller_bp)
app.register_blueprint(public)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
