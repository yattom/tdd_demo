# coding: utf-8

import subprocess
import io
from datetime import datetime, timedelta

import pytest
from todoapp import todo

def sh(cmd, with_stderr=False):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate()
    if with_stderr:
        return stdoutdata.decode(), stderrdata.decode()
    else:
        return stdoutdata.decode()


class ObjectHelper:
    def 初期化(self):
        todo.clear()

    def TODO追加(self, text, state=None, add_at=None, due=None):
        todo.put(text=text, state=state, add_at=add_at, due=due)

    def すべてのTODO(self):
        return [dict(text=e.text, state=e.state, due=e.due, add_at=e.add_at) for e in todo.get_all()]

    def 最後のTODO(self):
        e = todo.get_last()
        if not e:
            return None
        return dict(text=e.text, state=e.state, due=e.due, add_at=e.add_at)


class CommandLineAppHelper:
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


class WebHelper:
    def __init__(self):
        print('webhelper init')
        self.procs = []
        x_proc = subprocess.Popen(['Xvfb', ':1'], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        webapp_proc = subprocess.Popen(['python', 'todoapp/webapp.py'], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.procs.append(x_proc)
        self.procs.append(webapp_proc)

    def 初期化(self):
        pass

    def すべてのTODO(self):
        pass

    def 後始末(self):
        for p in self.procs:
            try:
                p.terminate()
                p.wait()
            except:
                pass


@pytest.fixture(scope='function', params=[CommandLineAppHelper, ObjectHelper])
def helper(request):
    request.cls.helper = request.param()
    request.cls.helper.初期化()

@pytest.fixture(scope='module')
def webhelper(request):
    helper = WebHelper()

    def finalize():
        print('webhelper finalize')
        helper.後始末()

    request.addfinalizer(finalize)
    helper.初期化()
    return helper


