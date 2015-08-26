# coding: utf-8

TODO = 0

todos = []

def get_all():
    return todos

def put(text, state, due):
    item = {'text': text, 'state': state, 'due': due}
    todos.append(item)
