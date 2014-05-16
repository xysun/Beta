## Unit testing with decorators

### Features

* run `./beta.py f.py` for a quick example
* command-line interface ("beta"): 
    * `beta -f file1 file2 ...`: test provided files
    * `beta -d dir`: test current directory (non-recursive)
    * `beta -r dir`: recursively test current directory
* [DONE] functions can be normally used even with decorators
* allow assert against exceptions
* trace will point out file --> function --> test case

### API:

* style 1: `@test(input = 4, assertEqual(return, 5))`
    can assert against all variables reacheable in the function
    support all unittest assert methods (use unittest underneath?)
       [https://docs.python.org/3/library/unittest.html?highlight=unittest#unittest.TestCase.assertEqual]
    for variables not found, default treat as return value (?)

* style 2:
    default to assertEqual
    also allow files
@test(input = 4, output = 5) 
@test(input = 'in.json', output = 'out.json')

### Todo | bug fixes

* identify whether it's a python script or a directory
* make `./beta.py` a proper command `beta`
* multiple decorators, the first function name is "wrapped_f"
