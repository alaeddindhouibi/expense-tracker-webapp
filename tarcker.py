from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(260), nullable=True)

@app.route('/')
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        try:
            date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            amount = float(request.form['amount'])
            category = request.form['category']
            description = request.form.get('description', '')  # Use get to handle optional field
            new_expense = Expense(amount=amount, category=category, description=description, date=date)
            db.session.add(new_expense)
            db.session.commit()
            return redirect('/')
        except ValueError as e:
            return render_template('add_expense.html', error="Invalid date or amount format. Please try again.")
    return render_template('add_expense.html', error=None)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)