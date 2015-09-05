# coding: utf-8

import pytest
import datetime
import subprocess

from todoapp import todo

def sh(cmd, with_stderr=False):
    '''
    テスト用のコマンド実行ヘルパー
    '''
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate()
    retcode = p.wait()
    if retcode != 0:
        assert False, 'sh("%s") retcode: %d'%(cmd, retcode)
    if with_stderr:
        return stdoutdata.decode(), stderrdata.decode()
    else:
        return stdoutdata.decode()


def test_最初は空():
    assert todo.get_last() == None

def test_TODOのすべての属性を取得できる():
    todo.append(text='TODO 1',
                assigned_to='yattom',
                due=datetime.date(2015, 9, 12))
    actual = todo.get_last()
    assert actual.text == 'TODO 1'
    assert actual.assigned_to == 'yattom'
    assert actual.due == datetime.date(2015, 9, 12)

def test_最後に追加した詳細を取得できる_1個追加した場合():
    todo.append('TODO 1')
    actual = todo.get_last()
    assert actual.text == 'TODO 1'

def test_最後に追加した詳細を取得できる_2個追加した場合():
    todo.append('TODO 1')
    todo.append('TODO 2')
    actual = todo.get_last()
    assert actual.text == 'TODO 2'

def test_cmd_TODOのすべての属性を取得できる():
    sh("python -m todoapp.todo add 'TODO 1' yattom 2015/9/12")
    output = sh("python -m todoapp.todo get_last")
    output_lines = [l.strip() for l in output.split('\n')]
    assert output_lines[0] == 'TODO 1'
    assert output_lines[1] == 'yattom'
    assert output_lines[2] == '2015/9/12'
