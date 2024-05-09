import datetime
import os.path
import time
from functools import wraps

import flask_wtf
from flask_bootstrap import Bootstrap
import flask
import sqlalchemy
import werkzeug.security as security
from flask import redirect, url_for, send_from_directory, request
from flask_login import login_user, current_user, UserMixin, LoginManager, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base, DeclarativeBase
from flask_bootstrap import Bootstrap5
import art_functions
# convert_image_food
import recipe_functions
from forms import UserForm, MessageForm, EducationForm, HobbiesForm, Work_experience_Form, Add_recipe, \
    Add_art, Add_comment, Add_papers, Add_Programs
from functions_for_route_basic import create_new_user, login_requested_user, save_message, add_education_details, \
    add_hobbies_forms, add_work_experience, function_to_delete, create_pdfs

app = flask.Flask(__name__, static_folder='static')

app.secret_key = 'super secret string'
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap5(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website_database.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['CKEDITOR_WIDTH'] = 400  # px
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, db.ForeignKey('user.id'))
    art_name = db.Column(db.String, db.ForeignKey('art.id'))
    program_name = db.Column(db.String, db.ForeignKey('programs.id'))
    recipes_name = db.Column(db.String, db.ForeignKey('recipes.id'))
    paper_name = db.Column(db.String, db.ForeignKey('papers.id'))
    comment = db.Column(db.String(100))
    date = db.Column(db.String)


class Messages(db.Model, Base):
    id = db.Column(Integer, primary_key=True)
    contact_details = db.Column(String)
    message = db.Column(String)
    name = db.Column(String)
    date = db.Column(String)


class Programs(db.Model, Base):
    id = db.Column(Integer, primary_key=True)
    file_ref = db.Column(String, unique=True)
    program_name = db.Column(String, unique=True)
    description = db.Column(String)
    date = db.Column(String)


class Education(db.Model, Base):
    id = db.Column(Integer, primary_key=True)
    institution = db.Column(String)
    qualification_name = db.Column(String, unique=True)
    qualification_date = db.Column(String)
    qualification_modules = db.Column(String)


class Hobbies(db.Model, Base):
    id = db.Column(Integer, primary_key=True)
    hobbies = db.Column(String, unique=True)
    description = db.Column(String)


class Work_experience(db.Model, Base):
    id = db.Column(Integer, primary_key=True)
    location = db.Column(String)
    start_end_date = db.Column(String)
    description_of_tasks = db.Column(String)


class Recipes(db.Model, Base):
    id = db.Column(Integer, primary_key=True)
    file_path = db.Column(String, unique=True)
    cooking_steps = db.Column(String)
    ingredients = db.Column(String)
    recipe_name = db.Column(String, unique=True)
    recipe_date = db.Column(String)
    subject = db.Column(String)
    recipe_pdf = db.Column(String)
    description = db.Column(String)
    comment = db.relationship('Comment', lazy=True, backref='recipes')


class Papers(db.Model, Base):
    id = db.Column(Integer, primary_key=True)
    paper_name = db.Column(String, unique=True)
    paper_pdf = db.Column(String, unique=True)
    paper_description = db.Column(String)
    comment = db.relationship('Comment', lazy=True, backref='papers')


class Art(db.Model, Base):
    id = db.Column(Integer, primary_key=True)
    picture_name = db.Column(String, unique=True)
    file_path = db.Column(String, unique=True)
    date = db.Column(String)
    description = db.Column(String)
    comment = db.relationship('Comment', lazy=True, backref='art')


