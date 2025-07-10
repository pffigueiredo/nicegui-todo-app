from nicegui import Client, ui
from app import todo_app


def startup() -> None:
    todo_app.create()