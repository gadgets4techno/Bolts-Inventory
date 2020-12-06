from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, HiddenField, DecimalField, TextAreaField
from wtforms.fields.html5 import IntegerRangeField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class NewPartForm(FlaskForm):
    partName = StringField("Part Name", validators=[DataRequired()])
    partNickname = StringField("Part Nickname or Alias")
    unit = StringField("Inventory ID", validators=[DataRequired()])
    description=TextAreaField(label="Description")

    partno = StringField("Part Number", validators=[DataRequired()])
    partType = StringField("Part Type")
    # partType = SelectField(label="Part Type", validators=[DataRequired()], choices=[("0", "Tools and Fab HW"), (
    #     "1", "Finite HW"), ("2", "Electronics"), ("3", "Motor Madness"), ("4", "Chasis"), ("5", "Other")])
    partMfg = StringField("Manufacturer")

    serialno = StringField("Serial Number", validators=[
                           DataRequired(), Length(min=4)])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    # multi_serial=BooleanField("Multi serial?", validators=[DataRequired()])
    multi_serial = SelectField("Multi Serial?", choices=[(
        "false", "False"), ("true", "True")], validators=[DataRequired()])
    # location=None
    rooms = [("A", "Canteen"), ("B", "Storage"), ("C", "X-Carve"), ("D", "Materials Storage"), ("E", "Wood Shop"), ("F", "Metal Cutting #1"), ("G", "Metal Cutting #2"),
             ("H", "Parts Storage"), ("I", "Electronics"), ("J", "Old Bots"), ("K", "Fab & Assem #1"), ("L", "Fab & Assem #2"), ("M", "Micro Field"), ("N", "CAD/SW Dev")]
    location = SelectField("Location", validators=[
                           DataRequired()], choices=rooms)
    walls = [("N", "North"), ("E", "East"), ("W", "West"), ("S", "South")]
    locationWall = SelectField("Wall Location", validators=[
                               DataRequired()], choices=walls)

    objType = [("0", "Shop Tools & Fab"), ("1", "Finite HW"), ("2", "Electronics"),
               ("3", "Motor Materials"), ("4", "Chasis"), ("5", "Other")]
    obj = SelectField(label="Item Type", validators=[
                      DataRequired()], choices=objType)
    shelfNum = IntegerField(label="Shelf #", validators=[
                            DataRequired(), NumberRange(min=1, max=9)])
    shelfLevel = IntegerField(label="Shelf Level", validators=[
                              DataRequired(), NumberRange(min=1, max=9)])
    quadrant = IntegerField(label="Quadrant", validators=[
                            NumberRange(min=0, max=9)])
    submit = SubmitField("Submit")


class EditPartForm(NewPartForm):
    # addSerial = StringField("Serial Number", validators=[
    #                         Length(min=4, max=25)])
    add = SubmitField("Add")
    delete = SubmitField("Delete")
    pass

class DeletePartForm(FlaskForm):
    delete=SubmitField("Delete")


class NavForm(FlaskForm):
    # add = SubmitField(label="Add Item")
    querybox = StringField(label="Query Field", validators=[DataRequired()])
    query = SubmitField(label="Query")
    edit = SubmitField(label="Edit")


class LocationForm(FlaskForm):
    placeid = StringField("ID", validators=[DataRequired()])
    name = StringField("Location Name", validators=[DataRequired()])
    description = StringField("Location Description")
    submit = SubmitField("Submit")
    # color = StringField("Hex code - #000000")
