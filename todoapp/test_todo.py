from todoapp import todo
import pytest
import subprocess

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

def test_1件追加したとき():
    todo.clear()
    todo.add('TODO 1')
    actual = todo.get_last()
    assert actual == 'TODO 1'

def test_空の時():
    todo.clear()
    actual = todo.get_last()
    assert actual == None

def test_ファイル保存():
    todo.clear()
    todo.add('TODO 1')
    todo.save()
    todo.clear()
    assert 'TODO 1' != todo.get_last()
    todo.load()
    assert 'TODO 1' == todo.get_last()

@pytest.fixture
def app():
    class CmdApp:
        def add(self, text):
            sh("python -m todoapp.todo '%s'"%(text))
        def get_all(self):
            out = sh("python -m todoapp.todo")
            return out

        def remove(self, text):
            pass

    return CmdApp()

def test_実際に使うシナリオ_1件の場合(app):
    app.add('午後までにメールする')
    assert '午後までにメールする' in app.get_all()
    app.remove('午後までにメールする')
    assert '午後までにメールする' not in app.get_all()
 
@pytest.mark.skipif(True)
def test_実際に使うシナリオ():
    app.add('午後までにメールする')
    app.add('昼までにジムに請求書を送る')
    app.remove('昼までにジムに請求書を送る')
    assert '午後までにメールする' in app.get_all()
    app.remove('午後までにメールする')
    assert '午後までにメールする' not in app.get_all()
    assert '昼までにジムに請求書を送る' not in app.get_all()
