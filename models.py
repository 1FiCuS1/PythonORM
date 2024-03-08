import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True)

    book_id = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=50), nullable=False)

    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    publisher = relationship("Publisher", backref="book")
    stock = relationship("Stock", backref="book")

    def __str__(self):
        return f'{self.id}: {self.title}'

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    stock = relationship("Stock", backref="shop")

    def __str__(self):
        return f'{self.id}: {self.name}'

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer)

    book_id = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    sale_id = sq.Column(sq.Integer, sq.ForeignKey("sale.id"), nullable=False)

    book = relationship("Book", backref="stock")
    shop = relationship("Shop", backref="stock")
    sale = relationship("Sale", backref="stock")

    def __str__(self):
        return f'{self.id}: {self.count}'

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer)
    date_sale = sq.Column(sq.Date)
    count = sq.Column(sq.Integer)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    stock = relationship("Stock", backref="sale")

    def __str__(self):
        return f'{self.id}: {self.price}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)