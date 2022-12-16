from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from HomeWork_16.utils_homework_16 import load_json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
db: SQLAlchemy = SQLAlchemy(app)


# Создаем модель
class User(db.Model):
    __tablename__ = 'users'
    """
    Таблица  users содержит информацию о пользователе (имя, фамилию, возраст, емейл, роль и телефон)
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def __repr__(self):
        return f"User: {self.id}, {self.first_name}"

    def to_dict(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = 'orders'
    """
    Таблица orders содержит информацию о заказах (название, описание, даты начала и конца выполнения, цену, id заказчика и исполнителя))
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("offers.executor_id"))

    users = relationship("User")
    offers = relationship("Offer", foreign_keys=[executor_id])

    def __repr__(self):
        return f"Order: {self.id}, {self.name}"

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offers'
    """
    Таблица offers содержит информацию об оффере (id, id заказа и id исполнителя)
    """
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = relationship("User")
    order = relationship("Order", foreign_keys=[order_id])

    def __repr__(self):
        return f"Offer: {self.id}"

    def to_dict(self):
        return{
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


file_users = 'JSON_data/data_users.json'
file_orders = 'JSON_data/data_orders.json'
file_offers = 'JSON_data/data_offers.json'

# Загружаем данные из файлов
data_users = load_json(file_users)
data_orders = load_json(file_orders)
data_offers = load_json(file_offers)

# Добавляем данные в модель
with app.app_context():
    db.drop_all()
    db.create_all()
    users = [User(**user_data) for user_data in data_users]
    orders = [Order(**order_data) for order_data in data_orders]
    offers = [Offer(**offer_data) for offer_data in data_offers]
    db.session.add_all(users)
    db.session.add_all(orders)
    db.session.add_all(offers)
    db.session.commit()


