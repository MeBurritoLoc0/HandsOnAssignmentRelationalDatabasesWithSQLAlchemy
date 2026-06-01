from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# -------------------------
# Part 1: Setup
# -------------------------
engine = create_engine('sqlite:///shop.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# -------------------------
# Part 2: Define Tables
# -------------------------

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    orders = relationship("Order", back_populates="user")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    orders = relationship("Order", back_populates="product")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    # Bonus (optional)
    status = Column(Boolean, default=False)

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")


# -------------------------
# Part 3: Create Tables
# -------------------------
Base.metadata.create_all(engine)

# Clear old data so the script can be run multiple times
session.query(Order).delete()
session.query(Product).delete()
session.query(User).delete()
session.commit()
# -------------------------
# Part 4: Insert Data
# -------------------------

# Users
user1 = User(name="Alice", email="alice@example.com")
user2 = User(name="Bob", email="bob@example.com")

# Products
product1 = Product(name="Laptop", price=1000)
product2 = Product(name="Phone", price=500)
product3 = Product(name="Headphones", price=100)

# Orders
order1 = Order(user=user1, product=product1, quantity=1)
order2 = Order(user=user1, product=product2, quantity=2)
order3 = Order(user=user2, product=product3, quantity=3)
order4 = Order(user=user2, product=product1, quantity=1)

session.add_all([
    user1, user2,
    product1, product2, product3,
    order1, order2, order3, order4
])

session.commit()


# -------------------------
# Part 5: Queries
# -------------------------

print("\n--- All Users ---")
users = session.query(User).all()
for user in users:
    print(user.id, user.name, user.email)


print("\n--- All Products ---")
products = session.query(Product).all()
for product in products:
    print(product.name, product.price)


print("\n--- All Orders ---")
orders = session.query(Order).all()
for order in orders:
    print(
        f"User: {order.user.name}, "
        f"Product: {order.product.name}, "
        f"Quantity: {order.quantity}"
    )


# Update product price
print("\n--- Update Product Price ---")
product_to_update = session.query(Product).filter_by(name="Phone").first()
product_to_update.price = 600
session.commit()
print("Updated Phone price to:", product_to_update.price)


# Delete a user
print("\n--- Delete User ---")
user_to_delete = session.query(User).filter_by(name="Bob").first()
session.delete(user_to_delete)
session.commit()
print("Deleted user Bob")


# -------------------------
# Bonus (Optional)
# -------------------------

print("\n--- Orders Not Shipped ---")
not_shipped = session.query(Order).filter_by(status=False).all()

for order in not_shipped:
    if order.user:
        print(order.id, order.user.name)
    else:
        print(order.id, "No user found")


print("\n--- Orders Per User ---")
from sqlalchemy import func

counts = session.query(User.name, func.count(Order.id))\
    .join(Order)\
    .group_by(User.id)\
    .all()

for name, count in counts:
    print(name, count)