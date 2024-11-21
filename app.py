from flask import Flask, jsonify, abort
from flask_migrate import Migrate
from models import db, PowerPlant, Model, Prediction
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)

@app.cli.command('seed-db')
def seed_db():
    plant_1 = PowerPlant(name='Богучанская ГЭС', node=60533014)
    plant_2 = PowerPlant(name="Красноярская ГЭС", node=60522003)

    model_1 = Model(name="LSTM Богучанской ГЭС", input_width=40)
    model_2 = Model(name="LSTM Красноярской ГЭС", input_width=30)

    prediction_1 = Prediction(rst_file="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\rst\\БоАЗ.rst",
                              scn_file="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\scn\\сценарий_УРОВ_1.scn",
                              result="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\res\\результат_1.csv",
                              plant_id=1, model_id=1)

    prediction_2 = Prediction(rst_file="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\rst\\КрАЗ.rst",
                              scn_file="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\scn\\сценарий_УРОВ_2.scn",
                              result="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\res\\результат_2.csv",
                              plant_id=2, model_id=2)

    with app.app_context():
        db.session.add(plant_1)
        db.session.add(plant_2)
        db.session.add(model_1)
        db.session.add(model_2)
        db.session.add(prediction_1)
        db.session.add(prediction_2)

        db.session.commit()


@app.route('/powerplant/<int:plant_id>', methods=['GET'])
def get_power_plant(plant_id):
    # Запрос в БД для получения записи по ID
    plant = PowerPlant.query.get(plant_id)

    if plant is None:
        # Если запись не найдена, вернем 404
        abort(404)

    # Вернем атрибут name как JSON
    return jsonify({'name': plant.name})


if __name__ == '__main__':
    app.run(debug=True)

