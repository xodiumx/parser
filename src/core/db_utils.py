from datetime import datetime, timezone

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import Table


def create_db_objects(
        table: Table,
        data: dict,
        db_session: Session) -> None:
    """функция создания объектов в базе данных."""
    statement = insert(table).values(data)

    db_session.execute(statement)
    db_session.commit()

    print(f'{len(data)} объектов созданы в таблице {table}')


def get_db_objects(
        table: Table,
        db_session: Session) -> list[tuple]:
    """Функция получения всех объектов в таблице."""
    query = select(table)
    return db_session.execute(query).all()


def get_todays_data(
        table: Table,
        db_session: Session) -> list[tuple]:
    """Функция получения данных полученых сегодня."""
    today = datetime.now(timezone.utc).date()
    query = select(table).where(table.c.created_at == today)
    return db_session.execute(query).all()


def delete_all_db_objects(
        table: Table,
        db_session: Session) -> None:
    query = delete(table)
    db_session.execute(query)
    db_session.commit()

    print(f'Данные из таблицы {table} успешно удалены.')
