from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Employee('{self.name}', '{self.email}', '{self.department}', '{self.salary}')"

@app.route('/')
def home():
    return redirect(url_for('view_employees'))

@app.route('/employees')
def view_employees():
    employees = Employee.query.all()
    return render_template('view_employees.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        salary = request.form['salary']
        new_employee = Employee(name=name, email=email, department=department, salary=salary)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('view_employees'))
    return render_template('add_employee.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        employee.department = request.form['department']
        employee.salary = request.form['salary']
        db.session.commit()
        return redirect(url_for('view_employees'))
    return render_template('update_employee.html', employee=employee)

@app.route('/delete/<int:id>', methods=['GET'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('view_employees'))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
