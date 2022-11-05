# **ezr Wiki (for v2m0)**

## Running code
- **From the command-line**
    - Open ezrshell
    - Write the code
    - Press the 'enter' key

- **From a file**
    - **Option a**
        - Open/create a file with the extension '.ezr'
        - Write the code
        - Open ezrshell
        - Type in ```run('path/to/source/file')``` (the run function is explained better in the **builtins** section)

    - **Option b**
        - Open/create a file
        - Write the code
        - Open the file with ezrshell.exe (windows)
            - Right-click the file
            - Click on 'open with'
            - Click on 'choose another app'
            - Click on 'more apps'
            - Click on ezrshell.exe
            - If you don't see ezrshell as an option:
                - Click on 'look for another app on this pc'
                - Browse to where-ever you installed ezrshell
                - Click on 'ezrshell.exe'
                - Click on 'open'

## Comments
```
@ Anything after the '@' symbol is a comment
```

## Variable definition
```
@ Variables are defined with the 'item' keyword
item i: 'hello!'
show(i)

@ The 'global' keyword can be used to 'globalize' the variable
item test: 1
show(test)

function test_func do
    global item test: 2
end

test_func()
show(test)

function test_func_2 do
    item test: 3 @ This would just create a local variable 'test' with the value 3
end

test_func_2()
show(test) @ 'test' will still be 2
```

## Variable types
- **Number (Integer/Float values)**
```
item n: 100
show(n)

show(n+3.2) @ Addition
show(n-2) @ Subtraction
show(n*3.5) @ Multiplication
show(n/2) @ Division
show(n^3.342) @ Power
show(n%2.45) @ Modulo
```

- **String (Text)**
```
@ Strings can be defined with either ' or "
item s: 's'
show(s)

item s: "s"
show(s)

@ Strings can be concatenated
show(s + 'a')

@ Strings can multiplied with numbers
show(s * 4)

@ Strings can be divided with numbers
show((s * 4) / 2) @ 's*4' = 'ssss'

@ Here '<=' returns the character at index 1 in the string
show('hello!' <= 1)

@ The '\' symbol 'escapes' special symbols
show('this will print \' ') @ here '\' escapes ', which usually signifies the end of a string

show('new \n line') @ Here '\n' signifies a new-line
show('tab \t space') @ Here '\t' signifies a tab-space
show('backslash \\ ') @ Here '\' escapes itself
```

- **Function (Callable snippets of code)**
```
function add with a, b do a + b
    
@ Functions can be called with [name]([args])
show(add(3, 4))

@ Functions can have any number of args
function add_more with a, b, c, d, e, f do a + b + c + d + e + f
show(add_more(3, 5, 2, 7, 3, 6))

@ Functions can have no args
function return_1 do 1
show(return_1())

@ Functions can be anonymous
item anonymous_add: function with a, b do a + b
show(anonymous_add(3, 6))

item anonymous_return_1: function do 1
show(anonymous_return_1())

@ Functions can be mult-line
function multi_line_add with a, b do
    item out: a + b

    show(convert(a, 'String') + ' + ' + convert(b, 'String') + ' is ' + convert(out, 'String'))
    item ans: get('is that correct? y/n ')

    if ans = 'y' do
        show('exiting program...')
        return out
        @ 'return' exits the function and returns the variable 'out'
    else if ans = 'n' do
        item correct_answer: get('please enter the correct answer: ')
        show('noted. exiting program...')
        return correct_answer
    else do
        show('error: invalid input')
    end

    return @ Here it's returning 'nothing'
    show('this won\'t print!') @ This won't print as the function will exit before this can be run

    @ Note the 'end' keyword
end

show(multi_line_add(4, 3))

@ Multi-line functions can also be anonymous
item anonymous_multi_line_ask_name: function with name do
    if name do
        show('hello, ' + convert(name, 'String') + '!')
    else do
        item name: get('hello! what\'s your name? ')
        show('hello, ' + convert(name, 'String') + '!')
        return name
    end

    @ A function doesn't have to return anything
end

anonymous_multi_line_ask_name('defname')
show(anonymous_multi_line_ask_name(nothing))

@ A multi line function doesn't need to have arguments either
function do_something do @ This can also be anonymous
    item stop_: false
    while invert stop_ do
        count from 0 as i to 10 do
            show('==========================')
        end

        item input: get('stop? y/n ')
        item stop_: if input = 'y' do true else do false
    end
end

do_something()
```

