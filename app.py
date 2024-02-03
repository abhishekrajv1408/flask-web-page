from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATOINS'] = False

db = SQLAlchemy(app)
app.app_context().push()

migrate = Migrate(app, db)

# Models
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), unique = False, nullable = False)
    number = db.Column(db.Integer, unique = False, nullable = False)

    def __repr__(self):
        return f"name:{self.name}, number: {self.number} "


@app.route("/")
def hello():
    current_time = datetime.datetime.now()
    time = current_time.time()
    date = current_time.date()
    return render_template("index.html",time = time, date = date  )


@app.route('/add', methods = ["POST","GET"])
def add_profile():
    if request.method == "POST":
        name1 = request.form.get("name")
        number = request.form.get("contact-number")
        if name1 and number :
            p = Profile(name=name1, number=number)
            db.session.add(p)
            db.session.commit()
            # with app.app_context():  # Application context starts here
            #     p = Profile(name=name1, number=number)
            #     db.session.add(p)
            #     db.session.commit()
            #     print("success")
            return redirect('/')
        # p = Profile(name=name1, number=number)
        # db.session.add(p)
        # db.session.commit()
    return redirect('/')
        

@app.route('/display')
def display():
    profiles = Profile.query.all()
    return render_template("display.Html", profile=profiles)



@app.route('/delete/<int:id>')
def erase(id):
    data = Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')



if __name__  ==  "__main__" :
    with app.app_context():
        db.create_all()
    app.run(debug=True)