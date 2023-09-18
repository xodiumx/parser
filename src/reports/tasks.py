import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from parser.settings import SMTP_SETTINGS

from core.celery import celery_app
from db.tables_analytics import (petrovich_analytics, saturn_analytics,
                                 stroyudacha_analytics)

from .services import get_xlsx_report

smtp_host = SMTP_SETTINGS['smtp_host']
smtp_port = SMTP_SETTINGS['smtp_port']
smtp_username = SMTP_SETTINGS['smtp_username']
smtp_password = SMTP_SETTINGS['smtp_password']
sender_email = SMTP_SETTINGS['sender_email']
receiver_email = SMTP_SETTINGS['receiver_email']


@celery_app.task
def send_reports() -> str:
    """Функция отправки аналитических отчетов на почту."""
    analytics_tables = (
        petrovich_analytics, stroyudacha_analytics, saturn_analytics
    )
    for table in analytics_tables:

        report_name, csv_name = get_xlsx_report(table)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f'Analytical report {report_name}'

        with open(report_name, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={report_name}'
            )
            msg.attach(part)

        smtp = smtplib.SMTP_SSL(smtp_host, smtp_port)
        smtp.connect(smtp_host, smtp_port)
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(sender_email, receiver_email, msg.as_string())
        smtp.close()

        os.remove(report_name)
        os.remove(csv_name)

    return f'Аналитические отчеты успешно отправлены на {receiver_email}'
