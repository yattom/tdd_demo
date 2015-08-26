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
        todo.clear()

    @staticmethod
    def TODO追加(text, state=None, add_at=None, due=None):
        if not state:
            state = todo.TODO_STATES['TODO']

        if state == todo.TODO_STATES['TODO']:
            statearg = "-s TODO"
        else:
            statearg = ""

        if add_at:
            addatarg = "--add-at '%d/%d/%d %02d:%02d'"
        else:
            addatarg = ""

        if due:
            duearg = "-d %d/%d/%d"
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
            value['due'] = datetime.strptime(lines[2].strip(), '%Y/%m/%d %H:%M')
            value['add_at'] = datetime.strptime(lines[3].strip(), '%Y/%m/%d %H:%M')
            todos.append(value)
            lines = lines[4:]
        return todos

    @staticmethod
    def 最後のTODO():
        return todo.get_last()

def setup_function(fn):
    Helper.初期化()

@pytest.mark.xfail
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

@pytest.mark.xfail
def test_TODOの属性_add_atは現在時刻():
    Helper.TODO追加(text='TODO1')
    actual = Helper.最後のTODO()['add_at']
    now = datetime.now()
    assert now - actual <= timedelta(seconds=1)

@pytest.mark.xfail
def test_最後の項目を取得する_空の場合():
    assert Helper.最後のTODO() == None

@pytest.mark.xfail
def test_最後の項目を取得する():
    Helper.TODO追加(text='TODO1')
    assert Helper.最後のTODO()['text'] == 'TODO1'

@pytest.mark.xfail
def test_最後の項目を取得する_2件の場合():
    Helper.TODO追加(text='TODO1')
    Helper.TODO追加(text='TODO2')
    assert Helper.最後のTODO()['text'] == 'TODO2'
