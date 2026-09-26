from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr

# ==========================================
# Schemas para Datos Personales
# ==========================================


class UserPersonalDataBase(BaseModel):
    name: str
    lastname: str
    dni: str
    birthdate: date | None = None
    telephone: str | None = None
    domicile: str | None = None


class UserPersonalDataCreate(UserPersonalDataBase):
    pass


class UserPersonalDataUpdate(BaseModel):
    name: str | None = None
    lastname: str | None = None
    dni: str | None = None
    birthdate: date | None = None
    telephone: str | None = None
    domicile: str | None = None


class UserPersonalDataResponse(UserPersonalDataBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Schemas para Usuario
# ==========================================


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str
    personal_data: UserPersonalDataCreate | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None
    personal_data: UserPersonalDataUpdate | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    personal_data: UserPersonalDataResponse | None = None

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserResponse):
    hashed_password: str
