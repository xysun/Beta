## Unit testing with decorators

### Features

* run `./beta.py -f f.py` for a quick example
* command-line interface ("beta"): 
    * `beta -f file1 file2 ...`: test provided files
    * `beta -d dir`: test all Python scripts within directory (non-recursive)
    * `beta -r dir`: recursively test all Python scripts within directory
* functions can be used as normal even after being decorated
* allow assert against exceptions
* trace will point out file --> function --> test case
* can test against itself! `cd` into source code, run `beta -f beta.py`

### API:

* available test calls:
    * `@Beta(4, 5)` -- assert output == 5 when input == 4
    * `@Beta(4, assertRaises(Exception, msg = None))` -- assert `Exception` will be raised with message `msg` when input == 4


### Todo | bug fixes

* make `./beta.py` a proper command `beta`
* multiple decorators, all function names except last are shown as "wrapped_f"
* cannot handle function with no arguments
* better assert message
* ~~handle relative paths import (both non-recursive and recursive) ~~
* test all cases, report #success, #failure (follow python `unittest` output)
* avoid testing beta.py when testing other files
* how to catch raised exceptions? 
* more assert methods
* support json input/output files? 
* clean import namespace after one file
