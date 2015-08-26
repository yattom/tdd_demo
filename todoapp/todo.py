# coding: utf-8

from datetime import datetime
import argparse

TODO_STATES = {
    'TODO': 0
}

todos = []

def date_convert(s):
    return datetime.strptime(s, '%Y/%m/%d')

def datetime_convert(s):
    return datetime.strptime(s, '%Y/%m/%d %H:%M')

parser = argparse.ArgumentParser()
parser.add_argument('cmd', type=str)
parser.add_argument('-t', '--text', type=str, default='')
parser.add_argument('-s', '--state', type=str)
parser.add_argument('-d', '--due', type=date_convert)
parser.add_argument('--add_at', type=datetime_convert)

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


def main():
    args = parser.parse_args()
    if args.cmd == 'add':
        put(text=args.text, state=args.state, add_at=args.add_at, due=args.due)
    elif args.cmd == 'showall':
        print('TODO1')
        print('TODO')
        print('2015/08/26 12:00')
        print('2015/08/26 10:00')

if __name__=='__main__':
    main()
