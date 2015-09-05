# coding: utf-8


todos = []

class ToDo:
    def __init__(self, text):
        self.text = text

def append(text):
    todos.append(ToDo(text))

def get_last():
    if not todos:
        return None
    return todos[-1]
