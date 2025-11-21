# backend/main.py
from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from fastapi.staticfiles import StaticFiles
import os, shutil
from .database import Base, engine, SessionLocal
from .admin import CategoryAdmin, ContactAboutAdmin, ContactSocialAdmin, HeroAdmin, ProjectAdmin, ContactAdmin, AboutAdmin, TechnologyAdmin,StatsAdmin
from .models import Category, Hero, Project, Contact, About, Technology, ContactAbout, ContactSocial,Stats
from pydantic import BaseModel


app = FastAPI(title="Portfolio API")

# Ma'lumotlar bazasini yaratamiz
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin panel
admin = Admin(app, engine)
admin.add_view(HeroAdmin)
admin.add_view(AboutAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(TechnologyAdmin)
admin.add_view(ProjectAdmin)
admin.add_view(ContactAboutAdmin)
admin.add_view(ContactSocialAdmin)
admin.add_view(ContactAdmin)
admin.add_view(StatsAdmin)

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === API ===
@app.get("/hero")
def get_hero(db=Depends(get_db)):
    return db.query(Hero).first()

@app.get("/about")
def get_about(db=Depends(get_db)):
    return db.query(About).all()

# === Stats API ===
@app.get("/stats")
def get_stats(db=Depends(get_db)):
    return db.query(Stats).all()

@app.get("/categories")
def get_categories(db=Depends(get_db)):
    return db.query(Category).all()

@app.get("/technologies")
def get_technologies(db=Depends(get_db)):
    return db.query(Technology).all()

@app.get("/projects")
def get_projects(db=Depends(get_db)):
    projects = db.query(Project).all()
    # Ensure technologies are loaded
    for project in projects:
        project.technologies
    return projects

@app.get("/contactsAbout")
def get_contacts_about(db=Depends(get_db)):
    return db.query(ContactAbout).all()

@app.get("/contactsSocial")
def get_contacts_social(db=Depends(get_db)):
    return db.query(ContactSocial).all()

class ContactMessage(BaseModel):
    name: str
    email: str
    subject: str
    message: str

@app.post("/contact")
def send_message(contact: ContactMessage, db=Depends(get_db)):
    contact_db = Contact(
        name=contact.name, 
        email=contact.email, 
        subject=contact.subject, 
        message=contact.message
    )
    db.add(contact_db)
    db.commit()
    db.refresh(contact_db)
    return {"success": True, "message": "Xabar yuborildi!"}

# === Rasm yuklash API ===
@app.post("/upload/about-image")
async def upload_about_image(file: UploadFile = File(...), db=Depends(get_db)):
    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = f"/static/uploads/{file.filename}"

    about = db.query(About).first()
    if about:
        about.image = image_url
        db.commit()
        db.refresh(about)
        return {"success": True, "url": image_url, "about": about}
    return {"error": "About ma'lumot topilmadi"}

# === Static files ===
app.mount("/static", StaticFiles(directory="static"), name="static")