- **Object (custom variable types)**
```
object obj do
    @ All the code below is executed when a new 'obj' is created
    @ Anything that can be done in a normal ezr script can be done in objects!

    item obj_item: 'hello!'

    function show_obj_item do
        show(obj_item)
    end

    function change_obj_item with new do
        global item obj_item: new
    end

    show('item created')
end

item object_: obj() @ Create a new 'obj' and assign it to 'object_'

@ Variables in an object can be accessed with:
show(object_.obj_item)

@ Same with functions
object_.show_obj_item()

object_.change_obj_item('obj_item has been changed!')
object_.show_obj_item()
show(object_.obj_item)

@ Objects can also take in arguments, just like functions!
object obj_2 with obj_item_default do
    item obj_item: obj_item_default

    function set_and_get_obj_item with new do
        global item obj_item: new
        return 'obj_item is now: ' + convert(obj_item, 'String')
    end

    show('item created!')
end

show(obj_2('default!').obj_item) @ Objects can be created like this too!
item object_2: obj_2('default!')
show(object_2.set_and_get_obj_item('new value!'))

@ A lot more can be done with objects, try it yourself!
```

- **List (Groups of variables)**
```
item l: ['list', 53, 34.12, ['nested list']]
show(l)

@ Lists can contain any type of data, even other lists
item l: [1, 2.54, 'hello', ['nested', 'list'], show]
show(l)

item l: ['s', 'a']
show(l)

item l: ['s', ['a', 's']]
show(l)

@ Lists can be extended with any type of data
item l: [1, 2]; show(l)
l + 3; show(l)
@ At 'l + 3', we're are adding number 3 to 'l'

item l: ['h', 'e']; show(l)
l + ['l', 'l', 'o']; show(l)
@ At 'l + ['l', 'l', 'o']', we're extending 'l' with strings 'l', 'l' and 'o'

@ Lists can be removed from
item l: [1, 2, 'sa']; show(l)
l - 1; show(l)
@ At 'l - 1', we're removing the variable at index 1

@ Here '<=' returns the variable at index 1 in the list 
show([1, 2, 3, 4] <= 1)

@ For nested lists, you can also do this:
show([1, 2, [3, 4]] <= 2 <= 0)

@ Lists can be multiplied with numbers
show([1, 2] * 4)

@ Lists can be divided with numbers
show([1, 2, 3, 4] / 2)
```

- **Array (Unchangable list)**
```
item l: ('array', 53, 34.12, ('nested array'))
show(l)

@ Arrays are just like lists, except they can't be changed after creation
item l: (1, 2.54, 'hello', ('nested', 'array'), show)
show(l)

@ Here '<=' returns the variable at index 1 in the array 
show((1, 2, 3, 4) <= 1)

@ For nested arrays, you can also do this:
show((1, 2, (3, 4)) <= 2 <= 0)

@ Arrays can be multiplied with numbers
show((1, 2) * 4)

@ Arrays can be divided with numbers
show((1, 2, 3, 4) / 2)
```

- **Dictionary (List but the indices are other variables, known as 'keys')**
```
item l: {'list':53, 34.12:['nested list']}
show(l)

@ Dictionaries can also contain any type of data, but the 'key' values must be hashable
item l: {1:2.54, 'hello':['nested', 'list'], show:5}
show(l)

@ Dictionaries can be extended with other dictionaries
l + {6:4}; show(l)
@ At 'l + {6:4}' we're extending 'l' with '{6:4}'

@ But if a 'key' value repeats, the old pair is overridden by the new pair
l + {1:9}; show(l)
@ At 'l + ['l', 'l', 'o']', we're extending 'l' with '{1:9}', but as the 'key' 1 already exists, -
@ ezr overrides '1:2.54' with '1:9'

@ Dictionaries can be removed from
l - show; show(l)
@ At 'l - show', we're removing the pair 'show:5' from 'l'

@ Here '<=' returns the variable of 'key' 'hello' in the dictionary
show(l <= 'hello')

@ For variables which are arrays, lists or other dictionaries, you can also do this:
show(l <= 'hello' <= 1)

@ Dictionaries can be divided with numbers
show(l / 1.5)
```

