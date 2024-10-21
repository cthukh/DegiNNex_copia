from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from app import op_form

class FormularioRegistro(FlaskForm):
    nombre            = StringField('Nombre', validators=[DataRequired(), Length(min=3)])
    apellido          = StringField('Apellido', validators=[DataRequired(), Length(min=3)])
    correo            = EmailField('Correo', validators=[DataRequired(), Email()])
    clave             = PasswordField('Clave', validators=[DataRequired(), EqualTo('confirmar_clave', message="Las claves deben ser iguales.")])
    confirmar_clave   = PasswordField('Confirmar clave', validators=[DataRequired()])
    submit            = SubmitField('Registrarme')

class FormularioAcceso(FlaskForm):
    correo            = EmailField('Correo', validators=[DataRequired(), Email()])
    clave             = PasswordField('Clave', validators=[DataRequired()])
    submit            = SubmitField('Acceder')

class FormularioValidar(FlaskForm):
    edad              = IntegerField('Edad', validators=[DataRequired(), NumberRange(min=18)])
    telefono          = StringField('Telefono (+56 9 87654321)', default='+56 9 ' , validators=[DataRequired()])
    categoria         = SelectField('Selecciona una categoria',choices=op_form,default='default',validators=[DataRequired()]) #cambiar a area o campo
    submit            = SubmitField('Completar')
