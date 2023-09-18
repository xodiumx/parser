from datetime import datetime, timezone

import pandas as pd
from pandas.core.frame import DataFrame
from sqlalchemy.sql.schema import Table

from core.db_utils import get_todays_data
from db.connect import get_session


def get_csv_data(table: Table) -> str:
    """Функция создания отчета в формате csv."""

    db_session = next(get_session())
    data = get_todays_data(table, db_session)

    competitor = f'{table}'.split('_')[0]
    csv_file_name = f'reports/{table}.csv'
    df = pd.DataFrame(data)
    df.to_csv(csv_file_name, index=False, sep=';')

    return csv_file_name, competitor


def highlight(
        df: DataFrame,
        col2highlite: str = 'abs_diff',
        competitor: str = None, ) -> DataFrame:
    """
    Функция покраски поля abs_diff
    - Если цена вимос меньше конкурента (зеленый)
    - Если цена вимос больше конкурента (красный)
    - Если цена вимос равна конкуренту (желтый)
    """
    ret = pd.DataFrame('', index=df.index, columns=df.columns)
    ret.loc[
        df['vimos_price'] < df[f'{competitor}_price'], col2highlite
    ] = 'background-color: lime'
    ret.loc[
        df['vimos_price'] > df[f'{competitor}_price'], col2highlite
    ] = 'background-color: orange'
    ret.loc[
        df['vimos_price'] == df[f'{competitor}_price'], col2highlite
    ] = 'background-color: yellow'
    return ret


def get_xlsx_report(table: Table) -> tuple[str]:
    """Функция создания отчета в формате xlsx."""

    today = datetime.now(timezone.utc).date()

    csv_name, competitor = get_csv_data(table)

    df = pd.read_csv(csv_name, delimiter=';')
    df = df.style.apply(
        highlight,
        col2highlite='abs_diff',
        axis=None,
        competitor=competitor
    )

    report_name = f'reports/{table}_{today}.xlsx'
    writer = pd.ExcelWriter(report_name, engine='xlsxwriter')
    df.to_excel(writer, f'{table}')
    writer._save()

    return report_name, csv_name
