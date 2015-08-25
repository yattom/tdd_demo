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
def watch():
    from watchdog.observers import Observer
    from watchdog import events

    class MyHandler(events.FileSystemEventHandler):
        def on_any_event(self, event):
            if isinstance(event, events.FileModifiedEvent) or isinstance(event, events.FileDeletedEvent):
                if event.src_path.endswith('.py'):
                    self.fire()

        def fire(self):
            sh('clear')
            try:
                test()
            except paver.tasks.BuildFailure:
                pass

    observer = Observer()
    observer.schedule(MyHandler(), APP_PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
