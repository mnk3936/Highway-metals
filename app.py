# app.py
from flask import Flask, render_template
from flask_migrate import Migrate
from models import db
from flask_cors import CORS
import os
from dotenv import load_dotenv
import secrets
load_dotenv()

app = Flask(__name__)
DB_URL=os.getenv('DB_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(16))

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)  # ← This is critical for flask db commands

# Import blueprints AFTER app and db are created
from routes.raw_materials import raw_materials_bp
from routes.products import products_bp 
from routes.auth import auth_bp

# Register blueprints
app.register_blueprint(raw_materials_bp)
app.register_blueprint(products_bp)
app.register_blueprint(auth_bp)

# Frontend routes
@app.route('/')
def home():
    return render_template('home.html')  # ← New home page

@app.route('/admin')
def admin_panel():
    return render_template('admin.html')


@app.route('/products')
def product_catalog():
    return render_template('products.html')

if __name__ == '__main__':
    app.run(debug=True)
