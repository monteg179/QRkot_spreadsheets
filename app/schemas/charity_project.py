from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel as BaseSchema,
    Extra,
    Field,
    validator,
)

from app.models.charity import CharityProject as CharityProjectModel


class CharityProjectUpdate(BaseSchema):

    name: str = Field(
        default=None,
        min_length=1,
        max_length=CharityProjectModel.NAME_MAX_LENGTH
    )
    description: str = Field(
        default=None,
        min_length=1
    )
    full_amount: int = Field(
        default=None,
        gt=0
    )

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(BaseSchema):
    name: str = Field(
        min_length=1,
        max_length=CharityProjectModel.NAME_MAX_LENGTH
    )
    description: str = Field(min_length=1)
    full_amount: int = Field(gt=0)

    @validator('name', 'description')
    def none_and_empty_not_allowed(cls, value: str):
        if not value or value is None:
            raise ValueError('Все поля обязательны.')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