## Importing other files
```
@ Files can be imported with the 'include' keyword
include 'time.py' @ This is a builtin ezr-python library
@ Normal ezr files can also be imported

@ Imported files are treated like objects
show(time.epoch.readableTime())
show(time.localTime(time.time()).readableTime())

@ Files can also be given a nickname when importing
include 'time.py' as fn
show(fn.epoch.readableTime())
show(fn.localTime(fn.time()).readableTime())

@ Files in different folders can also be imported
include 'Libraries/time.py'
show(time.epoch.readableTime())
show(time.localTime(time.time()).readableTime())
```

## Comparison
```
@ Numbers can be compared with '=', '!', '<', '>', '<=', '>=', 'and' and 'or'
@ Most other types are limited to '=', '!', 'and' and 'or'

@ 'invert' will invert the outcome of an expression and is only supported by numbers and booleans
show(invert true) @ Will be false
show(invert false) @ Will be true
show(invert 1) @ Will be 0
show(invert 0) @ Will be 1

@ The 'in' expression can be used to check if a variable contains another variable
@ It is supported by most types
show('1' in '1234567890')
show('element' in [1, 2, 'element'])
show(1 in [1, 2])
```

## If statements
```
item input: get('enter y/n ')

@ Here, the 'if' statement checks if 'input' is equal to 'y' and returns 1 if it is
item out: if input = 'y' do 1
show(out)

@ Here, the 'else if' statement checks if 'input' is equal to 'n' and returns 2 if it is
item out: if input = 'y' do 1 else if input = 'n' do 2
show(out)

@ Here, if 'input' is neither 'y' or 'n', it executes the last 'else' statement, which returns 3
item out: if input = 'y' do 1 else if input = 'n' do 2 else do 3
show(out)

@ Some other examples
show(if 1 / 2 = 0.5 do '1 / 2 is 0.5' else do '1 / 2 is not 0.5')
show(if 1 * 2 = 0.5 do '1 * 2 is 0.5' else do '1 * 2 is not 0.5')
show(if 1 * 2 = 0.5 do '1 * 2 is 0.5' else if 1 * 2 = 2 do '1 * 2 is 2' else do '1 * 2 is not 0.5')
show(if 1 * 2 = 0.5 do '1 * 2 is 0.5' else if 1 * 2 = 2 do '1 * 2 is 2') @ Same thing as above, just the without else

show(if [1, 2] = [1, 2] do 'both lists are equal' else do 'both lists are not equal')
show(if [1, 2] = [1, 6] do 'both lists are equal' else do 'both lists are not equal')
show(if [1, 2] = [1, 6] do 'both lists are equal' else if 3 * 3 = 9 do '3 * 3 = 9' else do 'both lists  are not equal')

show('\n\n')

show(if [1, 2, [3, 4]] = [1, 2, [3, 4]] do 'both lists are equal' else do 'both lists are not equal')

@ NOTE: You can have an unlimited number of 'else if' statements

@ Multi-line if statements are the same as single-line statements, but they don't return any values

item input: get('enter y/n ')

@ Here, the 'if' statement checks if 'input' is equal to 'y'
if input = 'y' do
    item out: 1
    show('item out is 1!')
    show(out)

    @ Note the 'end' keyword
end

@ Here, the 'else if' statement checks if 'input' is equal to 'n'
if input = 'y' do
    item out: 1
    show('item out is 1!')
    show(out)
else if input = 'n' do
    item out: 2
    show('item out is 2!')
    show(out)
end

@ Here, if 'input' is neither 'y' or 'n', it executes the last 'else' statement
if input = 'y' do
    item out: 1
    show('item out is 1!')
    show(out)
else if input = 'n' do
    item out: 2
    show('item out is 2!')
    show(out)
else do
    item out: 3
    show('item out is 3!')
    show(out)
end

@ Try comparing other variable types too!
```

