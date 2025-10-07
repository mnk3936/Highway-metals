# routes/raw_materials.py
from flask import Blueprint, request, jsonify, session
from models import db, RawMaterial
from pricing_algorithm import update_product_prices
from utils import admin_required  # ← Import from utils, not app

raw_materials_bp = Blueprint('raw_materials', __name__)

@raw_materials_bp.route('/api/raw-materials', methods=['GET'])
def get_all_materials():
    materials = RawMaterial.query.all()
    return jsonify([m.to_dict() for m in materials])

@raw_materials_bp.route('/api/raw-materials/<int:id>', methods=['GET'])
def get_material(id):
    material = RawMaterial.query.get_or_404(id)
    return jsonify(material.to_dict())

@raw_materials_bp.route('/api/raw-materials', methods=['POST'])
@admin_required
def create_material():
    data = request.get_json()
    material = RawMaterial(
        name=data['name'],
        current_price=data['current_price']
    )
    db.session.add(material)
    db.session.commit()
    return jsonify(material.to_dict()), 201

@raw_materials_bp.route('/api/raw-materials/<int:id>', methods=['PUT'])
@admin_required
def update_material(id):
    material = RawMaterial.query.get_or_404(id)
    data = request.get_json()
    
    old_price = material.current_price
    new_price = data.get('current_price', old_price)
    
    material.current_price = new_price
    
    updated_products = []
    if old_price != new_price:
        updated_products = update_product_prices(
            material.id, 
            old_price, 
            new_price,
            session.get('user_id')
        )
    
    db.session.commit()
    
    return jsonify({
        'material': material.to_dict(),
        'updated_products': updated_products
    })

@raw_materials_bp.route('/api/raw-materials/<int:id>', methods=['DELETE'])
@admin_required
def delete_material(id):
    material = RawMaterial.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    return jsonify({'message': 'Material deleted'}), 204
