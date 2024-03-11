import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


class PasswordManager:
    def __init__(self):
        self.key = os.getenv("ENCRYPTION_KEY").encode()
        self.cipher_suite = Fernet(self.key)
        self.encrypted_password = self.cipher_suite.encrypt(
            os.getenv("DB_PASSWORD").encode()
        )

    def get_password(self):
        decrypted_password = self.cipher_suite.decrypt(self.encrypted_password)
        return decrypted_password.decode()


password_manager = PasswordManager()
db_password = password_manager.get_password()


DNS = f"postgresql://postgres:{db_password}@localhost:5432/ORM"
engine = sqlalchemy.create_engine(DNS)

Session = sessionmaker(bind=engine)
session = Session()
create_tables(engine)

p1 = Publisher(name="Пушкин")
p2 = Publisher(name="Булгаков")
p3 = Publisher(name="Гоголь")

b1 = Book(title="Капитанская дочка", publisher=p1)
b2 = Book(title="Евгений Онегин", publisher=p1)
b3 = Book(title="Руслан и Людмила", publisher=p1)
b4 = Book(title="Морфий", publisher=p2)
b5 = Book(title="Идиот", publisher=p2)
b6 = Book(title="Мастер и Маргарита", publisher=p2)
b7 = Book(title="Ревизор", publisher=p3)
b8 = Book(title="Вий", publisher=p3)
b9 = Book(title="Шинель", publisher=p3)

shop1 = Shop(title="Книжный Лабиринт")
stock1 = Stock(book=b1, shop=shop1, count=50)
sale1 = Sale(book=b1, shop=shop1, count=55, price=540, date_sale="2022-01-01")
stock2 = Stock(book=b2, shop=shop1, count=50)
sale2 = Sale(book=b2, shop=shop1, count=52, price=545, date_sale="2022-02-03")
stock3 = Stock(book=b3, shop=shop1, count=50)
sale3 = Sale(book=b3, shop=shop1, count=20, price=400, date_sale="2023-03-05")
stock4 = Stock(book=b9, shop=shop1, count=50)
sale4 = Sale(book=b9, shop=shop1, count=26, price=400, date_sale="2023-03-05")

shop2 = Shop(title="Чикона")
stock5 = Stock(book=b4, shop=shop2, count=50)
sale5 = Sale(book=b4, shop=shop2, count=30, price=700, date_sale="2022-01-01")
stock6 = Stock(book=b3, shop=shop2, count=23)
sale6 = Sale(book=b3, shop=shop2, count=20, price=400, date_sale="2023-03-05")

session.add_all(
    [
        p1,
        p2,
        p3,
        b1,
        b2,
        b3,
        b4,
        b5,
        b6,
        b7,
        b8,
        b9,
        shop1,
        shop2,
        stock1,
        stock2,
        stock3,
        stock4,
        stock5,
        stock6,
        sale1,
        sale2,
        sale3,
        sale4,
        sale5,
        sale6,
    ]
)
session.commit()


def get_shops(data):
    query = (
        session.query(Book.title, Shop.title, Sale.price, Sale.date_sale)
        .select_from(Shop)
        .join(Stock)
        .join(Book)
        .join(Publisher)
        .join(Sale)
    )

    if data.isdigit():
        result = query.filter(Publisher.idpublisher == int(data)).all()
    else:
        result = query.filter(Publisher.name == data).all()

    for title, shop, price, date in result:
        print(f"{title: <40} | {shop: <10} | {price: <8} | {date.strftime('%d-%m-%Y')}")


if __name__ == "__main__":
    data = input("Введите id или имя издателя: ")
    get_shops(data)
