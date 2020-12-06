from cloudant import Cloudant, document
import json
import os
import atexit
from inventory.main.data import *
from pathlib import Path
from flask import render_template, request, Blueprint, flash, redirect, url_for, abort, Response
from inventory.main.forms import NewPartForm, NavForm, EditPartForm, LocationForm, DeletePartForm
main = Blueprint('main', __name__)
g = Path("inventory/main", "vcap-local.json")
client = None


if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'],
                      url=os.environ['CLOUDANT_URL'], connect=True)
else:
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
locationdb = client["bolts-locations"]


def update():
    partsdb = client["bolts-parts"]
    locationdb = client["bolts-locations"]


@main.route("/")
@main.route("/index")
def home():
    return render_template('index2.html', title="Bolts Inventory", x=partsdb.doc_count())


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/inventory", methods=["GET", "POST"])
def inv():
    form = NavForm()
    # Check form for errors
    if form.validate_on_submit():
        # Check for query button on POST
        # if "add" in request.form:
        #     return redirect(url_for("main.add"))

        if "query" in request.form:
            q = str(request.form["querybox"]).strip()
            if q.isdecimal():
                selector = {"_id": {"$eq": request.form["querybox"]}}
                fields = ["part", "location", "name", "_id", "quantity"]
                result = fg(partsdb, selector, fields)

                k1 = {}
                count = 1
                for each in result:
                    k1.update({count: each})
                    count += 1
                flash("Results found: " + str(len(k1)))
                return render_template("inventory.html", title="Inventory", form=form, table=k1)

            else:
                flash("No results found. Full text search not yet available.")
                return redirect(url_for("main.inv"))

    if form.errors:
        flash(form.errors, "warning")

    selector = {"_id": {"$gt": {}}}
    result = fg(partsdb, selector, fields=[
                "part", "quantity", "name", "_id", "location"])

    k1 = {}
    count = 1
    for each in result:
        k1.update({count: each})
        count += 1

    return render_template("inventory.html", title="Inventory", form=form, table=k1)


@main.route("/locate", methods=["GET", "POST"])
def locate():
    return render_template("locate.html")


@main.route("/location", methods=["GET", "POST"])
def location():
    form = LocationForm()
    selector = {"_id": {"$gt": {}}}
    result = fg(locationdb, selector, fields=["_id", "name"])

    if form.validate_on_submit():
        # for each in result:
        #     if each["_id"] in request.form.keys():
        #         print(each["_id"])

        doc = {"_id": request.form["placeid"],
               "name": request.form["name"], "desc": request.form["description"]}
        locationdb.create_document(doc)
        flash("{0} saved!".format(request.form["name"]))
        return redirect(url_for("main.location"))
        pass

    if form.errors:
        flash(form.errors, "warning")

    print(result)
    return render_template("location.html", title="Location", locs=result, form=form)


@main.route("/item/<int:item>", methods=["GET", "POST"])
def item(item):
    delForm = DeletePartForm()
    # update()
    if delForm.validate_on_submit():
        if document.Document(partsdb, str(item)).exists():
            d = document.Document(partsdb, str(item))
            d.fetch()

            flash(f"Successfully deleted {d['location']}-{d['_id']}")
            d.delete()
            return redirect(url_for("main.inv"))
        pass

    if delForm.errors:
        flash(delForm.errors, "warning")

    # if (str(item) in partsdb):
    if document.Document(partsdb,str(item)).exists():
        d=document.Document(partsdb, str(item))
        d.fetch()
        print(delTags(d))
        # print(delTags(partsdb[str(item)]))
        return render_template("item.html", title="Find Item", result=d, delForm=delForm)
    else:
        flash("Item not found.")
        return render_template("item.html", title="Find Item", result=Objects.emptyItem, delForm=delForm)


@main.route("/edit/<int:item>", methods=["GET", "POST"])
def edit(item):
    form = EditPartForm()
    # update()
    # selector = {"_id": {"$gt": {}}}
    # result = fg(locationdb, selector, fields=["_id", "name"])

    if form.validate_on_submit():
        if "submit" in request.form:
            # if newPartsDoc(request.form)["_id"] in partsdb:
            if document.Document(partsdb,newPartsDoc(request.form)["_id"]).exists():
                doc = newPartsDoc(request.form)
                # partsdb[str(item)].update(doc)
                with document.Document(partsdb, document_id=doc["_id"]) as d:
                    d.fetch()
                    for each in doc:
                        d[each] = doc[each]
                    pass

                # update()
                flash("{0} has been updated".format(request.form["partName"]))
                return redirect(url_for("main.item", item=int(item)))
            else:
                flash("Item not found.")

    if form.errors:
        flash(form.errors, "warning")

    # if (str(item) in partsdb):
    if document.Document(partsdb,str(item)).exists():
        # ritem = partsdb[str(item)]
        ritem = document.Document(partsdb, str(item))
        ritem.fetch()
        # print(ritem)
        return render_template("edit.html", title="Edit Item", form=form, item=ritem, opt1=form.rooms, opt2=form.walls, opt3=form.objType)
    else:
        flash("Item not found.")
        return abort(500)


@main.route("/add", methods=["GET", "POST"])
def add():
    form = NewPartForm()
    delForm = EditPartForm()
    # update()
    selector = {"_id": {"$gt": {}}}
    result = fg(locationdb, selector, fields=["_id", "name"])

    if form.validate_on_submit():
        if "submit" in request.form:
            # if newPartsDoc(request.form)["_id"] in partsdb:
            if document.Document(partsdb,newPartsDoc(request.form)["_id"]).exists():
                flash("Part Number already exists!")

            else:
                doc = newPartsDoc(request.form)
                # doc["_id"]=getLatestNo(partsdb)
                partsdb.create_document(doc)
                # document.Document(partsdb,doc).create()
                # update()
                flash("{0} successfully added!".format(
                    request.form["partName"]))
                return redirect(url_for("main.add"))

    if form.errors:
        flash(form.errors, "warning")

    # flash(str(request.form))
    return render_template("add.html", title="Add Item", form=form, delFrom=delForm, loc=result, num=getLatestNo(partsdb))


@atexit.register
def shutdown():
    client.disconnect()
