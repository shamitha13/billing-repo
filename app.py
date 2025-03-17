from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy  import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///billing.db'
db = SQLAlchemy(app)

# Database models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    bills = db.relationship('Bill', backref='customer', lazy=True)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

# Route to display billing form
@app.route('/')
def index():
    return render_template('billing_form.html')

# Route to handle form submission
@app.route('/add_bill', methods=['POST'])
def add_bill():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    amount = request.form['amount']
    date = request.form['date']
    
    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        customer = Customer(name=name, email=email, phone=phone)
        db.session.add(customer)
        db.session.commit()
    
    bill = Bill(amount=amount, date=date, customer_id=customer.id)
    db.session.add(bill)
    db.session.commit()
    
    return redirect(url_for('view_bills'))

# Route to retrieve and display all bills
@app.route('/view_bills')
def view_bills():
    bills = Bill.query.all()
    return render_template('view_bills.html', bills=bills)

if __name__ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True)