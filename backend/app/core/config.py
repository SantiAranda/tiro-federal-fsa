import json
import secrets
import warnings
from typing import Annotated, Any, Literal, Self

from pydantic import BeforeValidator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str]:
    if isinstance(v, str):
        if v.startswith("[") and v.endswith("]"):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(i) for i in parsed]
            except Exception:
                pass
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list):
        return [str(i) for i in v]
    raise ValueError(f"Formato CORS inválido: {v}")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "Tiro Federal Formosa - Sistema de Gestión"
    PROJECT_VERSION: str = "0.1.0"

    ENVIRONMENT: Literal["local", "development", "staging", "production", "testing"] = (
        "local"
    )

    DOMAIN: str = "http://localhost:8000"
    FRONTEND_HOST: str = "http://localhost:3000"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 días
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./sql_app.db"
    BACKEND_CORS_ORIGINS: Annotated[list[str] | str, BeforeValidator(parse_cors)] = [
        "http://localhost:3000"
    ]

    # Credenciales de superusuario inicial
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str = "admin"

    @property
    def FASTAPI_DEBUG(self) -> bool:
        return self.ENVIRONMENT in ("local", "development", "testing")

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        """
        Verifica si el valor de una variable de entorno sensible
        es el valor predeterminado "changethis".
        """
        if value == "changethis":
            message = (
                f'El valor de {var_name} es "changethis". '
                "Por seguridad, cámbielo en entornos que no sean locales."
            )
            if self.ENVIRONMENT == "production":
                raise ValueError(message)
            else:
                warnings.warn(message, stacklevel=2)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        """
        Valida que las variables sensibles no tengan valores inseguros en producción.
        """
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )
        return self


settings = Settings()
