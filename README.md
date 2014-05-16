## Unit testing with decorators

### Features

* run `./beta.py -f f.py` for a quick example
* command-line interface ("beta"): 
    * `beta -f file1 file2 ...`: test provided files
    * `beta -d dir`: test current directory (non-recursive)
    * `beta -r dir`: recursively test current directory
* functions can be used as normal even after being decorated
* allow assert against exceptions
* trace will point out file --> function --> test case
* can test against itself! `cd` into source code, run `beta -f beta.py`

### API:

* style 1: `@test(input = 4, assertEqual(return, 5))`

    can assert against all variables reacheable in the function
    support all unittest assert methods (use unittest underneath?)
       [https://docs.python.org/3/library/unittest.html?highlight=unittest#unittest.TestCase.assertEqual]
    for variables not found, default treat as return value (?)

* style 2:

    default to assertEqual
    also allow files

    ```
    @test(input = 4, output = 5) 
    @test(input = 'in.json', output = 'out.json')
    ```


### Todo | bug fixes

* identify whether it's a python script or a directory
* make `./beta.py` a proper command `beta`
* multiple decorators, the first function name is "wrapped_f"
* cannot handle function with no arguments
* better assert message
* cannot handle single file paths (absolute / relative)
* test all cases, report failure (right now stop when encountering first fail)
* avoid namespace in beta.py (otherwise currently it'll test beta.py as well)
