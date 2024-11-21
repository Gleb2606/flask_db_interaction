from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PowerPlant(db.Model):
    __tablename__ = 'powerplant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    node = db.Column(db.Integer, unique=True, nullable=False)

    predictions = db.relationship('Prediction', backref='powerplant', lazy=True)

class Model(db.Model):
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    input_width = db.Column(db.Integer, unique=True, nullable=False)

    predictions = db.relationship('Prediction', backref='model', lazy=True)

class Prediction(db.Model):
    __tablename__ = 'prediction'
    id = db.Column(db.Integer, primary_key=True)
    rst_file = db.Column(db.String(100), nullable=False)
    scn_file = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), unique=True, nullable=False)

    plant_id = db.Column(db.Integer, db.ForeignKey('powerplant.id'), nullable=False)

    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False)