from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Appointment

app=Flask(__name__)
app.config['SECRET_KEY']='12345678'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///healthcare.db'

db.init_app(app)
import click
from flask import Flask
def create_tables():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password='admin123',
                role='admin',
                name='Admin',
                email='admin@healthcare.com'
            )
            db.session.add(admin)
            db.session.commit()

# Call it once when starting your app
create_tables()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        name=request.form['name']
        email=request.form['email']
        role='patient'

        if User.query.filter_by(username=username).first():
            flash('user already exists!','danger')
            return redirect(url_for('register'))
        new=User(
            username=username,
            password=password,
            role=role,
            name=name,
            email=email
        )
        db.session.add(new)
        db.session.commit()

        flash('Registration done,Now login','success')
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username,password=password).first()
        if user:
            session['user_id']=user.id
            session['username']=user.username
            session['role']=user.role
            flash('Login Done!','success')
            return redirect(url_for('dashboard'))
        else:
            flash('invaild username or password','danger')
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user=User.query.get(session['user_id'])

    if user.role=='patient':
        appoint=Appointment.query.filter_by(patient_id=user.id).all()
    elif user.role=='doctor':
        appoint=Appointment.query.filter_by(doctor_id=user.id).all()
    else:
        appoint=Appointment.query.all()
    return render_template('dashboard.html',user=user,appointments=appoint)
@app.route('/book',methods=['POST','GET'])
def book_appointment():
    if 'user_id' not in session or session['role'] != 'patient':
        return redirect(url_for('login'))
    if request.method=='POST':
        doctor_id=request.form['doctor']
        date=request.form['date']
        time=request.form['time']
        reason=request.form['reason']

        new=Appointment(
            patient_id=session['user_id'],
            doctor_id=doctor_id,
            date=date,
            time=time,
            reason=reason
        )
        db.session.add(new)
        db.session.commit()
        flash('Appointment booked successfully!','success')
        return redirect(url_for('dashboard'))
    doctors = User.query.filter_by(role='doctor').all()
    return render_template('book.html', doctors=doctors)

@app.route('/admin/add-doctor', methods=['GET', 'POST'])
def add_doctor():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        #specialization = request.form['specialization']
        new_doctor = User(
            username=username,
            password=password,
            role='doctor',
            name=name,
            email=email,
            #specialization=specialization
        )
        db.session.add(new_doctor)
        db.session.commit()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('admin_panel'))
    return render_template('add_doctor.html')

@app.route('/admin')
def admin_panel():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    users = User.query.all()
    return render_template('admin.html', users=users)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
