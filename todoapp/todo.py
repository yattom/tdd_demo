# coding: utf-8

from datetime import datetime

TODO = 0

todos = []

def get_all():
    return todos

def put(text, state, due, add_at=None):
    if not add_at:
        add_at = datetime.now()
    item = {'text': text, 'state': state, 'add_at': add_at, 'due': due}
    todos.append(item)

def get_last():
    if not todos:
        return None
    return todos[-1]

def clear():
    global todos
    todos = []
