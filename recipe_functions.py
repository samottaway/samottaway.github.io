import os

import PIL
from PIL import Image
import PIL
import imghdr
def remove_recipe(db,Recipes,os,text):
    check_project = db.session.execute(db.select(Recipes).where(Recipes.id == text))
    art_project = check_project.scalar()
    os.remove(f'static/assets/recipes/{art_project.recipe_pdf}')
    os.remove(f'static/assets/recipe_image/{art_project.file_path}')
    entry = Recipes.query.filter_by(id=text).first()
    db.session.delete(entry)
    db.session.commit()
    return "deleted"


def link_to_recipe(db,os,Recipes,text,app):
    check_project = db.session.execute(db.select(Recipes).where(Recipes.id == text))
    art_project = check_project.scalar()
    app.config['UPLOAD_FOLDER'] = 'static/assets/recipes'
    print(art_project.recipe_pdf)

    file_name = os.path.abspath(f"{art_project.recipe_pdf}")
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return uploads,art_project

def make_new_recipe(add_recipe_form,db,Recipes,datetime,redirect,url_for):
    check = str(add_recipe_form.recipe_name.data)
    index = check.find('/')
    if index <= 0:
        add_recipe_form.file.data.save(f"static/assets/recipe_image/{add_recipe_form.file.data.filename}")

        recipe = Recipes(
            file_path=add_recipe_form.file.data.filename,
            cooking_steps=add_recipe_form.cooking_steps.data,
            ingredients=add_recipe_form.ingredients.data,
            recipe_name=add_recipe_form.recipe_name.data,
            description=add_recipe_form.description.data,
            recipe_date=datetime.datetime.today(),
            subject='recipe')
        db.session.add(recipe)
        db.session.commit()
        return db,True


def convert_image_food(db, Recipes):
    art = db.session.query(Recipes).all()
    type = True
    for a in art:
        file_name, file_extension = os.path.splitext(f'f"static/assets/recipe_image/{a.file_path}')
        file_types =['JPG',
    'PNG'
   ' GIF'
    'WEBP'
    'TIFF'
   ' PSD'
   ' RAW'
    'BMP'
    'HEIF'
    'INDD'
   ' JPEG 2000','jpeg']

        #if file_extension in file_types:
        test = imghdr.what(f"static/assets/recipe_image/{a.file_path}")
        print(test)
        if test != None:
            im = PIL.Image.open((f"static/assets/recipe_image/{a.file_path}"))
            print(im.size)
            size=(50, 50)
            im = im.resize(size)
            im.save(f"static/assets/recipe_image/{a.recipe_name}.png")
            print(im.size)

            if file_extension != ".png":
                os.remove(f'static/assets/recipe_image/{a.file_path}')
                a.file_path = f"{a.recipe_name}.png"
        else:
            check_project = db.session.execute(db.select(Recipes).where(Recipes.id == a.id))
            art_project = check_project.scalar()
            if art_project.recipe_pdf != None:
               os.remove(f'static/assets/recipes/{art_project.recipe_pdf}')
               os.remove(f'static/assets/recipe_image/{art_project.file_path}')

            entry = Recipes.query.filter_by(id=a.id).first()
            db.session.delete(entry)
            db.session.commit()