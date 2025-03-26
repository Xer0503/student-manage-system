from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Secret Key'

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/flask_app"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    course = db.Column(db.String(50))
    

    def __init__(self, name, age, email, course):
        self.name = name
        self.age = age
        self.email = email
        self.course = course

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    feedback = db.Column(db.String(50))

    def __init__(self, name, email, feedback):
        self.name = name
        self.email = email
        self.feedback = feedback

@app.route('/')
@app.route('/home')
def main():
    student = Student.query.all()
    return render_template('main.html', students = student)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    feedback = Feedback.query.all()
    return render_template('contact.html', feedbacks = feedback)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        course = request.form['course']

        my_data = Student(name, age, email, course)
        db.session.add(my_data)
        db.session.commit()

        flash("Student Inserted Successfully")

        return redirect(url_for('main'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        student_id = request.form['id']
        student = Student.query.get(student_id)

        if student:
            student.name = request.form['name']
            student.age = request.form['age']
            student.email = request.form['email']
            student.course = request.form['course']

            db.session.commit()
            flash("Student Updated Successfully")

        return redirect(url_for('main'))



@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    student = Student.query.get(id)
    
    if student:
        db.session.delete(student)
        db.session.commit()
        flash("Student Deleted Successfully")

    return redirect(url_for('main'))

@app.route('/feedback', methods=['POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        feedback_text = request.form.get('feedback')

        if not name or not email or not feedback_text:
            flash("All fields are required!", "danger")
            return redirect(url_for('contact'))

        new_feedback = Feedback(name=name, email=email, feedback=feedback_text)
        db.session.add(new_feedback)
        db.session.commit()

        flash("Feedback Submitted Successfully", "success")
        return redirect(url_for('contact'))

    
if __name__ == '__main__':
    app.run()