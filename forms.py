
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, SelectField, BooleanField, DateTimeField
from wtforms.fields import IntegerField

class CustomerEditForm(FlaskForm):
    GivenName = StringField("GivenName",[validators.Length(min=2, max=20)])
    Surname = StringField("Surname",[validators.Length(min=3, max=25)])
    Streetaddress = StringField("Streetaddress",[validators.Length(min=4, max=30)])
    City = StringField("City",[validators.Length(min=2, max=30)])    
    Zipcode = IntegerField("postalcode",[validators.NumberRange(10000,99999)])
    Country = StringField("Country",[validators.Length(min=2, max=20)])
    CountryCode = StringField("CountryCode",[validators.Length(min=2, max=2)])
    Birthday = DateTimeField("Birthday")#fixa validator validators=[DataRequired()]
    NationalId = StringField("NationalId",[validators.Length(min=8, max=30)])
    TelephoneCountryCode = IntegerField("TelephoneCountryCode",[validators.NumberRange(0,99)])
    Telephone = StringField("Telephone",[validators.Length(min=7, max=25)])

class TransactionForm(FlaskForm):
    fromAccount = IntegerField("From Account #",[validators.NumberRange(1,9999999999999999999999999)])
    amount = IntegerField("Amount",[validators.NumberRange(1,9999999999999999999999999)])
    toAccount = IntegerField("To Account #",[validators.NumberRange(1,9999999999999999999999999)])

