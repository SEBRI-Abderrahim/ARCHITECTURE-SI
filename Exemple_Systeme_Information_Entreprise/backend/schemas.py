from pydantic import BaseModel, EmailStr, ConfigDict, Field

class EmployeeBase(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=254)
    department: str = Field(min_length=2, max_length=80)
    job_title: str = Field(min_length=2, max_length=100)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
