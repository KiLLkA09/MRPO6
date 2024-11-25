from flask import Flask, request, jsonify
from repository.sqlalchemy_repository import SQLAlchemyRepository
from repository.json_repository import JSONRepository
from database import SessionLocal
from uow import UnitOfWork
from models import Buyer, Car

app = Flask(__name__)

# Инициализация репозиториев
json_repo = JSONRepository("data.json")

@app.route("/buyers", methods=["POST"])
def add_buyer():
    data = request.get_json()
    with UnitOfWork(SessionLocal) as uow:
        repo = SQLAlchemyRepository(uow.get_session(), Buyer)
        buyer = Buyer(name=data["name"], budget=data["budget"])
        repo.add(buyer)
    return jsonify({"message": "Buyer added successfully"}), 201

@app.route("/cars", methods=["POST"])
def add_car():
    data = request.get_json()
    with UnitOfWork(SessionLocal) as uow:
        repo = SQLAlchemyRepository(uow.get_session(), Car)
        car = Car(model=data["model"], price=data["price"], vin=data["vin"])
        repo.add(car)
    return jsonify({"message": "Car added successfully"}), 201

@app.route("/buyers/<int:buyer_id>", methods=["GET"])
def get_buyer(buyer_id):
    with UnitOfWork(SessionLocal) as uow:
        repo = SQLAlchemyRepository(uow.get_session(), Buyer)
        buyer = repo.get_by_id(buyer_id)
        if not buyer:
            return jsonify({"error": "Buyer not found"}), 404
    return jsonify({"id": buyer.id, "name": buyer.name, "budget": buyer.budget}), 200

@app.route("/cars", methods=["GET"])
def get_cars():
    with UnitOfWork(SessionLocal) as uow:
        repo = SQLAlchemyRepository(uow.get_session(), Car)
        cars = repo.get_all()
    return jsonify([{"id": car.id, "model": car.model, "price": car.price, "vin": car.vin} for car in cars]), 200

@app.route("/buyers/json", methods=["GET"])
def get_buyers_from_json():
    buyers = json_repo.get_all()
    return jsonify(buyers), 200

@app.route("/buyers/json", methods=["POST"])
def add_buyer_to_json():
    data = request.get_json()
    json_repo.add(data)
    return jsonify({"message": "Buyer added to JSON successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)
