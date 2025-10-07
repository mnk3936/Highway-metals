# routes/products.py
from flask import Blueprint, request, jsonify
from models import db, Product
from utils import admin_required  # ← Import from utils, not app

products_bp = Blueprint('products', __name__)

@products_bp.route('/api/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@products_bp.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@products_bp.route('/api/products', methods=['POST'])
@admin_required
def create_product():
    data = request.get_json()
    product = Product(
        name=data['name'],
        raw_material_id=data['raw_material_id'],
        base_price=data['base_price'],
        coefficient=data.get('coefficient', 1.0),
        current_price=data['base_price'],
        category=data.get('category')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@products_bp.route('/api/products/<int:id>', methods=['PUT'])
@admin_required
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    product.name = data.get('name', product.name)
    product.coefficient = data.get('coefficient', product.coefficient)
    product.category = data.get('category', product.category)
    
    db.session.commit()
    return jsonify(product.to_dict())

@products_bp.route('/api/products/<int:id>', methods=['DELETE'])
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 204