with app.app_context():
    db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return redirect(url_for('home'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/log_out')
def log_out():
    logout_user()
    return redirect(url_for('home'))


@app.route("/")
def home():
    art_functions.convert_image(db=db, aart=Art)
    recipe_functions.convert_image_food(db=db, Recipes=Recipes)
    create_pdfs(db=db, recipes=Recipes)

    return flask.render_template("index.html", current_user=current_user)


@app.route("/test")
@admin_only
def test():
    return flask.render_template("test.html", current_user=current_user)


@app.route("/register", methods=["get", "post"])
def register():
    register_form = UserForm()
    if register_form.validate_on_submit():
        new_user = create_new_user(db=db, register_form=register_form, User=User)
        login_user(new_user)
        return redirect(flask.url_for('home'))

    return flask.render_template("register.html", register_form=register_form, current_user=current_user)


@app.route("/login", methods=["post", 'get'])
def login():
    global password
    login_form = UserForm()
    if login_form.validate_on_submit():
        user = login_requested_user(db=db, User=User, login_form=login_form)
        if user:
            password = login_form.password.data
            password = security.check_password_hash(password=password, pwhash=user.password)
        if not user:
            return redirect(url_for('register'))
        elif not password == True:
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return flask.render_template('login.html', login_form=login_form, current_user=current_user)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = MessageForm()

    if request.method == 'POST':
        print('hh')
        save_message(Messages=Messages, db=db, contact_form=contact_form)
        return redirect(url_for('home'))

    return flask.render_template('contact.html', contact_form=contact_form, current_user=current_user)


@app.route('/about', methods=['GET', 'POST'])
# @admin_only
def about():
    wtf = flask_wtf
    education_form = EducationForm()
    hobbies_form = HobbiesForm()
    work_experience_form = Work_experience_Form()
    if education_form.validate_on_submit() and education_form.data:
        add_education_details(db=db, Education=Education, education_form=education_form)
        print('hh')
    if hobbies_form.submit.data and hobbies_form.validate_on_submit():
        add_hobbies_forms(db=db, hobbies_form=hobbies_form, Hobbies=Hobbies)
    if work_experience_form.validate_on_submit() and work_experience_form.data:
        add_work_experience(db=db, Work_experience=Work_experience, work_experience_form=work_experience_form)
        redirect(url_for('home'))

    return flask.render_template('about.html', education_form=education_form, hobbies_form=hobbies_form
                                 , Work_experience_Form=work_experience_form, current_user=current_user)


@app.route('/admin_page', methods=['get', 'post'])
@admin_only
def admin_page():
    users = db.session.query(User).all()
    messages = db.session.query(Messages).all()
    hobbies = db.session.query(Hobbies).all()
    work_expirence = db.session.query(Work_experience).all()

    return flask.render_template('admin_page.html', users=users, messages=messages, hobbies=hobbies,
                                 work_expirence=work_expirence,
                                 current_user=current_user)


@app.route('/delete/<id>/<func>')
@admin_only
def delete_entry(id, func):
    function_to_delete(id=id, func=func, User=User, db=db, Work_experience=Work_experience, Hobbies=Hobbies,
                       Messages=Messages)
    return redirect(url_for('admin_page'))


@app.route('/delete_comment/<int>')
def delete_comment(int):
    entry = Comment.query.filter_by(id=int).first()

    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('recipes'))


# programs routes
@app.route('/programs', methods=['get', 'post'])
def programs():
    add_program = Add_Programs()
    program_projects = db.session.query(Programs).all()
    if add_program.validate_on_submit():
        add_program.file.data.save(f"static/assets/programs/{add_program.file.data.filename}")
        program = Programs(
            program_name=add_program.program_name.data,
            description=add_program.description.data,
            date=datetime.date.today(),
            file_ref=add_program.file.data.filename
        )
        db.session.add(program)
        db.session.commit()
        return redirect(url_for('home'))

    return flask.render_template('programs.html', program=add_program, programs=program_projects)


@app.route('/download_program/<text>', methods=['GET', 'POST'])
def download_program(text):
    check_project = db.session.execute(db.select(Programs).where(Programs.id == text))
    programs = check_project.scalar()
    app.config['UPLOAD_FOLDER'] = 'static/assets/programs'
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=programs.file_ref, as_attachment=True)


@app.route('/delete_program/<text>', methods=['get', 'post'])
def delete_program(text):
    check_project = db.session.execute(db.select(Programs).where(Programs.id == text))
    program = check_project.scalar()
    os.remove(f'static/assets/programs/{program.file_ref}')

    entry = Programs.query.filter_by(id=text).first()
    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for('programs'))


# papers routes
@app.route('/papers', methods=['GET', 'POST'])
def papers():
    paper_form = Add_papers()
    papers_projects = db.session.query(Papers).all()
    if paper_form.validate_on_submit():
        paper_form.file.data.save(f"static/assets/papers/{paper_form.file.data.filename}")
        paper = Papers(
            paper_name=paper_form.paper_title.data,
            paper_pdf=paper_form.file.data.filename,
            paper_description=paper_form.description.data

        )
        db.session.add(paper)
        db.session.commit()
        return redirect(url_for('home'))
    return flask.render_template('papers.html', paper=paper_form, papers=papers_projects)


@app.route('/download_paper/<text>', methods=['GET', 'POST'])
def download_paper(text):
    check_project = db.session.execute(db.select(Papers).where(Papers.id == text))
    paper = check_project.scalar()

    app.config['UPLOAD_FOLDER'] = 'static/assets/papers'
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=paper.paper_pdf, as_attachment=True)


