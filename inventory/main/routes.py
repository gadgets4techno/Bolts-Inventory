from cloudant import Cloudant
import json, os
from pathlib import Path
from flask import render_template, request, Blueprint, flash, redirect, url_for, abort
from inventory.main.forms import NewPartForm, NavForm
main = Blueprint('main', __name__)
g=Path("inventory\\main", "vcap-local.json")

with open(g.absolute()) as f:
    vcap = json.load(f)
    print('Found local VCAP_SERVICES')
    creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
    user = creds['username']
    password = creds['password']
    url = 'https://' + creds['host']
    client = Cloudant(user, password, url=url, connect=True)

client.connect()
partsdb = client["bolts-parts"]

@main.route("/")
@main.route("/index")
def home():
    return render_template('index2.html', title="Bolts Inventory")


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/inventory", methods=["GET","POST"])
def inv():
    form = NavForm()
    if form.validate_on_submit():
        if "edit" in request.form:
            flash("Editing Item")
            return redirect(url_for("main.inv"))
    
    selector={"_id":{"$gt":{}}}
    result = partsdb.get_query_result(selector, fields=["part","description","quantity"])
    k1={}
    count = 1
    for each in result:
        k1.update({count:each})
        count +=1
    # flash("Hello World!", "success")
    return render_template("inventory.html", title="Inventory", form=form, table=k1)

@main.route("/find")
def find():
    return render_template("finditem.html", title="Find Item")

@main.route("/item/<int:item>", methods=["GET","POST"])
def item(item):
    selector={"part":{"$eq":item}}
    result=partsdb.get_query_result(selector, fields=["part","quantity"])
    k1={}
    return render_template("item.html", title="Find Item", result=result)

@main.route("/add", methods=["GET","POST"])
def add():
    form = NewPartForm()
    return render_template("add.html", title="Add Item", form=form)