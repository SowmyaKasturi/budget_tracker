#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)



project_dir = os.path.dirname(os.path.abspath(__file__))
dbfilename = "sqlite:///{}".format(os.path.join(project_dir, "expense_manager.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = dbfilename
db = SQLAlchemy(app)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    expense = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    cateogry = db.Column(db.String(50), nullable=False)


@app.route("/")
def index():
    return render_template("addexpense.html")

@app.route("/addexpense", methods=["POST"])
def addexpense():
    date, expense, amount, category = request.form["date"], request.form["expense"], request.form["amount"], request.form["category"]
    expense = Expenses(date=date, expense=expense, amount=amount, cateogry=category)
    db.session.add(expense)
    db.session.commit()
    return redirect(url_for("allexpenses"))

@app.route("/edit/<int:id>")
def edit(id):
    expense = Expenses(id=id).query.filter_by(id=id).first()
    return render_template("updateexpense.html", expense=expense)

@app.route("/updateexpense", methods=["POST"])
def update():
    id = request.form["id"]
    date = request.form["date"]
    expense = request.form["expense"]
    amount = request.form["amount"]
    cateogry = request.form["category"]

    expense_obj = Expenses(id=id).query.filter_by(id=id).first()
    expense_obj.date = date
    expense_obj.expense = expense
    expense_obj.amount = amount
    expense_obj.cateogry = cateogry

    db.session.add(expense_obj)
    db.session.commit()
    return redirect(url_for("allexpenses"))

@app.route("/delete/<int:id>")
def delete(id):
    book = Expenses(id=id).query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("allexpenses"))

@app.route("/allexpenses")
def allexpenses():
    expense=Expenses.query.all()
    total = 0
    total_b, total_f, total_e, total_o = 0,0,0,0
    for i in expense:
        total += i.amount
        if i.cateogry == "business":
            total_b += i.amount
        if i.cateogry == "entertainment":
            total_e += i.amount
        if i.cateogry == "food":
            total_f += i.amount
        if i.cateogry == "Other":
            total_o += i.amount
    return render_template("allexpenses.html", expense=expense, total=total,total_b=total_b,total_o=total_o, total_f=total_f, total_e=total_e)

if __name__ == "__main__":
    app.run(debug=True)