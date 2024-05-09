import imghdr
import os

from PIL import Image


def convert_image(db, aart):
    art = db.session.query(aart).all()
    type = True
    for a in art:
        file_name, file_extension = os.path.splitext(f'f"static/assets/art_images/{a.file_path}')
        file_types = ['JPG',
                      'PNG'
                      ' GIF'
                      'WEBP'
                      'TIFF'
                      ' PSD'
                      ' RAW'
                      'BMP'
                      'HEIF'
                      'INDD'
                      ' JPEG 2000', 'jpeg']

        # if file_extension in file_types:
        test = imghdr.what(f"static/assets/art_images/{a.file_path}")
        print(test)
        #print(test)
        # if test is not 'None':
        #     art = db.session.query(aart).all()
        #     if os.path.isfile(f"static/assets/art_images/{a.file_path}") == False:
        #         a.file_path = f"{a.picture_name}.png"
        #         db.session.commit()
        print(file_extension)
        if file_extension == '.png' and test != 'None':
         pass


        elif test == None:
            print(a.file_path)
            os.remove(f'static/assets/art_images/{a.file_path}')
            check_project = db.session.execute(db.select(aart).where(aart.id == a.id))
            art_project = check_project.scalar()
            db.session.delete(art_project)

        else:
            im = Image.open((f"static/assets/art_images/{a.file_path}"))
            im.resize(size=(100, 100))
            im.save(f"static/assets/art_images/{a.picture_name}.png")
            im = Image.open((f"static/assets/art_images/{a.file_path}"))
            #print(im.size)
            size = (50, 50)
            im = im.resize(size)
            im.save(f"static/assets/art_images/{a.picture_name}.png")
           # print(im.size)
            os.remove(f'static/assets/art_images/{a.file_path}')
            a.file_path = f"{a.picture_name}.png"
        db.session.commit()
        print(a.file_path)

            # db.session.delete(entry)
            #
            #
            # check_project = db.session.execute(db.select(Recipes).where(Recipes.id == a.id))
            # art_project = check_project.scalar()
            # if art_project.recipe_pdf != None:
            #     os.remove(f'static/assets/recipes/{art_project.recipe_pdf}')
            #     os.remove(f'static/assets/recipe_image/{art_project.file_path}')


