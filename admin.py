from sqladmin import ModelView
from wtforms import SelectMultipleField, StringField, TextAreaField, FileField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import os

from models import Category, Hero, Project, Contact, About, Technology, ContactAbout, ContactSocial, Stats
from database import SessionLocal

class HeroAdmin(ModelView, model=Hero):
    column_list = [Hero.id, Hero.name, Hero.profession, Hero.description, Hero.image]
    # form_excluded_columns ni olib tashlang yoki comment qiling
    form_columns = [Hero.name, Hero.profession, Hero.description, Hero.image]

    async def scaffold_form(self, form_create_rules=None):
        form = await super().scaffold_form()
        form.description = TextAreaField("Description", validators=[DataRequired()])
        form.image = FileField("Rasm yuklash")  # image ni FileField qilib qo'shing
        return form

    async def on_model_change(self, data, model, is_created, request):
        form = await request.form()
        image_file = form.get("image")

        # Agar yangi rasm yuklanmagan bo'lsa, mavjud rasmni saqlab qolish
        if image_file and hasattr(image_file, "filename") and image_file.filename:
            filename = image_file.filename
            save_path = f"static/uploads/{filename}"

            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(await image_file.read())

            model.image = f"/static/uploads/{filename}"
        # Yangi rasm yuklanmagan va model yangi yaratilayotgan bo'lsa
        elif is_created and not model.image:
            model.image = "/static/uploads/default.jpg"  # default rasm

        return await super().on_model_change(data, model, is_created, request)

class AboutAdmin(ModelView, model=About):
    column_list = [About.id, About.description, About.image]
    # form_excluded_columns ni olib tashlang
    form_columns = [About.description, About.image]

    async def scaffold_form(self, form_create_rules=None):
        form = await super().scaffold_form()
        form.description = TextAreaField("Description", validators=[DataRequired()])
        form.image = FileField("Rasm yuklash")  # image ni FileField qilib qo'shing
        return form

    async def on_model_change(self, data, model, is_created, request):
        form = await request.form()
        image_file = form.get("image")

        if image_file and hasattr(image_file, "filename") and image_file.filename:
            filename = image_file.filename
            save_path = f"static/uploads/{filename}"

            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(await image_file.read())

            model.image = f"/static/uploads/{filename}"
        elif is_created and not model.image:
            model.image = "/static/uploads/default.jpg"

        return await super().on_model_change(data, model, is_created, request)

class StatsAdmin(ModelView, model=Stats):
    column_list = [Stats.id, Stats.title, Stats.value]
    form_columns = [Stats.title, Stats.value]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name]
    form_columns = [Category.name]

class TechnologyAdmin(ModelView, model=Technology):
    column_list = [Technology.id, Technology.name, Technology.proficiency, Technology.category]
    form_columns = [Technology.name, Technology.proficiency, Technology.category]
    
    async def scaffold_form(self, form_create_rules=None):
        form = await super().scaffold_form()
        
        db = SessionLocal()
        try:
            categories = db.query(Category).all()
            category_choices = [(str(cat.id), cat.name) for cat in categories]
            
            form.category = SelectField("Category", choices=category_choices, coerce=int, validators=[DataRequired()])
            form.proficiency = IntegerField("Proficiency (0-100)", validators=[DataRequired(), NumberRange(min=0, max=100)])
        finally:
            db.close()
        
        return form

class ProjectAdmin(ModelView, model=Project):
    column_list = [
        Project.id, Project.title, Project.description,
        Project.technologies, Project.image, Project.link_demo, Project.link_git_github
    ]
    # form_excluded_columns ni olib tashlang
    form_columns = [Project.title, Project.description, Project.technologies, Project.image, Project.link_demo, Project.link_git_github]

    async def scaffold_form(self, form_create_rules=None):
        form = await super().scaffold_form()
        form.description = TextAreaField("Description", validators=[DataRequired()])
        form.image = FileField("Rasm yuklash")  # image ni FileField qilib qo'shing
        return form

    async def on_model_change(self, data, model, is_created, request):
        form = await request.form()
        image_file = form.get("image")

        if image_file and hasattr(image_file, "filename") and image_file.filename:
            filename = image_file.filename
            save_path = f"static/uploads/{filename}"

            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(await image_file.read())

            model.image = f"/static/uploads/{filename}"
        elif is_created and not model.image:
            model.image = "/static/uploads/default.jpg"

        return await super().on_model_change(data, model, is_created, request)

class ContactAboutAdmin(ModelView, model=ContactAbout):
    column_list = [ContactAbout.id, ContactAbout.title, ContactAbout.icon]
    # form_excluded_columns ni olib tashlang
    form_columns = [ContactAbout.title, ContactAbout.icon]

    async def scaffold_form(self, form_create_rules=None):
        form = await super().scaffold_form()
        form.title = TextAreaField("Title", validators=[DataRequired()])
        form.icon = FileField("Icon yuklash")  # icon ni FileField qilib qo'shing
        return form

    async def on_model_change(self, data, model, is_created, request):
        form = await request.form()
        icon_file = form.get("icon")

        if icon_file and hasattr(icon_file, "filename") and icon_file.filename:
            filename = icon_file.filename
            save_path = f"static/uploads/{filename}"

            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(await icon_file.read())

            model.icon = f"/static/uploads/{filename}"
        elif is_created and not model.icon:
            model.icon = "/static/uploads/default-icon.png"

        return await super().on_model_change(data, model, is_created, request)

class ContactSocialAdmin(ModelView, model=ContactSocial):
    column_list = [
        ContactSocial.id, ContactSocial.platform, ContactSocial.link
    ]
    form_columns = [ContactSocial.platform, ContactSocial.link]

class ContactAdmin(ModelView, model=Contact):
    column_list = [
        Contact.id, Contact.name, Contact.email,
        Contact.subject, Contact.message
    ]
    form_columns = [Contact.name, Contact.email, Contact.subject, Contact.message]