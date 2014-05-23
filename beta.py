#!/usr/local/bin/python3

import argparse
import importlib
import inspect
import os
import pdb
import sys
import weakref
from collections import defaultdict
from functools import wraps

class BetaErrors(Exception):
    """
    base exception class
    """
    pass

class NotAModuleError(BetaErrors):
    def __init__(self, path):
        self.path = path
    
    def __str__(self):
        return self.path + " is not a valid module path"

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

class Pipe(object):
    
    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return Pipe(lambda x : self.function(x, *args, **kwargs))


class Beta(KeepRefs):
    def __init__(self, test_input, test_output):
        super(Beta, self).__init__()
        self.test_input = test_input
        self.test_output = test_output
        self.enabled = False

    def __call__(self, f): # only invoked once during decoration
        wraps(f)
        def wrapped_f(*args): # replace f after decoration
            if self.enabled:
                if isinstance(self.test_input, tuple):
                    o = f(*self.test_input)
                else:
                    o = f(self.test_input)
                if o == self.test_output:
                    print ("Testing function [" + f.__name__ + "], passed...")
                else:
                    print ("Testing function [" + f.__name__ + "], failed..")
            return f(*args)
        self.wrapped_f = wrapped_f
        return wrapped_f

def test_single_file(fname):
    module_path, module_name = path_to_module(fname)
    sys.path.insert(0, module_path)
    m = importlib.import_module(module_name)
    
    for name, obj in inspect.getmembers(m):
        if inspect.isclass(obj) and obj.__name__ == 'Beta':
            betas = obj.get_instances()
    
    for beta in betas:
        beta.enabled = True
        if beta.enabled:
            if isinstance(beta.test_input, tuple):
                beta.wrapped_f(*beta.test_input)
            else:
                beta.wrapped_f(beta.test_input)

def test_directory(dir_name, recursive = False):
    """
    test python scripts within directory
    """
    for dirpath, dirnames, filenames in os.walk(dir_name):
        for filename in filenames:
            if filename[-3:] == '.py':
                fpath = os.path.join(dirpath, filename)
                if recursive or (not recursive and fpath == os.path.join(dir_name, filename)):
                    print("Testing file..", fpath)
                    test_single_file(fpath)


#@Beta('test/f.py', ('./test', 'f'))
#@Beta('test/test1/f2.py', ('./test/test1', 'f2'))
#@Beta('f.py', ('.', 'f'))
#@Beta('f', assertRaises(NotAModuleError, "'f' is not a valid module path"))
def path_to_module(path):
    '''
    convert file path to proper import module path and name
    '''
    if path[-3:] != ".py":
        raise NotAModuleError(path)
    module_name = path[:-3].split('/')[-1]
    last_index = path.find('/' + module_name + '.py')
    if last_index == -1:
        module_path = '.'
    else:
        module_path = './' + path[:last_index]
    
    return module_path, module_name


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", nargs = '+', help = 'files to test')
    parser.add_argument('-d', help = 'test single directory')
    parser.add_argument('-r', help = 'recursively test single directory')

    args = parser.parse_args()
    if args.f and len(args.f) > 0:
        for fname in args.f:
            test_single_file(fname)

    if args.d:
        test_directory(args.d)
    
    if args.r:
        test_directory(args.r, recursive = True)

def main():
    parse_args()

if __name__ == '__main__':
    main()

