# coding: utf-8

import pytest

from todoapp import todo

def test_最初は空():
    assert todo.get_last() == None

