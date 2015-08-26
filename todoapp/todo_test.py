# coding: utf-8

from todoapp import todo
from datetime import datetime, timedelta

def setup_function(fn):
    todo.clear()

def test_最初は空():
    assert todo.get_all() == []

def test_TODOの属性():
    todo.put(text='TODO1',
             state=todo.TODO,
             add_at=datetime(2015, 8, 26, 10, 0, 0),
             due=datetime(2015, 8, 26, 12, 0, 0))
    assert todo.get_all() == [{'text': 'TODO1',
                               'state': todo.TODO,
                               'add_at': datetime(2015, 8, 26, 10, 0, 0),
                               'due': datetime(2015, 8, 26, 12, 0, 0)},
                             ]

def test_TODOの属性_add_atは現在時刻():
    todo.put(text='TODO1',
             state=todo.TODO,
             due=datetime(2015, 8, 26, 12, 0, 0))
    actual = todo.get_last()['add_at']
    now = datetime.now()
    assert now - actual <= timedelta(seconds=1)

def test_最後の項目を取得する_空の場合():
    assert todo.get_last() == None

def test_最後の項目を取得する():
    todo.put(text='TODO1',
             state=todo.TODO,
             add_at=datetime(2015, 8, 26, 10, 0, 0),
             due=datetime(2015, 8, 26, 12, 0, 0))
    assert todo.get_last() == {'text': 'TODO1',
                               'state': todo.TODO,
                               'add_at': datetime(2015, 8, 26, 10, 0, 0),
                               'due': datetime(2015, 8, 26, 12, 0, 0)}
                              
