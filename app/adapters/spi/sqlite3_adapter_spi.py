import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import logging

from app.core.model.call import Call

Row = tuple[int, str, int, int, str]
NewRow = tuple[None, str, int, int, str]


def call_to_row(call: Call) -> Row | NewRow:
    return (
        call.id,
        call.phone_number,
        round(call.start_time.timestamp()),
        round(call.duration.total_seconds()),
        json.dumps(call.cases)
    )


def row_to_call(row: Row) -> Call:
    _id, phone_number, start, duration, cases = row
    return Call(_id, phone_number, datetime.fromtimestamp(start), timedelta(seconds=duration),
                tuple(json.loads(cases)))


class SQLite3AdapterSPI:
    def __init__(self, database: Path):
        self.database = database

        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    CREATE TABLE "call" (
                        "id" INTEGER NOT NULL PRIMARY KEY,
                        "phone_number" TEXT,
                        "start_time"  INTEGER,
                        "duration" INTEGER,
                        "cases" TEXT
                    );
                """)
                connection.commit()
            except sqlite3.OperationalError:
                logging.debug("Table \"call\" already created")

    def store_call(self, call: Call) -> Call:
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            id_ = cursor.execute(
                """
                    INSERT INTO "call" (
                        "id",
                        "phone_number",
                        "start_time",
                        "duration",
                        "cases"
                    )
                    VALUES (?, ?, ?, ?, ?);
                """,
                call_to_row(call)
            ).lastrowid
            connection.commit()
            return Call(id_, call.phone_number, call.start_time, call.duration, call.cases)

    def delete_call(self, id_: int) -> Call:
        call = self.get_call(id_)
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM "call" WHERE "id"=?;""", (id_,))
            connection.commit()
        return call

    def update_call(self, call: Call) -> Call:
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                    UPDATE "call" SET
                        "phone_number"=?,
                        "start_time"=?,
                        "duration"=?,
                        "cases"=?
                    WHERE "id"=?;
                """,
                (*call_to_row(call)[1:], call.id)
            )
            connection.commit()
        return call

    def get_call(self, id_: int) -> Call:
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM "call" WHERE "id"=?;""", (id_,))
            return row_to_call(cursor.fetchone())

    def get_calls_by_date_range(self, start: datetime, end: datetime) -> tuple[Call, ...]:
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT * FROM "call" WHERE "start_time" BETWEEN ? AND ? ORDER BY "start_time" ASC;""",
                (round(start.timestamp()), round(end.timestamp()))
            )
            return tuple(map(row_to_call, cursor.fetchall()))
