# coding: utf-8

from datetime import datetime, timedelta
import pytest

from todoapp import todo


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


def test_hello_web(webhelper):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By

    browser = webdriver.Firefox()
    browser.get('http://localhost:5000/hello')
    assert 'Hello' in browser.find_element(By.CSS_SELECTOR, "BODY").text

def test_最初は空_web(webhelper):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By

    browser = webdriver.Firefox()
    browser.get('http://localhost:5000/')
    assert browser.find_elements(By.CSS_SELECTOR, ".todos .todo") == []

def test_最後の項目を取得する():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By

    browser = webdriver.Firefox()
    browser.get('http://localhost:5000/create')
    input_text = browser.find_element_by_name("text")
    input_text.send_keys('TODO1')
    input_text.submit()

    actual = browser.find_elements(By.CSS_SELECTOR, ".todos .todo")[0]
    assert 'TODO1' in actual.text
