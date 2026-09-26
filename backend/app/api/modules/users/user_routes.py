from typing import Sequence

from fastapi import APIRouter, Depends, Query, status

from app.api.modules.users.user_schema import UserCreate, UserResponse, UserUpdate
from app.api.modules.users.user_service import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
)
def create_user(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.create(user_in=user_in)


@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
)
def list_users(
    skip: int = Query(0, ge=0, description="Registros a omitir para paginación"),
    limit: int = Query(100, ge=1, le=100, description="Límite de registros a retornar"),
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_all(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
)
def get_user_by_id(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.get_by_id(user_id=user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un usuario existente",
)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    return user_service.update(user_id=user_id, user_in=user_in)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario por ID",
)
def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    user_service.delete(user_id=user_id)
