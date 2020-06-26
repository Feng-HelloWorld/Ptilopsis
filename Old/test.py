from multiprocessing import Process
import os, time

from test2 import test_1
# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))
    a = name
    print(a)
    time.sleep(5)
    print(a)
'''

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=test_1, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
    s = Process(target=test_1, args=('Test',))
    print('Child process will start.')
    s.start()
    s.join()
    print('Child process end.')
    '''

test_1("SDF")
test_1("FGH")