## Count loops
```
item start: get_int('enter loop start: ')
item length: get_int('enter loop length: ') @ 'get_int' is another built-in function

@ NOTE: ezr ignores all spaces and tab-spaces

item l: count from start as i to length do i
@ Here, ezr starts counting from 'start' to 'length' - 1 and sets the loop variable to 'i'
@ The loop then returns an array of variables, the variables being the output of the code after the 'do' keyword each iteration
@ The loop also increments 'i' by 1 each iteration

show(l)

item step_: get_int('enter loop increment: ')
item l: count from start as i to length step step_ do i
@ Here, it does the same as above, but sets the loop increment as 'step_'

show(l)

@ Multi-line count loops are the same, but they don't return anything

item l: []
@ The below code does the same thing as the first example, but also prints the list and loop variable each iteration
count from start as i to length do
    l + i
    show(l)
    show('i = ' + convert(i, 'String'))

    @ Note the 'end' keyword
end

show(l)

item l: []
@ The below code does the same thing as the second example, but also prints the list and loop variable each iteration
count from start as i to length step step_ do
    l + i
    show(l)
    show('i = ' + convert(i, 'String'))
end

show(l)

item l: []
@ The below code uses the 'skip' keyword to skip an iteration if 'i' = 3 and uses the 'stop' keyword to stop/break the loop if 'i' = 7
count from start as i to length do
    if i = 3 do
        skip
    else if i = 7 do
        stop
    end

    l + i
    show(l)
    show('i = ' + convert(i, 'String'))
end

show(l)
```

## While loops
```
item start: 0
item length: 9

item i: start
item l: while i < length do item i: i + 1
@ Here, ezr checks if 'i' is less than 'length' each iteration
@ In the code after the 'do' keyword we're adding 1 to 'i', so each iteration 'i' will be 'i' + 1, -
@ so in the last iteration, 'i' = 9 and the loop stops and returns an array of variables, -
@ the variables being the output of the code after the 'do' keyword each iteration

show(l)
show(i)

@ Multi-line while loops are the same, but they don't return anything

item i: start
item l: []

while i < length do
    l + (item i: i + 1)
    show(l)
    show('i = ' + convert(i, 'String'))

    @ Note the 'end' keyword
end

item i: 0
item l: []
while i < 10 do
    item i: i + 1

    if i = 3 do
        skip
    else if i = 6 do
        stop
    end

    show(l)
    l + i
end

show(l)
```

## Try statements
```
@ The 'try' statement is used for error handling
try do
    @ This code should show an error, but because it is in a 'try' statement, it won't
    convert('s', 'int')

    @ Note the 'end' keyword
end

@ Same as above
item a: try do convert('s', 'int')
show(a)

try do
    convert('s', 'int')
error do
    @ This code will execute if an error occurred in the above code
    show('an error occurred!')
end

@ Same as above
item a: try do convert('s', 'int') error do 'an error occurred!'
show(a) @ a = 'an error occurred'

try do
    convert('s', 'Int')
error 'INCORRECT-TYPE' do
    @ This code will execute only if the 'INCORRECT-TYPE' error occurs in the above code
    show('an incorrect-type error occurred!')
error do
    show('an unknown error occurred.')
end

@ Same as above
item a: try do convert('s', 'Int') error 'INCORRECT-TYPE' do 'an incorrect-type error occurred!' error do 'an unknown error occurred.'
show(a) @ a = 'an incorrect-type error occurred!'

try do
    1/0
error as i do
    @ Here, 'i' is given a string value which signifies the error type, in this case, 'MATH'
    show(i)
end

@ Same as above
try do 1/0 error as i do show(i)

try do
    1/0
error 'MATH' as i do
    @ This is the same as above, but only triggers if the 'MATH' error occurs
    show('error: ' + i)
end

@ Same as above
try do 1/0 error 'math' as i do show('error: ' + i)

@ Other errors:
@    RUNTIME              - For unknown errors
@    CUSTOM               - For errors raised with the 'show_error' function
@    DICTIONARY-KEY       - For dictionary key errors
@    ILLEGAL-OPERATION    - For illegal operation errors
@    UNDEFINED-VAR        - For undefined variable errors
@    INDEX-OUT-OF-RANGE   - For index out of range errors
@    TOO-MANY-ARGS        - For if a function/object was given too many args
@    TOO-FEW-ARGS         - For if a function/object was given too few args
@    INCORRECT-TYPE       - For incorrect type errors
@    MATH                 - For any math related errors
@    IO                   - For any IO related errors
```

