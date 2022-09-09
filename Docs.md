# **Documentation (for ezr V1.17.0)**

## Running code
- **FROM THE COMMAND-LINE**
    - Open ezrShell
    - Write the code (The ';' symbol signifies a new line)
    - Press the 'enter' key

- **FROM A FILE**
    - **Option A**
        - Open/Create a file (the official extension for ezr is '.ezr')
        - Write the code
        - Open ezrShell
        - Type in ```RUN('path/to/source/file')``` (The run function is explained better in the **Built-in FUNCTIONs and variables** section)

    - **Option B**
        - Open/Create a file
        - Write the code
        - Open the file with ezrShell.exe (Windows)
            - Right-click the file
            - Click on 'Open with'
            - Click on 'Choose another app'
            - Click on 'More apps'
            - Click on ezrShell.exe
            - IF YOU DON'T SEE ezrShell AS AN OPTION:
                - Click on 'Look for another app on this PC'
                - Browse to where-ever you installed ezrShell
                - Click on ezrShell.exe
                - Click on 'Open'

## Variable types
- **INT (Numbers)**
```
@ NOTE: The '@' symbol signifies a 'comment' (i.e. Text in a script which ezr won't recognize as code)

ITEM n: 100
SHOW(n) @ The 'SHOW' FUNCTION displays the input parameter to the screen (more about that later)

SHOW(n+3) @ Addition
SHOW(n-2) @ Subtraction
SHOW(n*3) @ Multiplication
SHOW(n/2) @ Division, which returns a FLOAT
SHOW(n^3) @ Power
SHOW(n%2) @ Modulo, which returns the remainder of a division (i.e. remainder of 100/2) Also returns a FLOAT

@ INTs can do all math operations with other INTs or FLOATs
```

- **FLOAT (Decimal-point numbers)**
```
ITEM n: 3.53
SHOW(n)
    
SHOW(n+2.34) @ Addition
SHOW(n-5.21) @ Subtraction
SHOW(n*23.342) @ Multiplication
SHOW(n/5.13) @ Division, which returns a FLOAT
SHOW(n^6.21) @ Power
SHOW(n%7.4325) @ Modulo, which returns the remainder of a division (i.e. remainder of 100/2) Also returns a FLOAT

@ FLOATs can do all math operations with other INTs or FLOATs
```

- **STRING (Text)**
```
ITEM s: 's'
SHOW(s)

@ STRINGs can be concatenated
SHOW(s + 'a')

@ STRINGs can multiplied with INTs
SHOW(s * 4)

@ STRINGs can be divided with INTs
SHOW((s * 4) / 2) @ s*4 = 'ssss'

@ Here '<=' returns the character at index INT 1 in the STRING
SHOW('Hello!' <= 1)

@ The '\' symbol 'escapes' or 'creates' special symbols
SHOW('This will print \' ') @ Here '\' escapes ', which usually signifies the end of a string

SHOW('NEW \n LINE') @ Here '\n' signifies a new-line
SHOW('TAB \t SPACE') @ Here '\t' signifies a tab-space
SHOW('BACKSLASH \\ ') @ Here '\' escapes itself
```

