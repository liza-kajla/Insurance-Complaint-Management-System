from pydantic import BaseModel

#------------------------------------------------------------------------------------------------------#
class UserRegistration(BaseModel):
    id: int
    username: str
    password: str
    role: str

#------------------------------------------------------------------------------------------------------#
class UserLogin(BaseModel):
    username: str
    password: str

#------------------------------------------------------------------------------------------------------#
class ComplaintCreate(BaseModel):
    insurance_product: str
    complaint_text: str
    complaint_category: str

#------------------------------------------------------------------------------------------------------#
class ComplaintUpdate(BaseModel):
    insurance_product: str
    complaint_text: str
    complaint_category: str