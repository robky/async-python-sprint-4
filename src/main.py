from typing import Any

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from api.v1 import base_api
from core.config import app_settings
from db.database import get_session
from schemas.short_link_schema import TransferCreate
from services.short_link_crud import link_crud, transfer_crud

app = FastAPI(
    title=app_settings.PROJECT_NAME,
    # Адрес документации
    docs_url="/api/openapi",
    # Адрес документации в формате OpenAPI
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(base_api.api_router, prefix="/api/v1")


@app.get("/{id}", tags=["Transfer link"])
async def transfer_link(
    *,
    request: Request,
    db: AsyncSession = Depends(get_session),
    id: str,
) -> Any:
    """
    Safe transfer action and redirect to original link.
    """
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
    transfer_in = TransferCreate(
        client_host=client_host,
        link_id=link.id,
    )
    await transfer_crud.create(db, obj_in=transfer_in)
    return RedirectResponse(link.original_url)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=app_settings.PROJECT_HOST,
        port=app_settings.PROJECT_PORT,
        reload=True,
    )
