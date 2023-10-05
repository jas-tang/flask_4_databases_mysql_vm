from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI using PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://jason:jason2023@172.174.249.223:3306/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)

class Patients(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    MRN = db.Column(db.String(50), nullable=False)

class Demographics(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    patients = Patients.query.all()
    demographics = Demographics.query.all()
    return render_template('index.html', patients=patients, demographics=demographics)

if __name__ == '__main__':
    app.run(
        debug=True,
        port=8080
    )
