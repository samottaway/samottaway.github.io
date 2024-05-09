from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import IntegerField,StringField, SubmitField, FileField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import file_required, FileField
import flask_ckeditor

class UserForm(FlaskForm):
    name = StringField("your name", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    submit = SubmitField("submit")


class MessageForm(FlaskForm):
    email = StringField("details", validators=[DataRequired()],render_kw={"placeholder": "Email"},)
    message = flask_ckeditor.CKEditorField("message",validators=[DataRequired()],render_kw={"placeholder": "Message"})
    subject = StringField("details", validators=[DataRequired()],render_kw={"placeholder": "Subject"})
    name = StringField("name", validators=[DataRequired()],render_kw={"placeholder": "Name","type":"text"})
    submit = SubmitField("Send Message",render_kw={"placeholder": "Send Message"})


class EducationForm(FlaskForm):
    institution = StringField("education institute", validators=[DataRequired()])
    qualification_name = StringField('name of qualification ', validators=[DataRequired()])
    description_of_tasks = flask_ckeditor.CKEditorField('qualification date', validators=[DataRequired()])
    qualification_modules = flask_ckeditor.CKEditorField('qualification modules', validators=[DataRequired()])
    qualification_date  = StringField('name of qualification ', validators=[DataRequired()])

    submit = SubmitField("submit_education")


class HobbiesForm(FlaskForm):
    hobbies = StringField("enter hobby", validators=[DataRequired()])
    description = StringField("enter description", validators=[DataRequired()])
    submit = SubmitField("submit_hobbies")


class Work_experience_Form(FlaskForm):
    location = StringField("enter location", validators=[DataRequired()])
    start_end_date = StringField("start end date ", validators=[DataRequired()])
    description_of_tasks = flask_ckeditor.CKEditorField("enter duties ", validators=[DataRequired()])
    submit = SubmitField("submit_work")


class Add_Project(FlaskForm):
    subject = SelectField('filetype', choices=['programs', 'papers'])
    name = StringField('file name', validators=[DataRequired()])
    description = flask_ckeditor.CKEditorField('project description', validators=[DataRequired()])
    file = FileField("file", validators=[file_required()])
    submit = SubmitField('submit')


class Add_recipe(FlaskForm):
    recipe_name = StringField(validators=[DataRequired()])
    cooking_steps = flask_ckeditor.CKEditorField(validators=[DataRequired()])
    ingredients = flask_ckeditor.CKEditorField(validators=[DataRequired()])
    description = flask_ckeditor.CKEditorField(validators=[DataRequired()])
    file = FileField("file", validators=[file_required()])
    submit = SubmitField()



class Add_art(FlaskForm):
    picture_name = StringField( validators=[DataRequired()])
    description = StringField(validators=[DataRequired(),Length(min=6, max=85)])
    file = FileField("file", validators=[file_required()])
    submit = SubmitField()


class Add_comment(FlaskForm):
    text = flask_ckeditor.CKEditorField('comment form',validators=[DataRequired()])
    submit = SubmitField()

class  Add_papers(FlaskForm):
    paper_title = StringField(validators=[DataRequired()])
    description = flask_ckeditor.CKEditorField(validators=[DataRequired(),Length(min=6, max=85)])
    file = FileField('file', validators=[DataRequired()])
    thumbnail = FileField("display pic", validators=[file_required()])
    submit = SubmitField('submit')

class Add_Programs(FlaskForm):
    program_name = StringField(validators=[DataRequired()])

    description = flask_ckeditor.CKEditorField(validators=[DataRequired(),Length(min=6, max=85)])
    file = FileField('file', validators=[DataRequired()])
    submit = SubmitField()
