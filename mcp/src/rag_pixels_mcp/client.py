from pathlib import Path
from typing import Any

import httpx

from rag_pixels_mcp.config import api_base_url, auth_headers


async def request_json(
    method: str,
    path: str,
    *,
    json_body: dict[str, Any] | None = None,
    timeout: float = 60.0,
) -> dict[str, Any]:
    async with httpx.AsyncClient(
        base_url=api_base_url(),
        headers=auth_headers(),
        timeout=timeout,
    ) as client:
        response = await client.request(method, path, json=json_body)
    response.raise_for_status()
    return response.json()


async def upload_file(
    path: Path,
    *,
    form_data: dict[str, str],
    timeout: float = 120.0,
) -> dict[str, Any]:
    async with httpx.AsyncClient(
        base_url=api_base_url(),
        headers=auth_headers(),
        timeout=timeout,
    ) as client:
        with path.open("rb") as document:
            response = await client.post(
                "/documents/upload",
                data=form_data,
                files={"file": (path.name, document, "application/octet-stream")},
            )
    response.raise_for_status()
    return response.json()
