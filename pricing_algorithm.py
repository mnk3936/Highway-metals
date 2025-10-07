# pricing_algorithm.py
from models import db, Product, PriceHistory

def update_product_prices(material_id, old_price, new_price, user_id=None):
    """
    Updates all product prices when raw material price changes.
    Formula: new_product_price = base_price * (1 + coefficient * ((new_raw_price - old_raw_price) / old_raw_price))
    """
    if old_price == 0:
        raise ValueError("Old price cannot be zero")
    
    # Calculate percentage change
    price_change_ratio = (new_price - old_price) / old_price
    
    # Get all products linked to this material
    products = Product.query.filter_by(raw_material_id=material_id).all()
    
    updated_products = []
    for product in products:
        # Calculate new price using proportional formula
        price_adjustment = product.base_price * product.coefficient * price_change_ratio
        product.current_price = product.base_price + price_adjustment
        
        updated_products.append({
            'id': product.id,
            'name': product.name,
            'old_price': product.base_price,
            'new_price': product.current_price
        })
    
    # Log the change in history
    history_entry = PriceHistory(
        material_id=material_id,
        old_price=old_price,
        new_price=new_price,
        changed_by=user_id
    )
    db.session.add(history_entry)
    db.session.commit()
    
    return updated_products
