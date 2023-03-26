from datetime import datetime

from pydantic import (BaseModel, HttpUrl, IPvAnyAddress, root_validator,
                      validator)

from core.config import app_settings


class LinkBase(BaseModel):
    original_url: HttpUrl

    @validator("original_url", pre=True)
    @classmethod
    def prepend_http(cls, value):
        if isinstance(value, str) and not value.startswith("http"):
            return f"http://{value}"
        return value


class LinkCreate(LinkBase):
    pass


class LinkBulkCreate(BaseModel):
    links: list[LinkBase]


class LinkUpdate(LinkBase):
    pass


class LinkInDBBase(LinkBase):
    id: str
    original_url: HttpUrl
    created_at: datetime
    deleted: bool

    class Config:
        orm_mode = True


class Link(LinkInDBBase):
    short_link_full: str = ""

    @root_validator()
    @classmethod
    def validate_atts(cls, values):
        id = values.get("id")
        host = f"{app_settings.project_host}:{app_settings.project_port}"
        values["short_link_full"] = f"http://{host}/{id}"
        return values


class TransferBase(BaseModel):
    client_host: IPvAnyAddress
    link_id: str


class TransferUpdate(TransferBase):
    pass


class TransferCreate(TransferBase):
    pass


class TransferInDBBase(TransferBase):
    id: int
    date: datetime
    client_host: IPvAnyAddress
    link_id: str

    class Config:
        orm_mode = True


class Transfer(TransferInDBBase):
    pass


class TransferStatus(BaseModel):
    date: datetime
    client_host: IPvAnyAddress

    class Config:
        orm_mode = True


class StatusBase(Link):
    transfer_count: int


class StatusFullBase(Link):
    transfer: list[TransferStatus] = []
