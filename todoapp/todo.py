# coding: utf-8


todos = []

class ToDo:
    def __init__(self, text, assigned_to, due):
        self.text = text
        self.assigned_to = assigned_to
        self.due = due

def append(text, assigned_to=None, due=None):
    todos.append(ToDo(text, assigned_to, due))

def get_last():
    if not todos:
        return None
    return todos[-1]
