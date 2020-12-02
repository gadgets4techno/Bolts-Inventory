from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectField, HiddenField, DecimalField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class NewPartForm(FlaskForm):
    partName=StringField("Part Name", validators=[DataRequired()])
    partNickname=StringField("Part Nickname or Alias")
    part=StringField("Inventory ID", validators=[DataRequired()])
    partno = IntegerField("Part Number", validators=[DataRequired()])
    partType = StringField("Part Type")
    partMfg = StringField("Manufacturer")

    serialno=StringField("Serial Number", validators=[DataRequired(),Length(min=4)])
    quantity=DecimalField("Quantity", validators=[DataRequired()])
    # multi_serial=BooleanField("Multi serial?", validators=[DataRequired()])
    multi_serial=SelectField("Multi Serial?", choices=[("false", "False"),("true", "True")], validators=[DataRequired()])
    # location=None
    submit=SubmitField("Submit")

class EditPartForm(NewPartForm):
    addSerial=StringField("Serial Number", validators=[Length(min=4,max=25)])
    add=SubmitField("Add")
    delete=SubmitField("Delete")
    pass

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