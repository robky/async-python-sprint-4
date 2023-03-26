from datetime import datetime
from random import choice

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        func, select)
from sqlalchemy.orm import column_property, relationship

from core.config import app_settings
from db.database import Base


def generate_short_link():
    string = "2345679abcdefghijkmnopqrstuvwxyzABCEFGHJKLMNPRSTUVWXYZ"
    return "".join(
        choice(string) for _ in range(app_settings.short_link_length)
    )


class Transfer(Base):
    __tablename__ = "transfer"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, index=True, default=datetime.utcnow)
    client_host = Column(String(40))
    link_id = Column(String, ForeignKey("link.id"))

    link = relationship("Link", back_populates="transfer")


class Link(Base):
    __tablename__ = "link"
    id = Column(String(12), primary_key=True, default=generate_short_link)
    original_url = Column(String(100), nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    deleted = Column(Boolean, default=False)

    transfer = relationship(
        "Transfer",
        cascade="all, delete",
        back_populates="link",
        lazy="selectin",
    )

    transfer_count = column_property(
        select(func.count(Transfer.id))
        .filter(Transfer.link_id == id)
        .scalar_subquery()
    )
