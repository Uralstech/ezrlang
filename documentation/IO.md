# Built-in IO library (for ezr V1.22.0.0)
## READ(filepath: STRING, mode: STRING)
**Reads file at 'filepath' and returns data in mode 'mode'**
```
INCLUDE 'IO.py'

@ Returns all data in file as STRING (\n = newline, \t = tab-space)
ITEM f_READ: IO.READ('path/to/file', 'READ')
SHOW(f_READ)

@ Returns first line of file as STRING
ITEM f_READ_LINE: IO.READ('path/to/file', 'READ_LINE')
SHOW(f_READ_LINE)

@ Returns all lines of file as LIST
ITEM f_READ_LINES: IO.READ('path/to/file', 'READ_LINES')
SHOW(f_READ_LINES)
```

## WRITE(filepath: STRING, mode: STRING, data: Any type)
**Writes data 'data' to file at 'filepath' in mode 'mode'**
```
INCLUDE 'IO.py'

@ Appends data to file
IO.WRITE('path/to/file', 'EXTEND', 'test\ndata')

@ Overwrites all existing data in file
IO.WRITE('path/to/file', 'OVERWRITE', 'test\ndata')
```

## DELETE(filepath: STRING)
**Deletes file at 'filepath'**
```
INCLUDE 'IO.py'

IO.DELETE('path/to/file')
```

## CREATE_DIR(dirpath: STRING)
**Creates directory at 'dirpath'**
```
INCLUDE 'IO.py'

IO.CREATE_DIR('path/to/dir/dir-name')
```

## DELETE_DIR(dirpath: STRING)
**Deletes directory at 'dirpath'**
```
INCLUDE 'IO.py'

IO.DELETE_DIR('path/to/dir/dir-name')
```