- **FUNCTION (Callable snippets of code)**
```
FUNCTION add WITH a, b DO a + b
    
@ FUNCTIONs can be called with [name]\([args])
SHOW(add(3, 4))

@ FUNCTIONs can have any number of [args]
FUNCTION add_more WITH a, b, c, d, e, f DO a + b + c + d + e + f
SHOW(add_more(3, 5, 2, 7, 3, 6))

@ FUNCTIONs can have no [args]
FUNCTION return_1 DO 1
SHOW(return_1())

@ FUNCTIONs can be anonymous
ITEM anonymous_add: FUNCTION WITH a, b DO a + b
SHOW(anonymous_add(3, 6))

ITEM anonymous_return_1: FUNCTION DO 1
SHOW(anonymous_return_1())

@ FUNCTIONs can be mult-line
FUNCTION multi_line_add WITH a, b DO
    ITEM out: a + b

    SHOW(CONVERT(a, 'STRING') + ' + ' + CONVERT(b, 'STRING') + ' is ' + CONVERT(out, 'STRING'))
    ITEM ans: GET('Is that correct? y/n ') @ More about built-in functions (CONVERT, SHOW, GET, etc) later

    IF ans = 'y' DO @ More about 'IF' statements later
        SHOW('Exiting program...')
        RETURN out
        @ 'RETURN' exits the function and returns the item 'out'
    ELSE IF ans = 'n' DO
        ITEM correct_answer: GET('Please enter the correct answer: ')
        SHOW('Noted. Exiting program...')
        RETURN correct_answer
    ELSE DO
        SHOW('ERROR: INVALID INPUT')
    END

    RETURN @ Here it's returning 'NOTHING'
    SHOW('This won\'t print!') @ This won't print as the function will exit before this can be run

    @ Note the 'END' keyword
END

SHOW(multi_line_add(4, 3))

@ Multi-line functions can also be anonymous
ITEM anonymous_multi_line_ask_name: FUNCTION WITH name DO
    IF name DO
        SHOW('Hello, ' + CONVERT(name, 'STRING') + '!')
    ELSE DO
        ITEM name: GET('Hello! What\'s your name? ')
        SHOW('Hello, ' + CONVERT(name, 'STRING') + '!')
        RETURN name
    END

    @ A function doesn't HAVE to return anything
END

anonymous_multi_line_ask_name('defname')
SHOW(anonymous_multi_line_ask_name(NOTHING))

@ A multi line function doesn't NEED to have arguments either
FUNCTION do_something DO @ This can also be anonymous
    ITEM stop: FALSE @ More about 'FALSE' later
    WHILE INVERT stop DO @ More about 'WHILE' loops and 'INVERT' later
        COUNT FROM 0 AS i TO 10 DO @ More about 'COUNT' loops later
            SHOW('==========================')
        END

        ITEM input: GET('Stop? y/n ')
        ITEM stop: IF input = 'y' DO TRUE ELSE DO FALSE
    END
END

do_something()
```

- **LIST (Groups of items)**
```
ITEM l: ['List', 53, 34.12, ['Nested list']]
SHOW(l)

@ LISTs can 'contain' any type of data, even other lists
ITEM l: [1, 2.54, 'hello', ['nested', 'list'], SHOW]
SHOW(l)

ITEM l: ['s', 'a']
SHOW(l)

ITEM l: ['s', ['a', 's']]
SHOW(l)

@ LISTs can be extended with any type of data
ITEM l: [1, 2]; SHOW(l)
ITEM l: l + 3; SHOW(l)
@ At l + 3, we're are adding INT 3 to l

ITEM l: ['h', 'e']; SHOW(l)
ITEM l: l + ['l', 'l', 'o']; SHOW(l)
@ At l + ['l', 'l', 'o'], we're extending l with STRINGs 'l', 'l' and 'o'

@ LISTs can be removed from at index
ITEM l: [1, 2, 'sa']; SHOW(l)
ITEM l: l - 1; SHOW(l)
@ At l - 1, we're removing the item at index 1, which is INT 2

@ Here '<=' returns the item at index INT 1 in the LIST 
SHOW([1, 2, 3, 4] <= 1)

@ For nested LISTs, you can also do this
SHOW([1, 2, [3, 4]] <= 2 <= 0)

@ LISTs can multiplied with INTs
SHOW([1, 2] * 4)

@ LISTSs can be divided with INTs
SHOW([1, 2, 3, 4] / 2)
```

