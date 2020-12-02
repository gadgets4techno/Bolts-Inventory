from cloudant import Cloudant
import json
import os
import atexit
import requests
from uuid import uuid4
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from inventory.main.data import *
from pathlib import Path
from flask import render_template, request, Blueprint, flash, redirect, url_for, abort, Response
from flask_login import login_user, current_user, logout_user, login_required
from inventory.models import User

from inventory.main.forms import NewPartForm, NavForm, EditPartForm, LocationForm
main = Blueprint('main', __name__)
g = Path("inventory/main", "vcap-local.json")
client = None
token = None
signing_secret = None

client_id = None
client_secret = None

with open(g.absolute()) as f:
    vcap = json.load(f)
    print('Found local VCAP_SERVICES')
    creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
    user = creds['username']
    password = creds['password']
    url = 'https://' + creds['host']
    client = Cloudant(user, password, url=url, connect=True)
    token = vcap["services"]["slack"]["token"]
    signing_secret = vcap["services"]["slack"]["signing_secret"]
    client_id = vcap["services"]["slack"]["client_id"]
    client_secret = vcap["services"]["slack"]["client_secret"]

client.connect()
partsdb = client["bolts-parts"]
locationdb = client["bolts-locations"]
userdb = client["bolts-users"]
slack = App(token=token, signing_secret=signing_secret)
handler = SlackRequestHandler(slack)


def update():
    partsdb = client["bolts-parts"]
    locationdb = client["bolts-locations"]
    userdb = client["bolts-users"]


@main.route("/")
@main.route("/index")
def home():
    x = len(partsdb)
    if current_user.is_authenticated:
        e=False
    else:
        e=True
    return render_template('index2.html', title="Bolts Inventory", x=x, entered=e)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/inventory", methods=["GET", "POST"])
@login_required
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
                fields = ["part", "description", "quantity"]
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
                "part", "description", "quantity", "name", "_id"])

    k1 = {}
    count = 1
    for each in result:
        k1.update({count: each})
        count += 1

    return render_template("inventory.html", title="Inventory", form=form, table=k1)


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
    delForm = EditPartForm()
    update()
    if delForm.validate_on_submit():
        if "delete" in request.delForm:
            flash("Feature not yet ready.")
            # flash(dir(request))
            pass
        pass

    if delForm.errors:
        flash(delForm.errors, "warning")

    if (str(item) in partsdb):
        print(delTags(partsdb[str(item)]))
        return render_template("item.html", title="Find Item", result=delTags(partsdb[str(item)]), delForm=delForm)
    else:
        flash("Item not found.")
        return render_template("item.html", title="Find Item", result=Objects.emptyItem, delForm=delForm)


@main.route("/edit/<int:item>", methods=["GET", "POST"])
def edit(item):
    form = EditPartForm()
    update()
    selector = {"_id": {"$gt": {}}}
    result = fg(locationdb, selector, fields=["_id", "name"])

    if form.validate_on_submit():
        if "submit" in request.form:
            if newPartsDoc(request.form)["_id"] in partsdb:
                doc = newPartsDoc(request.form)
                partsdb[str(item)].update(doc)
                partsdb[str(item)].save()
                update()
                flash("{0} has been updated".format(request.form["part"]))
                return redirect(url_for("main.item", item=int(item)))
            else:
                flash("Item not found.")
                return

    if (str(item) in partsdb):
        ritem = partsdb[str(item)]
        # print(ritem)
        return render_template("edit.html", title="Edit Item", form=form, item=ritem, loc=result)
    else:
        flash("Item not found.")
        return abort(500)


@main.route("/add", methods=["GET", "POST"])
def add():
    form = NewPartForm()
    delForm = EditPartForm()
    update()
    selector = {"_id": {"$gt": {}}}
    result = fg(locationdb, selector, fields=["_id", "name"])

    if form.validate_on_submit():
        if "submit" in request.form:
            if newPartsDoc(request.form)["_id"] in partsdb:
                flash("Part Number already exists!")

            else:
                doc = newPartsDoc(request.form)
                # doc["_id"]=getLatestNo(partsdb)
                partsdb.create_document(doc)
                update()
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


@main.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Until next time!")
    return redirect(url_for("main.home"))


@main.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@main.route("/slack/auth", methods=["GET", "POST"])
def slack_auth():
    r = slack.client.oauth_v2_access(
        client_id=client_id, client_secret=client_secret, code=request.args["code"])
    # q = {"client_id": client_id, "client_secret": client_secret,
    #      "code": request.args["code"]}
    # r = requests.get("https://slack.com/api/oauth.v2.access", params=q)

    # if r.status_code == 200:

    if r["ok"]:  # If authed with Slack
        result = getUser(r['authed_user']['id'], slack)
        if result["ok"]:  # If user exists in workspace
            # If user is not registered in DB
            if newSlackUser(r)["_id"] not in userdb:
                doc = newSlackUser(r)
                doc['userid'] = int(uuid4().int)
                userdb.create_document(doc)
                update()

            user=User.getSlack(uid=newSlackUser(r)["_id"])
            login_user(user)
            next_page = request.args.get('next')

            return redirect(next_page or url_for('main.inv'))

            # flash(f"{r['authed_user']['id']} has been authenticated!")
            # return redirect(url_for("main.inv"))
        else:
            flash("Please join our Slack server to gain entry.")
            abort(500)

    else:
        flash("Authentication error with Slack :(")
        abort(500)


@slack.command("/getpart")
def stats(ack, say, command):
    ack()
    update()
    if (str(command['text']) in partsdb):
        item = str(command['text'])
        say(f"Query: {command['text']}\n\n{Slack(partsdb[item])}")
    else:
        say("Try again, part ID not found. :(")
