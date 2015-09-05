import os
import time
from paver.easy import task, needs, sh
import paver.tasks
import subprocess

import tempfile


APP_PATH = 'todoapp'

@task
def test():
    os.environ['PYTHONPATH'] = '.'
    sh('py.test %s'%(APP_PATH))

@task
def testv():
    os.environ['PYTHONPATH'] = '.'
    sh('py.test -v %s'%(APP_PATH))

@task
def watch():
    from watchdog.observers import Observer
    from watchdog import events
    from threading import Thread

    def delayed_action(func):
        time.sleep(1)
        func()

    class MyHandler(events.FileSystemEventHandler):

        changed = False

        def on_any_event(self, event):
            if isinstance(event, events.FileModifiedEvent) or isinstance(event, events.FileDeletedEvent):
                if event.src_path.endswith('.py') or event.src_path.endswith('.html'):
                    if not MyHandler.changed:
                        MyHandler.changed = True
                        Thread(target=self.fire).start()

        def fire(self):
            sh('clear')
            try:
                test()
            except paver.tasks.BuildFailure:
                pass
            MyHandler.changed = False

    observer = Observer()
    observer.schedule(MyHandler(), APP_PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