## Comparison
    @ Numbers (INTs and FLOATS) can be compared with '=', '!', '<', '>', '<=', '>=', 'AND' and 'OR'
    SHOW(5 = 5) @ Is 5 equal to 5?
    SHOW(5 ! 7) @ Is 5 NOT equal to 7?
    SHOW(5 < 7) @ Is 5 less than 7?
    SHOW(7 > 5) @ Is 7 greater than 5?
    SHOW(5 <= 5) @ Is 5 less than OR EQUAL TO 5?
    SHOW(5 >= 5) @ Is 5 greater than OR EQUAL TO 5?
    SHOW(5 > 5 AND 5 >= 5) @ (Is 5 greater than 5) equal to TRUE AND (is 5 greater than or equal to 5) equal to TRUE?
    SHOW(5 > 5 OR 5 >= 5) @ (Is 5 greater than 5) equal to TRUE OR (is 5 greater than or equal to 5) equal to TRUE?
    SHOW(TRUE AND TRUE) @ Will be true
    SHOW(TRUE AND FALSE) @ Will be false
    SHOW(TRUE OR TRUE) @ Will be true
    SHOW(TRUE OR FALSE) @ Will be true
    @ NOTE: If a statement is correct it will return 'TRUE' else it will return 'FALSE'

    @ STRING comparison is limited to '=', '!',
    @ 'AND' (which is true if both strings have a length of at least 1) and
    @ 'OR' (which is true if either of the strings have a length of at least 1)

    @ LIST comparison is just as limited as STRING comparison
    @ FUNCTIONs cannot be compared

    @ INVERT will invert the outcome of a statement
    SHOW(INVERT TRUE) @ Will be FALSE
    SHOW(INVERT FALSE) @ Will be TRUE

## IF statements
    ITEM in: GET('Enter y/n ')

    @ Here, the IF statement checks if 'in' is 'y' and returns INT 1 if it is
    ITEM out: IF in = 'y' DO 1
    SHOW(out)

    @ Here, the ELSE IF statement check if 'in' is 'n' and returns INT 2 if it is
    ITEM out: IF in = 'y' DO 1 ELSE IF in = 'n' DO 2
    SHOW(out)

    @ Here, if 'in' neither 'y' or 'n', it executes the last ELSE, which returns 3
    ITEM out: IF in = 'y' DO 1 ELSE IF in = 'n' DO 2 ELSE DO 3
    SHOW(out)

    @ Some other examples
    SHOW(IF 1 / 2 = 0.5 DO '1 / 2 is 0.5' ELSE DO '1 / 2 is NOT 0.5')
    SHOW(IF 1 * 2 = 0.5 DO '1 * 2 is 0.5' ELSE DO '1 * 2 is NOT 0.5')
    SHOW(IF 1 * 2 = 0.5 DO '1 * 2 is 0.5' ELSE IF 1 * 2 = 2 DO '1 * 2 is 2' ELSE DO '1 * 2 is NOT 0.5')
    SHOW(IF 1 * 2 = 0.5 DO '1 * 2 is 0.5' ELSE IF 1 * 2 = 2 DO '1 * 2 is 2') @ Same thing as above, just    without ELSE

    SHOW(IF [1, 2] = [1, 2] DO 'Both lists are equal' ELSE DO 'Both lists are NOT equal')
    SHOW(IF [1, 2] = [1, 6] DO 'Both lists are equal' ELSE DO 'Both lists are NOT equal')
    SHOW(IF [1, 2] = [1, 6] DO 'Both lists are equal' ELSE IF 3 * 3 = 9 DO '3 * 3 = 9' ELSE DO 'Both lists  are NOT equal')

    SHOW('\n\n') @ Ignore this, it just prints two lines

    @ The below code is commented out as it will show an error as ezr can't properly compare nested list
    @ SHOW(IF [1, 2, [3, 4]] = [1, 2, [3, 4]] DO 'Both lists are equal' ELSE DO 'Both lists are NOT equal')

    @ NOTE: You can have an unlimited number of 'ELSE IF' statements

    @ Multi-line IF statements are the same as single-line statements, but they don't return any values
    @ The below code is just the single-line-IF code 'ported' to multi-line IF statements

    ITEM in: GET('Enter y/n ')

    @ Here, the IF statement checks if 'in' is 'y'
    IF in = 'y' DO
        ITEM out: 1
        SHOW('ITEM out is 1!')
        SHOW(out)

        @ Note the 'END' keyword
    END

    @ Here, the ELSE IF statement check if 'in' is 'n'
    IF in = 'y' DO
        ITEM out: 1
        SHOW('ITEM out is 1!')
        SHOW(out)
    ELSE IF in = 'n' DO
        ITEM out: 2
        SHOW('ITEM out is 2!')
        SHOW(out)

        @ Note the 'END' keyword
    END

    @ Here, if 'in' neither 'y' or 'n', it executes the last ELSE
    IF in = 'y' DO
        ITEM out: 1
        SHOW('ITEM out is 1!')
        SHOW(out)
    ELSE IF in = 'n' DO
        ITEM out: 2
        SHOW('ITEM out is 2!')
        SHOW(out)
    ELSE DO
        ITEM out: 3
        SHOW('ITEM out is 3!')
        SHOW(out)

        @ Note the 'END' keyword
    END

    @ Try comparing other variable types too!
    
    @ NOTE: You can still have an unlimited number of 'ELSE IF' statements

