#impoet dependencies
import json
import razorpay
from flask import Flask,render_template,request,jsonify,redirect,url_for,make_response
from flask_sqlalchemy import SQLAlchemy
import smtplib
from datetime import datetime
#flask object
app = Flask(__name__)
#MySQL database
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="saiPratyush",
    password="Bhavana@123",
    hostname="saiPratyush.mysql.pythonanywhere-services.com",
    databasename="saiPratyush$user_database_razorpay",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "PAYMENT"
app.config["SQLDATABASE"] = "sqlite:///payment.db"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String(120),nullable=False)
    name = db.Column(db.String(120),nullable=False)
    amount = db.Column(db.String(120),nullable=False)
#main_page
@app.route('/',methods=["GET",'POST'])
def hello():
    if request.method == "POST":
        email=request.form.get("email")
        name=request.form.get("name")
        amount=request.form.get("amount")
        user = User(email=email , name=name, amount=amount)
        db.session.add(user)

        db.session.commit()
        print(user)
        return redirect(url_for("pay", id = user.id))

    return render_template("index.html")
#payment_page

@app.route('/pay/<id>',methods=["GET","POST"])
def pay(id):
    user = User.query.filter_by(id=id).first()
    client=razorpay.Client(auth=("rzp_test_Hh2tc3le8dMwt2","pQ5Eex0z4nxZNRm2iwCng86j"))
    payment = client.order.create({"amount":(int(user.amount) * 100),"currency":"INR","payment_capture":"1"})
    if request.method == "POST":
        return redirect(url_for("success", id = user.id))
    print(payment)
    return render_template("pay.html",payment = payment,user_id=user.id)
#Success page
@app.route('/success/<id>',methods=["GET","POST"])
def success(id):
    user = User.query.filter_by(id=id).first()
    mail(user.name,user.email,user.amount)#email function
    return render_template("success.html")

def mail(name,email,amount):   #function to send email
    with smtplib.SMTP("smtp.gmail.com",587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login("pratyush19919@gmail.com","vkor rsvt evzs modp")
        sub = "DONATION SUCCESSFUL-DETAILS"
        body = """Thank you {0} for your donaton. We have scessfully recieved your donation for the cancer support.
        We appreciate your involvement in such a social activity.We gaurantee that your many save many lives.
        The donation is successfully recieved.
                            PAYMENT DETAILS:
                            Name  :  {0}
                            EMail  :  {1}
                            Date  :  {2}
                            Time  :  {3}
                            Amount  :  {4}
                            """.format(name,email,datetime.now().strftime("%d-%m-%Y"),datetime.now().strftime("%H:%M:%S"),amount)

        msg = "Subject : {0}\n\n{1}".format(sub,body)

        smtp.sendmail("pratyush19919@gmail.com",email,msg)




if __name__ == '__main__':
    app.debug=True
    db.create_all()
    app.run()
    FLASK_APP=main.py
