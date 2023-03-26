from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from db.database import get_session
from schemas import short_link_schema
from services.short_link_crud import link_crud, transfer_crud

router_link = APIRouter()


def dashing_query(default: Any, *, convert_underscores=True, **kwargs) -> Any:
    query = Query(default, **kwargs)
    query.convert_underscores = convert_underscores
    return query


@router_link.get(
    "",
    response_model=list[short_link_schema.Link],
    description="Retrieve short links.",
)
async def read_links(
    db: AsyncSession = Depends(get_session), skip: int = 0, limit: int = 100
) -> Any:
    return await link_crud.get_multi(db, skip=skip, limit=limit)


@router_link.post(
    "/bulk",
    response_model=list[short_link_schema.Link],
    status_code=status.HTTP_201_CREATED,
    description="Bulk create new short links."
)
async def bulk_create_link(
    *,
    db: AsyncSession = Depends(get_session),
    link_in: list[short_link_schema.LinkCreate],
) -> Any:
    return await link_crud.bulk_create(db, obj_in=link_in)


@router_link.post(
    "",
    response_model=short_link_schema.Link,
    status_code=status.HTTP_201_CREATED,
    description="Create new short link."
)
async def create_link(
    *,
    db: AsyncSession = Depends(get_session),
    link_in: short_link_schema.LinkCreate,
) -> Any:
    return await link_crud.create(db, obj_in=link_in)


@router_link.get(
    "/transfer/{id}",
    tags=["Transfer link"],
    description="Safe transfer action and redirect to original link."
)
async def transfer_link(
    *,
    request: Request,
    db: AsyncSession = Depends(get_session),
    id: str,
) -> Any:
    link = await link_crud.get(db, id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
        )
    if link.deleted:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="Link removed"
        )
    client_host = request.client.host
    transfer_in = short_link_schema.TransferCreate(
        client_host=client_host,
        link_id=link.id,
    )
    await transfer_crud.create(db, obj_in=transfer_in)
    return RedirectResponse(link.original_url)


@router_link.get(
    "/ping",
    description="Get the DB availability status",
)
async def ping_db(db: AsyncSession = Depends(get_session)):
    result = await link_crud.ping(db)
    if result:
        return {"status_db": "The database is available"}
    return {"status_db": "The database is not available"}


@router_link.get(
    "/status",
    response_model=list[short_link_schema.StatusFullBase],
    tags=["Status info"],
    description="Retrieve status info."
)
async def read_retrieve_status(
    db: AsyncSession = Depends(get_session),
    full_info: Any = dashing_query(False),
    max_result: int = dashing_query(100),
    offset: int = 0,
) -> Any:
    if full_info is False:
        companies = parse_obj_as(
            list[short_link_schema.StatusBase],
            await link_crud.get_multi(db, skip=offset, limit=max_result),
        )
        return JSONResponse(jsonable_encoder(companies))
    return await link_crud.get_multi(db, skip=offset, limit=max_result)


@router_link.get(
    "/{id}",
    response_model=short_link_schema.Link,
    description="Get link by ID.",
)
async def read_link(
    *,
    db: AsyncSession = Depends(get_session),
    id: str,
) -> Any:
    link = await link_crud.get(db, id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return link


@router_link.get(
    "/{id}/status",
    response_model=short_link_schema.StatusFullBase,
    tags=["Status info"],
    description="Get status info by ID.",
)
async def read_status(
    *,
    id: str,
    db: AsyncSession = Depends(get_session),
    full_info: Any = dashing_query(False),
    max_result: int = dashing_query(100),
    offset: int = 0,
) -> Any:
    link = await link_crud.get(db, id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    if full_info is False:
        companies = parse_obj_as(list[short_link_schema.StatusBase], link)
        return JSONResponse(jsonable_encoder(companies))
    return link


@router_link.put(
    "/{id}",
    response_model=short_link_schema.Link,
    description="Update an link."
)
async def update_link(
    *,
    db: AsyncSession = Depends(get_session),
    id: str,
    link_in: short_link_schema.LinkUpdate,
) -> Any:
    link = await link_crud.get(db, id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return await link_crud.update(db, db_obj=link, obj_in=link_in)


@router_link.delete(
    "/{id}",
    response_model=short_link_schema.Link,
    description="Mark the link as deleted",
)
async def delete_link(
    *, db: AsyncSession = Depends(get_session), id: str
) -> Any:
    link = await link_crud.get(db, id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return await link_crud.delete(db, db_obj=link)
