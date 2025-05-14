from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    sowing_date = db.Column(db.String(20))
    expected_yield = db.Column(db.Float)
    harvest_date = db.Column(db.String(20))
    transactions = db.relationship('Transaction', backref='crop', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    crop = db.relationship('Crop', backref=db.backref('expenses', lazy=True))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(10))  # 'income' or 'expense'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    date = db.Column(db.String(20))
    notes = db.Column(db.String(200))
    type = db.Column(db.String(10))
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
