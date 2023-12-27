from pydantic import BaseModel as BaseSchema


class GoogleResponse(BaseSchema):
    url: str
