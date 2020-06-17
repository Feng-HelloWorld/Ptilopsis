import time, threading


class msg:
    text = str()

    def __init__(self,text:str='init msg'):
        self.text = text
        self.sent()

    def sent(self):
        print('==Message Send======\n> Text: {}\n> Time: {}\n> Thread: {}\n====================\n'.format(self.text, time.time(), threading.current_thread().name))

def func1(m:msg):
    print('* Thread Now:',threading.current_thread().name)
    print('func1 start')
    m.text='func1 out put'
    print('func1 sleeping')
    time.sleep(3)
    m.sent()
    print('func1 end')
    

def func2(m:msg):
    print('* Thread Now:',threading.current_thread().name)
    print('func2 start')
    m.text='func2 out put'
    print('func2 sleeping')
    time.sleep(5)
    m.sent()
    print('func2 end')


def deliver(cmd):
    m = msg()
    if cmd==1:
        t = threading.Thread(target=func1(m),name='ddd')
        t.start
        t.join
    elif cmd==2:
        t = threading.Thread(target=func2(m),name='eee')
        t.start
        t.join

t = threading.Thread(target=deliver(1),name='aaa')
t.start
t.join
t = threading.Thread(target=deliver(2),name='bbb')
t.start
t.join
t = threading.Thread(target=deliver(1),name='ccc')
t.start
t.join