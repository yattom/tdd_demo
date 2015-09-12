#coding: utf-8
import sys
import yaml

todo = None

def clear():
    global todo
    todo = None

def add(new_todo):
    global todo
    todo = new_todo

def get_last():
    return todo

def save():
    with open('todo.yml', 'w') as f:
        yaml.dump(get_last(), f)

def load():
    global todo
    with open('todo.yml') as f:
        todo = yaml.load(f)

def main():
    if len(sys.argv) <= 1:
        print(get_last())
    else:
        add(sys.argv[1])

if __name__=='__main__':
    main()
