from pydantic import BaseModel, ConfigDict, Field


class SBookBase(BaseModel):
    title: str
    author: str
    year: int
    pages: int = Field(gt=10)
    is_read: bool = False


class SBookAdd(SBookBase):
    pass


class SBook(SBookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# class SBookPatch(BaseModel):
#     title: str | None
#     author: str | None
#     year: int | None
#     pages: int | None = Field(None, gt=10)
#     is_read: bool | None = None
