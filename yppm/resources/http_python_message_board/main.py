# http python message board, use no javascript, just url + html + css
# 1. try to create a 5.7MB python3.2 + alpine based docker container first
# 2. find a way to monitor the main.py, when it gets changed, re-run main.py
# 3. how to set up a minimum http service with pure python

import os
os.environ['PYTHONUNBUFFERED'] = '1'
import sys

import time

from multiprocessing import Process

work_process = None

def start_work_process():
    if 'work' in sys.modules:
        del sys.modules['work']

    import work  # Now import will reflect the latest changes

    global work_process

    while work_process == None or work_process.is_alive() == False:
        try:
            http_port = 8899
            work_process = Process(target=work.work_function, args=(http_port, ))
            work_process.start()
            time.sleep(10)
        except Exception as e:
            print(e)
            work_process.terminate()

    #work_process.join()

def restart_work_process():
    global work_process
    if work_process != None:
        print("killing process...")
        #work_process.kill()
        work_process.terminate()
        print("process killed.\n")
        while work_process.is_alive() == True:
            time.sleep(1)
        start_work_process()


start_work_process()

# detect_file_changes, if changed, restart the work process
main_program_file_path = "./work.py"
last_modified = os.path.getmtime(main_program_file_path)
while True:
    current_modified = os.path.getmtime(main_program_file_path)
    if current_modified != last_modified:
        print("File has changed!")
        last_modified = current_modified
        restart_work_process()
    time.sleep(1) # 1 second
