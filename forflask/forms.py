from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, TextAreaField
from wtforms.validators import Required

class CreateForm(Form):
	name = TextField('name', validators = [Required()])
	info = TextAreaField('info')
	image = FileField('image')


	
class EditForm(Form):
	name = TextField('name', validators = [Required()])
	info = TextAreaField('info')
	image = FileField('image')