## COUNT loops
    ITEM start: GET_INT('Enter loop start: ')
    ITEM length: GET_INT('Enter loop length: ') @ 'GET_INT' is another built-in function

    @ NOTE: ezr ignores all spaces and tab-spaces

    ITEM l: COUNT FROM start AS i TO length DO i
    @ Here, ezr starts COUNTing FROM 'start' TO ('length' - 1) and sets the loop variable AS i
    @ The loop then returns a list of items, the items being the output of the code after 'DO' each iteration
    @ The loop also increments i by 1 each iteration

    SHOW(l)

    ITEM step: GET_INT('Enter loop increment: ')
    ITEM l: COUNT FROM start AS i TO length STEP step DO i
    @ Here, it does the same thing as above, but sets the loop increment as 'step'

    SHOW(l)

    @ Multi-line COUNT loops are the same, but they don't return anything

    ITEM l: []
    @ The below code does the same thing as the first example, but also prints the list and loop variable each iteration
    COUNT FROM start AS i TO length DO
        ITEM l: l + i
        SHOW(l)
        SHOW('i = ' + CONVERT(i, 'STRING'))

        @ Note the 'END' keyword
    END

    SHOW(l)

    ITEM l: []
    @ The below code does the same thing as the second example, but also prints the list and loop variable each iteration
    COUNT FROM start AS i TO length STEP step DO
        ITEM l: l + i
        SHOW(l)
        SHOW('i = ' + CONVERT(i, 'STRING'))
    END

    SHOW(l)

    ITEM l: []
    @ The below code uses the 'SKIP' keyword to skip an iteration if 'i' = 3 and uses the 'STOP' keyword to stop/break the loop if 'i' = 7
    COUNT FROM start AS i TO length DO
        IF i = 3 DO
            SKIP
        ELSE IF i = 7 DO
            STOP
        END

        ITEM l: l + i
        SHOW(l)
        SHOW('i = ' + CONVERT(i, 'STRING'))
    END

    SHOW(l)

## WHILE loops
    @ This code will 'port' the COUNT loop examples for WHILE loops

    ITEM start: 0
    ITEM length: 9
    
    ITEM i: start
    ITEM l: WHILE i < length DO ITEM i: i + 1
    @ Here, ezr checks if 'i' is less that 'length' (0 is less than 9, so that is true) each iteration
    @ In the code after 'DO' we're adding one to 'i', so each iteration 'i' will be 'i' + 1
    @ So in the last loop, 'i' = 9 and 9 !< 9 so it stops and returns a list of items,
    @ the items being the output of the code after 'DO' each iteration
    
    SHOW(l)
    SHOW(i)
    
    @ NOTE: There is no 'STEP' variable for the WHILE loop; Just set the increment to the step (eg: 'ITEM i: i + 2' is the same as setting STEP to 2)
    
    @ Multi-line WHILE loops are the same, but they don't return anything
    
    ITEM i: start
    ITEM l: []
    
    WHILE i < length DO
        ITEM l: l + (ITEM i: i + 1) @ Yes, this is legal; You can use it for anything, not just WHILE loops
        SHOW(l)
        SHOW('i = ' + CONVERT(i, 'STRING'))
    
        @ Note the 'END' keyword
    END
    
    ITEM i: 0
    ITEM l: []
    WHILE i < 10 DO
        IF i = 3 DO
            ITEM i: i + 1 @ Don't forget to do this!
            SKIP
        ELSE IF i = 6 DO
            STOP
        END

        SHOW(l)
        ITEM l: l + (ITEM i: i + 1)
    END

    SHOW(l)

