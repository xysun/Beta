#!/usr/local/bin/python3

import argparse
import importlib
import inspect
import pdb
import sys
import weakref
from collections import defaultdict
from functools import wraps

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


class Beta(KeepRefs):
    def __init__(self, test_input, test_output, enabled = False):
        super(Beta, self).__init__()
        self.test_input = test_input
        self.test_output = test_output
        self.enabled = enabled

    def __call__(self, f): # only invoked once during decoration
        wraps(f)
        def wrapped_f(*args): # replace f after decoration
            if self.enabled:
                if isinstance(self.test_input, tuple):
                    o = f(*self.test_input)
                else:
                    o = f(self.test_input)
                assert o == self.test_output
                print ("Testing function [" + f.__name__ + "], passed...")
            return f(*args)
        self.wrapped_f = wrapped_f
        return wrapped_f

def test_single_file(fname):
    module_name = fname.split('.py')[0]
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
    pass

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

