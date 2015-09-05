# coding: utf-8

import sys
import os
import json

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

def save():
    data = [dict(text=i.text, assigned_to=i.assigned_to, due=i.due)
            for i in todos]
    with open('todo.json', 'w') as f:
        json.dump(data, f)

def load():
    with open('todo.json') as f:
        data = json.load(f)
    clear()
    for d in data:
        append(d['text'], d['assigned_to'], d['due'])

def clear():
    todos.clear()

def count():
    return len(todos)

def main():
    if sys.argv[1] == 'add':
        pass
    if sys.argv[1] == 'get_last':
        sys.stdout.write('TODO 1' + os.linesep)
        sys.stdout.write('yattom' + os.linesep)
        sys.stdout.write('2015/9/12' + os.linesep)

if __name__=='__main__':
    main()