## TRY statements
    @ The TRY statement is used for error handling
    TRY DO
        @ This code SHOULD show an error, but because it is in a TRY statement, it won't
        CONVERT('s', 'INT')
    END

    @ Single line version
    ITEM a: TRY DO CONVERT('s', 'INT')
    SHOW(a) @ Prints 'NOTHING' as a = NOTHING

    TRY DO
        CONVERT('s', 'INT')
    ERROR DO
        @ This code will execute if an error occured in the above code
        SHOW('An error occured!')

        @ Note the 'END' keyword
    END

    @ Single line version
    ITEM a: TRY DO CONVERT('s', 'INT') ERROR DO 'An error occured!'
    SHOW(a) @ a = 'An error occured'

    TRY DO
        CONVERT('s', 'INT')
    ERROR 'INCORRECT-TYPE' DO
        @ This code will execute only if the 'RUNTIME' error occurs in the above code
        SHOW('An INCORRECT-TYPE error occured!')
    ERROR DO
        SHOW('An unknown error occured.')
    END

    @ Single line version
    ITEM a: TRY DO CONVERT('s', 'INT') ERROR 'INCORRECT-TYPE' DO 'An INCORRECT-TYPE error occured!' ERROR DO 'An unknown error occured.'
    SHOW(a) @ a = 'An INCORRECT-TYPE error occured'

    TRY DO
        1/0
    ERROR AS i DO
        @ Here, i is given a string value which signifies the error type-
        @ in this case, 'DIVISION-BY-ZERO'
        SHOW(i)
    END

    @ Single line version
    TRY DO 1/0 ERROR AS i DO SHOW(i)

    TRY DO
        1/0
    ERROR 'DIVISION-BY-ZERO' AS i DO
        @ This is the same as above, but only triggers if the 'DIVISION-BY-ZERO' error occurs
        SHOW('ERROR: ' + i)
    END

    @ Single line version
    TRY DO 1/0 ERROR 'DIVISION-BY-ZERO' AS i DO SHOW('ERROR: ' + i)

    @ Other errors:
    @     'RUNTIME' @ For unknown errors
    @     'ILLEGAL-OPERATION' @ For illegal operation errors
    @     'UNDEFINED-VAR' @ For undefined variable errors
    @     'DIVISION-BY-ZERO' @ For division by zero errors
    @     'MODULO-BY-ZERO' @ For modulo by zero errors
    @     'INDEX-OUT-OF-RANGE' @ For index out of range errors
    @     'TOO-MANY-FUNCTION-ARGS' @ For if a function was given too many args
    @     'TOO-FEW-FUNCTION-ARGS' @ For if a function was given too few args
    @     'INCORRECT-TYPE' @ For incorrect type errors
    @     'FILE-READ' @ For file read errors
    @     'FILE-WRITE' @ For file write errors
    @     'RUN-FILE' @ For errors while running a script