## Built-ins
### Main variables
```
@ nothing
@ A representation of nothing
show(nothing)

@ false
@ A representation of false
show(false)

@ true
@ A representation of true
show(true)

@ ezr_version
@ Version of ezr running the code
show(ezr_version)
```

### Main functions
```
@ show(out)
@     - out: any type
@     - Displays 'out' to the console 
@     - Variations: show_error (Raises runtime error ('try' statement tag 'CUSTOM') with message 'out')
show('hello, world!')
show(1.45)
show(show)
show([1.4, 1, show, 'hello!'])
@ show_error('This is a custom error!') - This is commented as it would stop the below code from executing

@ get(out)
@     - out: any type
@     - Displays 'out' to the console and waits for users' input
@     - Variations: get_int (returns 'integer' number value), get_float (returns 'float' number value)
show(get('enter text: '))
show(get_int('enter a number: '))
show(get_float('enter a float number: '))

get('press enter to clear the screen: ') @ Ignore this

@ clear()
@     - Clears the console screen
clear()

@ hash(value)
@     - value: any type
@     - Returns the hash of 'value' as an 'integer' number
show(hash(12))
show(hash(true))
show(hash([1,2,3]))
show(hash('Hello!'))

@ type_of(value)
@     - value: any type
@     - Returns a string, which signifies the variable type of 'value'
show(type_of('s'))
show(type_of(1))
show(type_of(nothing))

@ convert(value, type)
@     - value: any type
@     - type: string
@     - Converts 'value' to type signified by 'type' and returns the new value
show(convert('1', 'Int'))
show(convert(2.432, 'String'))
show(convert([1, 2, 3], 'String'))
show(convert(243, 'Bool'))
show(convert(show, 'String'))

@ insert(list, index, value)
@     - list: list
@     - index: number
@     - value: any type
@     - Inserts 'value' to 'list' at 'index'
item l: [1,2]
insert(l, 1, 1.5)
show(l)
insert(l, 1, [3,4])
show(l)

@ length_of(value)
@     - value: list, array, dictionary or string
@     - Returns an 'integer' number, which is the length of 'value'
show(length_of([1,2]))
show(length_of('hello!'))

@ split(value, separator)
@     - value: string
@     - separator: string
@     - Splits 'value' by 'separator' and returns the list
show(split('a a a', ' '))

@ join(list, separator)
@     - list: list or array
@     - separator: string
@     - Joins all values in 'list' with separator 'separator' and returns the string
show(join(['a', 'a', 'a'], ' '))

@ replace(value, arg_a, arg_b)
@     - value: string | list
@     - arg_a: string | any type
@     - arg_b: string | any type
@     - Replaces all instances of 'arg_a' with 'arg_b' in 'value' and returns the string/list
show(replace('hello hello', 'ell', 'ipp'))
show(replace([1, 'hello!', 3, 4, 5], 1, 2))
show(replace([1, 2, 3, 4, 5], 1, 'hello!'))

@ run(filepath)
@     - filepath: string
@     - Runs file at 'filepath'
@ run('path/to/source/file') - Replace with actual filepath
```