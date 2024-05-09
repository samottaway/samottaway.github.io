import datetime
import imghdr
import os
import smtplib
from email.message import EmailMessage

import requests
import yagmail
import mailersend
from  werkzeug import security
import reportlab
from reportlab.platypus import Frame
import werkzeug
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Image
from werkzeug.utils import send_from_directory
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image
import PIL
from mailersend import emails

from  dotenv import  load_dotenv



def create_new_user(User, register_form, db):
    password = register_form.password.data
    password = security.generate_password_hash(password, salt_length=16)
    new_user = User(
        name=register_form.name.data,
        password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def login_requested_user(db, login_form, User):
    password = login_form.password.data
    check_user = db.session.execute(db.select(User).where(User.name == login_form.name.data))
    user = check_user.scalar()
    return user


def save_message(Messages, contact_form, db):
    new = Messages(
        contact_details=contact_form.email.data,
        message=contact_form.message.data,
        name=contact_form.name.data,
        date=str(datetime.date.today())
    )
    db.session.add(new)
    db.session.commit()

    print("gghk")


def add_education_details(db, Education, education_form):
    new = Education(
        institution=education_form.institution.data,
        qualification_name=education_form.qualification_name.data,
        qualification_date=education_form.qualification_date.data,
        qualification_modules=education_form.qualification_modules.data)

    db.session.add(new)

    db.session.commit()


def add_hobbies_forms(db, Hobbies, hobbies_form):
    new = Hobbies(
        hobbies=hobbies_form.hobbies.data,
        description=hobbies_form.description.data

    )
    db.session.add(new)
    db.session.commit()
    print("okay")


def add_work_experience(db, Work_experience, work_experience_form):
    work_experience = Work_experience(
        location=work_experience_form.location.data,
        start_end_date=work_experience_form.start_end_date.data,
        description_of_tasks=work_experience_form.descrition_of_tasks.data)
    db.session.add(work_experience)
    db.session.commit()
    print('jjk')


def function_to_delete(id, func, User, db, Work_experience, Hobbies, Messages):
    if func == "user_account":
        user_to_remove = User.query.filter_by(id=int(id)).first()
        db.session.delete(user_to_remove)
        db.session.commit()

    elif func == 'work':
        user_to_remove = Work_experience.query.filter_by(id=int(id)).first()
        db.session.delete(user_to_remove)
        db.session.commit()

    if func == 'message':
        user_to_remove = Messages.query.filter_by(id=int(id)).first()
        db.session.delete(user_to_remove)
        db.session.commit()

    if func == 'hobby':
        user_to_remove = Hobbies.query.filter_by(id=int(id)).first()
        db.session.delete(user_to_remove)
        db.session.commit()


def save_new_project(add_project, db, Projects):
    if add_project.subject.data == "papers":
        file_to_use = add_project.file.data.save(f"static/assets/papers/{add_project.file.data.filename}")
        project = Projects(
            subject=add_project.subject.data,
            file_path=add_project.file.data.filename,
            description=add_project.description.data,
            name=add_project.name.data
        )
        db.session.add(project)
        db.session.commit()
    elif add_project.subject.data == "programs":
        add_project.file.data.save(f"assets/programs/{add_project.file.data.filename}")

        project = Projects(
            subject=add_project.subject.data,
            file_path=add_project.file.data.filename,
            description=add_project.description.data,
            name=add_project.name.data
        )
        db.session.add(project)
        db.session.commit()


def download_file(db, subject, Projects, os, text, app):
    check_user = db.session.execute(db.select(Projects).where(Projects.id == text))
    user = check_user.scalar()
    if subject == 'art':
        app.config['UPLOAD_FOLDER'] = 'assets/art'
    elif subject == 'program':
        app.config['UPLOAD_FOLDER'] = 'static/assets/programs'
    elif subject == 'paper':
        app.config['UPLOAD_FOLDER'] = 'assets/papers'
    elif subject == 'recipe':
        app.config['UPLOAD_FOLDER'] = 'assets/recipes'

    file_name = os.path.abspath(f"{user.file_path}")
    print(file_name)

    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    print(uploads)
    return send_from_directory(directory=uploads, path=user.file_path)


def create_pdfs(db, recipes):
    recipes = db.session.query(recipes).all()
    for r in recipes:
        if r.recipe_pdf is None:
            doc = SimpleDocTemplate(f'static/assets/recipes/{r.recipe_name}.pdf', pagesize=letter, rightMargin=72,
                                    leftMargin=72,
                                    topMargin=72, bottomMargin=18)
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justify', alignment=TA_CENTER))

            recipe = []
            print(r.file_path)
            picture = f'static/assets/recipe_image/{r.file_path}'
            recipe_picture = reportlab.platypus.Image(picture, 5 * inch, 5 * inch)

            recipe.append(Paragraph(f'{r.recipe_name}', styles["Normal"]))
            recipe.append(recipe_picture)
            recipe.append(Paragraph(f'{r.ingredients}', styles["Normal"]))
            recipe.append(Spacer(1, 12))
            recipe.append(Paragraph(f'{r.cooking_steps}', styles["Normal"]))
            doc.build(recipe)
            file_pdf = f'{r.recipe_name}.pdf'
            r.recipe_pdf = file_pdf
            db.session.commit()
        else:
            pass
