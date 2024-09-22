from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

class Sale(Base):
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    counter_id = Column(Integer, ForeignKey('counters.id'))
    
    product = relationship("Product")
    counter = relationship("Counter")

class Counter(Base):
    __tablename__ = 'counters'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
