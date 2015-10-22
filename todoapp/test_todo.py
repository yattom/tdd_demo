import pytest

class ToDo:
    _todos = []

    @staticmethod
    def get_first():
        return ToDo._todos[0]

    @staticmethod
    def get_last():
        return ToDo._todos[-1]

    @staticmethod
    def add(todo):
        ToDo._todos.append(todo)

    @staticmethod
    def clear():
        ToDo._todos = []

def add_itmes(*todos):
    for todo in todos:
        ToDo.add(todo)


def test_add_an_item():
    ToDo.clear()
    ToDo.add("buy milk")
    assert "buy milk" == ToDo.get_first()


def test_add_two_items():
    ToDo.clear()
    add_itmes("buy milk", "walk dog")
    assert "buy milk" == ToDo.get_first()

def test_add_two_items_and_get_last():
    ToDo.clear()
    add_itmes("buy milk", "walk dog")
    assert "walk dog" == ToDo.get_last()

def test_add_three_items_and_get_last():
    ToDo.clear()
    add_itmes("buy milk", "walk dog", "get drunk")
    assert "get drunk" == ToDo.get_last()

