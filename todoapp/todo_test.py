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
    def 初期化(self):
        sh("python -m todoapp.todo clear")

    def TODO追加(self, text, state=None, add_at=None, due=None):
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

    def すべてのTODO(self):
        output = sh("python -m todoapp.todo showall")
        return self.parse_todos(output)

    def 最後のTODO(self):
        output = sh("python -m todoapp.todo showlast")
        todos = self.parse_todos(output)
        if todos:
            return todos[-1]
        else:
            return None

    def parse_todos(self, output):
        todos = []
        lines = [l.strip() for l in output.split('\n')]
        while len(lines) > 1:
            value = {}
            value['text'] = lines[0]
            value['state'] = todo.TODO_STATES[lines[1]]
            if lines[2]:
                value['due'] = datetime.strptime(lines[2], todo.DATETIME_FMT)
            else:
                value['due'] = None
            value['add_at'] = datetime.strptime(lines[3], todo.DATETIME_FMT)
            todos.append(value)
            lines = lines[4:]
        return todos

@pytest.fixture()
def helper(request):
    request.cls.helper = Helper()
    request.cls.helper.初期化()

@pytest.mark.usefixtures("helper")
class TestTODO操作:
    def test_最初は空(self):
        assert self.helper.すべてのTODO() == []

    def test_TODOの属性(self):
        add_at = datetime(2015, 8, 26, 10, 0, 0)
        due=datetime(2015, 8, 26, 12, 0, 0)
        self.helper.TODO追加(text='TODO1',
                        state=todo.TODO_STATES['TODO'],
                        add_at=add_at,
                        due=due)
        assert self.helper.すべてのTODO() == [{'text': 'TODO1',
                                         'state': todo.TODO_STATES['TODO'],
                                         'add_at': add_at,
                                         'due': due},
                                        ]

    def test_TODOの属性_add_atは現在時刻(self):
        self.helper.TODO追加(text='TODO1')
        actual = self.helper.最後のTODO()['add_at']
        now = datetime.now()
        assert now - actual <= timedelta(seconds=60)

    def test_最後の項目を取得する_空の場合(self):
        assert self.helper.最後のTODO() == None

    def test_最後の項目を取得する(self):
        self.helper.TODO追加(text='TODO1')
        assert self.helper.最後のTODO()['text'] == 'TODO1'

    def test_最後の項目を取得する_2件の場合(self):
        self.helper.TODO追加(text='TODO1')
        self.helper.TODO追加(text='TODO2')
        assert self.helper.最後のTODO()['text'] == 'TODO2'

    def test_すべての項目を取得する(self):
        self.helper.TODO追加(text='TODO1')
        actual = self.helper.すべてのTODO()
        assert len(actual) == 1
        assert [e['text'] for e in actual] == ['TODO1']

    def test_すべての項目を取得する_2件の場合(self):
        self.helper.TODO追加(text='TODO1')
        self.helper.TODO追加(text='TODO2')
        actual = self.helper.すべてのTODO()
        assert [e['text'] for e in actual] == ['TODO1', 'TODO2']
