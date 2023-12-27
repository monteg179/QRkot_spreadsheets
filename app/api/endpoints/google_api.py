from aiogoogle import Aiogoogle
from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value,
)
from app.schemas.google_api import GoogleResponse

router = APIRouter()


@router.get(
    path='/',
    response_model=GoogleResponse,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charityproject_crud.get_projects_by_completion_rate(
        session=session
    )
    spreadsheet = await spreadsheets_create(wrapper_services)
    spreadsheet_id = spreadsheet['spreadsheetId']
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(
        spreadsheet_id,
        projects,
        wrapper_services
    )
    return GoogleResponse(url=spreadsheet['spreadsheetUrl'])
