from typing import Protocol, Sequence

from sqlalchemy.orm import Session

from app.api.modules.users.user_model import User, UserPersonalData
from app.api.modules.users.user_schema import (
    UserCreate,
    UserPersonalDataCreate,
    UserUpdate,
)


class IUserRepository(Protocol):
    def get_by_id(self, user_id: int) -> User | None: ...

    def get_by_username(self, username: str) -> User | None: ...

    def get_by_email(self, email: str) -> User | None: ...

    def get_by_dni(self, dni: str) -> UserPersonalData | None: ...

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[User]: ...

    def create(self, user_in: UserCreate, hashed_password: str) -> User: ...

    def update(
        self, db_user: User, user_in: UserUpdate, hashed_password: str | None = None
    ) -> User: ...

    def delete(self, db_user: User) -> None: ...


class UserRepository:
    """
    Implementación concreta de persistencia usando SQLAlchemy (SRP & LSP).
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_dni(self, dni: str) -> UserPersonalData | None:
        return (
            self.db.query(UserPersonalData).filter(UserPersonalData.dni == dni).first()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, user_in: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=user_in.is_active,
        )

        if user_in.personal_data:
            personal_data = UserPersonalData(
                name=user_in.personal_data.name,
                lastname=user_in.personal_data.lastname,
                dni=user_in.personal_data.dni,
                birthdate=user_in.personal_data.birthdate,
                telephone=user_in.personal_data.telephone,
                domicile=user_in.personal_data.domicile,
            )
            db_user.personal_data = personal_data

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(
        self,
        db_user: User,
        user_in: UserUpdate,
        hashed_password: str | None = None,
    ) -> User:
        if user_in.username is not None:
            db_user.username = user_in.username
        if user_in.email is not None:
            db_user.email = user_in.email
        if user_in.is_active is not None:
            db_user.is_active = user_in.is_active
        if hashed_password is not None:
            db_user.hashed_password = hashed_password

        if user_in.personal_data is not None:
            pd_data = user_in.personal_data
            if db_user.personal_data is None:
                db_user.personal_data = UserPersonalData(
                    user_id=db_user.id,
                    name=pd_data.name or "",
                    lastname=pd_data.lastname or "",
                    dni=pd_data.dni or "",
                    birthdate=pd_data.birthdate,
                    telephone=pd_data.telephone,
                    domicile=pd_data.domicile,
                )
            else:
                if pd_data.name is not None:
                    db_user.personal_data.name = pd_data.name
                if pd_data.lastname is not None:
                    db_user.personal_data.lastname = pd_data.lastname
                if pd_data.dni is not None:
                    db_user.personal_data.dni = pd_data.dni
                if pd_data.birthdate is not None:
                    db_user.personal_data.birthdate = pd_data.birthdate
                if pd_data.telephone is not None:
                    db_user.personal_data.telephone = pd_data.telephone
                if pd_data.domicile is not None:
                    db_user.personal_data.domicile = pd_data.domicile

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, db_user: User) -> None:
        self.db.delete(db_user)
        self.db.commit()
