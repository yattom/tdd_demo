# coding: utf-8

import subprocess
import io

from todoapp import todo
from datetime import datetime, timedelta

import pytest

def sh(cmd, with_stderr=False):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate()
    if with_stderr:
        return stdoutdata.decode(), stderrdata.decode()
    else:
        return stdoutdata.decode()


class Helper:
    @staticmethod
    def 初期化():
        sh("python -m todoapp.todo clear")

    @staticmethod
    def TODO追加(text, state=None, add_at=None, due=None):
        if not state:
            state = todo.TODO_STATES['TODO']

        if state == todo.TODO_STATES['TODO']:
            statearg = "-s TODO"
        else:
            statearg = ""

        if add_at:
            addatarg = "--add-at '%s'"%(add_at.strftime(todo.DATETIME_FMT))
        else:
            addatarg = ""

        if due:
            duearg = "-d '%s'"%(due.strftime(todo.DATETIME_FMT))
        else:
            duearg = ""
        sh("python -m todoapp.todo add %s %s %s -t '%s'"%(statearg, addatarg, duearg, text))

    @staticmethod
    def すべてのTODO():
        todos = []
        output = sh("python -m todoapp.todo showall")
        lines = output.split('\n')
        while len(lines) > 1:
            value = {}
            value['text'] = lines[0].strip()
            value['state'] = todo.TODO_STATES[lines[1].strip()]
            if lines[2].strip():
                value['due'] = datetime.strptime(lines[2].strip(), todo.DATETIME_FMT)
            else:
                value['due'] = None
            value['add_at'] = datetime.strptime(lines[3].strip(), todo.DATETIME_FMT)
            todos.append(value)
            lines = lines[4:]
        return todos

    @staticmethod
    def 最後のTODO():
        todos = []
        output = sh("python -m todoapp.todo showlast")
        lines = output.split('\n')
        while len(lines) > 1:
            value = {}
            value['text'] = lines[0].strip()
            value['state'] = todo.TODO_STATES[lines[1].strip()]
            if lines[2].strip():
                value['due'] = datetime.strptime(lines[2].strip(), todo.DATETIME_FMT)
            else:
                value['due'] = None
            value['add_at'] = datetime.strptime(lines[3].strip(), todo.DATETIME_FMT)
            todos.append(value)
            lines = lines[4:]
        if todos:
            return todos[-1]
        else:
            return None


def setup_function(fn):
    Helper.初期化()

def test_最初は空():
    assert Helper.すべてのTODO() == []

def test_TODOの属性():
    Helper.TODO追加(text='TODO1',
                    state=todo.TODO_STATES['TODO'],
                    add_at=datetime(2015, 8, 26, 10, 0, 0),
                    due=datetime(2015, 8, 26, 12, 0, 0))
    assert Helper.すべてのTODO() == [{'text': 'TODO1',
                                      'state': todo.TODO_STATES['TODO'],
                                      'add_at': datetime(2015, 8, 26, 10, 0, 0),
                                      'due': datetime(2015, 8, 26, 12, 0, 0)},
                                    ]

def test_TODOの属性_add_atは現在時刻():
    Helper.TODO追加(text='TODO1')
    actual = Helper.最後のTODO()['add_at']
    now = datetime.now()
    assert now - actual <= timedelta(seconds=60)

def test_最後の項目を取得する_空の場合():
    assert Helper.最後のTODO() == None

def test_最後の項目を取得する():
    Helper.TODO追加(text='TODO1')
    assert Helper.最後のTODO()['text'] == 'TODO1'

def test_最後の項目を取得する_2件の場合():
    Helper.TODO追加(text='TODO1')
    Helper.TODO追加(text='TODO2')
    assert Helper.最後のTODO()['text'] == 'TODO2'

def test_すべての項目を取得する():
    Helper.TODO追加(text='TODO1')
    actual = Helper.すべてのTODO()
    assert len(actual) == 1
    assert actual[0]['text'] == 'TODO1'

def test_すべての項目を取得する_2件の場合():
    Helper.TODO追加(text='TODO1')
    Helper.TODO追加(text='TODO2')
    actual = Helper.すべてのTODO()
    assert len(actual) == 2
    assert actual[0]['text'] == 'TODO1'
    assert actual[1]['text'] == 'TODO2'
