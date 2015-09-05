# coding: utf-8

import pytest

from todoapp import todo

def test_最初は空():
    assert todo.get_last() == None

def test_最後に追加した詳細を取得できる_1個追加した場合():
    todo.append('TODO 1')
    actual = todo.get_last()
    assert actual.text == 'TODO 1'
