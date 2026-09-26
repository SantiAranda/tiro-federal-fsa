from typing import Sequence

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.modules.users.user_model import User
from app.api.modules.users.user_repository import (
    IUserRepository,
    UserRepository,
)
from app.api.modules.users.user_schema import UserCreate, UserUpdate
from app.core.db import get_db
from app.core.security import get_password_hash


class UserService:
    """
    Capa de Lógica de Negocio (SRP & DIP).
    Encapsula reglas de negocio, validaciones y hashing de contraseñas.
    """

    def __init__(self, repository: IUserRepository) -> None:
        self.repository = repository

    def get_by_id(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado",
            )
        return user

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[User]:
        return self.repository.get_all(skip=skip, limit=limit)

    def create(self, user_in: UserCreate) -> User:
        # Validación: Username duplicado
        if self.repository.get_by_username(user_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya se encuentra registrado",
            )

        # Validación: Email duplicado
        if self.repository.get_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado",
            )

        # Validación: DNI duplicado si se incluye datos personales
        if user_in.personal_data:
            if self.repository.get_by_dni(user_in.personal_data.dni):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El DNI ya se encuentra registrado en el sistema",
                )

        hashed_password = get_password_hash(user_in.password)
        return self.repository.create(user_in=user_in, hashed_password=hashed_password)

    def update(self, user_id: int, user_in: UserUpdate) -> User:
        db_user = self.get_by_id(user_id)

        if user_in.username and user_in.username != db_user.username:
            if self.repository.get_by_username(user_in.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya está en uso",
                )

        if user_in.email and user_in.email != db_user.email:
            if self.repository.get_by_email(user_in.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El correo electrónico ya está en uso",
                )

        if user_in.personal_data and user_in.personal_data.dni:
            existing_dni_entry = self.repository.get_by_dni(user_in.personal_data.dni)
            if existing_dni_entry and existing_dni_entry.user_id != db_user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El DNI ya se encuentra registrado por otro usuario",
                )

        hashed_password = None
        if user_in.password:
            hashed_password = get_password_hash(user_in.password)

        return self.repository.update(
            db_user=db_user,
            user_in=user_in,
            hashed_password=hashed_password,
        )

    def delete(self, user_id: int) -> None:
        db_user = self.get_by_id(user_id)
        self.repository.delete(db_user)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """
    Proveedor de inyección de dependencias para FastAPI (DIP).
    """
    repository = UserRepository(db)
    return UserService(repository)
