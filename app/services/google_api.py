from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = '%Y/%m/%d %H:%M:%S'
TITLE = 'Отчёт по закрытым пожертвованиям на {}'
ROWS_AMOUNT = 100
COLUMNS_AMOUNT = 11


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    data = {
        'properties': {
            'title': TITLE.format(datetime.now().strftime(FORMAT)),
            'locale': 'ru_RU',
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Лист1',
                    'gridProperties': {
                        'rowCount': ROWS_AMOUNT,
                        'columnCount': COLUMNS_AMOUNT,
                    }
                }
            }
        ]
    }
    return await wrapper_services.as_service_account(
        service.spreadsheets.create(json=data)
    )


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', datetime.now().strftime(FORMAT)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        length = str(project.close_date - project.create_date)
        table_values.append([project.name, project.description, length])

    rows_value = len(table_values)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:C{rows_value}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values,
            }
        )
    )
