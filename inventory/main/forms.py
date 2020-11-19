from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectField, HiddenField, DecimalField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class NewPartForm(FlaskForm):
    partno = IntegerField("Part Number", validators=[DataRequired()])
    serialno=StringField("Serial Number", validators=[DataRequired(),Length(min=4,max=25)])
    quantity=DecimalField("Quantity", validators=[DataRequired()])
    # multi_serial=BooleanField("Multi serial?", validators=[DataRequired()])
    multi_serial=SelectField("Multi Serial?", choices=[("false", "False"),("true", "True")], validators=[DataRequired()])
    submit=SubmitField("Submit")

class NavForm(FlaskForm):
    add = SubmitField(label="Add")
    querybox = StringField(label="Query Field")
    query = SubmitField(label="Query")
    edit = SubmitField(label="Edit")