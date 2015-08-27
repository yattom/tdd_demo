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

def state_name(val):
    for n, v in TODO_STATES.items():
        if v == val:
            return n
    raise ValueError()

def get_all():
    return todos

def put(text, state, due, add_at=None):
    if not add_at:
        add_at = datetime.now()
    item = {'text': text, 'state': state, 'add_at': add_at, 'due': due}
    todos.append(item)

def get_last():
    if not todos:
        return None
    return todos[-1]

def clear():
    global todos
    todos = []

def save():
    with open('todo.json', 'w') as f:
        json.dump(todos, f, default=json_util.default)

def load():
    global todos
    with open('todo.json') as f:
        todos = json.load(f, object_hook=json_util.object_hook)

def dump_item(item):
    print(item['text'])
    print(state_name(item['state']))
    if item['due']:
        print(item['due'].strftime(DATETIME_FMT))
    else:
        print('')
    print(item['add_at'].strftime(DATETIME_FMT))

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
