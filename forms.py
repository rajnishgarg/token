# forms.py
from wtforms import Form, StringField, SelectField, validators, SubmitField, validators, TextField, TextAreaField
from mapping import MAPPING_DICT

class ProductSelectForm(Form):

	f = lambda x: (x, '{} ({})'.format(x, MAPPING_DICT[x]["type"]))
	choices = map(f, MAPPING_DICT) 

	select = SelectField('Select a Product:', choices=choices)  #TODO: sort it (Aphabatically, type, etc)