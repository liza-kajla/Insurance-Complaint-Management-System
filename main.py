from fastapi import FastAPI, Depends, HTTPException, Header, UploadFile, File
 
from sqlalchemy.orm import Session
 
from database import engine, get_db
 
from models import Base, Complaint
 
from schemas import UserRegistration
 
from schemas import UserLogin
 
from schemas import ComplaintCreate
 
from schemas import ComplaintUpdate
 
from jose import jwt, JWTError
 
from passlib.context import CryptContext
 
import shutil
 
import os
 
Base.metadata.create_all(bind=engine)
 
app = FastAPI()
 
# implimenting password hashing
pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto")
 
def hash_password(password):
    return pwd_context.hash(password)
#------------------------------------------------------------------------------------------------------#
def verify_password(plain_password, hashed_password):
 
    return pwd_context.verify(plain_password, hashed_password)
 
#------------------------------------------------------------------------------------------------------#
#Implimenting JWT tokens
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
 
def create_token(data: dict):
 
    token = jwt.encode(
 
        data,
 
        SECRET_KEY,
 
        algorithm = ALGORITHM
    )
 
    return token
 
#------------------------------------------------------------------------------------------------------#
# verify token sent in the header and pull out the username
def verify_token(authorization: str = Header(...)):
 
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header")
 
    token = authorization.split(" ")[1]
 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
 
    username = payload.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
 
    return username
 
#------------------------------------------------------------------------------------------------------#
@app.post("/register")
def register_user(user : UserRegistration, db = Depends(get_db)):
 
    existing_user = db.query(Complaint).filter(Complaint.username == user.username).first()
 
    if existing_user:
        raise HTTPException(status_code=400, detail = "User already Exists")
 
    new_user = Complaint(id = user.id, username = user.username, password = hash_password(user.password), role = user.role)
 
    db.add(new_user)
 
    db.commit()
 
    return{"message" : "user registeration done"}
 
#--------------------------------------------------------------------------------------------------#
@app.post("/login")
def login_user(user: UserLogin, db = Depends(get_db)):
    existing_user = db.query(Complaint).filter(Complaint.username == user.username).first()
    if existing_user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code = 401, detail = "Incorrect Password!")
    token = create_token({"username": user.username})
    return{"access_token": token}
 
#-----------------------------------------------------------------------------------------------------#
@app.get("/protected")
def protected_route(username: str = Depends(verify_token)):
    return {"message": f"Access granted, welcome {username}"}
 
#-----------------------------------------------------------------------------------------------------#
@app.post("/create_complaint")
def create_complaint(
    complaint: ComplaintCreate,
    db = Depends(get_db),
    username: str = Depends(verify_token)
):
    user = db.query(Complaint).filter(Complaint.username == username).first()
 
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
 
    user.insurance_product = complaint.insurance_product
    user.complaint_text = complaint.complaint_text
    user.complaint_category = complaint.complaint_category
 
    db.commit()
    db.refresh(user)
 
    return {
        "message": "Complaint Created Successfully",
        "data": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "insurance_product": user.insurance_product,
            "complaint_text": user.complaint_text,
            "complaint_category": user.complaint_category
        }
    }
 
#-----------------------------------------------------------------------------------------------------#
@app.get("/view_complaints")
def view_complaints(skip: int = 0, limit: int = 5, db = Depends(get_db), username: str = Depends(verify_token)):
    complaints = (db.query(Complaint)
             .filter(Complaint.complaint_text.isnot(None))
             .order_by(Complaint.id)
             .offset(skip)
             .limit(limit)
             .all()
    )
    return complaints
 
#------------------------------------------------------------------------------------------------------#
@app.put("/update_complaint/{id}")
def update_complaint(id: int, complaint: ComplaintUpdate, db = Depends(get_db), username: str = Depends(verify_token)):
 
    existing_complaint = db.query(Complaint).filter(Complaint.id == id).first()
 
    if existing_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
 
    existing_complaint.insurance_product = complaint.insurance_product
    existing_complaint.complaint_text = complaint.complaint_text
    existing_complaint.complaint_category = complaint.complaint_category
 
    db.commit()
 
    return {"message": "Complaint Updated Successfully"}
 
#------------------------------------------------------------------------------------------------------#
@app.delete("/delete_complaint/{id}")
def delete_complaint(id: int, db = Depends(get_db), username: str = Depends(verify_token)):
 
    existing_complaint = db.query(Complaint).filter(Complaint.id == id).first()
 
    if existing_complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
 
    db.delete(existing_complaint)
    db.commit()
 
    return {"message": "Complaint Deleted Successfully"}
 
#------------------------------------------------------------------------------------------------------#
@app.get("/search_complaint")
def search_complaint(insurance_product: str, db = Depends(get_db), username: str = Depends(verify_token)):
    complaints = db.query(Complaint).filter(Complaint.insurance_product.contains(insurance_product)).all()
    return complaints
 
#------------------------------------------------------------------------------------------------------#
@app.get("/filter_complaint")
def filter_complaint(complaint_category: str = None, db = Depends(get_db), username: str = Depends(verify_token)):
    query = db.query(Complaint)
 
    if complaint_category:
        query = query.filter(Complaint.complaint_category == complaint_category)
 
    return query.all()
 
#------------------------------------------------------------------------------------------------------#
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
@app.post("/upload")
def upload_file(file: UploadFile = File(...), username: str = Depends(verify_token)):
 
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
 
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
 
    return {"filename": file.filename}