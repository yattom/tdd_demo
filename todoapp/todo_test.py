# coding: utf-8

from todoapp import todo

def test_最初は空():
    assert todo.get_all() == []

def test_追加したものを取得できる():
    todo.put('TODO1')
    assert todo.get_all() == ['TODO1']
