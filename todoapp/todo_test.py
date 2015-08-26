# coding: utf-8

from todoapp import todo
from datetime import datetime, timedelta


class Helper:
    @staticmethod
    def 初期化():
        todo.clear()

    @staticmethod
    def TODO追加(text, state=None, add_at=None, due=None):
        if not state:
            state = todo.TODO
        todo.put(text=text, state=state, add_at=add_at, due=due)

    @staticmethod
    def すべてのTODO():
        return todo.get_all()

    @staticmethod
    def 最後のTODO():
        return todo.get_last()

def setup_function(fn):
    Helper.初期化()

def test_最初は空():
    assert todo.get_all() == []

def test_TODOの属性():
    Helper.TODO追加(text='TODO1',
                    state=todo.TODO,
                    add_at=datetime(2015, 8, 26, 10, 0, 0),
                    due=datetime(2015, 8, 26, 12, 0, 0))
    assert Helper.すべてのTODO() == [{'text': 'TODO1',
                                      'state': todo.TODO,
                                      'add_at': datetime(2015, 8, 26, 10, 0, 0),
                                      'due': datetime(2015, 8, 26, 12, 0, 0)},
                                    ]

def test_TODOの属性_add_atは現在時刻():
    Helper.TODO追加(text='TODO1')
    actual = Helper.最後のTODO()['add_at']
    now = datetime.now()
    assert now - actual <= timedelta(seconds=1)

def test_最後の項目を取得する_空の場合():
    assert Helper.最後のTODO() == None

def test_最後の項目を取得する():
    Helper.TODO追加(text='TODO1')
    assert Helper.最後のTODO()['text'] == 'TODO1'

def test_最後の項目を取得する_2件の場合():
    Helper.TODO追加(text='TODO1')
    Helper.TODO追加(text='TODO2')
    assert Helper.最後のTODO()['text'] == 'TODO2'
