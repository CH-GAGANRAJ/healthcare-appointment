from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'patient' or 'doctor' or 'admin'
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    appointments = db.relationship(
        'Appointment',
        primaryjoin="User.id==Appointment.patient_id",
        backref=db.backref('patient', lazy=True),
        lazy=True
    )

    # As doctor
    doctor_appointments = db.relationship(
        'Appointment',
        primaryjoin="User.id==Appointment.doctor_id",
        backref=db.backref('doctor', lazy=True),
        lazy=True
    )


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)  # In real app, use DateTime
    time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Cancelled
    reason = db.Column(db.String(200))