## Built-in FUNCTIONs and variables
    @ NOTHING
    @ A representation of 'nothing'
    SHOW(NOTHING)

    @ FALSE
    @ A representation of 'false'
    SHOW(FALSE)

    @ TRUE
    @ A representation of 'true'
    SHOW(TRUE)

    @ SHOW(out)
    @     - out: Any type
    @     - Displays 'out' to the console 
    SHOW('Hello, World!')
    SHOW(1.45)
    SHOW(SHOW)
    SHOW([1.4, 1, SHOW, 'Hello!'])

    @ GET(out)
    @     - out: Any type
    @     - Displays 'out' to the console and waits for users' input
    @     - Variations: GET_INT (returns INT value), GET_FLOAT (returns FLOAT value)
    SHOW(GET('Enter text: '))
    SHOW(GET_INT('Enter a number: '))
    SHOW(GET_FLOAT('Enter a float number: '))

    GET('Press enter to clear the screen: ') @ Ignore this

    @ CLEAR_SCREEN()
    @     - Clears console screen
    CLEAR_SCREEN()

    @ TYPE_OF(value)
    @     - value: Any type
    @     - Returns a STRING, which signifies the variable type of 'value'
    SHOW(TYPE_OF('s'))
    SHOW(TYPE_OF(1))
    SHOW(TYPE_OF(1.54))
    SHOW(TYPE_OF(SHOW))
    SHOW(TYPE_OF([1, 2]))
    SHOW(TYPE_OF(TRUE))
    SHOW(TYPE_OF(NOTHING))

    @ CONVERT(value, type)
    @     - value: Any type
    @     - type: STRING
    @     - Converts 'value' to type signified by 'type' and returns the new valu
    SHOW(CONVERT('1', 'INT'))
    SHOW(CONVERT(2.432, 'STRING'))
    SHOW(CONVERT([1, 2, 3], 'STRING'))
    SHOW(CONVERT(243, 'BOOLEAN'))
    SHOW(CONVERT(SHOW, 'STRING'))

    @ EXTEND(list, value)
    @     - list: LIST
    @     - value: Any type
    @     - Extends 'list' with 'value'
    ITEM l: [1,2]
    EXTEND(l, 6)
    SHOW(l)
    EXTEND(l, [3,4])
    SHOW(l)

    @ REMOVE(list, index)
    @     - list: LIST
    @     - index: INT
    @     - Removes item from 'list' at 'index'
    ITEM l: [1,2,6]
    REMOVE(l, 2)
    SHOW(l)

    @ INSERT(list, index, value)
    @     - list: LIST
    @     - index: INT
    @     - value: Any type
    @     - Inserts 'value' to 'list' at 'index'
    ITEM l: [1,2]
    INSERT(l, 1, 1.5)
    SHOW(l)
    INSERT(l, 1, [3,4])
    SHOW(l)

    @ LEN(value)
    @     - value: LIST or STRING
    @     - Returns an INT, which is the length of 'value'
    SHOW(LEN([1,2]))
    SHOW(LEN('Hello!'))

    @ SPLIT(value, separator)
    @     - value: STRING
    @     - separator: STRING
    @     - Splits 'value' by 'separator' and returns the LIST
    SHOW(SPLIT('a a a', ' '))

    @ JOIN(list, separator)
    @     - list: LIST
    @     - separator: STRING
    @     - Joins all values in 'list' with separator 'separator' and returns the STRING
    SHOW(JOIN(['a', 'a', 'a'], ' '))

    @ REPLACE(value, substring, new_substring)
    @     - value: STRING
    @     - substring: STRING
    @     - new_substring: STRING
    @     - Replaces all instances 'substring' with 'new_substring' in 'value' and returns the STRING
    SHOW(REPLACE('hello hello', 'ell', 'ipp'))

    @ The below area is commented because they need the path to a file
    @ Replace all instances of 'path/to/file' and 'path/to/source/file' with the path to a real file,   depending on the use of the function
    @ and uncomment the lines with the 'tag': 'UNCOMMENT' 

    @ READ_FILE(filepath, mode)
    @     - filepath: STRING
    @     - mode: STRING
    @     - Reads data from file at 'filepath', in mode 'mode', and returns the data
    @     - Modes:
    @         - 'READ': Returns file data as a continuous STRING
    @         - 'READ_LINE': Returns first line of file as a continuous STRING
    @         - 'READ_LINES': Returns file data as a LIST
    @ SHOW(READ_FILE('path/to/file', 'READ')) @ UNCOMMENT
    @ SHOW(READ_FILE('path/to/file', 'READ_LINE')) @ UNCOMMENT
    @ SHOW(READ_FILE('path/to/file', 'READ_LINES')) @ UNCOMMENT

    @ WRITE_FILE(filepath, mode, data)
    @     - filepath: STRING
    @     - mode: STRING
    @     - data: LIST, STRING, INT or FLOAT
    @     - Writes 'data' to file at 'filepath', in mode 'mode'
    @     - Modes:
    @         - 'EXTEND': Adds to already existing data in file
    @         - 'OVERWRITE': Overwrites all content in file and writes the data
    @ WRITE_FILE('path/to/file', 'EXTEND', 'TEST DATA') @ UNCOMMENT
    @ SHOW(READ_FILE('path/to/file', 'READ')) @ UNCOMMENT
    @ WRITE_FILE('path/to/file', 'OVERWRITE', 'TEST DATA V2') @ UNCOMMENT
    @ SHOW(READ_FILE('path/to/file', 'READ')) @ UNCOMMENT

    @ RUN(filepath)
    @     - filepath: STRING
    @     - Runs file at 'filepath'
    @ RUN('path/to/source/file') @ UNCOMMENT

## Before you go
**Make sure you try out, modify and test all snippets of the code for yourself!**