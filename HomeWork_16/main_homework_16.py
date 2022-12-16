import json
from flask import request, jsonify
from model import User, Order, Offer, app, db

# Создаем вью для вывода всех ползователей и добавления новых пользователей из url
@app.route("/users", methods=["GET", "POST"])
def all_users():
    if request.method == "GET":
        result = []
        for user in User.query.all():
            result.append(user.to_dict())
        return jsonify(result)
    elif request.method == "POST":
        try:
            user_data = json.loads(request.data)
            new_user = User(
                id=user_data["id"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                age=user_data["age"],
                email=user_data["email"],
                role=user_data["role"],
                phone=user_data["phone"])
            nested = db.session.begin_nested()
            try:
                db.session.add(new_user)
            except Exception:
                nested.rollback()
                raise Exception("database exception")
            db.session.commit()
        except KeyError:
            return "not enough data"
        return "user_added"


# Создаем вью для вывода ползователя по id, измение его данных и удаления по id
@app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def user_by_id(user_id):
    if request.method == "GET":
        return jsonify(User.query.get(user_id).to_dict())

    elif request.method == "PUT":
        try:
            user_data = json.loads(request.data)
            update_user = User.query.get(user_id)
            update_user.first_name = user_data["first_name"]
            update_user.last_name = user_data["last_name"]
            update_user.age = user_data["age"]
            update_user.email = user_data["email"]
            update_user.role = user_data["role"]
            update_user.phone = user_data["phone"]
            db.session.add(update_user)
            db.session.commit()
        except KeyError:
            return "not enough data"
        return "user_updated"

    elif request.method == "DELETE":
        try:
            delete_user = User.query.get(id)
            db.session.delete(delete_user)
            db.session.commit()
        except Exception:
            raise Exception("id not exist")
        return "user_deleted"


# Создаем вью для вывода всех заказов и добавления новых заказов из url
@app.route("/orders", methods=["GET", "POST"])
def all_orders():
    if request.method == "GET":
        result = []
        for order in Order.query.all():
            result.append(order.to_dict())
        return jsonify(result)
    elif request.method == "POST":
        try:
            order_data = json.loads(request.data)
            new_order = Order(
                id=order_data["id"],
                name=order_data["name"],
                description=order_data["description"],
                start_date=order_data["start_date"],
                end_date=order_data["end_date"],
                address=order_data["address"],
                price=order_data["price"],
                customer_id=order_data["customer_id"],
                executor_id=order_data["executor_id"])
            try:
                db.session.add(new_order)
            except Exception:
                db.session.rollback()
                raise Exception("database exception")
            db.session.commit()
        except KeyError:
            return "not enough data"
        return "order_created"


# Создаем вью для вывода заказа по id, измение его данных и удаления заказа по id
@app.route("/orders/<int:order_id>", methods=["GET", "PUT", "DELETE"])
def order_by_id(order_id):
    if request.method == "GET":
        return jsonify(Order.query.get(order_id).to_dict())

    elif request.method == "PUT":
        try:
            order_data = json.loads(request.data)
            update_order = Order.query.get(order_id)
            update_order.name = order_data["name"]
            update_order.description = order_data["description"]
            update_order.start_date = order_data["start_date"]
            update_order.end_date = order_data["end_date"]
            update_order.address = order_data["address"]
            update_order.price = order_data["price"]
            update_order.customer_id = order_data["customer_id"]
            update_order.executor_id = order_data["executor_id"]
            db.session.add(update_order)
            db.session.commit()
        except KeyError:
            return "not enough data"
        return "order_updated"

    elif request.method == "DELETE":
        try:
            delete_order = Order.query.get(id)
            db.session.delete(delete_order)
            db.session.commit()
        except Exception:
            raise Exception("id not exist")
        return "order_deleted"


# Создаем вью для вывода всех офферов и добавления новых офферов из url
@app.route("/offers", methods=["GET", "POST"])
def all_offers():
    if request.method == "GET":
        result = []
        for offer in Offer.query.all():
            result.append(offer.to_dict())
        return jsonify(result)
    elif request.method == "POST":
        try:
            offer_data = json.loads(request.data)
            new_offer = Offer(
                id=offer_data["id"],
                order_id=offer_data["order_id"],
                executor_id=offer_data["executor_id"])
            try:
                db.session.add(new_offer)
            except Exception:
                db.session.rollback()
                raise Exception("database exception")
            db.session.commit()
        except KeyError:
            return "not enough data"
        return "offer_created"


# Создаем вью для вывода предложения по id, измение его данных и удаления по id
@app.route("/offers/<int:offer_id>", methods=["GET", "PUT", "DELETE"])
def offer_by_id(offer_id):
    if request.method == "GET":
        return jsonify(Offer.query.get(offer_id).to_dict())

    elif request.method == "PUT":
        try:
            offer_data = json.loads(request.data)
            update_offer = Offer.query.get(id)
            update_offer.order_id = offer_data["order_id"]
            update_offer.executor_id = offer_data["executor_id"]
            db.session.add(update_offer)
            db.session.commit()
        except KeyError:
            return "not enough data"
        return "offer_updated"

    elif request.method == "DELETE":
        try:
            delete_offer = Offer.query.get(offer_id)
            db.session.delete(delete_offer)
            db.session.commit()
        except Exception:
            raise Exception("id not exist")
        return "offer_deleted"


if __name__ == '__main__':
    app.run(debug=True)