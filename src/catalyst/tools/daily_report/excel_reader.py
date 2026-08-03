from dataclasses import dataclass
from datetime import date

import openpyxl

SHEET_NAME = "Users"


@dataclass
class Comment:
    date: date
    user_name: str
    comment: str
    link: str
    country: str
    follower_count: int
    tone: str


def read_comments(path) -> list[Comment]:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[SHEET_NAME]

    comments = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if all(value is None for value in row):
            continue
        raw_date, user_name, comment, link, country, follower_count, tone = row
        comments.append(
            Comment(
                date=raw_date.date() if hasattr(raw_date, "date") else raw_date,
                user_name=user_name,
                comment=comment,
                link=link,
                country=country,
                follower_count=follower_count,
                tone=tone,
            )
        )
    return comments
