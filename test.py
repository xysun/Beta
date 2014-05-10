"""
mocking my unit test module idea

Unit testing with decorators

* command-line interface: 
    does not need __main__
    know how to find all test cases, support allow config files or command line argument parsing
* [CHECK] functions can be normally used even with decorators
* allow assert against exceptions
* trace will point out file --> function --> test case
"""

# API:
# style 1: 
"""
    can assert against all variables reacheable in the function
    support all unittest assert methods
       [https://docs.python.org/3/library/unittest.html?highlight=unittest#unittest.TestCase.assertEqual]
    for variables not found, default treat as return value (?)
@test(input = 4, assertEqual(return, 5))
"""

# style 2:
"""
    default to assertEqual
    also allow files
@test(input = 4, output = 5) 
@test(input = 'in.json', output = 'out.json')
"""

from collections import defaultdict
import weakref, sys

class KeepRefs(object):
    """
    to find all Test instances, so that we can enable/disable unittest externally by changing test.enabled
    [thanks](http://stackoverflow.com/questions/328851/printing-all-instances-of-a-class)
    """
    __refs__ = defaultdict(list)
    def __init__(self):
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref() # obtain the referant by calling it
            if inst is not None:
                yield inst


class Test(KeepRefs):
    def __init__(self, test_input, test_output, enabled = False):
        super(Test, self).__init__()
        self.test_input = test_input
        self.test_output = test_output
        self.enabled = enabled

    def __call__(self, f): # only invoked once during decoration
        print ("In __call__")
        def wrapped_f(*args): # replace f after decoration
            if self.enabled:
                o = f(self.test_input)
                print (o)
                assert o == self.test_output
                print ("test passed..")
            return f(*args)
        return wrapped_f


@Test(3, 4)
def f(v):
    return v + 1

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'test':
        for r in Test.get_instances():
            r.enabled = True
    
    f(3)
