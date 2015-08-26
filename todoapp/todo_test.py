# coding: utf-8

from todoapp import todo
from datetime import datetime

def test_最初は空():
    assert todo.get_all() == []

def test_TODOの属性():
    todo.put(text='TODO1',
             state=todo.TODO,
             due=datetime(2015, 8, 26, 12, 0, 0))
    assert todo.get_all() == [{'text': 'TODO1',
                               'state': todo.TODO,
                               'due': datetime(2015, 8, 26, 12, 0, 0)},
                             ]

