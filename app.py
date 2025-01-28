from flask import Flask, jsonify, abort
from flask_migrate import Migrate
from models import db, PowerPlant, Model, Prediction, Generator
from config import Config
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

migrate = Migrate(app, db)

@app.cli.command('seed-db')
def seed_db():
    """
    Метод заполнения базы данных
    :return: None
    """
    # Очистить БД
    db.session.query(Generator).delete()
    db.session.query(Prediction).delete()
    db.session.query(Model).delete()
    db.session.query(PowerPlant).delete()
    db.session.commit()

    # Добавление данных по станциям
    plant_1 = PowerPlant(name='Богучанская ГЭС', node=60533014)
    plant_2 = PowerPlant(name="Харанорская ГРЭС", node=60522003)

    # Добавление записей в сессию
    db.session.add(plant_1)
    db.session.add(plant_2)

    # Зафиксировать изменения для получения ID моделей
    db.session.commit()

    # Добавление данных по моделям
    model_1 = Model(name="LSTM Богучанской ГЭС", input_width=40, data_in_frame=144, plant_id=plant_1.id)
    model_2 = Model(name="LSTM Харанорской ГРЭС", input_width=30, data_in_frame=100, plant_id=plant_2.id)

    # Добавление записей в сессию
    db.session.add(model_1)
    db.session.add(model_2)

    # Зафиксировать изменения для получения ID моделей
    db.session.commit()

    # Создание записей для Prediction
    prediction_1 = Prediction(
        rst_file="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\rst\\БоАЗ.rst",
        scn_file="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\scn\\сценарий_УРОВ_1.scn",
        result="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\res\\результат_1.csv",
        model_id=model_1.id
    )

    prediction_2 = Prediction(
        rst_file="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\rst\\ХГРЭС.rst",
        scn_file="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\scn\\сценарий_УРОВ_2.scn",
        result="C:\\Users\\Umaro\\OneDrive\\Рабочий стол\\res\\результат_2.csv",
        model_id=model_2.id
    )

    # Добавление записей для Prediction в сессию
    db.session.add(prediction_1)
    db.session.add(prediction_2)

    # Зафиксировать изменения
    db.session.commit()

    generator_1 = Generator(name='Богучанская ГЭС - Г1', node=60533008, plant_id=plant_1.id)
    generator_2 = Generator(name='Богучанская ГЭС - Г2', node=60533009, plant_id=plant_1.id)
    generator_3 = Generator(name='Богучанская ГЭС - Г3', node=60533010, plant_id=plant_1.id)
    generator_4 = Generator(name='Богучанская ГЭС - Г4', node=60533011, plant_id=plant_1.id)
    generator_5 = Generator(name='Богучанская ГЭС - Г5', node=60533012, plant_id=plant_1.id)
    generator_6 = Generator(name='Богучанская ГЭС - Г6', node=60533013, plant_id=plant_1.id)
    generator_7 = Generator(name='Богучанская ГЭС - Г7', node=60533014, plant_id=plant_1.id)
    generator_8 = Generator(name='Богучанская ГЭС - Г8', node=60533015, plant_id=plant_1.id)
    generator_9 = Generator(name='Богучанская ГЭС - Г9', node=60533016, plant_id=plant_1.id)

    generator_10 = Generator(name='Харанорская ГРЭС - ТГ-1', node=60301094, plant_id=plant_2.id)
    generator_11 = Generator(name='Харанорская ГРЭС - ТГ-2', node=60301095, plant_id=plant_2.id)
    generator_12 = Generator(name='Харанорская ГРЭС - ТГ-3', node=60301096, plant_id=plant_2.id)

    # Добавление записей в сессию
    db.session.add(generator_1)
    db.session.add(generator_2)
    db.session.add(generator_3)
    db.session.add(generator_4)
    db.session.add(generator_5)
    db.session.add(generator_6)
    db.session.add(generator_7)
    db.session.add(generator_8)
    db.session.add(generator_9)
    db.session.add(generator_10)
    db.session.add(generator_11)
    db.session.add(generator_12)

    # Зафиксировать изменения
    db.session.commit()

@app.route('/powerplant/<int:plant_id>', methods=['GET'])
def get_power_plant(plant_id):
    """
    Функция представления получения станции по id
    :param plant_id: id станции
    :return: JSON типа {'name': Наименование станции}
    """
    # Запрос в БД для получения записи по ID
    plant = PowerPlant.query.get(plant_id)

    if plant is None:
        abort(404, description="Станции не существует")

    return jsonify({'name': plant.name})

@app.route('/model', methods=['GET'])
def get_model():
    """
    Функция представления получения всех моделей из БД
    :return: JSON со списком всех моделей
    """
    # Запрос в БД для получения всех моделей
    models = Model.query.all()

    if models is None:
        abort(404, description="В БД нет моделей")

    # Запись наименований моделей в список
    model_list = [{'name': model.name} for model in models]

    return jsonify(model_list)

@app.route('/powerplant/<string:model_name>', methods=['GET'])
def get_generators_count(model_name):
    """
    Функция представления получения количества генераторов станции
    :param model_name: Модель для определенной станции
    :return: JSON типа {'generators_count': кол-во генераторов}
    """
    # Поиск модели по имени
    model = Model.query.filter_by(name=model_name).first()
    if model is None:
        abort(404, description="Модель не найдена")

    # Поиск станции, связанной с моделью
    plant = PowerPlant.query.get(model.plant_id)
    if plant is None:
        abort(404, description="Станция не найдена")

    # Подсчет количество генераторов, связанных с этой электростанцией
    generator_count = Generator.query.filter_by(plant_id=plant.id).count()

    return jsonify({'generators_count': generator_count})

if __name__ == '__main__':
    app.run(debug=True, port=5005)