# coding: utf-8

from datetime import datetime
from bson import json_util

import argparse
import json

TODO_STATES = {
    'TODO': 0
}

todos = []

DATETIME_FMT = '%Y/%m/%d %H:%M'

def datetime_convert(s):
    return datetime.strptime(s, DATETIME_FMT)

parser = argparse.ArgumentParser()
parser.add_argument('cmd', type=str)
parser.add_argument('-t', '--text', type=str, default='')
parser.add_argument('-s', '--state', type=str)
parser.add_argument('-d', '--due', type=datetime_convert)
parser.add_argument('--add-at', type=datetime_convert)

class ToDo:
    def __init__(self, text, state, due, add_at=None):
        self.text = text
        self.state = state
        self.due = due
        if not add_at:
            add_at = datetime.now()
        self.add_at = add_at

    def __eq__(self, other):
        if not isinstance(other, ToDo):
            return False
        return (self.text == other.text and
                self.state == other.state and
                self.due == other.due and
                self.add_at == other.add_at)


def state_name(val):
    for n, v in TODO_STATES.items():
        if v == val:
            return n
    raise ValueError()

def get_all():
    return todos

def put(text, state, due, add_at=None):
    item = ToDo(text, state, due, add_at)
    todos.append(item)

def get_last():
    if not todos:
        return None
    return todos[-1]

def clear():
    todos.clear()

def save():
    data = []
    for t in todos:
        d = dict(text=t.text, state=t.state, due=t.due, add_at=t.add_at)
        data.append(d)
    with open('todo.json', 'w') as f:
        json.dump(data, f, default=json_util.default)

def load():
    clear()
    with open('todo.json') as f:
        data = json.load(f, object_hook=json_util.object_hook)
    for d in data:
        t = ToDo(text=d['text'], state=d['state'], due=d['due'], add_at=d['add_at'])
        todos.append(t)

def dump_item(item):
    print(item.text)
    print(state_name(item.state))
    if item.due:
        print(item.due.strftime(DATETIME_FMT))
    else:
        print('')
    print(item.add_at.strftime(DATETIME_FMT))

def main():
    args = parser.parse_args()
    if args.cmd == 'clear':
        clear()
        save()
    elif args.cmd == 'add':
        load()
        if not args.state:
            state = TODO_STATES['TODO']
        else:
            state = TODO_STATES[args.state]
        put(text=args.text, state=state, add_at=args.add_at, due=args.due)
        save()
    elif args.cmd == 'showall':
        load()
        for item in get_all():
            dump_item(item)
    elif args.cmd == 'showlast':
        load()
        item = get_last()
        if not item:
            return
        dump_item(item)


if __name__=='__main__':
    main()
