#!/usr/bin/env python
'''
class A(object):
    def __init__(self,
                a):
       self.a = a 
       print a
t = A(5)
t 
'''
kwargs={'a':1,'b':2}
t={'a':1,'b':2}
c = 5
def test(c, **kwargs):
    print c
    for key  in kwargs:
        print kwargs[key] 
print test('5',**t)  
