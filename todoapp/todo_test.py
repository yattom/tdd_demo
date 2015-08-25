# coding: utf-8

from todoapp import todo

def test_最初は空():
    assert todo.get_all() == []
