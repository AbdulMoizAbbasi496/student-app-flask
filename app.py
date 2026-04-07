from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Get database config from environment variables
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('DB_NAME', 'studentdb')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Info(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    reg = db.Column(db.String(200), nullable=False)
    dep = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.name}"

@app.route('/', methods=['GET','POST'])
def indexPg():
    if request.method=='POST':
        name = request.form['name']
        reg = request.form['reg']
        dep = request.form['dep']
        info = Info(name=name, reg=reg, dep=dep)
        db.session.add(info)
        db.session.commit()
    allinfo = Info.query.all()
    return render_template('index.html', allinfo=allinfo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todel = Info.query.filter_by(sno=sno).first()
    db.session.delete(todel)
    db.session.commit()
    return redirect("/")

@app.route('/Records')
def records():
    allinfo = Info.query.all()
    return render_template('records.html', allinfo=allinfo)

if __name__ == "__main__":
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=False, host='0.0.0.0', port=5000)