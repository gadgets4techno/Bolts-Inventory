from flask import render_template, request, Blueprint
from inventory.main.forms import NewPartForm
main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
def home():
    return render_template('index2.html', title="Bolts Inventory")


@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/inventory")
def inv():
    return render_template("inventory.html", title="Inventory")

@main.route("/find")
def find():
    return render_template("finditem.html", title="Find Item")

@main.route("/add", methods=["GET","POST"])
def add():
    form = NewPartForm()
    return render_template("add.html", title="Add Item", form=form)