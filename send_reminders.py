from sqlalchemy import create_engine, text
from mailer import send_sales_reminder
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}
)


def send_all_reminders():

    with engine.connect() as conn:

        users = conn.execute(
            text("""
            SELECT
                full_name,
                email
            FROM users
            WHERE
                receive_sales_reminder = TRUE
            AND
                role = 'employee'
            ORDER BY full_name
            """)
        ).fetchall()

    for row in users:

        try:

            send_sales_reminder(
                row.full_name,
                row.email
            )

            print("Sent to", row.full_name)

        except Exception as e:

            print(e)


if __name__ == "__main__":
    send_all_reminders()
