# coding: utf-8

import pytest
import datetime

from todoapp import todo

def test_最初は空():
    assert todo.get_last() == None

def test_TODOのすべての属性を取得できる():
    todo.append(text='TODO 1',
                assigned_to='yattom',
                due=datetime.date(2015, 9, 12))
    actual = todo.get_last()
    assert actual.text == 'TODO 1'
    assert actual.assigned_to == 'yattom'
    assert actual.due == datetime.date(2015, 9, 12)

def test_最後に追加した詳細を取得できる_1個追加した場合():
    todo.append('TODO 1')
    actual = todo.get_last()
    assert actual.text == 'TODO 1'

def test_最後に追加した詳細を取得できる_2個追加した場合():
    todo.append('TODO 1')
    todo.append('TODO 2')
    actual = todo.get_last()
    assert actual.text == 'TODO 2'
