from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://admin:1111@localhost:5432/mobiquity"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ATM(db.Model):
    __tablename__ = 'atms'

    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer, nullable=True)
    functionality = db.Column(db.String(128), nullable=True)
    type = db.Column(db.String(128), nullable=True)
    street = db.Column(db.Text, nullable=True)
    house_number = db.Column(db.String(128), nullable=True)
    postal_code = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    lat = db.Column(db.String(128), nullable=True)
    long = db.Column(db.String(128), nullable=True)


class WeekDays(db.Model):
    __tablename__ = 'weekdays'

    atm_id = db.Column(db.Integer, ForeignKey(ATM.id), primary_key=True)
    days_of_week = db.Column(db.Integer, nullable=True)
    hour_from = db.Column(db.String(128), nullable=True)
    hour_to = db.Column(db.String(128), nullable=True)

    atm = relationship('ATM', foreign_keys='WeekDays.atm_id')
