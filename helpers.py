# management.py

from sqlalchemy.exc import IntegrityError
from database import Session
from models import Product, Sale, Counter

ADMIN_PASSWORD = "admin123"
VALID_COUNTERS = ("counter1", "counter2")  # Example usernames

# Product Management Functions
def add_product(name, price, password):
    if password != ADMIN_PASSWORD:
        return "Incorrect admin password."

    session = Session()
    new_product = Product(name=name, price=price)
    session.add(new_product)
    try:
        session.commit()
        return f"Product {name} added."
    except IntegrityError:
        session.rollback()
        return "Error adding product."
    finally:
        session.close()

def delete_product(product_id, password):
    if password != ADMIN_PASSWORD:
        return "Incorrect admin password."

    session = Session()
    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        session.delete(product)
        session.commit()
        return f"Product ID {product_id} deleted."
    else:
        return "Product not found."
    
    session.close()

def view_products():
    session = Session()
    products = session.query(Product).all()
    session.close()
    
    if not products:
        return "No products found."
    else:
        return [f"ID: {product.id}, Name: {product.name}, Price: {product.price}" for product in products]

# Sale Management Functions
def add_sale(product_id, username):
    if username not in VALID_COUNTERS:
        return "Invalid counter username."

    session = Session()
    sale = Sale(product_id=product_id)

    # Check if the counter exists
    counter = session.query(Counter).filter_by(username=username).first()
    if not counter:
        counter = Counter(username=username)
        session.add(counter)

    sale.counter = counter
    session.add(sale)

    try:
        session.commit()
        return f"Sale for product ID {product_id} added by {username}."
    except IntegrityError:
        session.rollback()
        return "Error adding sale."
    finally:
        session.close()

def view_sales():
    session = Session()
    sales = session.query(Sale).all()
    session.close()
    
    if not sales:
        return "No sales found."
    else:
        return [f"Sale ID: {sale.id}, Product ID: {sale.product_id}, Counter ID: {sale.counter_id}" for sale in sales]

# Counter Management Functions
def add_counter(username, password):
    if password != ADMIN_PASSWORD:
        return "Incorrect admin password."

    session = Session()
    new_counter = Counter(username=username)
    session.add(new_counter)

    try:
        session.commit()
        return f"Counter {username} added."
    except IntegrityError:
        session.rollback()
        return "Error adding counter."
    finally:
        session.close()

def delete_counter(username, password):
    if password != ADMIN_PASSWORD:
        return "Incorrect admin password."

    session = Session()
    counter = session.query(Counter).filter_by(username=username).first()
    
    if counter:
        session.delete(counter)
        session.commit()
        return f"Counter {username} deleted."
    else:
        return "Counter not found."

    session.close()

def view_counters():
    session = Session()
    counters = session.query(Counter).all()
    session.close()

    if not counters:
        return "No counters found."
    else:
        return [f"ID: {counter.id}, Username: {counter.username}," for counter in counters]
