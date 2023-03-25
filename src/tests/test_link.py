import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_short_link(
    async_client: AsyncClient,
    async_session: AsyncSession,
    link_test_data: dict,
    prefix_shorten: str,
):
    # База пуста
    empty_links = await async_client.get(prefix_shorten)
    assert empty_links.status_code == status.HTTP_200_OK
    assert empty_links.json() == []

    # Добавление ссылки
    response = await async_client.post(prefix_shorten, json=link_test_data)
    assert response.status_code == status.HTTP_201_CREATED
    got_post = response.json()

    # Проверка добавленной ссылки
    links = await async_client.get(prefix_shorten)
    assert links.status_code == status.HTTP_200_OK
    got_get = response.json()
    assert got_post["id"] == got_get["id"]
    assert got_get["original_url"] == link_test_data["full_url"]

    # Получение добавленной ссылки
    link_id = got_get["id"]
    response = await async_client.get(f"{prefix_shorten}/{link_id}")
    assert response.status_code == status.HTTP_200_OK

    # Переход по ссылке
    response = await async_client.get(link_id)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.next_request.url == link_test_data["full_url"]

    # Удалить (пометить как удаленная) ссылку
    response = await async_client.delete(f"{prefix_shorten}/{link_id}")
    assert response.status_code == status.HTTP_200_OK

    # Нет перехода по "удаленной" ссылке
    response = await async_client.get(link_id)
    assert response.status_code == status.HTTP_410_GONE


@pytest.mark.asyncio
async def test_short_link_bulk_create(
    async_client: AsyncClient,
    async_session: AsyncSession,
    link_bulk_test_data: dict,
    prefix_shorten: str,
):
    # База пуста
    empty_links = await async_client.get(prefix_shorten)
    assert empty_links.status_code == status.HTTP_200_OK
    assert empty_links.json() == []

    # Добавление ссылок
    response = await async_client.post(
        f"{prefix_shorten}/bulk", json=link_bulk_test_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Добавлены все ссылки
    links = await async_client.get(prefix_shorten)
    assert empty_links.status_code == status.HTTP_200_OK
    assert len(links.json()) == len(link_bulk_test_data)