@app.route('/delete_papers/<text>', methods=['get', 'post'])
def delete_paper(text):
    check_project = db.session.execute(db.select(Papers).where(Papers.id == text))
    paper = check_project.scalar()
    os.remove(f'static/assets/papers/{paper.paper_pdf}')

    entry = Papers.query.filter_by(id=text).first()
    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for('papers'))


# art routes
@app.route('/art', methods=['GET', 'POST'])
def art():
    add_art = Add_art()
    art_projects = db.session.query(Art).all()

    if add_art.validate_on_submit():
        check = add_art.picture_name.data
        index = check.find('/')
        if index <= 0:
            add_art.file.data.save(f"static/assets/art_images/{add_art.file.data.filename}")
            art = Art(
                picture_name=add_art.picture_name.data,
                file_path=add_art.file.data.filename,
                date=datetime.date.today()
            )
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('home'))

    return flask.render_template('art.html', current_user=current_user, add_art=add_art, art=art_projects,
                                 )


@app.route('/download_art/<text>', methods=['GET', 'POST'])
def download_art(text):
    check_project = db.session.execute(db.select(Art).where(Art.id == text))
    art_project = check_project.scalar()
    app.config['UPLOAD_FOLDER'] = 'static/assets/art_images'
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, path=art_project.file_path, as_attachment=True)


@app.route('/view_art/<r>', methods=['GET', 'POST'])
def view_art(r):
    time.sleep(0.2)
    check_project = db.session.execute(db.select(Art).where(Art.id == r))
    result = db.session.execute(db.select(Comment).where(Comment.art_name == Art.picture_name)).scalars().all()
    art_project = check_project.scalar()
    comment_form = Add_comment()
    if comment_form.validate_on_submit():
        try:
            check = db.session.execute(db.select(User).where(User.id == current_user.get_id()))
            user = check.scalar()
            comment = Comment(user_name=current_user.name, comment=comment_form.text.data,
                              art_name=art_project.picture_name, date=datetime.datetime.today())
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('home'))
        except AttributeError:
            comment = Comment(user_name='anoynamous', comment=comment_form.text.data,
                              art_name=art_project.picture_name, date=datetime.datetime.today())
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('home'))

    return flask.render_template('view_art.html', comment=comment_form, current_user=current_user,
                                 user_name=current_user.get_id(), a=art_project, comments=result)


@app.route('/delete_art/<text>', methods=['get', 'post'])
def delete_art(text):
    check_project = db.session.execute(db.select(Art).where(Art.id == text))
    art = check_project.scalar()
    os.remove(f'static/assets/art_images/{art.file_path}')

    entry = Art.query.filter_by(id=text).first()
    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for('art'))


# recipe routes
@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    recipes_project = db.session.query(Recipes).all()
    add_recipe_form = Add_recipe()

    if add_recipe_form.validate_on_submit():
        Db, check = recipe_functions.make_new_recipe(add_recipe_form=add_recipe_form, db=db, Recipes=Recipes,
                                                     datetime=datetime, url_for=url_for, redirect=redirect)
        if check == True:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('recipes'))

    return flask.render_template('recipes.html', current_user=current_user, recipe_form=add_recipe_form,
                                 recipes=recipes_project)


@app.route('/delete_recipes/<text>', methods=['get', 'post'])
def delete_recipes(text):
    recipe_functions.remove_recipe(db=db, text=text, os=os, Recipes=Recipes)
    return redirect(url_for('recipes'))


@app.route('/download_recipes/<text>')
def download_recipes(text):
    uploads, art_project = recipe_functions.link_to_recipe(db=db, os=os, text=text, Recipes=Recipes, app=app)
    return send_from_directory(directory=uploads, path=f"{art_project.recipe_pdf}", as_attachment=True)


@app.route('/view_recipe/<r>', methods=['get', 'post'])
def view_recipe(r):
    time.sleep(0.2)
    comment_form = Add_comment()
    check_project = db.session.execute(db.select(Recipes).where(Recipes.id == r))
    recipe = check_project.scalar()

    result = db.session.execute(sqlalchemy.select(Comment)).scalars().all()
    if comment_form.validate_on_submit():
        try:
            comment = Comment(user_name=current_user.name, comment=comment_form.text.data,
                              recipes_name=recipe.recipe_name, date=datetime.datetime.today())
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('home'))

        except AttributeError:
            comment = Comment(user_name='anoynamous', comment=comment_form.text.data,
                              recipes_name=recipe.recipe_name, date=datetime.datetime.today())
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('home'))

    return flask.render_template('view_recipe.html', comments=result, r=recipe, comment_form=comment_form,
                                 current_user=current_user)


if app.name == "2":
    app.run(debug=True)
