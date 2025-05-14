from flask import Flask, render_template, request, redirect, url_for
from models import db, Crop, Transaction, Category, Expense  # all models should be imported

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def dashboard():
    crops = Crop.query.all()
    return render_template('dashboard.html', crops=crops)

@app.route('/add_crop', methods=['GET', 'POST'])
def add_crop():
    if request.method == 'POST':
        name = request.form['name']
        sowing_date = request.form['sowing_date']
        expected_yield = request.form['expected_yield']
        harvest_date = request.form['harvest_date']
        
        new_crop = Crop(
            name=name,
            sowing_date=sowing_date,
            expected_yield=expected_yield,
            harvest_date=harvest_date
        )
        db.session.add(new_crop)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_crop.html')

@app.route('/crop/<int:crop_id>/add_expense', methods=['GET', 'POST'])
def add_expense(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        expense = Expense(description=description, amount=amount, crop_id=crop.id)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html', crop=crop)

@app.route('/add_transaction/<int:crop_id>', methods=['GET', 'POST'])
def add_transaction(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    categories = Category.query.all()

    if request.method == 'POST':
        type = request.form['type']
        amount = float(request.form['amount'])
        date = request.form['date']
        notes = request.form['notes']
        category_id = int(request.form['category'])

        transaction = Transaction(
            crop_id=crop_id,
            type=type,
            amount=amount,
            date=date,
            notes=notes,
            category_id=category_id
        )
        db.session.add(transaction)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('add_transaction.html', crop=crop, categories=categories)

@app.route('/crop/<int:crop_id>')
def crop_detail(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    transactions = Transaction.query.filter_by(crop_id=crop_id).all()
    expenses = Expense.query.filter_by(crop_id=crop_id).all()
    return render_template('crop_detail.html', crop=crop, transactions=transactions, expenses=expenses)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
